# Buscador de fuentes

App de [Streamlit](https://streamlit.io) para buscar información en un solo lugar. Escribes un tema una vez y, según la pestaña, la app filtra tus propios datos o te da el enlace de búsqueda en sitios confiables.

## Qué incluye

| Pestaña | Para qué sirve |
| --- | --- |
| Mis datos | Carga un CSV (o pega su contenido) y fíltralo sin distinguir tildes ni mayúsculas. Puedes descargar los resultados. |
| Académico | Google Académico, SciELO, Redalyc, Dialnet, PubMed y Semantic Scholar. |
| Datos y cifras | Google Dataset Search, Banco Mundial, Our World in Data, CEPAL, OCDE y FMI. |
| Noticias | Google Noticias, Reuters, BBC Mundo, EFE, Gestión y El Comercio. |
| Perú oficial | gob.pe, INEI, BCRP, SUNAT, OSIPTEL, INDECOPI, Datos Abiertos y ALICIA (CONCYTEC). |
| Mi fuente | Agrega cualquier dominio o enlace y busca solo dentro de ese sitio, con el buscador y el formato de archivo que elijas. |

La app arma enlaces de búsqueda y no consulta Internet por su cuenta. Algunas fuentes no tienen un enlace directo de búsqueda, así que se buscan dentro del sitio usando Google (`site:`). Cada tarjeta indica cuál de los dos modos usa.

## Probar en tu computadora

Necesitas Python 3.10 o superior.

```bash
git clone https://github.com/tdmtagata-hue/Business_Uno.git
cd Business_Uno

python -m venv .venv
source .venv/bin/activate        # en Windows: .venv\Scripts\activate

pip install -r requirements.txt
streamlit run app.py
```

Se abre en <http://localhost:8501>. Puedes compartir una búsqueda con el parámetro `?q=`, por ejemplo `http://localhost:8501/?q=inflación`.

## Subirlo a GitHub

Crea un repositorio vacío en GitHub y, desde la carpeta del proyecto:

```bash
git init
git add .
git commit -m "Buscador de fuentes"
git branch -M main
git remote add origin https://github.com/tdmtagata-hue/Business_Uno.git
git push -u origin main
```

Con cada `push` y cada pull request, GitHub Actions corre las pruebas (`.github/workflows/ci.yml`).

## Publicarlo en Streamlit Community Cloud

1. Sube el proyecto a GitHub como se explica arriba.
2. Entra a <https://share.streamlit.io> e inicia sesión con tu cuenta de GitHub.
3. Elige **Create app**, selecciona tu repositorio, la rama `main` y el archivo principal `app.py`.
4. Pulsa **Deploy**. Streamlit instala lo que está en `requirements.txt` y te da un enlace público.

## Agregar o cambiar fuentes

Las fuentes están en `sources.py`. Para sumar una, agrega un diccionario a la lista de su pestaña:

```python
{
    "name": "Mi sitio",
    "kind": "Tipo de fuente",
    "desc": "Qué ofrece el sitio.",
    "home": "https://ejemplo.org/",
    "url": "https://ejemplo.org/buscar?q={q}",   # si tiene búsqueda propia
    # "site": "ejemplo.org",                      # si no, busca con Google dentro del sitio
}
```

Para dejar sitios fijos en la pestaña **Mi fuente**, edita `DEFAULT_SITES` en `app.py`. Los sitios que agregas desde la app duran lo que dura la sesión.

## Pruebas

```bash
pip install -r requirements-dev.txt
pytest
```

## Estructura

```
app.py                  interfaz de Streamlit
core.py                 lógica (lectura de CSV, filtro, enlaces); no depende de Streamlit
sources.py              catálogo de fuentes
data/                   CSV de ejemplo
tests/                  pruebas de la lógica y de la app
.streamlit/config.toml  tema
.github/workflows/      integración continua
```

## Licencia

Agrega el archivo `LICENSE` que prefieras antes de publicar el repositorio (MIT es una opción común).
