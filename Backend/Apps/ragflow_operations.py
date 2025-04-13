import requests
import time
import os
from config import ragflow_BASE_URL,ragflow_API_KEY


HEADERS = {
    "Authorization": f"Bearer {ragflow_API_KEY}",
    "Content-Type": "application/json"
}


def create_dataset(name: str, description: str = "") -> str:
    """
    创建数据集，返回 dataset_id
    参数:
        name: 数据集名称
        description: 数据集描述
    """
    timestamp = int(time.time())
    unique_name = f"{name}_{timestamp}"

    url = f"{ragflow_BASE_URL}/api/v1/datasets"
    payload = {
        "name": unique_name,
        "description": description
    }

    response = requests.post(url, headers=HEADERS, json=payload)
    data = response.json()

    if data.get("code") == 0:
        dataset_id = data["data"]["id"]
        return dataset_id
    else:
        raise Exception(f"❌ 创建数据集失败: {data}")




def upload_and_parse_documents(dataset_id: str, file_paths: list) -> list:
    """
    批量上传文档到指定数据集并自动解析

    参数:
        dataset_id: 数据集ID
        file_paths: 要上传的文件路径列表

    返回:
        文档ID列表

    异常:
        如果上传或解析失败则抛出异常
    """
    # 1. 上传文档
    upload_url = f"{ragflow_BASE_URL}/api/v1/datasets/{dataset_id}/documents"
    document_ids = []

    try:
        for file_path in file_paths:
            with open(file_path, 'rb') as file:
                # 使用files参数上传文件
                response = requests.post(
                    upload_url,
                    headers={"Authorization": f"Bearer {ragflow_API_KEY}"},
                    files={'file': (os.path.basename(file_path), file)}
                )

                if response.status_code != 200:
                    raise Exception(f"上传失败，状态码: {response.status_code}, 响应: {response.text}")

                data = response.json()

                if data.get("code") != 0:
                    raise Exception(f"上传失败: {data}")

                document_id = data["data"][0]["id"]
                document_ids.append(document_id)
                print(f"✅ 文档上传成功: {document_id}")

        # 2. 触发解析
        parse_url = f"{ragflow_BASE_URL}/api/v1/datasets/{dataset_id}/chunks"
        parse_payload = {
            "document_ids": document_ids
        }

        parse_response = requests.post(parse_url, headers=HEADERS, json=parse_payload)
        parse_data = parse_response.json()

        if parse_data.get("code") != 0:
            raise Exception(f"解析触发失败: {parse_data}")

        print("✅ 批量文档解析已触发")
        return document_ids

    except Exception as e:
        raise Exception(f"❌ 批量上传和解析过程中出错: {str(e)}")



def get_file_paths(folder_path: str) -> list:
    """
    获取指定文件夹中的所有文件路径列表
    参数:
        folder_path: 文件夹路径
    返回:
        file_paths: 包含所有文件路径的列表
    """
    file_paths = []
    # 遍历文件夹中的所有文件和子文件夹
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            # 获取文件的完整路径
            file_path = os.path.join(root, file)
            file_paths.append(file_path)

    return file_paths



# 示例使用：
if __name__ == "__main__":
    try:
        # 1. 创建数据集
        dataset_id = create_dataset("测试数据集", "上传文档并解析测试")

        # 2. 上传并解析文档
        folder_path = "D:\projcet_LLM\EduPlatform\Backend\static\ragflowParserDocs"

        file_paths = get_file_paths(folder_path)
        document_id = upload_and_parse_documents(dataset_id, file_paths)

        print(f"🎉 操作成功完成！数据集ID: {dataset_id}, 文档ID: {document_id}")

    except Exception as e:
        print(f"❌ 操作失败: {str(e)}")