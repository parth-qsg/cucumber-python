Feature: User Login on demo.qmagic.ai

  Scenario Outline: Login fails with invalid credentials
    Given the user navigates to the login page at demo.qmagic.ai
    And the user is not authenticated
    When the user enters "<username>" as the username
    And the user enters "<password>" as the password
    And the user clicks the Login button
    Then the login attempt fails
    And an error message indicating invalid credentials is displayed
    And the user remains on the login page

    Examples:
      | username        | password        |
      | invaliduser     | validpassword   |
      | validuser       | wrongpassword   |
      | invaliduser     | wrongpassword   |
