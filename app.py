from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from routes import post, user, auth
from docs import router as docs_router


app = FastAPI(redoc_url=None)
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(docs_router)


@app.get("/")
async def root():
    return RedirectResponse(url="/redoc")
