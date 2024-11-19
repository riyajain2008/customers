Feature: The customer store service back-end
    As an administrator of customer database
    I need a RESTful catalog service
    So that I can keep track of all my customers

Background:
    Given the following customers
        | name                  | email                                  | phone_number         | address                       | state   |
        | Sherlock Holmes       | sherlock.holmes@detectivemail.com      | 555-123-4567         | 221B Baker Street             | True    |
        | Homer Simpson         | homer.simpson@springfieldmail.com      | 555-765-4321         | 742 Evergreen Terrace         | False   |
        | Frodo Baggins         | frodo.baggins@middleearthmail.com      | 555-000-1111         | Bag End, Hobbiton             | True    |
        | Bruce Wayne           | bruce.wayne@gothammail.com             | 555-987-6543         | Wayne Manor, Gotham           | True    |
        | Harry Potter          | harry.potter@hogwartsmail.com          | 555-321-4321         | Griffindor Tower, Hogwarts    | False   |


Scenario: The server is running
    When I visit the "Home Page"
    Then I should see "Customer Demo RESTful Service" in the title
    And I should not see "404 Not Found"

# CREATE
Scenario: Create a Customer
    When I visit the "Home Page"
    And I set the "Name" to "Sirius Black"
    And I set the "Email" to "sirius.black@wizardmail.com"
    And I set the "Phone Number" to "555-112-3345"
    And I set the "Address" to "12 Grimmauld Place"
    And I select "True" in the "State" dropdown
    And I press the "Create" button
    Then I should see the message "Success"
    When I copy the "Id" field
    And I press the "Clear" button
    Then the "Id" field should be empty
    And the "Name" field should be empty
    And the "Email" field should be empty
    When I paste the "Id" field
    And I press the "Retrieve" button
    Then I should see the message "Success"
    And I should see "Sirius Black" in the "Name" field
    And I should see "sirius.black@wizardmail.com" in the "Email" field
    And I should see "555-112-3345" in the "Phone Number" field
    And I should see "12 Grimmauld Place" in the "Address" field
    And I should see "True" in the "State" dropdown

Scenario: List all customers
    When I visit the "Home Page"
    And I press the "Clear" button
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "Sherlock Holmes" in the results
    And I should see "Homer Simpson" in the results
    And I should see "Frodo Baggins" in the results
    And I should see "Bruce Wayne" in the results
    And I should see "Harry Potter" in the results

Scenario: Search by email
    When I visit the "Home Page"
    And I press the "Clear" button
    And I set the "Email" to "sherlock.holmes@detectivemail.com"
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "Sherlock Holmes" in the results
    And I should not see "Homer Simpson" in the results
    And I should not see "Harry Potter" in the results

Scenario: Search by phone number
    When I visit the "Home Page"
    And I press the "Clear" button
    And I set the "Phone Number" to "555-765-4321"
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "Homer Simpson" in the results
    And I should not see "Sherlock Holmes" in the results

Scenario: Search by address
    When I visit the "Home Page"
    And I press the "Clear" button
    And I set the "Address" to "Bag End, Hobbiton"
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "Frodo Baggins" in the results
    And I should not see "Homer Simpson" in the results

Scenario: Search by state
    When I visit the "Home Page"
    And I press the "Clear" button
    And I select "True" in the "State" dropdown
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "Sherlock Holmes" in the results
    And I should not see "Homer Simpson" in the results
    And I should see "Frodo Baggins" in the results
    And I should see "Bruce Wayne" in the results
    And I should not see "Harry Potter" in the results

# READ
Scenario: Read a Customer
    When I visit the "Home Page"
    And I set the "Name" to "Sherlock Holmes"
    And I press the "Search" button
    Then I should see the message "Success"
    When I copy the "Id" field
    And I press the "Clear" button
    And I paste the "Id" field
    And I press the "Retrieve" button
    Then I should see the message "Success"
    And I should see "Sherlock Holmes" in the "Name" field
    And I should see "sherlock.holmes@detectivemail.com" in the "Email" field
    And I should see "555-123-4567" in the "Phone Number" field
    And I should see "221B Baker Street" in the "Address" field
    And I should see "True" in the "State" dropdown

# UPDATE
Scenario: Update a Customer
    When I visit the "Home Page"
    And I set the "Name" to "Sherlock Holmes"
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "sherlock.holmes@detectivemail.com" in the "Email" field
    And I should see "555-123-4567" in the "Phone Number" field
    And I should see "221B Baker Street" in the "Address" field
    When I change "Name" to "Loki"
    And I press the "Update" button
    Then I should see the message "Success"
    When I copy the "Id" field
    And I press the "Clear" button
    And I paste the "Id" field
    And I press the "Retrieve" button
    Then I should see the message "Success"
    And I should see "Loki" in the "Name" field
    When I press the "Clear" button
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "Loki" in the results
    And I should not see "Sherlock Holmes" in the results

# DELETE
Scenario: Delete a Customer
    When I visit the "Home Page"
    And I set the "Name" to "Sherlock Holmes"
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "sherlock.holmes@detectivemail.com" in the "Email" field
    And I should see "555-123-4567" in the "Phone Number" field
    And I should see "221B Baker Street" in the "Address" field
    When I copy the "Id" field
    And I press the "Clear" button
    And I paste the "Id" field
    And I press the "DELETE" button
    Then I should see the message "Customer has been Deleted!"
    When I press the "Clear" button
    And I paste the "Id" field
    And I press the "Retrieve" button
    Then I should see the message "404 Not Found"