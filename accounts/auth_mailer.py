import requests

EMAIL_BASE_URL = "https://email.microapi.dev/v1"
CONFIRMATION_EMAIL_PATH = "/send_confirmation/"
WELCOME_EMAIL_PATH = "/send_welcome/"

MICRODEV_EMAIL= "phemmylintry@gmail.com"  # "no-reply@microapi.dev"
MICRODEV_EMAIL_API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjVmMjJmY2QxYTUwOTA4MDAwNGQ5MmVlMSIsImVtYWlsIjoidWphbWVzNDFAeWFob28uY29tIiwiREJVUkkiOiJtb25nb2RiK3NydjovL2Z1bGxzdGFjazpmdWxsc3RhY2tAc2FuZGJveC0xbG00aC5tb25nb2RiLm5ldC9hdXRoLWFwcD9yZXRyeVdyaXRlcz10cnVlIiwiaWF0IjoxNTk2MTMzODMyfQ.Hj4qWdwl7F-nDsI76noGLMo-hz0uZphntLMjG-SPMQs"
SITE_NAME = "microAPI.dev"


class MicroApiMailer:
    def __init__(self, sender=MICRODEV_EMAIL, company_name=SITE_NAME):
        self.sender = sender
        self.company_name = company_name
        self.backend_type = ""

    def send_confirmation_link(self, recipient, link):
        body = "Thank you for signing up to our service. Follow the link provided" \
               " to complete your registration on our site"
        path = CONFIRMATION_EMAIL_PATH
        return self._send_link(recipient, path, body, confirmation_link=link)

    def send_welcome_link(self, recipient, link):
        body = ""
        path = WELCOME_EMAIL_PATH
        return self._send_link(recipient, path, body, login_link=link)

    def _send_link(self, recipient, _path, body, **kwargs):
        url = EMAIL_BASE_URL + _path
        body = body
        payload = {
            "recipient": recipient,
            "body": body,
            "site_name": self.company_name,
            "sender": self.sender,
            "backend_type": self.backend_type,
        }
        for key in kwargs:
            payload[key] = kwargs[key]

        req = requests.request("POST", url, data=payload)
        if req.status_code == 200:
            return self._on_success()
        else:
            return self._on_failure()

    def _on_success(self):
        return 'success', 200

    def _on_failure(self):
        return 'failure', 400

    def __repr__(self):
        return "<MicroApiMailer: {}>".format(self.sender)

    __str__ = __repr__
