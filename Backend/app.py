from flask import Flask, jsonify
from flask_cors import CORS
# 导入蓝图
from Apps.lesson_plan import lesson_plan_bp
from Apps.ppt_generator import ppt_generator_bp
from Apps.DatabaseTables import db,User
import Apps.config

app = Flask(__name__)

# 注册蓝图
app.register_blueprint(lesson_plan_bp, url_prefix='/plan')  # 可以设置 URL 前缀
app.register_blueprint(ppt_generator_bp, url_prefix='/ppt')  # 可以设置 URL 前缀
CORS(app)

app.config.from_object(Apps.config)
db.init_app(app)

@app.route('/')
def home():
    return "你好呀，这里是EduPlatform系统！"


# 增加用户
@app.route('/users/add', methods=['POST',"GET"])
def add_user():
    new_user = User(
        token='sample_token',
        mobile='1234567890',
        head='http://example.com/image.jpg',
        nickName='Test User',
        status=None  # 假设状态为 None
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User added successfully!'}), 201

# 查询用户
@app.route('/users/get/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get(user_id)
    if user:
        return jsonify({
            'id': user.id,
            'token': user.token,
            'mobile': user.mobile,
            'head': user.head,
            'nickName': user.nickName,
            'status': user.status
        }), 200
    return jsonify({'message': 'User not found!'}), 404

# 更新用户
@app.route('/users/update/<int:user_id>', methods=['GET','POST'])
def update_user(user_id):
    user = User.query.get(user_id)
    if user:
        # 使用假设的新数据进行更新
        user.token = 'updated_token'
        user.mobile = '0987654321'
        user.head = 'http://example.com/new_image.jpg'
        user.nickName = 'Updated User'
        user.status = None  # 假设状态为 None
        db.session.commit()
        return jsonify({'message': 'User updated successfully!'}), 200
    return jsonify({'message': 'User not found!'}), 404

# 删除用户
@app.route('/users/delete/<int:user_id>', methods=['GET','POST'])
def delete_user(user_id):
    user = User.query.get(user_id)
    if user:
        db.session.delete(user)
        db.session.commit()
        return jsonify({'message': 'User deleted successfully!'}), 200
    return jsonify({'message': 'User not found!'}), 404


if __name__ == '__main__':
    with app.app_context():  # 进入应用上下文
        db.create_all()  # 创建表格
    app.run(host='0.0.0.0',port=5001, debug=True)