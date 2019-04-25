from flask_restful import Resource,reqparse
from flask_jwt import jwt_required

from models.item import ItemModel


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price', type=float,required = True)
    parser.add_argument('store_id', type=int,required = True)

    @jwt_required()
    def get(self,name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message': 'Item not found'},404

    @jwt_required()
    def post(self,name):
        if ItemModel.find_by_name(name):
            return {'message':"An item with this name, '{}', is already in the database".format(name)},400
        
        data=Item.parser.parse_args()

        item=ItemModel(name,**data)
        try:
            item.save_to_db()
        except:
            return {'message': "An error occurred inserting an item."},500
        
        return item.json(), 201

    @jwt_required()
    def delete(self,name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
        return {'message': 'Item deleted!'}
        
    @jwt_required()
    def put(self,name):
        data = Item.parser.parse_args()
        
        item = ItemModel.find_by_name(name)

        if not item: 
           item = ItemModel(name,**data)
        else: 
            item.price = data['price']
            item.store_id = data['store_id']

        item.save_to_db()
        
        return item.json()
        
        

class ItemList(Resource):
    def get(self):
        return {'items':[item.json() for item in ItemModel.query.all()]}
