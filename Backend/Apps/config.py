import json
import os
import openai

DIALECT = 'mysql'
DRIVER = 'pymysql'
USERNAME = 'root'
PASSWORD = '123456'
HOST = '127.0.0.1'
PORT = '3306'
DATABASE = 'eduplatform'

#mysql 不会认识utf-8,而需要直接写成utf8
SQLALCHEMY_DATABASE_URI = "{}+{}://{}:{}@{}:{}/{}?charset=utf8".format(DIALECT,DRIVER,USERNAME,PASSWORD,HOST,PORT,DATABASE)
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_ECHO = True


#LLM 基本配置信息
os.environ["OPENAI_BASE_URL"] = "https://api.chatanywhere.tech/v1"
os.environ["OPENAI_API_KEY"] = "sk-OyEPaIflRbJXIospoq197kPskfatY1UmbfKKOszLJicK7RuJ"
model = "gpt-4o-mini"
