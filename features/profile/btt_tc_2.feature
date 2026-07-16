Feature: BTT Parking Section

  Scenario: BTT parking section displays correct content and layout
    Given the developer is logged into the application
    When the developer navigates to the BTT parking section
    Then the BTT parking section heading is displayed
    And the main content area of the BTT parking section is visible
    And any primary action buttons or controls within the section are rendered
