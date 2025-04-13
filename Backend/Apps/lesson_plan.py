from flask import Blueprint, jsonify
from .genericFunction import LLM,lesson_plan_prompt

#这是教案生成
lesson_plan_bp = Blueprint('lesson_plan', __name__)

@lesson_plan_bp.route("/generate", methods=["GET","POST"])
def generate():
    return jsonify({"result": "这是一个内容内容内容"})



@lesson_plan_bp.route('/lesson_plan', methods=['GET', 'POST'])
def get_lesson_plan():
    messages = [{"role": "system",
                 "content": "你是一个教案生成专家，严格按JSON格式输出结构化教案内容，确保键值命名与层级关系绝对准确"},
                {"role": "user", "content": lesson_plan_prompt}]
    print(f"test:###\n{LLM(messages)}\n###")

    return jsonify({"message": "This is the lesson plan blueprint!"})