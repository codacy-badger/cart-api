from flask import Flask

app = Flask(__name__)
api = Api(app)

products = []

class ProductsList(Resource):
    def get(self):
        return {'products': products}


api.add_resource(ProductsList, '/products')


if __name__ == '__main__':
    app.run(debug=True)
