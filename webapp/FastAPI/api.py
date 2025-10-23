from fastapi import FastAPI
from get_last_prediction import get_last_prediction
from fastapi.responses import JSONResponse

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "API is working"}

@app.get("/last-prediction")
def last_prediction():
    try:
        result = get_last_prediction()
        if result is None:
            return JSONResponse(content={"error": "No se encontraron datos"}, status_code=404)
        return result
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)


@app.get("/routes")
def list_routes():
    routes = []
    for route in app.routes:
        routes.append({
            "path": route.path,
            "name": route.name,
            "methods": list(route.methods) if hasattr(route, 'methods') else []
        })
    return routes