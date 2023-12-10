# from flask_restx import Resource, fields
# from app.extensions import swagger_api


# # api = Api(app, version='1.0', title='Your API', description='API documentation using Swagger', doc='/swagger')

# # Namespace
# ns = swagger_api.namespace('example', description='Example API')

# # Model for request payload
# example_model = swagger_api.model('Example', {
#     'name': fields.String(required=True, description='Name of the example')
# })

# # Model for response payload
# example_response_model = swagger_api.model('ExampleResponse', {
#     'message': fields.String(description='Response message')
# })

# def init_swagger():
#     swagger_api.add_namespace(ns)
#     swagger_api.add_resource(ExampleResource, '/example')

# # Example route
# @ns.route('/example')
# class ExampleResource(Resource):
#     @ns.expect(example_model)
#     @ns.marshal_with(example_response_model)
#     def post(self):
#         """Create a new example"""
#         # Your implementation here


# if __name__ == '__main__':
#     app.run(debug=True)
