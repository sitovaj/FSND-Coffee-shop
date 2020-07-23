import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)

'''
@DONE uncomment the following line to initialize the datbase
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
'''
db_drop_and_create_all()

# ROUTES
'''
@DONE implement endpoint
    GET /drinks
        it should be a public endpoint
        it should contain only the drink.short() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''


@app.route('/drinks', methods=['GET'])
def get_drinks():
    selection = Drink.query.order_by('id').all()
    drinks = [drink.short() for drink in selection]
    if len(selection) == 0:
        # to throw error when there's no drinks to display
        abort(404)
    return jsonify({
        'success': True,
        'drinks': drinks
    }), 200


'''
@DONE implement endpoint
    GET /drinks-detail
        it should require the 'get:drinks-detail' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''


@app.route('/drinks-detail', methods=['GET'])
@requires_auth('get:drinks-detail')
def get_drinks_details(payload):
    selection = Drink.query.order_by('id').all()
    if len(selection) == 0:
        # to throw error when there's no drinks to display
        abort(404)
    drinks = [drink.long() for drink in selection]

    return jsonify({
        'success': True,
        'drinks': drinks
    })


'''
@DONE implement endpoint
    POST /drinks
        it should create a new row in the drinks table
        it should require the 'post:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the newly created drink
        or appropriate status code indicating reason for failure
'''


@app.route('/drinks', methods=['POST'])
@requires_auth('post:drinks')
def post_drinks(payload):
    body = request.get_json()  # get drink information
    if body == None:
        abort(404)
    # from request get necessary info on new drink, if it's not given, then it'll be None
    new_drink_title = body.get('title', None)
    new_recipe = body.get('recipe', None)
    try:
        drink = Drink(title=new_drink_title, recipe=json.dumps([new_recipe]))
        drink.insert()
        return jsonify({
            'success': True,
            'drinks': drink.long()
        })
    except exc.IntegrityError:
        return jsonify({
            "status": False,
            "message": "This title already exists"})
    except:
        abort(422)


'''
@DONE implement endpoint
    PATCH /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should update the corresponding row for <id>
        it should require the 'patch:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the updated drink
        or appropriate status code indicating reason for failure
'''


@app.route('/drinks/<id>', methods=['PATCH'])
@requires_auth('patch:drinks')
def patch_drinks(payload, id):
    body = request.get_json()  # get request information sent within URL
    try:
        drink = Drink.query.filter(
            Drink.id == id).one_or_none()  # find drink by id
        if not drink:
            raise
        if 'title' in body:
            drink.title = body.get('title')
        if 'recipe' in body:
            drink.recipe = json.dumps(body.get('recipe'))
        drink.update()

        return jsonify({
            'success': True,
            "drinks": [drink.long()]
        })
    except:
        if not drink:
            abort(404)
        abort(400)


'''
@DONE implement endpoint
    DELETE /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should delete the corresponding row for <id>
        it should require the 'delete:drinks' permission
    returns status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
        or appropriate status code indicating reason for failure
'''


@app.route('/drinks/<id>', methods=['DELETE'])
@requires_auth('delete:drinks')
def delete_drinks(payload, id):
    try:
        drink = Drink.query.filter(
            Drink.id == id).one_or_none()  # find drink by id
        # if drink is None:
        #     abort(404)
        if not drink:
            raise
        drink.delete()

        return jsonify({
            'success': True,
            'delete': id
        })
    except:
        if not drink:
            abort(404)
        abort(400)


# Error Handling
'''
Example error handling for unprocessable entity
'''


@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422


'''
@DONE implement error handlers using the @app.errorhandler(error) decorator
    each error handler should return (with approprate messages):
             jsonify({
                    "success": False, 
                    "error": 404,
                    "message": "resource not found"
                    }), 404

'''


@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": "resource not found"
    }), 404


@app.errorhandler(400)
def bad_request(error):
    return jsonify({
        "success": False,
        "error": 400,
        "message": "Bad request, server couldnt understand it"
    }), 400


@app.errorhandler(405)
def not_allowed(error):
    return jsonify({
        "success": False,
        "error": 405,
        "message": "Method not allowed"
    }), 405


@app.errorhandler(500)
def not_allowed(error):
    return jsonify({
        "success": False,
        "error": 500,
        "message": " Internal Server Error, check your request"
    }), 500


'''
@DONE implement error handler for AuthError
    error handler should conform to general task above 
'''


@app.errorhandler(AuthError)
def auth_error(e):
    return jsonify(e.error), e.status_code
