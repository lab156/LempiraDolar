import pandas as pd
import requests as rq
import pylightxl as xl

# This address returns an excel file from Banco Central data
url = 'https://www.bch.hn/estadisticos/GIE/LIBTipo%20de%20cambio/Precio%20Promedio%20Diario%20del%20D%C3%B3lar.xlsx'

wrt = '/tmp/lps_dolar'

def open_w_pylightxl(xlsx_path=wrt+'.xlsx', write_to=wrt):
    '''
    opens file wrt.xlxs and saves is to .csv format
    returns the name of the csv file
    '''
    db = xl.readxl(fn=xlsx_path)
    xl.writecsv(db=db, fn=write_to, delimiter='\t')
    suffix = db.ws_names[0]
    return write_to + '_' + suffix
     



def download_bch(url=url, write_to=wrt):
    '''
    Downloads an excel file from `url` and optionally writes
    to write_to full path
    '''
    resp = rq.get(url, allow_redirects=True)
    if resp.ok:
        with open(write_to+'.xlsx', 'wb') as fobj:
            fobj.write(resp.content)
    else:
        print('Respuesta de la pagina es not "ok"')
        return None

    csv_filename = open_w_pylightxl()
    lemp_df = pd.read_csv(csv_filename+'.csv', sep='\t')
    #lemp_df = pd.read_excel(resp.content, engine='pylightxl')
    #sheet = xlrd.open_workbook(resp.content).sheet_by_index(0)
    
    # drop empty colums
    lemp_df = lemp_df.drop(['Unnamed: 3', 'Unnamed: 4'], axis=1)

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
