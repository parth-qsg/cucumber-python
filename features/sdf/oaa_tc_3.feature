Feature: User Login and Client Selection

  Scenario: User logs out successfully and session is terminated
    Given the user is authenticated and on the main website
    When the user clicks the Logout button or option
    Then the user is redirected to the login page
    And the user session is terminated
    When the user attempts to navigate directly to the main website URL
    Then the user is redirected to the login page again
