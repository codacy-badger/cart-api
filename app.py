from flask import Flask, request
from flask_restful import Resource, Api, abort

app = Flask(__name__)
api = Api(app)

products = []


def find_product(product_id):
    return [product for product in products if product['product_id'] == product_id]


class ProductsList(Resource):
    def get(self):
        return {'products': products}

    def post(self):
        data = request.get_json()
        product = {
            "product_id": products[-1]["product_id"] + 1 if products else 1,
            "name": data['name'],
            "price": data['price'],
            "description": data['description']
        }

        products.append(product)

        return {"product": product}, 201


class Product(Resource):
    def get(self, product_id):
        product = find_product(product_id)
        if len(product) == 0:
            return abort(404, message=f"Product { product_id } doesn't exit.")
        return {'product': product[0]}

    def put(self, product_id):
        product = find_product(product_id)
        if len(product) == 0:
            return abort(404, message=f"Product { product_id } doesn't exit.")
        product[0]['name'] = request.json.get(
            'name', product[0]['name'])
        product[0]['price'] = request.json.get('price', product[0]['price'])
        product[0]['description'] = request.json.get(
            'description', product[0]['description'])

        return {"products": products}

    def delete(self, product_id):
        product = find_product(product_id)
        if len(product) == 0:
            return abort(404, message=f"Product { product_id } doesn't exit.")
        products.remove(product[0])
        return {"products": products}


api.add_resource(ProductsList, '/products')
api.add_resource(Product, '/product/<int:product_id>')


if __name__ == '__main__':
    app.run(debug=True)
