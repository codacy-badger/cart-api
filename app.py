from flask import Flask
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

products = []


class ProductsList(Resource):
    def get(self):
        return {'products': products}


class Product(Resource):
    def find_product(self, product_id):
        return [product for product in products if product['id'] == product_id]

    def get(self, product_id):
        self.product = self.find_product(product_id)
        if len(self.product) == 0:
            return {'message': 'Not Found'}, 404
        return {'product': self.product[0]}


api.add_resource(ProductsList, '/products')
api.add_resource(Product, '/product/<int:product_id>')


if __name__ == '__main__':
    app.run(debug=True)
