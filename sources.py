"""Catálogo de fuentes. Para agregar una, añade un diccionario a la lista de su pestaña.

Campos de cada fuente:
  name  nombre que se muestra
  kind  etiqueta corta (tipo de fuente)
  desc  qué ofrece el sitio
  home  página principal
  url   plantilla de búsqueda directa, con {q} donde va el tema (opcional)
  site  dominio para buscar con Google usando site: (se usa si no hay url)
"""

SOURCE_TABS = {
    "academico": {
        "label": "Académico",
        "intro": "Artículos revisados por pares, revistas científicas y tesis.",
        "items": [
            {
                "name": "Google Académico",
                "kind": "Buscador académico",
                "desc": "Artículos, tesis, libros y citas de editoriales y repositorios universitarios.",
                "home": "https://scholar.google.com/",
                "url": "https://scholar.google.com/scholar?q={q}",
            },
            {
                "name": "SciELO",
                "kind": "Acceso abierto",
                "desc": "Revistas científicas de Latinoamérica, España y Portugal con texto completo gratuito.",
                "home": "https://scielo.org/",
                "url": "https://search.scielo.org/?q={q}",
            },
            {
                "name": "Redalyc",
                "kind": "Acceso abierto",
                "desc": "Revistas científicas iberoamericanas de acceso abierto.",
                "home": "https://www.redalyc.org/",
                "site": "redalyc.org",
            },
            {
                "name": "Dialnet",
                "kind": "Producción hispana",
                "desc": "Artículos, tesis y libros de la producción científica en español.",
                "home": "https://dialnet.unirioja.es/",
                "site": "dialnet.unirioja.es",
            },
            {
                "name": "PubMed",
                "kind": "Biomedicina",
                "desc": "Literatura biomédica de la Biblioteca Nacional de Medicina de EE. UU.",
                "home": "https://pubmed.ncbi.nlm.nih.gov/",
                "url": "https://pubmed.ncbi.nlm.nih.gov/?term={q}",
            },
            {
                "name": "Semantic Scholar",
                "kind": "Buscador académico",
                "desc": "Artículos con resúmenes breves y conteo de citas.",
                "home": "https://www.semanticscholar.org/",
                "url": "https://www.semanticscholar.org/search?q={q}",
            },
        ],
    },
    "cifras": {
        "label": "Datos y cifras",
        "intro": "Estadísticas, indicadores y conjuntos de datos de organismos internacionales.",
        "items": [
            {
                "name": "Google Dataset Search",
                "kind": "Conjuntos de datos",
                "desc": "Encuentra datasets publicados en la web por gobiernos, universidades y centros de investigación.",
                "home": "https://datasetsearch.research.google.com/",
                "url": "https://datasetsearch.research.google.com/search?query={q}",
            },
            {
                "name": "Banco Mundial",
                "kind": "Indicadores",
                "desc": "Indicadores de desarrollo y series históricas por país.",
                "home": "https://data.worldbank.org/",
                "site": "data.worldbank.org",
            },
            {
                "name": "Our World in Data",
                "kind": "Gráficos y datos",
                "desc": "Datos abiertos con gráficos sobre salud, economía, tecnología y medio ambiente.",
                "home": "https://ourworldindata.org/",
                "url": "https://ourworldindata.org/search?q={q}",
            },
            {
                "name": "CEPAL",
                "kind": "América Latina",
                "desc": "Estadísticas e informes económicos y sociales de la región.",
                "home": "https://www.cepal.org/es",
                "site": "cepal.org",
            },
            {
                "name": "OCDE",
                "kind": "Organismo internacional",
                "desc": "Estadísticas comparadas y estudios de políticas públicas.",
                "home": "https://www.oecd.org/",
                "site": "oecd.org",
            },
            {
                "name": "FMI",
                "kind": "Organismo internacional",
                "desc": "Datos y perspectivas económicas mundiales.",
                "home": "https://www.imf.org/es",
                "site": "imf.org",
            },
        ],
    },
    "noticias": {
        "label": "Noticias",
        "intro": "Prensa y agencias con cobertura nacional e internacional.",
        "items": [
            {
                "name": "Google Noticias",
                "kind": "Agregador",
                "desc": "Coberturas de muchos medios sobre el mismo tema, ordenadas por relevancia.",
                "home": "https://news.google.com/",
                "url": "https://news.google.com/search?q={q}&hl=es-419",
            },
            {
                "name": "Reuters",
                "kind": "Agencia",
                "desc": "Agencia internacional de noticias, con foco en economía y negocios.",
                "home": "https://www.reuters.com/",
                "url": "https://www.reuters.com/site-search/?query={q}",
            },
            {
                "name": "BBC Mundo",
                "kind": "Medio internacional",
                "desc": "Noticias y análisis en español de la BBC.",
                "home": "https://www.bbc.com/mundo",
                "site": "bbc.com/mundo",
            },
            {
                "name": "EFE",
                "kind": "Agencia",
                "desc": "Agencia de noticias en español con cobertura de Iberoamérica.",
                "home": "https://efe.com/",
                "site": "efe.com",
            },
            {
                "name": "Gestión",
                "kind": "Economía del Perú",
                "desc": "Diario peruano de economía, empresas y finanzas.",
                "home": "https://gestion.pe/",
                "site": "gestion.pe",
            },
            {
                "name": "El Comercio",
                "kind": "Prensa peruana",
                "desc": "Diario peruano con cobertura política, económica y social.",
                "home": "https://elcomercio.pe/",
                "site": "elcomercio.pe",
            },
        ],
    },
    "peru": {
        "label": "Perú oficial",
        "intro": "Portales del Estado peruano y entidades que publican cifras y normas.",
        "items": [
            {
                "name": "gob.pe",
                "kind": "Portal del Estado",
                "desc": "Portal único con trámites, normas y comunicados de las entidades públicas.",
                "home": "https://www.gob.pe/",
                "url": "https://www.gob.pe/busquedas?term={q}",
            },
            {
                "name": "INEI",
                "kind": "Estadística oficial",
                "desc": "Censos, encuestas y estadísticas oficiales del país.",
                "home": "https://www.inei.gob.pe/",
                "site": "inei.gob.pe",
            },
            {
                "name": "BCRP",
                "kind": "Banco central",
                "desc": "Series estadísticas, tipo de cambio, inflación y notas económicas.",
                "home": "https://www.bcrp.gob.pe/",
                "site": "bcrp.gob.pe",
            },
            {
                "name": "SUNAT",
                "kind": "Tributos",
                "desc": "Normas y estadísticas de tributos y comercio exterior.",
                "home": "https://www.sunat.gob.pe/",
                "site": "sunat.gob.pe",
            },
            {
                "name": "OSIPTEL",
                "kind": "Telecomunicaciones",
                "desc": "Regulación y estadísticas del sector de telecomunicaciones.",
                "home": "https://www.osiptel.gob.pe/",
                "site": "osiptel.gob.pe",
            },
            {
                "name": "INDECOPI",
                "kind": "Consumidor y competencia",
                "desc": "Protección al consumidor, competencia y propiedad intelectual.",
                "home": "https://www.indecopi.gob.pe/",
                "site": "indecopi.gob.pe",
            },
            {
                "name": "Datos Abiertos",
                "kind": "Datos del Estado",
                "desc": "Plataforma nacional de datos abiertos del gobierno peruano.",
                "home": "https://www.datosabiertos.gob.pe/",
                "site": "datosabiertos.gob.pe",
            },
            {
                "name": "ALICIA (CONCYTEC)",
                "kind": "Investigación peruana",
                "desc": "Repositorio nacional de acceso abierto con tesis y artículos del país.",
                "home": "https://alicia.concytec.gob.pe/",
                "site": "alicia.concytec.gob.pe",
            },
        ],
    },
}
