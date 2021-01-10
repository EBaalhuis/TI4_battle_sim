import os


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'aeaq56a5yaq5a737yu'
