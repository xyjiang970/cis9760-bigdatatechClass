SELECT Company,
       High,
       Hour,
       Datetime
FROM (SELECT Table_1.Company,
             Table_2.high,
             Table_1.Datetime,
             Table_1.Hour
             FROM (SELECT name AS Company,
                          high AS High,
                          ts AS Datetime,
                          hour AS Hour
                          FROM "bigdata_prj3") Table_1
                              INNER JOIN (SELECT name AS Company,
                                                 hour AS Hour,
                                                 MAX(high) AS High
                                                 FROM "bigdata_prj3"
                                                 GROUP BY name, hour) Table_2 ON
                                                    Table_1.Company = Table_2.Company
                                                        AND Table_1.High = Table_2.High
                                                        AND Table_1.Hour = Table_2.Hour)
ORDER BY Company, Hour, Datetime
