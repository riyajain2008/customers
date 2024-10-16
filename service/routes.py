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

from flask import jsonify, request, url_for, abort
from flask import current_app as app  # Import Flask application
from service.models import Customer
from service.common import status  # HTTP Status Codes


######################################################################
# GET INDEX
######################################################################
@app.route("/")
def index():
    """Root URL response"""
    return (
        "Reminder: return some useful information in json format about the service here",
        status.HTTP_200_OK,
    )


######################################################################
# LIST ALL customerS
######################################################################
@app.route("/customers", methods=["GET"])
def list_customers():
    """Returns all of the Customers"""
    app.logger.info("Request for customer list")

    customers = []

    # Parse any arguments from the query string
    # category = request.args.get("category")
    name = request.args.get("name")
    email = request.args.get("email")
    phone_number = request.args.get("phone_number")
    address = request.args.get("address")

    if name:
        app.logger.info("Find by name: %s", name)
        customers = Customer.find_by_name(name)
    elif email:
        app.logger.info("Find by email: %s", email)
        customers = Customer.find(email)
    elif phone_number:
        app.logger.info("Find by phone_number: %s", phone_number)
        # create enum from string
        customers = Customer.find(phone_number)
    elif address:
        app.logger.info("Find by address: %s", address)
        customers = Customer.find(address)
    else:
        app.logger.info("Find all")
        customers = Customer.all()

    results = [customer.serialize() for customer in customers]
    app.logger.info("Returning %d customers", len(results))
    return jsonify(results), status.HTTP_200_OK


@app.route("/customers/<int:customer_id>", methods=["GET"])
def get_customers(customer_id):
    """
    Retrieve a single Customer

    This endpoint will return a Customer based on it's id
    """
    app.logger.info("Request to Retrieve a customer with id [%s]", customer_id)

    # Attempt to find the Customer and abort if not found
    customer = Customer.find(customer_id)
    if not customer:
        abort(
            status.HTTP_404_NOT_FOUND,
            f"Customer with id '{customer_id}' was not found.",
        )

    app.logger.info("Returning customer: %s", customer.name)
    return jsonify(customer.serialize()), status.HTTP_200_OK


######################################################################
#  R E S T   A P I   E N D P O I N T S
######################################################################


@app.route("/customers", methods=["POST"])
def create_customers():
    """
    Create a Customer
    This endpoint will create a Customer based the data in the body that is posted
    """
    app.logger.info("Request to Create a Customer...")
    check_content_type("application/json")

    customer = Customer()
    # Get the data from the request and deserialize it
    data = request.get_json()
    app.logger.info("Processing: %s", data)
    customer.deserialize(data)

    # Save the new Customer to the database
    customer.create()
    app.logger.info("Customer with new id [%s] saved!", customer.id)

    # Return the location of the new Customer
    # TODO: uncomment this line after implementing get_customers
    location_url = url_for("get_customers", customer_id=customer.id, _external=True)
    # location_url = "url_for_get_customers"
    return (
        jsonify(customer.serialize()),
        status.HTTP_201_CREATED,
        {"Location": location_url},
    )


def check_content_type(content_type) -> None:
    """Checks that the media type is correct"""
    if "Content-Type" not in request.headers:
        app.logger.error("No Content-Type specified.")
        abort(
            status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            f"Content-Type must be {content_type}",
        )

    if request.headers["Content-Type"] == content_type:
        return

    app.logger.error("Invalid Content-Type: %s", request.headers["Content-Type"])
    abort(
        status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
        f"Content-Type must be {content_type}",
    )


######################################################################
# DELETE A CUSTOMER
######################################################################


@app.route("/customers/<int:customer_id>", methods=["DELETE"])
def delete_customer(customer_id):
    """
    Delete a customer

    This endpoint will delete a customer based the id specified in the path
    """
    app.logger.info("Request to Delete a customer with id [%s]", customer_id)

    # Delete the customer if it exists
    customer = Customer.find(customer_id)
    if customer:
        app.logger.info("Customer with ID: %d found.", customer.id)
        customer.delete()
        app.logger.info("Customer with ID: %d deleted.", customer.id)
        return {}, status.HTTP_204_NO_CONTENT
    else:
        app.logger.info("Customer with ID: %d not found.", customer_id)
        abort(
            status.HTTP_404_NOT_FOUND,
            f"Customer with id '{customer_id}' was not found.",
        )


# Todo: Uncomment this code when last_active has been updated in model in sprint2
# @app.route("/customers/inactive", methods=["DELETE"])
# def delete_inactive_customers():
#     """
#     Delete the customer with inactive_period more than 360 days
#     """
#     inactive_period = timedelta(days=360)
#     customers = Customer.find_inactive_customers(inactive_period)

#     if not customers:
#         abort(status.HTTP_404_NOT_FOUND, "No inactive customers found.")

#     for customer in customers:
#         customer.delete()
#         app.logger.info(f"Customer with ID {customer.id} deleted due to inactivity.")

#     return (
#         jsonify({"message": f"{len(customers)} customers deleted."}),
#         status.HTTP_200_OK,
#     )
