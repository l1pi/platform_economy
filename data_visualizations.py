import sqlalchemy as db
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns


def main():
    try:
        engine = db.create_engine('sqlite:///platform_economy.db')
        connection = engine.connect()
    except RuntimeError:
            print('No database available')
    
    try:
        firms = pd.read_sql_table('firms', connection)
    except RuntimeError:
        print('No firms table available')
    
    try:
        financials = pd.read_sql_table('financials', connection)
    except RuntimeError:
        print('No financials table available')
    
    try:
        trbcs = pd.read_sql_table('trbc', connection)
    except RuntimeError:
        print('No trbc table available')

    try:
            continents = pd.read_excel('continent_country_codes.xlsx')
    except RuntimeError:
        print('No continent_country_codes excel file available')

    pd.set_option('display.float_format', lambda x: '%.0f' % x)
    firms_countries = firms[['id', 'country']]
    firms_countries.rename(columns={'id': 'firm_id'}, inplace=True)

    countries_continents = continents[['continent_name', 'two_letter_country_code']]
    countries_continents.rename(columns={'two_letter_country_code': 'country'}, inplace=True)

    financials['year'] = pd.DatetimeIndex(financials['period_end_date']).year
    financials = financials.merge(firms_countries, on='firm_id', how='left')
    financials = financials.merge(countries_continents, on='country', how='left')

    yearly_sums = financials.groupby(['year', 'continent_name']).sum().reset_index()
    yearly_sums = yearly_sums[['year', 'continent_name', 'revenue', 'net_income_after_taxes', 'total_assets_reported', 'employees']]
    yearly_sums = yearly_sums[(yearly_sums['year'] >= 2010) & (yearly_sums['year'] < 2021)].fillna(0)
    yearly_sums['year'] = yearly_sums['year'].astype(int)

    sns.set()
    
    # Stacked bar chart of revenue
    yearly_sums_revenue = yearly_sums[['year', 'continent_name', 'revenue']].copy()
    yearly_sums_revenue['revenue'] = yearly_sums_revenue['revenue'] / 1000000
    yearly_sums_revenue = yearly_sums_revenue.pivot(columns='continent_name',index='year').fillna(0)    
    ax1 = yearly_sums_revenue.plot(kind='bar',stacked=True,legend=True)
    ax1.get_yaxis().set_major_formatter(matplotlib.ticker.FuncFormatter(lambda x, p: format(int(x), ',')))
    ax1.set_ylabel('Revenue in USD millions')
    ax1.set_xlabel('Year')
    ax1.legend(title='Revenues per continent')

    # Stacked bar chart of net income
    yearly_sums_net_income = yearly_sums[['year', 'continent_name', 'net_income_after_taxes']].copy()
    yearly_sums_net_income['net_income_after_taxes'] = yearly_sums_net_income['net_income_after_taxes'] / 1000000
    yearly_sums_net_income = yearly_sums_net_income.pivot(columns='continent_name',index='year').fillna(0)    
    ax2 = yearly_sums_net_income.plot(kind='bar',stacked=True,legend=True)
    ax2.get_yaxis().set_major_formatter(matplotlib.ticker.FuncFormatter(lambda x, p: format(int(x), ',')))
    ax2.set_ylabel('Net income in USD millions')
    ax2.set_xlabel('Year')
    ax2.legend(title='Net income per continent')

    # Stacked bar chart of total assets
    yearly_sums_total_assets = yearly_sums[['year', 'continent_name', 'total_assets_reported']].copy()
    yearly_sums_total_assets['total_assets_reported'] = yearly_sums_total_assets['total_assets_reported'] / 1000000
    yearly_sums_total_assets = yearly_sums_total_assets.pivot(columns='continent_name',index='year').fillna(0)    
    ax3 = yearly_sums_total_assets.plot(kind='bar',stacked=True,legend=True)
    ax3.get_yaxis().set_major_formatter(matplotlib.ticker.FuncFormatter(lambda x, p: format(int(x), ',')))
    ax3.set_ylabel('Total assets in USD millions')
    ax3.set_xlabel('Year')
    ax3.legend(title='Total assets per continent')

    # # Stacked bar chart of employees
    # yearly_sums_employees = yearly_sums[['year', 'continent_name', 'employees']]
    # yearly_sums_employees = yearly_sums_employees.pivot(columns='continent_name',index='year').fillna(0)    
    # ax4 = yearly_sums_employees.plot(kind='bar',stacked=True,legend=True)
    # ax4.get_yaxis().set_major_formatter(matplotlib.ticker.FuncFormatter(lambda x, p: format(int(x), ',')))

    # Bar chart of market cap
    # market_caps = firms[['country', 'market_cap']]
    # market_caps = market_caps.merge(countries_continents, on='country', how='left')
    # market_caps = market_caps[['continent_name', 'market_cap']]
    # market_caps = market_caps.groupby(['continent_name']).sum().reset_index()
    # ax5 = market_caps.plot(kind='bar',stacked=False,legend=False)
    # ax5.get_yaxis().set_major_formatter(matplotlib.ticker.FuncFormatter(lambda x, p: format(int(x), ',')))

    # Finnish firms
    finnish_firms = firms[firms['country'].str.match('FI')].copy()
    finnish_firms = finnish_firms[['id', 'name']]
    finnish_firms.rename(columns={'id': 'firm_id'}, inplace=True)
    finnish_financials = financials[financials['country'].str.match('FI')]
    finnish_financials = finnish_financials.merge(finnish_firms, on='firm_id', how='left')

    finnish_yearly_sums = finnish_financials.groupby(['year', 'name']).sum().reset_index()
    finnish_yearly_sums = finnish_yearly_sums[['year', 'name', 'revenue', 'net_income_after_taxes', 'total_assets_reported', 'employees']]
    finnish_yearly_sums = finnish_yearly_sums[(finnish_yearly_sums['year'] >= 2010) & (finnish_yearly_sums['year'] < 2021)].fillna(0)
    finnish_yearly_sums['year'] = finnish_yearly_sums['year'].astype(int)

    f_revenue = finnish_yearly_sums[['year', 'name', 'revenue']].copy()
    f_revenue['revenue'] = f_revenue['revenue'] / 1000000
    f_revenue = f_revenue.pivot(columns='name',index='year').fillna(0)     
    ax6 = f_revenue.plot(kind='bar',stacked=True, legend=True, title='Revenue sum of Finnish "platform" firms')
    ax6.get_yaxis().set_major_formatter(matplotlib.ticker.FuncFormatter(lambda x, p: format(int(x), ',')))
    ax6.set_ylabel('Revenue in USD millions')
    ax6.set_xlabel('Year')

    f_net_income = finnish_yearly_sums[['year', 'name', 'net_income_after_taxes']].copy()
    f_net_income['net_income_after_taxes'] = f_net_income['net_income_after_taxes'] / 1000000
    f_net_income = f_net_income.pivot(columns='name',index='year').fillna(0) 
    ax7 = f_net_income.plot(kind='bar', stacked=True, legend=True, title='Net income sum of Finnish "platform" firms')
    ax7.get_yaxis().set_major_formatter(matplotlib.ticker.FuncFormatter(lambda x, p: format(int(x), ',')))
    ax7.set_ylabel('Net income in USD millions')
    ax7.set_xlabel('Year')

    f_net_assets = finnish_yearly_sums[['year', 'name', 'total_assets_reported']].copy()
    f_net_assets['total_assets_reported'] = f_net_assets['total_assets_reported'] / 1000000
    f_net_assets = f_net_assets.pivot(columns='name',index='year').fillna(0)
    ax8 = f_net_assets.plot(kind='bar', stacked=True, legend=True, title='Total assets sum of Finnish "platform" firms')
    ax8.get_yaxis().set_major_formatter(matplotlib.ticker.FuncFormatter(lambda x, p: format(int(x), ',')))
    ax8.set_ylabel('Total assets in USD millions')
    ax8.set_xlabel('Year')

    # Stacked bar charts of different industries
    firms_industries = firms[['id', 'trbc']].copy()
    firms_industries['trbc'] = firms_industries['trbc'].astype(str)
    firms_industries['trbc'] = firms_industries['trbc'].str[:2]
    trbc_names = trbcs[['name', 'trbc']]
    firms_industries = firms_industries.merge(trbc_names, on='trbc', how='left')
    firms_industries = firms_industries[['id', 'name']]

    firms_industries.rename(columns={'id': 'firm_id', 'name': 'trbc'}, inplace=True)
    financials_industries = financials.merge(firms_industries, on='firm_id', how='left')

    industry_yearly_sums = financials_industries.groupby(['year', 'trbc']).sum().reset_index()
    industry_yearly_sums = industry_yearly_sums[['year', 'trbc', 'revenue', 'net_income_after_taxes', 'total_assets_reported', 'employees']]
    industry_yearly_sums = industry_yearly_sums[(industry_yearly_sums['year'] >= 2010) & (industry_yearly_sums['year'] < 2021)].fillna(0)
    industry_yearly_sums['year'] = industry_yearly_sums['year'].astype(int)

    industry_yearly_sums_revenue = industry_yearly_sums[['year', 'trbc', 'revenue']].copy()
    industry_yearly_sums_revenue['revenue'] = industry_yearly_sums_revenue['revenue'] / 1000000
    industry_yearly_sums_revenue = industry_yearly_sums_revenue.pivot(columns='trbc',index='year').fillna(0)    
    ax9 = industry_yearly_sums_revenue.plot(kind='bar',stacked=True,legend=True)
    ax9.get_yaxis().set_major_formatter(matplotlib.ticker.FuncFormatter(lambda x, p: format(int(x), ',')))
    ax9.set_ylabel('Revenue in USD millions')
    ax9.set_xlabel('Year')
    ax9.legend(title='Revenues per industry classification')    

    plt.show()


if __name__ == '__main__':
    main()
