######################################################################
# Copyright 2016, 2024 John J. Rofrano. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
######################################################################

"""
Customer Service

This service implements a REST API that allows you to Create, Read, Update
and Delete Customer
"""

from flask import current_app as app  # Import Flask application
from flask import jsonify
from flask_restx import Api, Resource, fields, reqparse, inputs
from service.models import Customer
from service.common import status  # HTTP Status Codes

######################################################################
# Configure Swagger before initializing it
######################################################################
api = Api(
    app,
    version="1.0.0",
    title="Customer Demo REST API Service",
    description="This is a sample server for Customer.",
    default="customers",
    default_label="customers operations",
    doc="/apidocs",  # default also could use doc='/apidocs/'
    prefix="/api",
)


######################################################################
# Configure the Root route before OpenAPI
######################################################################
@app.route("/")
def index():
    """Base URL for our service"""
    return app.send_static_file("index.html")


# Define the model so that the docs reflect what can be sent
create_model = api.model(
    "Customer",
    {
        "name": fields.String(required=True, description="The name of the Customer"),
        "email": fields.String(
            required=True,
            description="The email of Customer",
        ),
        "phone_number": fields.String(
            required=True, description="The phone number of Customer"
        ),
        "address": fields.String(required=True, description="The address of Customer"),
        "state": fields.Boolean(
            required=True, description="The state of Customer, false when suspended"
        ),
    },
)

customer_model = api.inherit(
    "CustomerModel",
    create_model,
    {
        "id": fields.Integer(
            readOnly=True, description="The unique id assigned internally by service"
        ),
    },
)

# query string arguments
customer_args = reqparse.RequestParser()
customer_args.add_argument(
    "name", type=str, location="args", required=False, help="List Customers by name"
)
customer_args.add_argument(
    "email", type=str, location="args", required=False, help="List Customers by email"
)
customer_args.add_argument(
    "phone_number",
    type=str,
    location="args",
    required=False,
    help="List Customers by phone_number",
)
customer_args.add_argument(
    "address",
    type=str,
    location="args",
    required=False,
    help="List Customers by address",
)
customer_args.add_argument(
    "state",
    type=inputs.boolean,
    location="args",
    required=False,
    help="List Customer by state",
)


######################################################################
#  R E S T   A P I   E N D P O I N T S
######################################################################


######################################################################
#  PATH: /customers/{id}
######################################################################
@api.route("/customers/<customer_id>")
@api.param("customer_id", "The Customer identifier")
class CustomerResource(Resource):
    """
    CustomerResource class

    Allows the manipulation of a single Customer
    GET /customer{id} - Returns a Customer with the id
    PUT /customer{id} - Update a Customer with the id
    DELETE /customer{id} -  Deletes a Customer with the id
    """

    # ------------------------------------------------------------------
    # RETRIEVE A CUSTOMER
    # ------------------------------------------------------------------
    @api.doc("get_customers")
    @api.response(404, "Customer not found")
    @api.marshal_with(customer_model)
    def get(self, customer_id):
        """
        Retrieve a single Customer

        This endpoint will return a Customer based on it's id
        """
        app.logger.info("Request to Retrieve a customer with id [%s]", customer_id)
        customer = Customer.find(customer_id)
        if not customer:
            abort(
                status.HTTP_404_NOT_FOUND,
                f"Customer with id '{customer_id}' was not found.",
            )
        return customer.serialize(), status.HTTP_200_OK

    # ------------------------------------------------------------------
    # UPDATE AN EXISTING CUSTOMER
    # ------------------------------------------------------------------
    @api.doc("update_customers")
    @api.response(404, "Customer not found")
    @api.response(400, "The posted Customer data was not valid")
    @api.expect(customer_model)
    @api.marshal_with(customer_model)
    def put(self, customer_id):
        """
        Update a Customer

        This endpoint will update a Customer based the body that is posted
        """
        app.logger.info("Request to Update a customer with id [%s]", customer_id)
        customer = Customer.find(customer_id)
        if not customer:
            abort(
                status.HTTP_404_NOT_FOUND,
                f"Customer with id '{customer_id}' was not found.",
            )
        app.logger.debug("Payload = %s", api.payload)
        data = api.payload
        customer.deserialize(data)
        customer.id = customer_id
        customer.update()
        return customer.serialize(), status.HTTP_200_OK

    # ------------------------------------------------------------------
    # DELETE A CUSTOMER
    # ------------------------------------------------------------------
    @api.doc("delete_customers")
    @api.response(204, "Customer deleted")
    def delete(self, customer_id):
        """
        Delete a Customer

        This endpoint will delete a Customer based the id specified in the path
        """
        app.logger.info("Request to Delete a customer with id [%s]", customer_id)
        customer = Customer.find(customer_id)
        if customer:
            customer.delete()
            app.logger.info("Customer with id [%s] was deleted", customer_id)

        return "", status.HTTP_204_NO_CONTENT


######################################################################
#  PATH: /customers
######################################################################
@api.route("/customers", strict_slashes=False)
class CustomerCollection(Resource):
    """Handles all interactions with collections of Customers"""

    # ------------------------------------------------------------------
    # LIST ALL CUSTOMERS
    # ------------------------------------------------------------------
    @api.doc("list_customers")
    @api.expect(customer_args, validate=True)
    @api.marshal_list_with(customer_model)
    def get(self):
        """Returns all of the Customers"""
        app.logger.info("Request to list Customers...")
        customers = []
        args = customer_args.parse_args()
        if args["name"]:
            app.logger.info("Filtering by name: %s", args["name"])
            customers = Customer.find_by_name(args["name"])
        elif args["email"]:
            app.logger.info("Filtering by email: %s", args["email"])
            customers = Customer.find_by_email(args["email"])
        elif args["phone_number"]:
            app.logger.info("Filtering by phone_number: %s", args["phone_number"])
            customers = Customer.find_by_phone_number(args["phone_number"])
        elif args["address"]:
            app.logger.info("Filtering by address: %s", args["address"])
            customers = Customer.find_by_address(args["address"])
        elif args["state"] is not None:
            app.logger.info("Filtering by state: %s", args["state"])
            customers = Customer.find_by_state(args["state"])
        else:
            app.logger.info("Returning unfiltered list.")
            customers = Customer.all()

        app.logger.info("[%s] Customers returned", len(customers))
        results = [customer.serialize() for customer in customers]
        return results, status.HTTP_200_OK

    # ------------------------------------------------------------------
    # ADD A NEW CUSTOMER
    # ------------------------------------------------------------------
    @api.doc("create_customers")
    @api.response(400, "The posted data was not valid")
    @api.expect(create_model)
    @api.marshal_with(customer_model, code=201)
    def post(self):
        """
        Creates a Customer
        This endpoint will create a Customer based the data in the body that is posted
        """
        app.logger.info("Request to Create a Customer")
        customer = Customer()
        app.logger.debug("Payload = %s", api.payload)
        customer.deserialize(api.payload)
        customer.create()
        app.logger.info("Customer with new id [%s] created!", customer.id)
        location_url = api.url_for(
            CustomerResource, customer_id=customer.id, _external=True
        )
        return customer.serialize(), status.HTTP_201_CREATED, {"Location": location_url}


######################################################################
#  PATH: /customers/{id}/suspend
######################################################################
@api.route("/customers/<customer_id>/suspend")
@api.param("customer_id", "The Customer identifier")
class SuspendResource(Resource):
    """Suspend actions on a Customer"""

    @api.doc("suspend_customers")
    @api.response(404, "Customer not found")
    @api.response(409, "The state of Customer is already invalid")
    def put(self, customer_id):
        """
        Suspend a Customer

        This endpoint will suspend a Customer and make it invalid
        """
        app.logger.info("Request to Suspend a Customer")
        customer = Customer.find(customer_id)
        if not customer:
            abort(
                status.HTTP_404_NOT_FOUND,
                f"Customer with id [{customer_id}] was not found.",
            )
        if not customer.state:
            abort(
                status.HTTP_409_CONFLICT,
                f"Customer with id [{customer_id}] is invalid.",
            )
        customer.state = False
        customer.update()
        app.logger.info("Customer with id [%s] has been suspended!", customer.id)
        return customer.serialize(), status.HTTP_200_OK


######################################################################
#  U T I L I T Y   F U N C T I O N S
######################################################################

def abort(error_code: int, message: str):
    """Logs errors before aborting"""
    app.logger.error(message)
    api.abort(error_code, message)

<<<<<<< HEAD

=======
>>>>>>> 2d3299e591d2e74f68665eca283d297414ece198
######################################################################
# HEALTH CHECK
######################################################################
@app.route("/health")
def health_check():
    """Let them know our heart is still beating"""
    return jsonify(status=200, message="Healthy"), status.HTTP_200_OK
