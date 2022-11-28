import pandas as pd


def __open_csv(path):
  return pd.read_csv(path)


def __split_date(file):
  file['Fecha'] = pd.to_datetime(file['Fecha'])
  return file

def __filter_csv(file):
  return __split_date(file.filter(items=['CodigoEstacion', 'Municipio', 'IdParametro', 'Fecha', 'Valor', 'Frecuencia']))

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

def read_ideam_data(path, station):
  dictionary = {}
  file = __open_csv(path=path)
  file = __filter_csv(file)
  dictionary['data'] = __load_data(file, station)
  dictionary['info'] = __extract_info(file)
  return dictionary
