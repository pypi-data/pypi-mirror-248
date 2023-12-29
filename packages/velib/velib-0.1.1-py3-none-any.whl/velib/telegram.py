from datetime import datetime
import requests
import logging
import time

TELEGRAM_CHATS=''
TELEGRAM_BOT_TOKEN=''

TIMEOUT = 5
RETRIES = 5
RETRY_DELAY = 3
TG_CHATS = TELEGRAM_CHATS.split(',')
TG_BOT_TOKEN = TELEGRAM_BOT_TOKEN
URL_REQUEST_TEMPLATE = "https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text={text}"
URL = "https://api.telegram.org/bot{token}/sendMessage"

TELEGRAM_ENABLED = True if TG_BOT_TOKEN and TG_CHATS else False

def send_message(message: str):
    if TELEGRAM_ENABLED:
        response = None
        for chat_id in TG_CHATS:
            response = _send_message(chat_id, message)
        return response


def _send_message(chat_id, message):
    data = dict(chat_id=chat_id, text=message)
    send_url = URL.format(token=TG_BOT_TOKEN)
    for i in range(RETRIES):
        try:
            response = requests.post(send_url, json=data, timeout=TIMEOUT)
        except Exception as e:
            if i < RETRIES - 1:
                time.sleep(RETRY_DELAY)
                continue
            else:
                raise
        return response


class AdminTelegramHandler(logging.Handler):
    """An exception log handler that emails log entries to site admins.

    If the request is passed as the first argument to the log record,
    request data will be provided in the email report.
    """
    
    def __init__(self, *args, **kwargs):
        super().__init__()
        self.include_html = kwargs.get('include_html')
        self.email_backend = kwargs.get('email_backend')
        self.reporter_class = kwargs.get('reporter_class')
        # TODO self.reporter_class = import_string(reporter_class or settings.DEFAULT_EXCEPTION_REPORTER)
    
    def emit(self, record):
        message = "{levelname}: [{datetime}] {name}\nPath: {path}\nLine: {line}\nMessage: {msg}\n" \
                  "ExceptionInfo: {exc_info}\nException: {exc_text}".format(
            levelname=record.levelname,
            datetime=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            name=record.name,
            path=record.pathname,
            line=record.lineno,
            msg=record.getMessage(),
            exc_info=record.exc_info,
            exc_text=record.exc_text
        )
        send_message(message)
