from flask import Blueprint, jsonify

ppt_generator_bp = Blueprint('ppt_generator', __name__)

@ppt_generator_bp.route('/ppt', methods=['GET'])
def generate_ppt():
    return jsonify({"message": "This is the PPT generator blueprint!"})