Feature: Yandex Market user Journey
  Test that imitate user's search activity
  Open/Close browser implement in fixture


#  @search
  Scenario: Check ware's rating but ya market sucks
        # яндекс маркет иногда не грузит фильтры, этот сценарий их не использует

    Given Open market.yandex.ru
    And in the "Catalog → Electronics" section, select "Smartphones"
    And go to "All Filters"
    Then click button "Show"
    Then count smartphone on first page and remember last one from the list
    Then change sort type on sort by 'по цене'
    Then find and click on remembered object
    And display the rating of the selected product

  @search
  Scenario: Check ware's rating

    Given Open market.yandex.ru
    And in the "Catalog → Electronics" section, select "Smartphones"
    And go to "All Filters"
    Then set the search parameter to 20000 rubles
    And the diagonal of the screen from 3 inches
    And at least 5 of any manufacturers
    Then click button "Show"
    Then count smartphone on first page and remember last one from the list
    Then change sort type on sort by 'по цене'
    Then find and click on remembered object
    And display the rating of the selected product



