from pathlib import Path

from streamlit.testing.v1 import AppTest

APP = str(Path(__file__).resolve().parent.parent / "app.py")


def test_la_app_abre_sin_errores():
    at = AppTest.from_file(APP, default_timeout=30).run()
    assert not at.exception
    assert len(at.tabs) == 6
    assert len(at.dataframe[0].value) == 7


def test_buscar_en_los_datos_de_ejemplo():
    at = AppTest.from_file(APP, default_timeout=30).run()
    at.text_input[0].set_value("lima").run()
    assert not at.exception
    assert len(at.dataframe[0].value) == 3
