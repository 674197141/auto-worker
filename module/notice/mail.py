import yagmail
from config import get_config


class Mail:

    def __init__(self):
        config = get_config('mail')
        self.user = config.user
        self.password = config.password
        self.host = config.host
        self.yag = yagmail.SMTP(
            user=mail.user, password=mail.password, host=mail.host)

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
