from datetime import datetime, timezone

from fastapi import FastAPI

app = FastAPI(title="Servicio de fecha")


@app.get("/fecha")
def obtener_fecha() -> dict[str, str]:
    """Devuelve la fecha actual en UTC."""
    return {"fecha": datetime.now(timezone.utc).date().isoformat()}
