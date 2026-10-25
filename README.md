# Microservicios con FastAPI

Proyecto sencillo con cuatro servicios independientes, cada uno con su propia
aplicación FastAPI y un endpoint de negocio. No necesita base de datos.

| Servicio | Endpoint GET | Respuesta de ejemplo |
| --- | --- | --- |
| Fecha | `http://localhost:8001/fecha` | `{"fecha": "2026-10-25"}` |
| Pares | `http://localhost:8002/pares` | `{"pares": [2, 4, 6, 8, 10, 12, 14, 16, 18, 20]}` |
| Moneda | `http://localhost:8003/moneda` | `{"resultado": "cara"}` o `{"resultado": "cruz"}` |
| Saludo | `http://localhost:8004/hello` | `{"mensaje": "Hello World"}` |

La fecha corresponde al día actual en UTC, en formato `AAAA-MM-DD`.
Los pares son los primeros diez números pares positivos, del 2 al 20.
Cada petición a `/moneda` elige aleatoriamente entre cara y cruz.

## Arrancar con Docker

Requisitos: Docker y Docker Compose.

```bash
docker compose up --build
```

Los servicios se construyen desde el mismo Dockerfile, pero se ejecutan en
contenedores separados. Cada contenedor incluye únicamente el código de su
servicio. Para detenerlos:

```bash
docker compose down
```

## Arrancar sin Docker

Requisito: Python 3.11 o superior. Desde la raíz del proyecto:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

Ejecuta cada comando en una terminal distinta con el entorno virtual activado:

```bash
python -m uvicorn services.fecha.app.main:app --reload --port 8001
python -m uvicorn services.pares.app.main:app --reload --port 8002
python -m uvicorn services.moneda.app.main:app --reload --port 8003
python -m uvicorn services.saludo.app.main:app --reload --port 8004
```

## Probar los endpoints

```bash
curl http://localhost:8001/fecha
curl http://localhost:8002/pares
curl http://localhost:8003/moneda
curl http://localhost:8004/hello
```

Cada servicio tiene documentación interactiva en `/docs`, por ejemplo:
<http://localhost:8001/docs>.

## Pruebas automáticas

Con el entorno virtual activado:

```bash
python -m pip install -r requirements-dev.txt
python -m pytest
```

Las pruebas comprueban las respuestas HTTP de los cuatro servicios, incluidos
ambos resultados posibles de la moneda.

## Estructura

```text
services/
  fecha/app/main.py
  pares/app/main.py
  moneda/app/main.py
  saludo/app/main.py
tests/test_endpoints.py
compose.yaml
Dockerfile
requirements.txt
requirements-dev.txt
```
