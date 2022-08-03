from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from . import models, config
from .database import engine
from .routers import post, user, auth, vote

# Create tables with SQLAlchemy
# models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Make a connection to the routes made in separate files
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

# Root of site
@app.get("/")
def root():
    return {"message": "Hello World"}



# title str, content str