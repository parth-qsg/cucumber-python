Feature: User Login on demo.qmagic.ai

  Scenario: Login with empty credentials shows validation error
    Given the user navigates to the login page at demo.qmagic.ai
    And the user is not authenticated
    When the user leaves the username field empty
    And the user leaves the password field empty
    And the user clicks the Login button
    Then a validation error message is displayed
    And the user is not logged in
    And the user remains on the login page
