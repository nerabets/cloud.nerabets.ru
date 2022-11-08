import os

class Config(): 
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASEURL")
    SECRET_KEY = "02*Bf)rWU+v#tdg3SHn/cc!MA=sm*S2e*4S:rWff7VAi2D#cTp6iYl.4BkB(Jcb=!mnNyAzd!35EDz:7-7(k!i5:+-)fX=98AC!BZ)H1SJ6uzmG)-z*nsOaglBU8JR*B"
    CORS_ALLOWED = ['http://192.168.0.197:8080/']
    JWT_ACCESS_TOKEN_EXPIRES = "ACCESS_EXPIRES"
