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
Test cases for Customer Model
"""

# pylint: disable=duplicate-code
import os
import logging
from unittest import TestCase
from wsgi import app
from service.models import Customer, DataValidationError, db
from .factories import CustomerFactory
from service.common import status

DATABASE_URI = os.getenv(
    "DATABASE_URI", "postgresql+psycopg://postgres:postgres@localhost:5432/testdb"
)


######################################################################
#  Customer   M O D E L   T E S T   C A S E S
######################################################################
# pylint: disable=too-many-public-methods
class TestCustomer(TestCase):
    """Test Cases for Customer Model"""

    @classmethod
    def setUpClass(cls):
        """This runs once before the entire test suite"""
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
        app.logger.setLevel(logging.CRITICAL)
        app.app_context().push()

    @classmethod
    def tearDownClass(cls):
        """This runs once after the entire test suite"""
        db.session.close()

    def setUp(self):
        """This runs before each test"""
        db.session.query(Customer).delete()  # clean up the last tests
        db.session.commit()

    def tearDown(self):
        """This runs after each test"""
        db.session.remove()

    ######################################################################
    #  T E S T   C A S E S
    ######################################################################


    def test_create_customer_model(self):
        """It should create a Customer"""
        resource = CustomerFactory()
        resource.create()
        self.assertIsNotNone(resource.id)
        found = Customer.all()
        self.assertEqual(len(found), 1)
        data = Customer.find(resource.id)
        self.assertEqual(data.name, resource.name)
        self.assertEqual(data.phone_number, resource.phone_number)
        self.assertEqual(data.email, resource.email)
        self.assertEqual(data.address, resource.address)

    def test_list_all_customers(self):
        """It should List all Customers in the database"""
        customers = Customer.all()
        self.assertEqual(customers, [])
        # Create 5 Customers
        for _ in range(5):
            customer = CustomerFactory()
            customer.create()
        # See if we get back 5 customers
        customers = Customer.all()
        self.assertEqual(len(customers), 5)

    def test_read_a_customer(self):
        """It should Read a Customer"""
        customer = CustomerFactory()
        logging.debug(customer)
        customer.id = None
        customer.create()
        self.assertIsNotNone(customer.id)
        # Fetch it back
        found_customer = Customer.find(customer.id)
        self.assertEqual(found_customer.id, customer.id)
        self.assertEqual(found_customer.name, customer.name)
        self.assertEqual(found_customer.email, customer.email)

    def test_update_customer(self):
        """It should Update a Customer"""
        customer = CustomerFactory()
        logging.debug(customer)
        customer.create()
        self.assertIsNotNone(customer.id)

        # Change it and save it
        customer.name = "Updated Name"
        customer.email = "updated_email@example.com"
        customer.phone_number = "123-456-7890"
        customer.address = "123 Updated Address"
        original_id = customer.id
        customer.update()
        self.assertEqual(customer.id, original_id)
        self.assertEqual(customer.name, "Updated Name")
        self.assertEqual(customer.email, "updated_email@example.com")
        self.assertEqual(customer.phone_number, "123-456-7890")
        self.assertEqual(customer.address, "123 Updated Address")

        customers = Customer.all()
        self.assertEqual(len(customers), 1)
        self.assertEqual(customers[0].id, original_id)
        self.assertEqual(customers[0].name, "Updated Name")
        self.assertEqual(customers[0].email, "updated_email@example.com")
        self.assertEqual(customers[0].phone_number, "123-456-7890")
        self.assertEqual(customers[0].address, "123 Updated Address")