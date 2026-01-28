from fastapi import FastAPI
from time7_gateway.api import verify, admin

app = FastAPI(title="Time7 Authentication Gateway")

# Register routers
app.include_router(verify.router, prefix="/api")
app.include_router(admin.router, prefix="/admin")


@app.get("/")
def hello():
    return {"message": "Hello FastAPI, Time7 Gateway is running!"}
