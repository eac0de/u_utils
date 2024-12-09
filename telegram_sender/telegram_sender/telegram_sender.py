import aiohttp

_CHAT_ID: int = 0
_TELEGRAM_BOT_TOKEN: str = ""


class TelegramSender:

    @staticmethod
    async def send(message: str):
        try:
            url = f"https://api.telegram.org/bot{_TELEGRAM_BOT_TOKEN}/sendMessage"
            payload = {
                "chat_id": _CHAT_ID,
                "text": message[:4000],
            }
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    url=url,
                    data=payload,
                    timeout=aiohttp.ClientTimeout(total=5),
                ):
                    pass
        except:
            pass


async def config_telegram_sender(
    chat_id: int | None = None,
    telegram_bot_token: str | None = None,
):

    if chat_id is not None:
        global _CHAT_ID
        _CHAT_ID = chat_id
    if telegram_bot_token is not None:
        global _TELEGRAM_BOT_TOKEN
        _TELEGRAM_BOT_TOKEN = telegram_bot_token
