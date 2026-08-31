import os
from dotenv import load_dotenv
from dataclasses import dataclass

load_dotenv()

@dataclass
class config:
    bot_token : str = os.getenv("TG_BOT_TOKEN")
#    admin_ids : list[int] = [int(x) for x in os.getenv("TG_ADMIN_IDS", "").split]
    debug_mode : bool = os.getenv("TG_DEBUG", "false").lower() == "true"
def load_config() -> config:
    return config()