import re

from flask import jsonify
from flask_restful import Resource, reqparse
from mongoengine import NotUniqueError
from .model import UserModel


_user_parser = reqparse.RequestParser()
_user_parser.add_argument('cpf', type=str, required=True,
                          help='This field cannot be blank')
_user_parser.add_argument('name', type=str, required=True,
                          help='This field cannot be blank')
_user_parser.add_argument('last_name', type=str, required=True,
                          help='This field cannot be blank')
_user_parser.add_argument('email', type=str, required=True,
                          help='This field cannot be blank')
_user_parser.add_argument('birth_date', type=str, required=True,
                          help='This field cannot be blank')


class Users(Resource):
    def get(self):
        users = []
        for user in UserModel.objects():
            user_dict = user.to_mongo().to_dict()
            user_dict["_id"] = str(user_dict["_id"])  # 👈 isso aqui resolve o problema
            users.append(user_dict)
        
        return jsonify(users)

        # return jsonify(UserModel.objects())


class User(Resource):
    def validate_cpf(self, cpf):
        # Has the correct mask?
        if not re.match(r'\d{3}\.\d{3}\.\d{3}-\d{2}', cpf):
            return False

        # Grab only numbers
        numbers = [int(digit) for digit in cpf if digit.isdigit()]

        # Does it have 11 digits
        if len(numbers) != 11 or len(set(numbers)) == 1:
            return False

        # Validate first digit after
        sum_of_products = sum(a*b for a, b in zip(numbers[0:9],
                                                  range(10, 1, -1)))
        expect_digit = (sum_of_products * 10 % 11) % 10
        if numbers[9] != expect_digit:
            return False

        # validate second digit after
        sum_of_products = sum(a*b for a, b in zip(numbers[0:10],
                                                  range(11, 1, -1)))
        expect_digit = (sum_of_products * 10 % 11) % 10
        if numbers[10] != expect_digit:
            return False

        return True

    def post(self):
        data = _user_parser.parse_args()
        if not self.validate_cpf(data['cpf']):
            return {'message': 'CPF is invalid'}, 400

        try:
            response = UserModel(**data).save()
            return {'message': "User %s successfully created!" % response.id}
        except NotUniqueError:
            return {'message': "CPF already exists in database!"}, 400

    def get(self, cpf):
        print(f"Recebendo CPF: {cpf}")  # Adicione este log
        response = UserModel.objects(cpf=cpf)
        if response.count() > 0:
            users = []
            for user in response:
                user_dict = user.to_mongo().to_dict()
                user_dict["_id"] = str(user_dict["_id"])  # 👈 Converte o ObjectId
                users.append(user_dict)
            return jsonify(users)
        return {'message': 'User does not exist in database'}, 404
