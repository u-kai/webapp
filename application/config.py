import os

class SystemConfig:
    DEBUG = True

    user = os.environ["MYSQL_USER"]
    password = os.environ["MYSQL_PASSWORD"]
    host = os.environ["MYSQL_HOST"]
    db_name = os.environ["FIRST_WEB_APP"]
    SECRET_KEY = os.environ["WEB_SECRET_KEY"] 
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{user}:{password}@{host}/{db_name}?charset=utf8"

Config = SystemConfig