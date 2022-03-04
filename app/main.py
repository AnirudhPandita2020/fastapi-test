
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers import post,user,auth,vote

from .config import Settings


settings = Settings()

# models.Base.metadata.create_all(bind=engine)




app = FastAPI()

origins = ["https://www.google.co.in"]

app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials =True,
    allow_methods =["*"],
    allow_headers = ["*"],
)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

@app.get("/")
def root():
    return {"message": "hello world"}



