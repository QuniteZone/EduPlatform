from flask import Blueprint, jsonify
from .genericFunction import LLM


lesson_plan_bp = Blueprint('lesson_plan', __name__)

@lesson_plan_bp.route("/generate", methods=["GET","POST"])
def generate():
    return jsonify({"result": "这是一个内容内容内容"})





@lesson_plan_bp.route('/lesson_plan', methods=['GET', 'POST'])
def get_lesson_plan():

    print(f"test:{LLM()}")

    return jsonify({"message": "This is the lesson plan blueprint!"})