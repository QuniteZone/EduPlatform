import requests

# 设置请求的 URL
url = 'https://94686t61i9.zicp.fun/plan/lesson_script'  # 根据你的 Flask 应用地址进行修改

# 要上传的文件路径
# file_paths = ['D:/projcet_LLM/EduPlatform/TestCode/test.docx']
# file_paths = ['D:/projcet_LLM/EduPlatform/TestCode/ttt.pdf']  # 替换为实际文件路径
file_paths = ['D:/projcet_LLM/EduPlatform/TestCode/test.docx','D:/projcet_LLM/EduPlatform/TestCode/ttt.pdf']  # 替换为实际文件路径

# 创建一个字典来存储文件
files = []
for file_path in file_paths:
    # 直接在 files 列表中打开文件，保持文件打开状态
    files.append(('files', (file_path.split('/')[-1], open(file_path, 'rb'))))

# 其他表单数据
data = {
    'require': '需要的逐字稿要求'  # 替换为实际的需求
}

# 发起 POST 请求
try:
    response = requests.post(url, files=files, data=data)
    # 打印响应内容
    print(response.status_code)
    print(response.json())
finally:
    # 确保在请求后关闭所有打开的文件
    for _, file_tuple in files:
        file_tuple[1].close()
