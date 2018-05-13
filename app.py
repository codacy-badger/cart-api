from flask import Flask, request
from flask_restful import Resource, Api, abort

app = Flask(__name__)
api = Api(app)

products = []


class ProductsList(Resource):
    def get(self):
        return {'products': products}

    def post(self):
        product = {
            "_id": products[-1]["_id"] + 1,
            "name": request.json.get('name'),
            "price": request.json.get('price'),
            "description": request.json.get("description", "")
        }

        products.append(product)

        return {"product": product}, 201


class Product(Resource):
    def find_product(self, product_id):
        return [product for product in products if product['_id'] == product_id]

    def not_found(self, product_id, product):
        if len(product) == 0:
            return abort(404, message=f"Product { product_id } doesn't exit.")

    def get(self, product_id):
        product = self.find_product(product_id)
        self.not_found(product_id, product)
        return {'product': product[0]}

    def put(self, product_id):
        product = self.find_product(product_id)
        self.not_found(product_id, product)
        product[0]['name'] = request.json.get('name', product[0]['name'])
        product[0]['price'] = request.json.get('price', product[0]['price'])
        product[0]['description'] = request.json.get(
            'description', product[0]['description'])

        return {"products": products}

    def delete(self, product_id):
        product = self.find_product(product_id)
        self.not_found(product_id, product)
        products.remove(product[0])
        return {"products": products}


api.add_resource(ProductsList, '/products')
api.add_resource(Product, '/product/<int:product_id>')


if __name__ == '__main__':
    app.run(debug=True)
