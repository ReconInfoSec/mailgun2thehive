import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    API_KEY=os.environ.get('HIVE_SECRET_KEY')
    HIVE_URL='https://myhive.mycompany.com'
    LOG_FILE='/var/log/mailgun2thehive.log'
