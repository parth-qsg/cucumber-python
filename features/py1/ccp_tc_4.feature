Feature: User Login on demo.qmagic.ai

  Scenario: Unauthenticated access to protected page redirects to login
    Given the user has no active session on demo.qmagic.ai
    When the user attempts to navigate directly to a protected page URL
    Then the user is redirected to the login page
    And the protected page content is not displayed
