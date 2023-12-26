from typing import Optional
import requests
import os
import yaml
from urllib.parse import quote


"""
You should first configure CallMeBot as explained at https://www.callmebot.com/
"""


def get(envvar: str, entry: str) -> Optional[str]:
    if 'callmebot' in secrets and entry in secrets['callmebot']:
        return str(secrets['callmebot'][entry]).strip()
    else:
        return os.getenv(envvar)


try:
    secrets_path = os.path.expanduser("~/.secrets/secrets.yml")
    secrets = yaml.load(open(secrets_path), Loader=yaml.Loader)
except:
    secrets = {}


whatsapp_phone = get('CALLMEBOT_WHATSAPP_PHONE', 'whatsapp_phone')
whatsapp_apikey = get('CALLMEBOT_WHATSAPP_APIKEY', 'whatsapp_apikey')
signal_phone = get('CALLMEBOT_SIGNAL_PHONE', 'signal_phone')
signal_apikey = get('CALLMEBOT_SIGNAL_APIKEY', 'signal_apikey')
telegram_username = get('CALLMEBOT_TELEGRAM_USERNAME', 'telegram_username')


def whatsapp(message: str) -> str:
    """Send a Whatsapp message."""

    assert whatsapp_phone is not None
    assert whatsapp_apikey is not None

    text = quote(message)
    url = f'https://api.callmebot.com/whatsapp.php?phone={whatsapp_phone}&apikey={whatsapp_apikey}&text={text}'
    return requests.get(url).text


def signal(message: str) -> str:
    """Send a Signal message."""

    assert signal_phone is not None
    assert signal_apikey is not None

    text = quote(message)
    url = f'https://api.callmebot.com/signal.php?phone={signal_phone}&apikey={signal_apikey}&text={text}'
    return requests.get(url).text


def telegram(message: str) -> str:
    """Send a Telegram message."""

    assert telegram_username is not None

    text = quote(message)
    url = f'https://api.callmebot.com/text.php?user={telegram_username}&text={text}'
    return requests.get(url).text
