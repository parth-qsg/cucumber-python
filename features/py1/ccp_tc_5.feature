Feature: Access Control and Route Protection

  Scenario: Unauthenticated user is redirected when accessing a protected page
    Given no authenticated session exists in the browser
    When the user attempts to navigate directly to a protected page URL on demo.qmagic.ai
    Then the application denies access to the protected content
    And the user is redirected to the login page
    And no protected page content is rendered or exposed
