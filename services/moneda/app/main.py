from secrets import choice
from typing import Literal

from fastapi import FastAPI

app = FastAPI(title="Servicio de cara o cruz")


@app.get("/moneda")
def lanzar_moneda() -> dict[str, Literal["cara", "cruz"]]:
    """Lanza una moneda y devuelve cara o cruz."""
    return {"resultado": choice(("cara", "cruz"))}
