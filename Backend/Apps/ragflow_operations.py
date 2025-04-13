import requests
import time
import os
from config import ragflow_BASE_URL,ragflow_API_KEY
from ragflow_sdk import RAGFlow,DataSet



rag_object = RAGFlow(api_key=ragflow_API_KEY, base_url=ragflow_BASE_URL)

dataset = rag_object.create_dataset(name="test_知识库2",description="测试数据集",embedding_model="text-embedding-3-small")


def get_file_paths(folder_path: str) -> list:
    file_paths = []
    # 遍历文件夹中的所有文件和子文件夹
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            # 获取文件的完整路径
            file_path = os.path.join(root, file)
            file_paths.append(file_path)

    file_doc_lists = []
    for file_path in file_paths:
        display_name = os.path.basename(file_path)  # 获取文件名
        with open(file_path, 'rb') as file:  # 以二进制模式打开文件
            blob = file.read()  # 读取文件内容
            file_doc_lists.append({"display_name": display_name, "blob": blob})

    return file_doc_lists

path=f"D:/projcet_LLM/EduPlatform/Backend/static/ragflowParserDocs"
file_doc_lists=get_file_paths(path)
print(file_doc_lists)

#上传文件到数据库，并进行解析
dataset.upload_documents(file_doc_lists)