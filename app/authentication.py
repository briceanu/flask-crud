from .redis_client import redis_client


def black_list_token(jti: str, ttl: int) -> None:
    """
    blacklists the token using the token's id and setting
    and setting a time to live.
    """
    redis_client.setex(f"blacklist:{jti}", ttl, "true")


def is_token_blacklisted(jti: str) -> bool:
    """checks to see if the token is already blacklisted"""
    return redis_client.exists(f"blacklist:{jti}") == 1
