#### 该文件用于存放各蓝图功能所通用功能函数、提示词等信息
import json
import re

import docx
import fitz
import openai
from Apps.ragflow_operations import RAGflow
from Apps.config import model,temperature,ragflow_BASE_URL,ragflow_API_KEY
import Apps.config

ALLOWED_EXTENSIONS = {'pdf', 'docx'} #在生成逐字稿时，所允许上传的文件类型
ragflow = RAGflow(ragflow_BASE_URL,ragflow_API_KEY)

def format_lesson_plan(text):
    # 使用正则表达式提取被 ```markdown 和 ``` 包裹的内容
    match = re.search(r'```markdown\s*(.*?)\s*```', text, re.DOTALL)
    if match:
        # 提取匹配到的内容并去掉前后的空白
        return match.group(1).strip()
    else:
        return False

def LLM(messages):
    max_retries = 5
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
        result = format_lesson_plan(content)

        if result:
            return result
        else:
            # 如果 JSON 解析失败，提供反馈并重试
            feedback = "请返回严格的 Markdown 格式"
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


def LLM_StreamOutput(messages):
    response = openai.chat.completions.create(
        model=model,
        temperature=temperature,
        messages=messages,
        max_tokens=4095,
        stream=True  # 启用流式输出
    )

    # 提取模型返回的内容
    content = response.choices[0].message.content

    # 逐步提取模型返回的内容
    for chunk in response:
        if chunk.choices and chunk.choices[0].delta.content:
            content = chunk.choices[0].delta.content
            print(content, end='', flush=True)  # 实时输出内容

    return content



def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def extract_text_from_pdf(path):
    text = ''
    try:
        pdf = fitz.open(stream=path.read(), filetype="pdf")
        for page in pdf:
            text += page.get_text()
    except Exception as e:
        text = f"[PDF解析失败]: {str(e)}"
    return text

def extract_text_from_docx(path):
    text = ''
    try:
        doc = docx.Document(path)
        for para in doc.paragraphs:
            text += para.text + '\n'
    except Exception as e:
        text = f"[Word解析失败]: {str(e)}"
    return text




######## 下面为提示词设计 #######

lesson_plan_prompt = """
        一，任务描述：
        请你为{grade}，{subject}，{knowledge}，设计一份内容丰富且完整的教案。

        二，输出要求:
        # 格式规范
        1. 使用Markdown代码块符号返回
        2. 字段顺序固定为：[输入模块,知识库检索,生成逻辑,输出样例]
        3. 每个教学环节必须包含：
           - 可执行脚本（具体到教师语言示例）
           - 设计意图（结合建构主义/最近发展区等教学理论）
        4. 数学符号使用LaTeX格式
        5. 每个层级的键名必须与示例完全一致（如"教学年级"不可改为"年级"）输出格式需要严格按照如下格式来，此外不要输出其他任何内容！输出的内容用{{}}包裹。

        ```markdown
        # 教案

## 课程标准

- **教学名称**: 本节课教学名称，名字要简洁且能概括本教案内容
- **教学内容**: 明确本课涉及的知识范畴与核心知识点
- **适用情境**: 说明课程最适合的授课场景与条件限制
- **教学目标**: 本节课希望学生达到的预期学习成果，包括知识、能力、情感等方面
- **核心素养**: 本节课着重培养的学生必备品格和关键能力
- **建议课时**: 根据知识密度与学生基础规划的教学时间分配

## 活动设计

### 新课导入
- **教学程序**: 通过情境创设或问题链激活前备知识，建立新旧知识联结。给出一个具体的可执行的脚本给老师执行。
- **设计意图**: 细致解释本小结设置的意义是什么，并且给出上面部分输出内容具体设计的原因，内容要丰富。

### 自主学习
- **教学程序**: 学生运用导学资源独立完成基础性知识建构的认知过程。给出一个具体的可执行的脚本给老师执行，例如老师提出什么问题让同学讨论。
- **设计意图**: 细致解释本小结设置的意义是什么，并且给出"教学程序"部分具体设计的原因。

### 案例分析
- **教学程序**: 选取典型实例引导学生运用理论解决问题的探究活动，这个要和"新课导入"、"自主学习"部分的内容相关联。
- **设计意图**: 细致解释本小结设置的意义是什么，并且给出"教学程序"部分具体设计的原因。

### 学习评价
- **教学程序**: 贯穿课堂的形成性评估与三维目标达成度检测，给出这教案可以通过那几点教学评价。
- **设计意图**: 细致解释本小结设置的意义是什么，并且给出"教学程序"部分具体设计的原因。

### 小结
- **教学程序**: 结构化梳理知识网络并提炼思维方法的总结环节。
- **设计意图**: 细致解释本小结设置的意义是什么，并且给出"教学程序"部分具体设计的原因。

### 作业布置
- **教学程序**: 分层设计的巩固型任务与拓展型实践项目。这部分给出具体布置什么作业。
- **设计意图**: 细致解释本小结设置的意义是什么，并且给出"教学程序"部分具体设计的原因。

## 素养培养
本课通过[实验误差分析/文本深度解读]等教学活动，重点发展学生的[学科专属能力]（如物理实验设计能力），同步渗透[跨学科能力]培养（如数据建模思维）。通过[具体教学策略]实现知识迁移，形成[可观测行为指标]（如提出2种实验改进方案），建立从素养培育到评估验证的完整闭环。```
        """
