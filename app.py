from flask import Flask, request
from flask_restful import Resource, Api, abort

app = Flask(__name__)
api = Api(app)

products = [{'_id': 1, "name": "Nokia 2", "price": 9800,
             "description": "Some nice Desc about the product"}]


class ProductsList(Resource):
    def get(self):
        return {'products': products}


class Product(Resource):
    def find_product(self, product_id):
        return [product for product in products if product['_id'] == product_id]

    def get(self, product_id):
        self.product = self.find_product(product_id)
        if len(self.product) == 0:
            return abort(404, message=f"Product { product_id } doesn't exit.")
        return {'product': self.product[0]}


api.add_resource(ProductsList, '/products')
api.add_resource(Product, '/product/<int:product_id>')


if __name__ == '__main__':
    app.run(debug=True)
