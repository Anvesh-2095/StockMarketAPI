## Proposed Routes
1. get stock info
   - Input: stock name or short code
   - Output: stock details including all the above features
2. filter stocks
   - Input: filter criteria based on the above features
   - Output: list of stocks that match the filter criteria
3. draw graph
   - Input: stock name or short code and start and end date
   - Output: graph of stock price over the specified period
   - will set up a minimum window of a week's data for the graph

### Features of stocks available for filtering:
1. Name
2. Short code
3. Market Cap : stockDetailsReusableData : marketCap
4. P/E Ratio : stockDetailsReusableData : peerCompanyList: priceToEarningsValueRatio in one with same company name without Ltd.
5. P/B Ratio : stockDetailsReusableData : peerCompanyList: priceToBookValueRatio in one with same company name without Ltd.
6. Debt to Equity : stockDetailsReusableData : peerCompanyList: ltDebtPerEquityMostRecentFiscalYear in one with same company name without Ltd.
7. % ROCE : view raw plan.txt : mostRecentFiscalYear, 5years, trailing twelve months
8. % ROE : keyMetrics : mgmtEffectiveness : returnOnAverageEquityMostRecentFiscalYear , 5years, trailing twelve months
9. % ROI: keyMetrics : mgmtEffectiveness : returnOnInvestmentMostRecentFiscalYear, 5years, trailing twelve months
10. 52-week high : keyMetrics : priceandVolume : 52WeekHigh , 52WeekHighDate
11. 52-week low : keyMetrics : priceandVolume : 52WeekLow , 52WeekLowDate
12. % Compounded Sales Growth : see raw plan.txt
13. % Compounded Profit Growth : see raw plan.txt
14. Share Holding Pattern: Promoter : shareholding : promoter : there are 4 values for previous 4 quarters
15. Share Holding Pattern: FII : shareholding : FII : there are 4 values for previous 4 quarters
16. Share Holding Pattern: Mutual Funds / DII : shareholding : MF : there are 4 values for previous 4 quarters
17. Share Holding Pattern: Public : shareholding : others : there are 4 values for previous 4 quarters
18. Revenue Growth : see raw plan.txt -- 5 years
19. Borrow : stockFinancialData : stockFinancialMap : BAL : totalDebt
20. EPS Growth : keyMetrics : growth : earningsPerShareGrowthMostRecentFiscalYear, 5years, trailing twelve months, 3 yr
21. industry : industry
22. nse and bse price: currentPrice : nse // companyProfile : peerCompanyList : price in one with same company name without Ltd.
23. Net Profit: financials : stockFinancialMap : INC : Net Income
24. Revenue: financials : stockFinancialMap : INC : Revenue
25. EPS: financials : stockFinancialMap : INC : DilutedEPSExcludingExtraOrdItems