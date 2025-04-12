import json
import os
import openai

SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:root@localhost/test'
SQLALCHEMY_TRACK_MODIFICATIONS = False

#LLM 基本配置信息
os.environ["OPENAI_BASE_URL"] = "https://api.chatanywhere.tech/v1"
os.environ["OPENAI_API_KEY"] = "sk-OyEPaIflRbJXIospoq197kPskfatY1UmbfKKOszLJicK7RuJ"
model = "gpt-4o-mini"
