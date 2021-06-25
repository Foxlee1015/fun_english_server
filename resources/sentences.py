# -*- coding: utf-8 -*-
import traceback

from flask_restplus import Namespace, Resource, fields, reqparse

from core import db
from core.resource import CustomResource, response, json_serializer
from core.utils import token_required

api = Namespace('sentences', description='Sentences related operations')


def create_sentence(args):
    try:
        text = args["text"]
        learn_level = args["learn_level"]
        db.insert_sentence(text,learn_level)
        return True
    except:
        traceback.print_exc()
        return False

def delete_sentences(ids):
    try:
        db.delete_sentences(ids)
        return True
    except:
        traceback.print_exc()
        return False

def update_sentence(args):
    try:
        text = args["text"]
        learn_level = args["learn_level"]
        db.update_sentence(text,learn_level)
        return True
    except:
        traceback.print_exc()
        return False


# https://flask-restplus.readthedocs.io/en/stable/parsing.html
parser_create = reqparse.RequestParser()
parser_create.add_argument('text', type=str, required=True, location='form')
parser_create.add_argument('learn_level', type=int, required=True, location='form')

parser_delete = reqparse.RequestParser()
parser_delete.add_argument('ids', type=str, required=True, action='split')

parser_header = reqparse.RequestParser()
parser_header.add_argument('Authorization', type=str, location='headers')

@api.route('/')
class Sentences(CustomResource):
    @api.doc('get sentences')
    @api.expect(parser_header)
    def get(self, **kwargs):
        sentences = db.get_sentences()
        print(sentences)
        return self.send(status=200, result=sentences)
    
    @api.doc('create a new sentence')
    @api.expect(parser_create, parser_header)
    # @token_required
    def post(self, **kwargs):
        args = parser_create.parse_args()
        
        result = create_sentence(args)
            
        status = 201 if result else 400
        return self.send(status=status)

    @api.doc('delete sentences')
    @api.expect(parser_delete, parser_header)
    # @token_required
    def delete(self,  **kwargs):
        args = parser_delete.parse_args()
        delete_sentences(args["ids"])
        return self.send(status=200)


@api.route('/<id_>')
@api.param('id_', 'The sentence identifier')
@api.response(404, 'Sentence not found')
class Sentence(CustomResource):
    @api.doc('update_sentence')
    @api.expect(parser_create, parser_header)
    # @token_required
    def put(self, id_, **kwargs):
        args = parser_create.parse_args()
        
        result = update_sentence(id_, args)
            
        status = 201 if result else 400
        return self.send(status=status)

