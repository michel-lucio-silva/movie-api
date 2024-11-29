from flask import Blueprint, jsonify
from app.utils import get_award_intervals

api = Blueprint('api', __name__)

@api.route('/producers/award-intervals', methods=['GET'])
def award_intervals():
    return jsonify(get_award_intervals())
