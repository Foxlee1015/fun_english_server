# -*- coding: utf-8 -*-
import traceback

from flask_restplus import Namespace, Resource, fields, reqparse

from core import db
from core.resource import CustomResource, response, json_serializer
from core.utils import token_required

api = Namespace('verbs', description='Verbs related operations')


def create_verb(args):
    try:
        present = args["present"]
        past = args["past"]
        participle= args["participle"]
        is_irregular = args["is_irregular"]
        learn_level = args["learn_level"]
        db.insert_verb(present,past,participle,is_irregular,learn_level)
        return True
    except:
        traceback.print_exc()
        return False

def update_verb(id_, args):
    try:
        present = args["present"]
        past = args["past"]
        participle= args["participle"]
        is_irregular = args["is_irregular"]
        learn_level = args["learn_level"]
        db.update_verb(id_, present,past,participle,is_irregular,learn_level)
        return True
    except:
        traceback.print_exc()
        return False


def delete_verbs(ids):
    try:
        db.delete_verb(ids)
        return True
    except:
        traceback.print_exc()
        return False


# https://flask-restplus.readthedocs.io/en/stable/parsing.html
parser_create = reqparse.RequestParser()
parser_create.add_argument('present', type=str, required=True, location='form')
parser_create.add_argument('past', type=str, required=True, location='form')
parser_create.add_argument('participle', type=str, required=True, location='form')
parser_create.add_argument('is_irregular', type=int, required=True, location='form')
parser_create.add_argument('learn_level', type=int, required=True, location='form')

parser_delete = reqparse.RequestParser()
parser_delete.add_argument('ids', type=str, required=True, action='split')

parser_header = reqparse.RequestParser()
parser_header.add_argument('Authorization', type=str, location='headers')

@api.route('/')
class Verbs(CustomResource):
    @api.doc('get verbs')
    @api.expect(parser_header)
    def get(self, **kwargs):
        verbs = db.get_verbs()
        print(verbs)
        return self.send(status=200, result=verbs)
    
    @api.doc('create a new verb')
    @api.expect(parser_create, parser_header)
    # @token_required
    def post(self, **kwargs):
        args = parser_create.parse_args()
        
        result = create_verb(args)
            
        status = 201 if result else 400
        return self.send(status=status)

    @api.doc('delete verbs')
    @api.expect(parser_delete, parser_header)
    # @token_required
    def delete(self,  **kwargs):
        args = parser_delete.parse_args()
        delete_verbs(args["ids"])
        return self.send(status=200)


@api.route('/<id_>')
@api.param('id_', 'The verb identifier')
@api.response(404, 'Verb not found')
class Verb(CustomResource):
    @api.doc('update_verb')
    @api.expect(parser_create, parser_header)
    # @token_required
    def put(self, id_, **kwargs):
        args = parser_create.parse_args()
        
        result = update_verb(id_, args)
            
        status = 201 if result else 400
        return self.send(status=status)

