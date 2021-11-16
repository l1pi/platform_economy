# platform_economy aims to measure and visualize platform economy

# Python files:
#     get_firms.py
#         Collect firms where business summary contains phrase "platform". Download basic financial data of the firms. Save all data to sqlite database.
#     
#     parse_trbc.py
#         Download and save TRBC data to sqlite database.
#     
#     data_visualizations.py
#         Visualize data.
#     
# Data sources:
#     Firms and financials:
#         Refinitiv Eikon
#         https://eikon.thomsonreuters.com/index.html
#     
#     Sector classification:
#         The Refinitiv Business Classifications (TRBC)
#         https://www.refinitiv.com/en/financial-data/indices/trbc-business-classification
#     
#     Country and Continent Codes List:
#        https://gist.github.com/stevewithington/20a69c0b6d2ff846ea5d35e5fc47f26c
#         Original Source: https://datahub.io/JohnSnowLabs/country-and-continent-codes-list
    