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
            continents = pd.read_excel('continent_country_codes.xlsx')
    except RuntimeError:
        print('No continent_country_codes excel file available')

    
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
    # yearly_sums.round(4)
    pd.set_option('display.float_format', lambda x: '%.0f' % x)
    print(yearly_sums)

    sns.set()

    yearly_sums_revenue = yearly_sums[['year', 'continent_name', 'revenue']]
    # yearly_sums_revenue['year'] = yearly_sums_revenue['year'].astype(str)
    # print(yearly_sums_revenue.dtypes)

    yearly_sums_revenue = yearly_sums_revenue.pivot(columns='continent_name',index='year').fillna(0)
    
    
    ax = yearly_sums_revenue.plot(kind='bar',stacked=True,legend=True)
    # x_labels = yearly_sums_revenue.index.astype(str)
    # ax.set_xticklabels(x_labels)
    ax.get_yaxis().set_major_formatter(matplotlib.ticker.FuncFormatter(lambda x, p: format(int(x), ',')))
    # ax.get_xaxis().set_major_formatter(matplotlib.ticker.FuncFormatter(lambda x, p: format(int(x), ',')))

    # yearly_sums_revenue.T.plot(kind='bar', stacked=True)

    print(yearly_sums_revenue)
    plt.show()



if __name__ == '__main__':
    main()