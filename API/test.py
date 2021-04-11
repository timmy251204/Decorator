from flask import Flask
from flask_restful import Resource, Api, reqparse, abort

app = Flask(__name__)
api = Api(app)

ITEMS = [
        {
            'name': 'chair',
            'price': 1500,
        }

]

class main(Resource):
    def get(self):
        return {'hello': 'world'}




def abort_if_name_doesnt_exist(name):
    if list(filter(lambda item: item['name'] == name, ITEMS)) == [] :
        return abort(404, message="name {} doesn't exist".format(name))

def abort_if_name_already_exist(name):
    if list(filter(lambda item: item['name'] == name, ITEMS)) != []:
        return abort(404,  message="name {} already exist".format(name))


parser = reqparse.RequestParser()
parser.add_argument('price')
parser.add_argument('items', type=dict, action="append")


class Item(Resource):
    def get(self, name):
        abort_if_name_doesnt_exist(name)
        item = list(filter(lambda item: item['name'] == name, ITEMS))
        return item

    def post(self, name):
        abort_if_name_already_exist(name)
        args = parser.parse_args()
        ITEMS.append({'name': name, 'price': args['price']})
        return ITEMS[-1], 201

    def put(self, name):
        abort_if_name_doesnt_exist(name)
        args = parser.parse_args()
        item = {'name': name, 'price': args['price']}
        if list(filter(lambda item: item['name'] == name, ITEMS)) == []:
            ITEMS.append({'name': name, 'price': args['price']})
        else:
            ITEMS[ITEMS.index(*list(filter(lambda item: item['name'] == name, ITEMS)))] = item
        return item, 201

    def delete(self, name):
        abort_if_name_doesnt_exist(name)
        del ITEMS[ITEMS.index(*list(filter(lambda item: item['name'] == name, ITEMS)))]
        return '', 204


class ItemList(Resource):

    def get(self):
        return ITEMS

    def post(self):
        args = parser.parse_args()
        for i in range(len(args['items'])):
            abort_if_name_already_exist(args['items'][i]['name'])
            ITEMS.append(args['items'][i])
        return "Successfully added items {}".format(args['items']), 201









api.add_resource(Item, '/items/<name>')
api.add_resource(main, '/')
api.add_resource(ItemList, '/items')

if __name__ == '__main__':
    app.run(debug=True)