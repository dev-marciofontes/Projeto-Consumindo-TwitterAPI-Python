from typing import Any, Dict, List

import tweepy
import uvicorn
from tweepy import API

from fastapi import FastAPI

from src.responses import TrendItem
from src.services import (
    get_trends,
    save_trends,
    get_friends,
    save_friends
)

app = FastAPI()


@app.get("/trends", response_model=List[TrendItem])
def get_trends_route():
    return get_trends()


@app.get("/friends/{screen_name}", response_model=List[int])
def get_friends_route(screen_name: str):
    return get_friends(screen_name)


if __name__ == "__main__":
    trends = get_trends()

    if not trends:
        save_trends()

    uvicorn.run(app, host="0.0.0.0", port=8000)
