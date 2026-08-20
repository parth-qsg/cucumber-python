Feature: User Login and Client Selection

  Scenario: Login fails with invalid credentials
    Given the user is on the application login page
    When the user enters "invalidUser" as the username
    And the user enters "wrongPassword" as the password
    And the user clicks the Login button
    Then an error message is displayed indicating invalid credentials
    And the user remains on the login page
