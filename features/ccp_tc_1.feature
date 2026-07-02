Feature: User Login on demo.qmagic.ai

  Scenario: Successful login with valid credentials
    Given the user navigates to the login page at demo.qmagic.ai
    And the user is not authenticated
    When the user enters a valid username
    And the user enters the correct password
    And the user clicks the Login button
    Then the user is redirected to the authenticated dashboard or home page
    And no error message is displayed
    And the user session is active
