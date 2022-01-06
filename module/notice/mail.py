import yagmail
from config import get_config


class Mail:

    def __init__(self):
        mail = get_config('mail')
        self.user = mail.get('user')
        self.password = mail.get('password')
        self.host = mail.get('host')


    @staticmethod
    def create_mail():
        mail = Mail()
        return mail

    def send(self, to, title, contents):
        yag = yagmail.SMTP(
            user=self.user, password=self.password, host=self.host)
        yag.send(to=to, subject=title,
                 contents=contents)


if __name__ == '__main__':
    mail = Mail.create_mail()
    mail.send()
