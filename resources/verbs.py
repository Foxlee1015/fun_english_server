# -*- coding: utf-8 -*-
import traceback

from flask_restplus import Namespace, Resource, fields, reqparse

from core import db
from core.resource import CustomResource, response, json_serializer
from core.utils import token_required

api = Namespace('verbs', description='Verbs related operations')


def create_verb(args):
        return db.insert_verb(
            args["present"], args["past"],
            args["participle"], args["is_irregular"],
            args["learn_level"])
        

def update_verb(id_, args):
    return db.update_verb(
        id_, args["present"], args["past"],
        args["participle"], args["is_irregular"],
        args["learn_level"])


def delete_verbs(ids):
    return db.delete_verbs(ids)


# https://flask-restplus.readthedocs.io/en/stable/parsing.html
parser_verb = reqparse.RequestParser()
parser_verb.add_argument('present', type=str, required=True, location='args')

parser_verb_tense = reqparse.RequestParser()
parser_verb_tense.add_argument('present', type=str, required=True, location='args')
parser_verb_tense.add_argument('past', type=str, required=True, location='args')
parser_verb_tense.add_argument('participle', type=str, required=True, location='args')
parser_verb_tense.add_argument('is_irregular', type=int, required=True, location='args')

parser_verb_learn_level = reqparse.RequestParser()
parser_verb_learn_level.add_argument('learn_level', type=int, required=True, location='args')

parser_ids = reqparse.RequestParser()
parser_ids.add_argument('ids', type=str, required=True, action='split')

parser_header = reqparse.RequestParser()
parser_header.add_argument('Authorization', type=str, location='headers')

@api.route('/')
@api.response(404, 'Server error')
class Verbs(CustomResource):
    @api.doc('get verbs')
    def get(self):
        verbs = db.get_verbs()
        return self.send(status=200, result=verbs)
    

    @api.doc('create a new verb')
    @api.expect(parser_verb_tense, parser_verb_learn_level, parser_header)
    # @token_required
    def post(self, **kwargs):
        args = parser_verb_tense.parse_args()
        args.update(parser_verb_learn_level.parse_args())
        
        result = create_verb(args)
            
        status = 201 if result else 400
        return self.send(status=status)


    @api.doc('delete verbs')
    @api.expect(parser_ids, parser_header)
    # @token_required
    def delete(self,  **kwargs):
        args = parser_ids.parse_args()
        result = delete_verbs(args["ids"])
        status = 200 if result else 500
        return self.send(status=status)


@api.route('/search')
class VerbSearch(CustomResource):
    @api.doc('find verb')
    @api.expect(parser_verb)
    def get(self):
        args = parser_verb.parse_args()
        
        verb = db.get_verb(args["present"])
        if verb is None:
            status = 204
        elif verb:
            status = 200
        else:
            status = 500

        return self.send(status=status, result=verb)


@api.route('/<id_>')
@api.param('id_', 'The verb identifier')
@api.response(404, 'Verb not found')
class Verb(CustomResource):
    @api.doc('update_verb')
    @api.expect(parser_verb_tense, parser_verb_learn_level, parser_header)
    # @token_required
    def put(self, id_, **kwargs):
        args = parser_verb_tense.parse_args()
        args.update(parser_verb_learn_level.parse_args())
        
        print("????")
        result = update_verb(id_, args)
            
        status = 201 if result else 400
        return self.send(status=status)
