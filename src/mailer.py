# Import Built-Ins
from datetime import datetime
# from smtplib import SMTP_SSL as SMTP <- TODO: we need SSL in prod.#
# use config to check which import? (we dont have the app context tho)

from smtplib import SMTP
from email.message import EmailMessage


class MailService:

    def __init__(self, app, app_name) -> None:
        self.app = app
        self.header_name = app_name

        self.MAIL_USER = self.FROM = self.app.config.MAIL_USER
        self.MAIL_PASS = self.app.config.MAIL_PASS
        self.MAIL_PORT = self.app.config.MAIL_PORT
        self.MAIL_SERVER = self.app.config.MAIL_SERVER 
        self.ADMIN_MAIL = self.app.config.ADMIN_MAIL


    def _subject(self, subject):
        return f'{self.header_name} {subject}'

    @property
    def connection(self):
        conn = SMTP()
        conn.connect(self.MAIL_SERVER, self.MAIL_PORT)
        if not self.app.config.DEBUG:
            conn.login(self.MAIL_USER, self.MAIL_PASS)

        return conn


    def send_error_mail(self, error, request, error_type=''):
        scope = request.scope
        timestamp = str(datetime.now())
        # todo: use starlette context for user agent



        endpoint = scope["endpoint"].__func__.__qualname__
        controller = scope["endpoint"].__self__.__class__.__name__
        path = scope["path"]
        path_params = scope["path_params"]
        subject = "[ERROR]"

        # mail content
        content = f"""Time: {timestamp}\n\n
            Error: {error}\n
            {error_type}
            Controller: {controller}\n
            Endpoint: {endpoint}\n
            Path: {path}\n
            Params: {path_params}
            """
        reciever = ADMIN_MAIL

        self._send(subject, content, reciever)


    def _send(self, subject, content, reciever):
        msg = EmailMessage()
        msg.set_content(content, subtype='html')
        msg['Subject'] = self._subject(subject)
        msg['From'] = self.FROM
        msg['to'] = reciever

        self.connection.send_message(msg)
        self.connection.quit()


