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
            "product_id": products[-1]["product_id"] + 1 if products else 1,
            "name": request.json.get('name'),
            "price": request.json.get('price'),
            "description": request.json.get("description", "")
        }

        products.append(product)

        return {"product": product}, 201


class Product(Resource):
    def find_product(self, productproduct_id):
        return [product for product in products if product['product_id'] == productproduct_id]

    def not_found(self, productproduct_id, product):
        if len(product) == 0:
            return abort(404, message=f"Product { productproduct_id } doesn't exit.")

    def get(self, productproduct_id):
        product = self.find_product(productproduct_id)
        self.not_found(productproduct_id, product)
        return {'product': product[0]}

    def put(self, productproduct_id):
        product = self.find_product(productproduct_id)
        self.not_found(productproduct_id, product)
        product[0]['name'] = request.json.get('name', product[0]['name'])
        product[0]['price'] = request.json.get('price', product[0]['price'])
        product[0]['description'] = request.json.get(
            'description', product[0]['description'])

        return {"products": products}

    def delete(self, productproduct_id):
        product = self.find_product(productproduct_id)
        self.not_found(productproduct_id, product)
        products.remove(product[0])
        return {"products": products}


api.add_resource(ProductsList, '/products')
api.add_resource(Product, '/product/<int:productproduct_id>')


if __name__ == '__main__':
    app.run(debug=True)
