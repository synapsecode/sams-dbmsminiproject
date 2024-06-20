import os

class Config:
    SECRET_KEY = 'SECRETSECRETSECRET'
    SQLALCHEMY_DATABASE_URI = 'postgresql://samsproject:@localhost/samsdatabase'
    SQLALCHEMY_TRACK_MODIFICATIONS = False