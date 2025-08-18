from fastapi import Depends, FastAPI
from persistence.dependencies import get_db

app = FastAPI()


@app.get("/", dependencies=[Depends(get_db)])
def read_root():
    return {"Hello": "World"}
