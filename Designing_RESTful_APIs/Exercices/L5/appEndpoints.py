import requests

from flask import Blueprint
from flask_login import current_user
from flask import redirect, request, render_template, url_for, jsonify

from models import User, MealRequest
from dbSession import session

from loginAPIKeyDecorator import require_api_key
from keyHelper import get_foursquare_key_dict, get_mapquest_key_dict

app_endpoints = Blueprint('app_endpoints', __name__)

mapquest_key_dict = get_mapquest_key_dict()
foursquare_key_dict = get_foursquare_key_dict()

@app_endpoints.route('/v1/users', methods = ['GET', 'PUT', 'DELETE'])
@require_api_key
def get_all_users():
    if request.method == 'GET':
        user_list = session.query(User).all()
        if user_list is not None:
            return jsonify([user.serialize for user in user_list])
        else:
            return 'None'
    elif request.method == 'PUT':
        username = request.json.get('user_name')
        new_password = request.json.get('password')
        new_token    = request.json.get('token')
        if username is not None:
            current_user = session.query(User).filter_by(user_name=username).first()
        else:
            current_user = None
        if current_user is not None:
            if new_password is not None:
                current_user.hash_password(new_password)
            if new_token is not None:
                current_user.api_key = new_token
            session.commit()
            return jsonify(dict(message="Success, updated user: {}!".format(username))),201
        else:
            return jsonify(dict(message="ERROR, not all parameter provided!")),404
    elif request.method == 'DELETE':
        username = request.json.get('user_name')
        if username is not None:
            current_user = session.query(User).filter_by(user_name=username).first()
        else:
            current_user = None
        if current_user is not None:
            session.delete(current_user)
            session.commit()
            return jsonify(dict(message="Success, deleted user: {}!".format(username))),200
        else:
            return jsonify(dict(message="ERROR, user not found or not provided!")),404

@app_endpoints.route('/v1/users/<int:id>', methods=['GET'])
@require_api_key
def get_user_with_id(id):
    user_search = session.query(User).filter_by(id=id).first()
    if user_search is not None:
        return jsonify(user_search.serialize),200
    else:
        return jsonify(dict(message="ERROR, user {} not found!".format(id))),404


@app_endpoints.route('/v1/requests', methods = ['GET', 'POST'])
@require_api_key
def show_make_user_requests():
    if request.method == 'GET':
        meal_requests = session.query(MealRequest).all()
        if meal_requests is not None:
            return jsonify( [req.serialize for req in meal_requests])
        else:
            return 'None'
    elif request.method == 'POST':
        try:
            new_meal_request = MealRequest(**request.json,user_id=current_user.id)
            response = requests.get('https://api.foursquare.com/v2/venues/search',params={**foursquare_key_dict, 'v':'20180323', 'limit':1,
                            'near':request.json.get('location_area'),
                            'query':request.json.get('meal_type')})
            if response.status_code != 200:
                return jsonify(dict(message="ERROR, foursquare api not working {}!".format(status_code))),404

            new_meal_request.location_name = response.json().get('response').get('venues')[0].get('name')
            new_meal_request.latitude = response.json().get('response').get('geocode').get('feature').get('geometry').get('center').get('lat')
            new_meal_request.longitude =  response.json().get('response').get('geocode').get('feature').get('geometry').get('center').get('lng')
            current_user.meal_requests.append(new_meal_request)
            session.commit()
            return jsonify(dict(message="Success, created request: {}!".format(new_meal_request.id))),201
        except ValueError as value_error:
            return jsonify(dict(message=value_error.args)),404
        return 'None'

@app_endpoints.route('/v1/requests/<int:id>', methods = ['GET', 'PUT', 'DELETE'])
@require_api_key
def show_make_edit_specific_user_request(id):
    if request.method == 'GET':
        request_query = session.query(MealRequest).filter_by(id=id).first()
        if request_query is not None:
            return jsonify(request_query.serialize),200
        else:
            return 'None'
