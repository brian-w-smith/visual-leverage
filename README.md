# Margin Visualizer

This tool provides a visualization of the risk/reward potential of a leveraged portfolio, specifically a margin loan. 

While most bank websites provide an example scenario in text, this tool aims to help provide an intuitive understanding. 

In short, its a quick way to see how bad your returns can be before you receive a margin call. 

### Controls

- Starting Equity: The equity in your portfolio to use as collateral for the margin loan
- Margin Equity %: This slider represents the ratio of margin to your equity.  Most banks have a 1:1 purchase limit therefore this control is limited to 50% (displayed as .5) 
- Annualized Rate of Return:  Yearly total portfolio return
- Maintenance requirement: Check your bank website for the formula, but informally can be thought of as minimum ratio of the amount you borrowed vs your equity. As of 2024, most banks keep this around 30%.  
- Interest Rate: Check your bank website, it varies based on the amount you hold with them. 
- Total Months: How far into the future to look
- Pay Interest with Equity: Check this button if you prefer to make interest payments by converting portfolio equity to cash.
- Pay Interest with Outside Income (Wages): Check this button if you prefer to pay off interest payments from an external account. This reduces the risk of a margin call. 

### Tech Requirements

This was tested with python 3.12 

### Installation

To install, create a virtual environment, then run `pip install -r requirements.txt`

### Screenshots

Some lessons of the tool can be summarized quickly with screenshots, which are provided below: 

1.  With a 50% margin to equity ratio, the worst return you can get is -25% before a margin call happens in a year



2.  However, with a 25% Margin to Equity ratio you can hold on for 33 months with a -25% annual return