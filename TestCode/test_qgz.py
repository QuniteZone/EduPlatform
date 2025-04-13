lesson_plan_prompt = """
一，任务描述：
请你为{grade}，{subject}，{knowledge}，设计一份内容丰富且完整的教案。

```json
{{
    "CurrStandards": {{
        "Curriculum_Name": "本节课教学名称，名字要简洁且能概括本教案内容",
        "Curriculum_Content": "明确本课涉及的知识范畴与核心知识点",
        "Applicable_Context": "说明课程最适合的授课场景与条件限制",
        "Teaching_Objectives": "本节课希望学生达到的预期学习成果，包括知识、能力、情感等方面",
        "Core_Competency": "本节课着重培养的学生必备品格和关键能力",
        "Recommended_Sessions": "根据知识密度与学生基础规划的教学时间分配"
    }}
}}```"""


ddd=lesson_plan_prompt.format(grade="qgz",subject="dd",knowledge="dd")
print(f"content:{ddd}")