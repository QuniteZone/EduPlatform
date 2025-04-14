import requests
import json

API_HOST = "http://127.0.0.1"
API_KEY = "ragflow-k5MTJmNmQ0MDdiMjExZjA5ZWY4MDI0Mm"
AGENT_ID = "0882ecc8168011f0a0f20242ac120003"
question = "中国国家主席是谁"

# 请求url
url = API_HOST + "/api/v1/agents/" + AGENT_ID + "/completions"
# print(url)

# 自定义请求头
headers = {
    "Authorization": "Bearer %s" % API_KEY,
    "Content-Type": "application/json",
}


class AgentStreamResponse:
    def __init__(self):
        pass

    def get_session_id(self):
        """
        获取会话 ID
        """
        data = {"id": AGENT_ID}
        # response = requests.post(url, data=data, headers=headers)
        try:
            line_list = []
            with requests.post(
                    url, json=data, headers=headers, stream=True, timeout=30
            ) as response:
                if response.status_code == 200:
                    for line in response.iter_lines():
                        if line:  # 过滤掉空行
                            line_list.append(line.decode("utf-8"))
                else:
                    print(f"请求失败，状态码: {response.status_code}")
                    return False

            first_line = line_list[0]
            line_row = first_line.split("data:")[1]# 提取data内容
            line_dict = json.loads(line_row)# json解析
            session_id = line_dict["data"]["session_id"]# 获取session_id
            return session_id
        except requests.exceptions.RequestException as e:
            print(f"请求错误: {e}")
            return False

    def get_data(self,stream=False):
        """
        获取数据
        :return:
        """
        try:
            session_id = self.get_session_id()
            data = {
                "id": AGENT_ID,
                "question": question,
                "stream": "true",
                "session_id": session_id,
            }
            with requests.post(url, json=data, headers=headers, stream=stream, timeout=30) as response:
                if response.status_code == 200:
                    if stream:
                        lines = response.iter_lines()
                        line_list = []  # 用于存储所有行
                        for line in lines:
                            if line:  # 过滤掉空行
                                decoded_line = line.decode("utf-8")
                                line_list.append(decoded_line)  # 将解码后的行添加到列表中

                        second_last_data = line_list[-2]
                        # for line in response.iter_lines():
                        #     if line:  # 过滤掉空行
                        #         print(line.decode("utf-8"))

                    else:
                        print(response.text)
                        print(f"{type(response.text)}")

                        # 将数据字符串按行分割
                        lines = response.text.strip().split('\n\n')
                        second_last_data = lines[-2]
                    json_part = second_last_data.split("data:")[1]  # 获取 提取 JSON 部分 "data:" 后面的部分
                    data_object = json.loads(json_part) # 解析 JSON 字符串为字典对象
                    return data_object
                else:
                    print(f"请求失败，状态码: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"请求错误: {e}")


if __name__ == "__main__":
    agent_stream_response = AgentStreamResponse()
    return_result= agent_stream_response.get_data(stream=True)
    print(f"return_result: {return_result}")