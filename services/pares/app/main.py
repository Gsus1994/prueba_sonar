from fastapi import FastAPI

app = FastAPI(title="Servicio de números pares")


@app.get("/pares")
def obtener_pares() -> dict[str, list[int]]:
    """Devuelve los primeros diez números pares positivos."""
    return {"pares": list(range(2, 21, 2))}
