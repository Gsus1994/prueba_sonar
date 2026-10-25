from fastapi import FastAPI

app = FastAPI(title="Servicio de saludo")


@app.get("/hello")
def saludar() -> dict[str, str]:
    """Devuelve el saludo Hello World."""
    return {"mensaje": "Hello World"}
