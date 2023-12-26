import callmebot
import typer
import html2text

app = typer.Typer(
    help='Send a Whatsapp, Signal or Telegram text message with CallMeBot. Configuration of CallMeBot is necessary.'
)


@app.command()
def whatsapp(
    message: str,
    phone: str = typer.Option('', envvar='CALLMEBOT_WHATSAPP_PHONE'),
    apikey: str = typer.Option('', envvar='CALLMEBOT_WHATSAPP_APIKEY'),
) -> None:
    """Send a WhatsApp message with CallMeBot."""

    if phone != '':
        callmebot.whatsapp_phone = phone
    if apikey != '':
        callmebot.whatsapp_apikey = apikey
    print(html2text.html2text(callmebot.whatsapp(message)))


@app.command()
def signal(
    message: str,
    phone: str = typer.Option('', envvar='CALLMEBOT_SIGNAL_PHONE'),
    apikey: str = typer.Option('', envvar='CALLMEBOT_SIGNAL_APIKEY'),
) -> None:
    """Send a Signal message with CallMeBot."""

    if phone != '':
        callmebot.signal_phone = phone
    if apikey != '':
        callmebot.signal_apikey = apikey
    print(html2text.html2text(callmebot.signal(message)))


@app.command()
def telegram(
    message: str,
    username: str = typer.Option('', envvar='CALLMEBOT_TELEGRAM_USERNAME'),
) -> None:
    """Send a Telegram message with CallMeBot."""

    if username != '':
        callmebot.telegram_username = username
    print(html2text.html2text(callmebot.telegram(message)))


def main() -> None:
    app()


if __name__ == "__main__":
    main()
