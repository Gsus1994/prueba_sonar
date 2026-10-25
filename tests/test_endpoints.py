from datetime import datetime, timezone

import pytest
from fastapi.testclient import TestClient

from services.fecha.app.main import app as fecha_app
from services.moneda.app import main as moneda
from services.pares.app.main import app as pares_app
from services.saludo.app.main import app as saludo_app


def test_fecha_actual_en_utc():
    antes = datetime.now(timezone.utc).date().isoformat()
    with TestClient(fecha_app) as client:
        response = client.get("/fecha")
    despues = datetime.now(timezone.utc).date().isoformat()

    assert response.status_code == 200
    assert response.json() in ({"fecha": antes}, {"fecha": despues})


def test_primeros_diez_pares_positivos():
    with TestClient(pares_app) as client:
        response = client.get("/pares")

    assert response.status_code == 200
    assert response.json() == {"pares": [2, 4, 6, 8, 10, 12, 14, 16, 18, 20]}


@pytest.mark.parametrize("resultado", ["cara", "cruz"])
def test_lanzar_moneda(monkeypatch, resultado):
    def elegir(opciones):
        assert opciones == ("cara", "cruz")
        return resultado

    monkeypatch.setattr(moneda, "choice", elegir)
    with TestClient(moneda.app) as client:
        response = client.get("/moneda")

    assert response.status_code == 200
    assert response.json() == {"resultado": resultado}


def test_hello_world():
    with TestClient(saludo_app) as client:
        response = client.get("/hello")

    assert response.status_code == 200
    assert response.json() == {"mensaje": "Hello World"}
