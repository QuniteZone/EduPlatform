import json

import openai
from config import model,temperature
import config


def load_json(content):
    try:
        json_obj = json.loads(content)
        return json_obj
    except json.JSONDecodeError as e:
        print(f"JSON解析错误: {e}")
        return None

def LLM_StreamOutput(messages):
    max_retries = 10
    retry_count = 0
    while retry_count < max_retries:
        # 调用 OpenAI API
        response = openai.chat.completions.create(
            model=model,
            temperature=temperature,
            messages=messages,
            max_tokens=4095,
        )

        # 提取模型返回的内容
        content = response.choices[0].message.content

        # 解析 JSON 内容
        result = load_json(content)
        if result:
            return result
        else:
            # 如果 JSON 解析失败，提供反馈并重试
            feedback = "请返回严格的 JSON 格式"
            messages.append({
                "role": "assistant",
                "content": content
            })
            messages.append({
                "role": "user",
                "content": feedback
            })
            retry_count += 1
            print(f"第 {retry_count} 次尝试")
    return False
lesson_plan_prompt = """
    一，任务描述：
    请你为{grade}，{subject}，{knowledge}，设计一份内容丰富且完整的教案。

    二，输出要求:
    # 格式规范
    1. 使用无缩进紧凑JSON格式，禁用Markdown代码块符号
    2. 字段顺序固定为：[输入模块,知识库检索,生成逻辑,输出样例]
    3. 每个层级的键名必须与示例完全一致（如"教学年级"不可改为"年级"）
    输出内容包含后缀表达式形式的新特征、新特征有用性描述、构造新特征的python字符串代码。输出格式需要严格按照如下格式来，且请确保你的输出能够被Python的json.loads函数解析，此外不要输出其他任何内容！
    4. 严格保持原始JSON键名层级结构
    5. 每个教学环节必须包含：
       - 可执行脚本（具体到教师语言示例）
       - 设计意图（结合建构主义/最近发展区等教学理论）
    6. 数学符号使用LaTeX格式

    ```json
    {{
        "CurrStandards": {{"Curriculum_Name": "本节课教学名称，名字要简洁且能概括本教案内容",
            "Curriculum_Content": "明确本课涉及的知识范畴与核心知识点",
            "Applicable_Context": "说明课程最适合的授课场景与条件限制",
            "Teaching_Objectives": "本节课希望学生达到的预期学习成果，包括知识、能力、情感等方面",
            "Core_Competency": "本节课着重培养的学生必备品格和关键能力",
            "Recommended_Sessions": "根据知识密度与学生基础规划的教学时间分配"
        }},
        "ActivityDesign": {{
            "Lesson_Introduction": {{
                "Teaching_Procedure": "通过情境创设或问题链激活前备知识，建立新旧知识联结。给出一个具体的可执行的脚本给老师执行",
                "Design_Intent": "细致解释本小结设置的意义是什么，并且给出上面部分输出内容具体设计的原因，内容要丰富"
            }},
            "Independent_Learning": {{
                "Teaching_Procedure": "学生运用导学资源独立完成基础性知识建构的认知过程。给出一个具体的可执行的脚本给老师执行，例如老师提出什么问题让同学讨论",
                "Design_Intent": "细致解释本小结设置的意义是什么，并且给出\"Teaching_Procedure\"部分具体设计的原因"
            }},
            "Case_Analysis": {{
                "Teaching_Procedure": "选取典型实例引导学生运用理论解决问题的探究活动，这个要和\"Lesson_Introduction(新课导入)\"\"Independent_Learning(自主学习)\"部分的内容相关联",
                "Design_Intent": "细致解释本小结设置的意义是什么，并且给出\"Teaching_Procedure\"部分具体设计的原因"
            }},
            "Learning_Assessment": {{
                "Teaching_Procedure": "贯穿课堂的形成性评估与三维目标达成度检测，给出这教案可以通过那几点教学评价",
                "Design_Intent": "细致解释本小结设置的意义是什么，并且给出\"Teaching_Procedure\"部分具体设计的原因"
            }},
            "Key_Summary": {{
                "Teaching_Procedure": "结构化梳理知识网络并提炼思维方法的总结环节",
                "Design_Intent": "细致解释本小结设置的意义是什么，并且给出\"Teaching_Procedure\"部分具体设计的原因"
            }},
            "Homework_Design": {{
                "Teaching_Procedure": "分层设计的巩固型任务与拓展型实践项目。这部分给出具体布置什么作业",
                "Design_Intent": "细致解释本小结设置的意义是什么，并且给出\"Teaching_Procedure\"部分具体设计的原因"
            }}
        }},
        "Competency_Development": "本课通过[实验误差分析/文本深度解读]等教学活动，重点发展学生的[学科专属能力]（如物理实验设计能力），同步渗透[跨学科能力]培养（如数据建模思维）。通过[具体教学策略]实现知识迁移，形成[可观测行为指标]（如提出2种实验改进方案），建立从素养培育到评估验证的完整闭环。"
    }}
    ```"""

promtp=lesson_plan_prompt.format(grade="高一",subject="数学",knowledge="三角函数")
messages = [{"role": "system",
                 "content": "你是一个教案生成专家，严格按JSON格式输出结构化教案内容，确保键值命名与层级关系绝对准确"},
                {"role": "user", "content": promtp}]

# print(f"###:{LLM_StreamOutput(messages)}\n###")





### 下面演示流式输出情况

import os
from openai import OpenAI

# 获取用户输入
# 初始化 OpenAI 客户端
API_KEY = 'sk-QBFgXmIcXeaR5v40BZN3jabFKtSkoudkpIz4vmGU6V8Uu4N6'  # 替换为有效密钥
BASE_URL = 'https://api.chatanywhere.tech/v1'  # 确保路径包含 /v1
model_name = 'gpt-3.5-turbo'
my_client = OpenAI(api_key=API_KEY, base_url=BASE_URL)

# 流式生成器函数
def generate():
    try:
        response = my_client.chat.completions.create(
            model=model_name,
            messages=[{"role": "user", "content": "你知道国家主席嘛"}],
            stream=True
        )
        for chunk in response:
            if chunk.choices and chunk.choices[0].delta.content:
                content = chunk.choices[0].delta.content
                print(f"内容：{(content).encode('utf-8') }")
                yield (content + "\n").encode('utf-8')  # 转换为字节
    except Exception as e:
        error_msg = f"Error: {str(e)}\n".encode('utf-8')
        yield error_msg


# print(f"开始演示流式：")
# for output in generate():
#     print(output, end='', flush=True)  # 使用 end='' 以避免换行，flush=True 以确保实时输出
#     print(f"\n#################\n")



###代码修改版####################################

def LLM_StreamOutput2(messages):
    max_retries = 10
    retry_count = 0
    while retry_count < max_retries:
        try:
            # 调用 OpenAI API，启用流式输出
            response = openai.chat.completions.create(
                model=model,
                temperature=temperature,
                messages=messages,
                max_tokens=4095,
                stream=True  # 启用流式输出
            )

            # 逐步提取模型返回的内容
            for chunk in response:
                if chunk.choices and chunk.choices[0].delta.content:
                    content = chunk.choices[0].delta.content
                    print(content, end='', flush=True)  # 实时输出内容

            # 解析 JSON 内容
            result = load_json(content)
            if result:
                return result
            else:
                # 如果 JSON 解析失败，提供反馈并重试
                feedback = "请返回严格的 JSON 格式"
                messages.append({
                    "role": "assistant",
                    "content": content
                })
                messages.append({
                    "role": "user",
                    "content": feedback
                })
                retry_count += 1
                print(f"第 {retry_count} 次尝试")
        except Exception as e:
            print(f"请求失败: {str(e)}")
            break  # 退出循环
    return False

# 调用流式输出函数
print(f"调用流式输出函数")
print(LLM_StreamOutput2(messages))


