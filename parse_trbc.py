import pandas as pd
from tika import parser
import sqlalchemy as db


def main():
    trbc_url = 'https://www.refinitiv.com/content/dam/marketing/en_us/documents/quick-reference-guides/trbc-business-classification-quick-guide.pdf'

    raw = parser.from_file(trbc_url)
    lines = raw['content'].split('\n\n')
    lines = list(filter(None, lines))

    new_rows = []
    for line in lines:
        name = ''
        type = ''
        perm_id = 0
        trbc = 0
        line = line.strip()
        line = line.replace('\n', '')
        line = line.split()
        for i in line:            
            if i.isnumeric():
                if perm_id == 0:
                    perm_id = i
                else:
                    trbc = i
                    if len(str(trbc)) == 2:
                        type = 'Economic Sector'
                        break
                    if len(str(trbc)) == 4:
                        type = 'Business Sector'
                        break
                    if len(str(trbc)) == 6:
                        type = 'Industry Group'
                        break
                    if len(str(trbc)) == 8:
                        type = 'Industry'
                        break
                    if len(str(trbc)) == 10:
                        type = 'Activity'
                        break
            else:
                if name == '':
                    name = i
                else:
                    name = name + ' ' + i
        new_rows.append([name, type, perm_id, trbc])
    trbc_df = pd.DataFrame(new_rows, columns=['name', 'type', 'perm_id', 'trbc'])
    trbc_df = trbc_df[trbc_df.trbc != 0]
    print(trbc_df)

    engine = db.create_engine('sqlite:///platform_economy.db')
    trbc_df.to_sql('trbc', con=engine, if_exists='replace', index=False)

if __name__ == '__main__':
    main()
