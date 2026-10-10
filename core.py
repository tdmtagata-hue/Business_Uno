"""Lógica del buscador. No depende de Streamlit, así se puede probar sola."""
from __future__ import annotations

import io
import re
import unicodedata
from urllib.parse import quote, urlparse

import pandas as pd

ENGINES = {
    "Google": "https://www.google.com/search?q=",
    "DuckDuckGo": "https://duckduckgo.com/?q=",
    "Bing": "https://www.bing.com/search?q=",
}

FORMATS = {
    "Cualquier formato": "",
    "PDF": "pdf",
    "Excel (xlsx)": "xlsx",
    "Word (docx)": "docx",
    "PowerPoint (pptx)": "pptx",
}


def normalize(text) -> str:
    """Minúsculas, sin tildes y solo letras y números separados por un espacio."""
    s = unicodedata.normalize("NFD", "" if text is None else str(text))
    s = "".join(c for c in s if unicodedata.category(c) != "Mn").lower()
    return re.sub(r"[^a-z0-9]+", " ", s).strip()


def read_table(content: bytes) -> pd.DataFrame:
    """Lee un CSV/TSV (detecta el separador) y devuelve todo como texto."""
    try:
        text = content.decode("utf-8-sig")
    except UnicodeDecodeError:
        text = content.decode("latin-1")

    try:
        df = pd.read_csv(io.StringIO(text), sep=None, engine="python", dtype=str, keep_default_na=False)
    except pd.errors.EmptyDataError as exc:
        raise ValueError("El archivo está vacío.") from exc
    except Exception:
        # Si no se puede detectar el separador (por ejemplo, una sola columna), probamos con coma.
        try:
            df = pd.read_csv(io.StringIO(text), dtype=str, keep_default_na=False)
        except pd.errors.EmptyDataError as exc:
            raise ValueError("El archivo está vacío.") from exc
        except Exception as exc:
            raise ValueError("No pude leer el archivo como tabla. Revisa que sea un CSV válido.") from exc

    df.columns = [str(c).strip() or f"Columna {i + 1}" for i, c in enumerate(df.columns)]
    df = df.apply(lambda col: col.str.strip())
    if df.empty:
        raise ValueError("El archivo necesita una fila de encabezados y al menos un registro.")
    return df


def filter_dataframe(df: pd.DataFrame, query: str, column: str | None = None) -> pd.DataFrame:
    """Deja los registros donde cada palabra de la búsqueda empieza alguna palabra del texto.

    No distingue mayúsculas ni tildes. Si `column` es None, busca en todas las columnas.
    """
    tokens = normalize(query).split()
    if not tokens or df.empty:
        return df

    columns = [column] if column else list(df.columns)
    haystack = pd.Series([""] * len(df), index=df.index)
    for name in columns:
        haystack = haystack + df[name].map(lambda v: " " + normalize(v))

    mask = pd.Series(True, index=df.index)
    for token in tokens:
        mask &= haystack.str.contains(" " + token, regex=False)
    return df[mask]


def search_url(source: dict, query: str) -> str:
    """Enlace de búsqueda de una fuente: directo si la fuente lo permite, si no vía Google con site:."""
    if source.get("url"):
        return source["url"].replace("{q}", quote(query, safe=""))
    return ENGINES["Google"] + quote(f"{query} site:{source['site']}", safe="")


def parse_domain(text: str | None) -> str | None:
    """Convierte un dominio o enlace en 'dominio/ruta'. Devuelve None si no parece un sitio."""
    s = (text or "").strip()
    if not s:
        return None
    if not re.match(r"^https?://", s, re.IGNORECASE):
        s = "https://" + s
    try:
        parsed = urlparse(s)
        host = parsed.hostname or ""
    except ValueError:
        return None
    host = host.lower().removeprefix("www.")
    if "." not in host or not re.fullmatch(r"[a-z0-9.-]+", host):
        return None
    return host + parsed.path.rstrip("/")


def custom_url(domain: str, query: str, engine: str = "Google", file_format: str = "") -> str:
    """Búsqueda limitada a un sitio (y opcionalmente a un formato de archivo)."""
    full = f"{query} site:{domain}" + (f" filetype:{file_format}" if file_format else "")
    return ENGINES.get(engine, ENGINES["Google"]) + quote(full, safe="")
