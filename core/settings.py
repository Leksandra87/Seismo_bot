from os import getenv
from pathlib import Path
from dataclasses import dataclass


@dataclass(frozen=True)
class SetData:
    bot_token: str
    admin_id: str
    api_key: str
    base_dir: str = f"{Path(__file__).resolve().parent.parent}"


def get_settings():
    return SetData(
        bot_token=getenv("BOT_TOKEN"),
        admin_id=getenv("ADMIN_ID"),
        api_key=getenv("API_KEY")
    )


settings = get_settings()
