import os

class Config:
    SECRET_KEY = 'SECRETSECRETSECRET'
    # SQLALCHEMY_DATABASE_URI = 'postgresql://samsproject:@localhost/samsdatabase'
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'
    SQLALCHEMY_DATABASE_URI = 'cockroachdb://krustel:vibe8FX9XSAchdkpZA9spQ@samsproject-5581.7s5.aws-ap-south-1.cockroachlabs.cloud:26257/defaultdb?sslmode=require'
    SQLALCHEMY_TRACK_MODIFICATIONS = False