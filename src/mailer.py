# Import Built-Ins

from datetime import datetime
#from smtplib import SMTP_SSL as SMTP
from smtplib import SMTP

from email.message import EmailMessage

# todo: get from env
# MAIL SETTTINGS
# todo: this is debug setting. use env config
ADMIN_MAIL = 'test@mail.lol'



class MailService:

    def __init__(self, app, app_name) -> None:
        self.app = app
        self.header_name = app_name

        # todo: cleanup dis!
        self.MAIL_USER = self.FROM = app.settings.MAIL_USER
        self.MAIL_PASS = app.settings.MAIL_PASS
        self.MAIL_PORT = app.settings.MAIL_PORT
        self.MAIL_SERVER = app.settings.MAIL_SERVER 


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


