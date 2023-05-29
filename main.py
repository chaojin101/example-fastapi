from database import engine
from app import app as app
import models


models.Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", reload=True)
