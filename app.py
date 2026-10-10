"""Buscador de fuentes: app de Streamlit.

Ejecutar:  streamlit run app.py
"""
from pathlib import Path

import streamlit as st

from core import (
    ENGINES,
    FORMATS,
    custom_url,
    filter_dataframe,
    parse_domain,
    read_table,
    search_url,
)
from sources import SOURCE_TABS

SAMPLE_PATH = Path(__file__).parent / "data" / "clientes_ejemplo.csv"
SAMPLE_NAME = "Datos de ejemplo (clientes)"
DEFAULT_SITES = ["inei.gob.pe", "who.int"]
SUGGESTED_SITES = ["bcrp.gob.pe", "sunat.gob.pe", "who.int", "cepal.org"]

st.set_page_config(page_title="Buscador de fuentes", page_icon="🔎", layout="centered")


# ---------- estado ----------
def load_sample() -> None:
    st.session_state.df = read_table(SAMPLE_PATH.read_bytes())
    st.session_state.df_name = SAMPLE_NAME
    st.session_state.df_is_example = True
    st.session_state.file_key = None


if "q" not in st.session_state:
    st.session_state.q = st.query_params.get("q", "")
if "sites" not in st.session_state:
    st.session_state.sites = DEFAULT_SITES.copy()
if "df" not in st.session_state:
    load_sample()


def add_site(raw: str) -> bool:
    domain = parse_domain(raw)
    if domain is None:
        return False
    if domain not in st.session_state.sites:
        st.session_state.sites.append(domain)
    return True


def remove_site(domain: str) -> None:
    st.session_state.sites = [s for s in st.session_state.sites if s != domain]


def short(text: str, n: int) -> str:
    return text if len(text) <= n else text[: n - 1] + "…"


# ---------- cabecera y consulta ----------
st.title("Buscador de fuentes")
st.write(
    "Escribe un tema, elige la pestaña y abre la búsqueda directamente en sitios confiables "
    "o en tus propios datos."
)

query = st.text_input(
    "Tema a buscar",
    key="q",
    placeholder="Ejemplo: inflación en Perú, comercio electrónico, energía solar",
).strip()

if query:
    st.query_params["q"] = query
elif "q" in st.query_params:
    del st.query_params["q"]

tab_labels = (
    ["Mis datos"]
    + [cfg["label"] for cfg in SOURCE_TABS.values()]
    + ["Mi fuente"]
)
tabs = st.tabs(tab_labels)


# ---------- Mis datos ----------
with tabs[0]:
    st.caption(
        "Filtra un archivo CSV dentro de la sesión de Streamlit. "
        "El archivo no se guarda en disco ni se envía a otros servicios."
    )

    uploaded = st.file_uploader("Cargar un archivo CSV, TSV o TXT", type=["csv", "tsv", "txt"])
    if uploaded is not None:
        key = (uploaded.name, uploaded.size)
        if st.session_state.get("file_key") != key:
            try:
                st.session_state.df = read_table(uploaded.getvalue())
                st.session_state.df_name = uploaded.name
                st.session_state.df_is_example = False
                st.session_state.file_key = key
            except ValueError as exc:
                st.error(str(exc))
    elif st.session_state.get("file_key"):
        load_sample()  # quitaron el archivo: volvemos al ejemplo

    with st.expander("O pega el contenido (primera fila con los encabezados)"):
        pasted = st.text_area(
            "Contenido",
            height=120,
            placeholder="nombre,ciudad,plan\nAna Torres,Lima,Fibra 300\nLuis Quispe,Arequipa,Móvil 20 GB",
            label_visibility="collapsed",
        )
        if st.button("Cargar texto pegado"):
            try:
                st.session_state.df = read_table(pasted.encode("utf-8"))
                st.session_state.df_name = "Texto pegado"
                st.session_state.df_is_example = False
                st.session_state.file_key = None
            except ValueError as exc:
                st.error(str(exc))

    df = st.session_state.df
    column_choice = st.selectbox("Buscar en", ["Todas las columnas", *df.columns])
    result = filter_dataframe(df, query, None if column_choice == "Todas las columnas" else column_choice)

    label = f"**{st.session_state.df_name}**"
    if st.session_state.df_is_example:
        label += " · ejemplo"
    st.markdown(label)
    st.caption(f"{len(result)} de {len(df)} registros · {len(df.columns)} columnas")

    if result.empty:
        st.info(f"Ningún registro coincide con “{query}”. Prueba con menos palabras o cambia la columna.")
    else:
        st.dataframe(result, hide_index=True)
        st.download_button(
            "Descargar resultados (CSV)",
            data=result.to_csv(index=False).encode("utf-8-sig"),
            file_name="resultados.csv",
            mime="text/csv",
        )


# ---------- pestañas de fuentes ----------
def render_sources(cfg: dict) -> None:
    st.caption(cfg["intro"])
    if not query:
        st.info("Escribe un tema arriba para generar los enlaces de búsqueda. Mientras tanto puedes abrir cada sitio.")
    columns = st.columns(2)
    for i, source in enumerate(cfg["items"]):
        with columns[i % 2]:
            with st.container(border=True):
                st.markdown(f"**{source['name']}**")
                st.caption(source["kind"])
                st.write(source["desc"])
                st.caption(
                    "Búsqueda directa en el sitio" if source.get("url") else "Búsqueda dentro del sitio con Google"
                )
                if query:
                    st.link_button(f"Buscar “{short(query, 26)}”", search_url(source, query), type="primary")
                st.link_button("Abrir sitio", source["home"])


for tab, cfg in zip(tabs[1:-1], SOURCE_TABS.values()):
    with tab:
        render_sources(cfg)


# ---------- Mi fuente ----------
with tabs[-1]:
    st.caption("Agrega los sitios donde quieres buscar. La búsqueda se limita a cada sitio que guardes.")

    with st.form("add_site", clear_on_submit=True):
        raw = st.text_input("Sitio o enlace", placeholder="inei.gob.pe o https://www.who.int/es")
        submitted = st.form_submit_button("Agregar sitio", type="primary")
    if submitted and not add_site(raw):
        st.error("No reconozco ese sitio. Escribe algo como inei.gob.pe o pega el enlace completo.")

    st.caption("Sugerencias")
    suggestion_cols = st.columns(len(SUGGESTED_SITES))
    for col, domain in zip(suggestion_cols, SUGGESTED_SITES):
        col.button(f"+ {domain}", key=f"sug_{domain}", on_click=add_site, args=(domain,))

    options_left, options_right = st.columns(2)
    engine = options_left.selectbox("Buscar con", list(ENGINES))
    file_format = FORMATS[options_right.selectbox("Formato", list(FORMATS))]

    if not query:
        st.info("Escribe un tema arriba para generar los enlaces de búsqueda.")

    if not st.session_state.sites:
        st.write("Aún no hay sitios guardados. Escribe un dominio o pega un enlace arriba.")

    for site in list(st.session_state.sites):
        with st.container(border=True):
            c_host, c_search, c_open, c_remove = st.columns([4, 4, 2, 2], vertical_alignment="center")
            c_host.markdown(f"`{site}`")
            if query:
                c_search.link_button(
                    f"Buscar “{short(query, 20)}”",
                    custom_url(site, query, engine, file_format),
                    type="primary",
                )
            c_open.link_button("Abrir sitio", f"https://{site}")
            c_remove.button("Quitar", key=f"rm_{site}", on_click=remove_site, args=(site,))

    st.caption(
        "Los sitios se conservan mientras dura tu sesión. Para dejar algunos fijos, edita DEFAULT_SITES en app.py."
    )

st.caption(
    "Cada enlace abre el buscador del sitio en otra pestaña. Antes de citar un dato, revisa el autor, "
    "la fecha y si proviene de la fuente original."
)
