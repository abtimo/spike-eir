#  Mapping - *MarketingExpenses2ExpReport*

| Source:ExpReport                    | Source Type       | Target: MarketingExpenses          | Target Type | Transformation rule                                          | Field Description                   |
| ----------------------------------- | ----------------- | ---------------------------------- | ----------- | ------------------------------------------------------------ | ----------------------------------- |
| expense-report/Person               | xs:anyType        | marketing-expenses/Person          | xs:anyType  |                                                              | Person                              |
| expense-report/Person/First         | xs:string         | marketing-expenses/Person/FullName | xs:string   | concat (First, " ", Last)                                | FullName                            |
| expense-report/Person/Last          | xs:string         | marketing-expenses/Person/FullName | xs:string   | concat (First, " ", Last) | FullName                            |
| expense-report/Person/Title         | xs:string         | marketing-expenses/Person/Title | xs:string    |                                                              | Title      |
| expense-report/Person/Phone         | xs:string [0-9 \-]* | marketing-expenses/Person/Phone | xs:string [0-9 \-]* |                                                              | Phone          |
| expense-report/Person/Email         | emailType         | marketing-expenses/Person/Email | xs:string     |                                                              | Email                   |
| expense-report/expense-item         | xs:anyType [1..∞] | marketing-expenses/expense-item | xs:anyType [1..∞]   |                                                              | expense-item |
| expense-report/expense-item/@type   | xs:string         | marketing-expenses/expense-item/type | xs:string      |                                                              | type         |
| expense-report/expense-item/Date    | xs:date           | marketing-expenses/expense-item/Date | xs:date     |  | Date |
| expense-report/expense-item/expense | xs:decimal        | marketing-expenses/expense-item/expense | xs:decimal    |  | expense |
