from typing import Any, Dict, List

import tweepy

from src.connection import (
    trends_collection,
    friends_collection
)

from src.constants import BRAZIL_WOE_ID
from src.secrets import (
    ACCESS_TOKEN,
    ACCESS_TOKEN_SECRET,
    CONSUMER_KEY,
    CONSUMER_SECRET,
)


def _get_trends(woe_id: int, api: tweepy.API) -> List[Dict[str, Any]]:
    """Obtém os tópicos em alta da API do Twitter.

    Args:
        woe_id (int): Identificador da localização.

    Returns:
        List[Dict[str, Any]]: Lista de tópicos.
    """
    trends = api.get_place_trends(id=woe_id)

    return trends[0]["trends"]


def get_trends() -> List[Dict[str, Any]]:
    """Obtém os tópicos em alta persistidos no MongoDB.

    Args:
        woe_id (int): Identificador da localização.

    Returns:
        List[Dict[str, Any]]: Lista de tópicos.
    """
    trends = trends_collection.find({})
    return list(trends)


def save_trends() -> None:
    """Obtém os tópicos em alta e os salva no MongoDB."""
    auth = tweepy.OAuthHandler(consumer_key=CONSUMER_KEY, consumer_secret=CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

    api = tweepy.API(auth)

    trends = _get_trends(woe_id=BRAZIL_WOE_ID, api=api)
    trends_collection.insert_many(trends)


def get_friends(screen_name: str) -> List[int]:
    """Obtém uma lista de IDs dos amigos (usuários seguidos) para um determinado usuário.

    Args:
        screen_name (str): Nome de usuário do Twitter.

    Returns:
        List[int]: Lista de IDs dos amigos.
    """
    auth = tweepy.OAuthHandler(consumer_key=CONSUMER_KEY, consumer_secret=CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

    api = tweepy.API(auth)

    friend_ids = api.friends_ids(screen_name=screen_name)

    return friend_ids


def save_friends(screen_name: str) -> None:
    """Obtém os amigos de um usuário e os salva no MongoDB.

    Args:
        screen_name (str): Nome de usuário do Twitter.
    """
    friends = get_friends(screen_name)
    friends_collection.insert_many(friends)
