from flask import Blueprint, jsonify, request
from .genericFunction import LLM,lesson_plan_prompt

#这是教案生成
lesson_plan_bp = Blueprint('lesson_plan', __name__)

@lesson_plan_bp.route("/generate", methods=["GET","POST"])
def generate():
    return jsonify({"result": "这是一个内容内容内容"})


@lesson_plan_bp.route('/lesson_plan', methods=['GET', 'POST'])
def get_lesson_plan():
    if request.method == 'POST':
        grade=request.json.get('grade')
        subject = request.json.get('subject')
        knowledge=request.json.get('knowledge')
    else:
        grade = request.args.get('grade')
        subject = request.args.get('subject')
        knowledge = request.args.get('knowledge')
    promtp=lesson_plan_prompt.format(grade=grade, subject=subject, knowledge=knowledge)
    messages = [{"role": "system",
                 "content": "你是一个教案生成专家，严格按Markdown格式输出结构化教案内容，确保键值命名与层级关系绝对准确"},
                {"role": "user", "content": promtp}]

    return_result=LLM(messages)
    content={} #返回结构

    if return_result==False:
        content["status"]=0 #报错
        content["content"]=None
    else:
        content["status"]=1
        content["content"]=return_result

    return_result=jsonify(content)
    return return_result




@lesson_plan_bp.route("/get_info", methods=["POST"])
def get_info():
    data = request.get_json()
    grade = data.get('grade')
    subject = data.get('subject')
    content = f"生成的内容:年级-{grade}，课程 - {subject}"

    return "test"

"""
1.零代码实现前端，时间重点花费在功能实现上面。
2.重点不是UI，重点实现功能是什么程度。一定程度上在集成到贵兰在线上面去。
3.以我们为主，集成到贵兰上面去。
4.PPT——AiPPT开源框架。
5.


"""



