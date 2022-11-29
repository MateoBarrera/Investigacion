import pandas as pd


def __open_csv(path, header="infer"):
  return pd.read_csv(path, header=header)


def __split_date(file):
  file['Fecha'] = pd.to_datetime(file['Fecha'])
  return file

def __filter_csv(file):
  return __split_date(file.filter(items=['CodigoEstacion', 'Municipio', 'IdParametro', 'Fecha', 'Valor', 'Frecuencia']))

def __filter_csv_pw_nasa(file, parameter=None):
  file = file.filter(items=['YEAR', 'MO', 'DY', 'ALLSKY_SFC_SW_DWN'])
  file = file.rename(
    columns={'YEAR': 'year', 'MO': 'month', 'DY': 'day', 'ALLSKY_SFC_SW_DWN': 'Valor'})
  file['Fecha'] = pd.to_datetime(file[['year', 'month', 'day']])
  file['Frecuencia'] = 'Diario'
  file.drop(['year', 'month', 'day'], axis=1)
  return __split_date(file)

def __get_stations(file):
  return file.drop_duplicates(subset=['CodigoEstacion'])['CodigoEstacion'].to_list()

def __extract_info(file):
  info = {}
  info['date_start'] = file['Fecha'].min()
  info['date_end'] = file['Fecha'].max()
  info['frequency'] = file['Frecuencia'][0]
  info['unit'] = 'm^3/s'
  return info

def __load_data(file, station):
  return file.loc[file['CodigoEstacion'] == station].filter(
    items=['Fecha', 'Valor'])  # .to_dict('records')

def __load_data_pw_nasa(file):
  return file.filter(items=['Fecha', 'Valor'])  # .to_dict('records')

def read_ideam_data(path, station):
  dictionary = {}
  file = __open_csv(path=path)
  file = __filter_csv(file)
  dictionary['data'] = __load_data(file, station)
  dictionary['info'] = __extract_info(file)
  return dictionary

def read_pw_nasa_data(path):
  dictionary = {}  
  file = __open_csv(path=path)
  file = __filter_csv_pw_nasa(file)
  dictionary['data'] = __load_data_pw_nasa(file)
  dictionary['info'] = __extract_info(file)
  return dictionary
