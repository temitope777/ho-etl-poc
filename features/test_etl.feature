Feature: ETL Processing with Delta Lake
  As a data engineer
  I want to ensure that the ETL process reads, transforms, and writes data correctly
  So that the data is stored properly in Delta format

  Scenario: Read data from CSV and write to Delta Lake
    Given a CSV file with data
    When the ETL process is executed
    Then the output should be stored in Delta Lake format without errors
