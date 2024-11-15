Feature: The customer store service back-end
    As an Administrator
    I need a RESTful catalog service
    So that I can keep track of all my customers

Scenario: The server is running
    When I visit the "Home Page"
    Then I should see "Customer Demo RESTful Service" in the title
    And I should not see "404 Not Found"