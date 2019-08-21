# finance-portfolio-selection
Created by Noah Baculi and inspired by Yahoo Finance's stock screener.

May 2019

Evaluate different financial securities using custom parameters to aid portfolio composition.
This tool is purely informational/educational and not endorsed by any finance professional.

## How to run (online *BETA*):
1. Navigate to https://nbfinanceselection.pythonanywhere.com/finance/
2. Input the desired security symbols for comparison.
3. Input the desired comparison parameters.
4. Click 'Calculate' to generate the comparison table.

## How to run (local):
1. Download or clone the project files to a desired directory.
2. Install the necessary dependecies and libraries in an virtualenv.
  - 'requests'
  - 'requests-html'
  - 'yahoo_fin'
  - 'bs4'
3. Open 'portfolio_selection.py' in a text editor or IDE and change the 'symbols_list' and 'parameters' variables to equal the a list of strings of desired symbols and parameters.
4. Run 'portfolio_selection.py' to generate the comparison table.
