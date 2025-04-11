from flask import Blueprint, jsonify

lesson_plan_bp = Blueprint('lesson_plan', __name__)

@lesson_plan_bp.route('/lesson_plan', methods=['GET'])
def get_lesson_plan():
    return jsonify({"message": "This is the lesson plan blueprint!"})