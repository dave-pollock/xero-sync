Feature: Sync
  Scenario: Sync correctly syncs wix orders
    Given wix order with line items:
      | amount | discount_amount | quantity | sku   | product_name |
      | 10.99  | 1               | 3        | 00001 | product1     |
    When sync runs
    Then the wix orders should exist in xero