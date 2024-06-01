import pandas as pd
import requests as rq

# This address returns an excel file from Banco Central data
url = 'https://www.bch.hn/estadisticos/GIE/LIBTipo%20de%20cambio/Precio%20Promedio%20Diario%20del%20D%C3%B3lar.xlsx'

def download_bch(url=url, write_to=None):
    '''
    Downloads an excel file from `url` and optionally writes
    to write_to full path
    '''
    resp = rq.get(url, allow_redirects=True, verify=False)
    if not resp.ok:
        return None

    lemp_df = pd.read_excel(resp.content)

    # drop empty colums
    lemp_df = lemp_df.drop(columns=['Unnamed: 3', 'Unnamed: 4'])

    # rename columns
    lemp_df = lemp_df.rename(columns=
        {'Banco Central de Honduras': "Fecha",
        'Unnamed: 1': 'Compra',
        'Unnamed: 2': 'Venta'}
    )

    # remove non-date rows
    lemp_df['Fecha'] = pd.to_datetime(
            lemp_df.Fecha, errors='coerce')
    lemp_df = lemp_df.loc[lemp_df.Fecha.notnull()]
    print(lemp_df.tail(10))

    return lemp_df

if __name__=='__main__':
    download_bch()
