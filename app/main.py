import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import measure, graph, message, device
from app.config import common_settings

app = FastAPI()

origins = ['*']
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(measure.router)
app.include_router(graph.router)
app.include_router(message.router)
app.include_router(device.router)


@app.get("/")
async def root():
    return {"message": "Server is up"}

if __name__ == "__main__":
    uvicorn.run("app.main:app",
                host=common_settings.app_host,  # localhost
                port=common_settings.app_port,  # 8000
                reload=True)

