from flask import Blueprint, jsonify, request
from .genericFunction import LLM,lesson_plan_prompt,allowed_file,extract_text_from_pdf,extract_text_from_docx,ragflow

#这是教案生成
lesson_plan_bp = Blueprint('lesson_plan', __name__)

#自动生成教案
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


#这是依据教案生成逐字稿的过程
@lesson_plan_bp.route('/lesson_script', methods=['POST'])
def handle_lesson_script():
    try:
        transcription_requirements = request.form.get('require') #
        uploaded_files = request.files.getlist('files')
        parsed_texts = {}
        content = {}  # 返回结构
        content["status"] = 1
        content["content"] = None
        updata_text=""
        if not uploaded_files:
            content["status"] = -1  # 表示文件未上传
            return jsonify(content)
        for file in uploaded_files:
            if file and allowed_file(file.filename):
                ext = file.filename.rsplit('.', 1)[1].lower()  # 直接读取文件内容
                if ext == 'pdf':
                    parsed_text = extract_text_from_pdf(file.stream)  # 使用 file.stream 直接读取
                else:
                    parsed_text = extract_text_from_docx(file.stream)  # 使用 file.stream 直接读取
                parsed_texts[file.filename] = parsed_text
                updata_text+=f"{file.filename}:{parsed_text}\n"
            else:
                content["status"] = -2  # 不支持该文件类型
                return jsonify(content)
                break
        ##将从知识库中检索内容，然后作为输入一并给到LLM进行处理。



        #【待处理中中！！！！！！！！！！！】
        content["content"] = f"这是逐字稿, 逐字稿要求: {transcription_requirements} + '解析' + {updata_text}"
        print(f"content:{content}")
        return jsonify(content)
    except Exception as e:
        content["status"] = 0 #报错
        return jsonify(content)







@lesson_plan_bp.route("/gen_question", methods=["POST"])
def get_info():
    data = request.get_json()# 从请求中获取 JSON 数据

    # 检查必需的参数是否存在
    required_fields = ['subject', 'grade', 'textbook', 'topic', 'questionType', 'difficulty', 'questionCount',
                       'knowledgePoints', 'otherRequirements']
    for field in required_fields:
        if field not in data:
            return jsonify({
        "content": None,
        "status": 0  #缺少参数
    })

    # 提取参数
    subject = data['subject']  #学科
    grade = data['grade']  #年级
    textbook = data['textbook']  #教材名称
    topic = data['topic']  #主题
    question_type = data['questionType']  #题型
    difficulty = data['difficulty']  #难度
    question_count = data['questionCount']  #问题数量
    knowledge_points = data['knowledgePoints']   #知识点
    other_requirements = data['otherRequirements']   #其他要求



    return jsonify({
        "content": "智能出题测试示例",
        "status": 1
    })




