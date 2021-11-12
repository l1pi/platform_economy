import eikon as ek    
import sqlalchemy as db
import datetime
import pandas as pd
import os
import time
from dotenv import load_dotenv
load_dotenv()


def get_env_variable(name):
    try:
        return os.getenv(name)
    except KeyError:
        message = "Expected environment variable '{}' not set.".format(name)
        raise Exception(message)


def main():
    # Remove old database
    try:
        os.remove('platform_economy.db')
        print('Old file removed')
    except OSError as e:
        print(str(e))
        pass

    engine = db.create_engine('sqlite:///platform_economy.db')
    connection = engine.connect()

    ek.set_app_key(get_env_variable("EIKON_APP_KEY"))


    # Add platform firms
    try:        
        screener_exp = 'SCREEN(U(IN(Equity(active,public,primary))), Contains(TR.BusinessSummary,"platform"), CURN=USD)'
        fields = ['TR.CommonName', 'TR.TRBCActivityCode', 'TR.HQCountryCode', 'TR.ISIN', 'TR.CUSIP', 'TR.BusinessSummary', 'TR.CompanyMarketCap']
        firms, e = ek.get_data(screener_exp, fields)
        firms.rename(columns={'Instrument': 'symbol', 
            'Company Common Name': 'name', 
            'TRBC Activity Code': 'trbc',
            'Country ISO Code of Headquarters': 'country',
            'ISIN': 'isin', 
            'CUSIP': 'cusip',
            'Business Description': 'description', 
            'Company Market Cap': 'market_cap'}, inplace=True)
        firms['id'] = firms.index
        firms['created_date'] = datetime.datetime.utcnow()
        firms['last_updated_date'] = datetime.datetime.utcnow()
        firms = firms[['id','symbol', 'name', 'trbc', 'country', 'isin', 'cusip', 'description', 'market_cap', 'created_date', 'last_updated_date']]        
        firms.to_sql('firms', con=engine, if_exists='append', index=False)
        print('Firms done')
    except Warning:
        print('Error in firms')


    # Add financials
    try:
        try:
            firms = pd.read_sql_table('firms', connection)
        except RuntimeError:
            print('No firms table available')
        fields = ['TR.ISPeriodEndDate', 'TR.Revenue', 'TR.NetIncomeAfterTaxes', 'TR.TotalAssetsReported', 'TR.CompanyNumEmploy']
        for symbol in firms['symbol']:
            counter = 1
            while True:
                try:
                    financials, e = ek.get_data(symbol, fields, {'SDate': 0, 'EDate': -10, 'Curn': 'USD', 'CH': 'Fd'})
                    break
                except ek.eikonError.EikonError:
                    print('Error in Eikon API with symbol: '+symbol)
                    print(e)
                    counter = counter + 1 
                    if counter >= 5:
                        break
                    else:
                        time.sleep(1)
                        continue
            firm_id = firms[firms['symbol'] == symbol].iloc[0, 0]
            financials['firm_id'] = firm_id
            financials['created_date'] = datetime.datetime.utcnow()
            financials['last_updated_date'] = datetime.datetime.utcnow()
            financials.rename(columns={
                'Income Statement Period End Date': 'period_end_date',
                'Revenue': 'revenue',
                'Net Income After Taxes': 'net_income_after_taxes', 
                'Total Assets, Reported': 'total_assets_reported',
                'Number of Employees': 'employees'}, inplace=True)
            financials = financials[['firm_id', 'period_end_date', 'revenue', 'net_income_after_taxes', 'total_assets_reported', 'employees', 'created_date', 'last_updated_date']]
            financials.to_sql('financials', connection, if_exists='append', index=False)
            print('Firm financials added: '+symbol)
        print('Financials done')
    except Warning:
        print('Error in financials')


if __name__ == '__main__':
    main()
