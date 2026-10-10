import pytest

from core import (
    custom_url,
    filter_dataframe,
    normalize,
    parse_domain,
    read_table,
    search_url,
)
from sources import SOURCE_TABS


def test_normalize_quita_tildes_y_simbolos():
    assert normalize("  María-Gómez, S.A. ") == "maria gomez s a"
    assert normalize(None) == ""


def test_read_table_detecta_punto_y_coma_y_comillas():
    content = 'nombre;ciudad;nota\n"Pérez, Ana";Lima;"dijo ""hola"""\nLuis;Cusco;ok\n'.encode("utf-8")
    df = read_table(content)
    assert list(df.columns) == ["nombre", "ciudad", "nota"]
    assert df.iloc[0]["nombre"] == "Pérez, Ana"
    assert df.iloc[0]["nota"] == 'dijo "hola"'


def test_read_table_acepta_latin1():
    df = read_table("nombre,ciudad\nJosé,Lima\n".encode("latin-1"))
    assert df.iloc[0]["nombre"] == "José"


def test_read_table_sin_registros_da_error():
    with pytest.raises(ValueError):
        read_table(b"nombre,ciudad\n")
    with pytest.raises(ValueError):
        read_table(b"")


def test_filter_sin_tildes_ni_mayusculas_y_por_prefijo():
    df = read_table("nombre,ciudad\nMaría Gómez,Lima\nLuis Quispe,Cusco\n".encode("utf-8"))
    assert list(filter_dataframe(df, "maria").nombre) == ["María Gómez"]
    assert list(filter_dataframe(df, "LIM mar").nombre) == ["María Gómez"]
    assert filter_dataframe(df, "lima", "nombre").empty
    assert len(filter_dataframe(df, "")) == 2


def test_search_url_directa_y_con_site():
    assert search_url({"url": "https://x.com/?q={q}"}, "a b") == "https://x.com/?q=a%20b"
    assert "site%3Ainei.gob.pe" in search_url({"site": "inei.gob.pe"}, "pobreza")


def test_parse_domain():
    assert parse_domain("https://www.WHO.int/es/") == "who.int/es"
    assert parse_domain("inei.gob.pe") == "inei.gob.pe"
    assert parse_domain("hola mundo") is None
    assert parse_domain("localhost") is None
    assert parse_domain("") is None


def test_custom_url_con_buscador_y_formato():
    url = custom_url("who.int", "dengue", "DuckDuckGo", "pdf")
    assert url.startswith("https://duckduckgo.com/?q=dengue%20site%3Awho.int%20filetype%3Apdf")


def test_catalogo_tiene_campos_obligatorios():
    for cfg in SOURCE_TABS.values():
        assert cfg["items"]
        for item in cfg["items"]:
            assert {"name", "kind", "desc", "home"} <= item.keys()
            assert item.get("url") or item.get("site")
            if item.get("url"):
                assert "{q}" in item["url"]
