# CallMeBot Python Client

This module offers a simple client to the [CallMeBot](https://www.callmebot.com/) service to send Whatsapp, Telegram and Signal text messages.


## Installation

Install with `pip3 install callmebot`.


## Usage

1. You should first configure CallMeBot as explained at https://www.callmebot.com/

2. You should then configure your keys. There are two ways to do it:

    - Store them in the `~/.secrets/secrets.yml` file in a `callmebot` entry for the text services you wish to use:

        ```
        callmebot:
            whatsapp_phone: '555123123123'
            whatsapp_apikey: '999999'
            signal_phone: '555123123123'
            signal_apikey: '999999'
            telegram_username: 'username'
        ```

    - Set environment variables for the text services you wish to use:

        ```bash
        export CALLMEBOT_WHATSAPP_PHONE='555123123123'
        export CALLMEBOT_WHATSAPP_APIKEY='999999'
        export CALLMEBOT_SIGNAL_PHONE='555123123123'
        export CALLMEBOT_SIGNAL_APIKEY='999999'
        export CALLMEBOT_TELEGRAM_USERNAME='username'
        ```

    The tool uses the `~/.secrets/secrets.yml` file first and the environment variables as fallback. If you do not configure some text service, you cannot use it.

3. Call the desired function (`whatsapp`, `signal`, `telegram`|) with the message to be sent:

    ```python
    import callmebot

    callmebot.whatsapp('This is an important message!\nRegards.')
    ```

4. Or, use the `callmebot` command line:

    ```bash
    callmebot whatsapp 'This is an important message!\nRegards.'
    ```

    Get help with `--help`:

    ```bash
    callmebot --help
    ```

## Credits

- [Jordi Petit](https://github.com/jordi-petit)


## License

Apache License 2.0
