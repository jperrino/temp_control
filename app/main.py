from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import measure, graph, message, device

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

