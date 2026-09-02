Feature: User Authentication

  Scenario: Login form rejects submission when required fields are empty
    Given the user navigates to the login page at demo.qmagic.ai
    And no authenticated session is active
    When the user enters "" in the username field
    And the user enters "" in the password field
    And the user submits the login form
    Then the login attempt is rejected
    And a field validation error or warning is displayed
    And the user remains on the login page
    And no authenticated session is established
