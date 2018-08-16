from settings import settings


def log(text):
    if settings.debug:
        print(text)
