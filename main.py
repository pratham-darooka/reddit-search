# brew services start docker
# docker build -t reddit-search .
# docker run -d -p 8000:8000 --name reddit-search-container reddit-search

__author__ = "pdarooka1011@gmail.com (Pratham Darooka)"

from fastapi import FastAPI
from search_utils import search_reddit
from globals import DIRECTORY

app = FastAPI()

@app.get("/search_reddit/")
def search_reddit_endpoint(user_request: str):
    # Call search_reddit function
    response = search_reddit(user_request, DIRECTORY)
    return {"answer": response}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
