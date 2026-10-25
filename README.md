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

## SonarCloud y CI

El workflow `.github/workflows/sonar.yml` ejecuta las pruebas y genera cobertura
en cada push a cualquier rama y al abrir o actualizar una PR. Después envía el
análisis a [SonarCloud](https://sonarcloud.io/dashboard?id=Gsus1994_prueba_sonar)
y espera el resultado del Quality Gate: si falla, también falla el CI.
Se puede ejecutar manualmente desde la pestaña Actions de GitHub.

`sonar-project.properties` contiene los identificadores reales del proyecto:

- Organización: `gsus1994`.
- Proyecto: `Gsus1994_prueba_sonar`.
- Servidor: `https://sonarcloud.io`.

Para activar el análisis en GitHub:

1. En [los secretos de Actions del repositorio](https://github.com/Gsus1994/prueba_sonar/settings/secrets/actions),
   crea un secreto llamado `SONAR_TOKEN` con un token vigente que tenga permisos
   de análisis sobre este proyecto. Usa un token nuevo si el anterior se compartió.
2. En SonarCloud, abre **Administration > Analysis Method** y desactiva
   **Automatic Analysis** si está habilitado. El análisis lo ejecutará el CI,
   tal como indica la [documentación oficial de cobertura para Python](https://docs.sonarsource.com/sonarqube-cloud/analyzing-source-code/test-coverage/python-test-coverage).
3. Publica los cambios en GitHub para que se ejecute el workflow.

El token se obtiene de `secrets.SONAR_TOKEN`; nunca se guarda en los archivos
del repositorio. Si falta en un evento con acceso a secretos, el workflow falla
con un mensaje que indica cómo configurarlo. En PRs desde forks y ejecuciones
de Dependabot se ejecutan las pruebas y se omite el escaneo, porque GitHub no
les proporciona los secretos de Actions del repositorio.

Para generar el mismo informe de cobertura localmente:

```bash
python -m coverage run -m pytest -q
python -m coverage xml
python -m coverage report
```

Con `pysonar` instalado y `SONAR_TOKEN` definido en el entorno, basta ejecutar
`pysonar` desde la raíz para usar las mismas claves y el informe `coverage.xml`.
Las carpetas `.sonar/` y `.scannerwork/` y los informes de cobertura se ignoran
en Git; son archivos generados y no se deben versionar.

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
