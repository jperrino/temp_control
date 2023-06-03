from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import measure

app = FastAPI()

origins = ['*']
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # this is the list of domains which our API is allowed to talk to
    allow_credentials=True,
    allow_methods=["*"], # not only domains, but also only some http methods could be allowed
    allow_headers=["*"],
)

app.include_router(measure.router)

