Feature: BTT Parking Section

  Scenario: BTT parking section is not accessible to unauthenticated users
    Given the user is not logged into the application
    When the user attempts to navigate directly to the BTT parking section URL
    Then the user is redirected to the login page
    And the BTT parking section content is not displayed
