import pandas as pd
import matplotlib.pyplot as plt
from .viability import Hydro, Pv, Wind, get_data_month
from .extract.load import read_ideam_data, read_pw_nasa_data

import seaborn as sns

font = {'family': 'serif',
        'color':  'black',
        'weight': 'bold',
        'size': 10,
        }

class PrimaryResource:
    """Definition for primary resource class
    Include info description and historical data.
    """
    name: str = None
    station: str = None
    source: str = None
    __stations: list = ()
    __type_resource: str = None
    __date_start: str = None
    __date_end: str = None
    __frequency: str = None
    __unit: str = None
    __data_df: pd.DataFrame = None

    def __init__(self, name=None, type_resource=None, source=None, station=None) -> None:
        """Constructor for PrimaryResource
        Args:
            name (str, optional): Name resource. Defaults to None.
            type_resource (str, optional): Type of resource (pv, hydro, wind, biomass, etc). Defaults to None.
            source (str, optional): Information source. Defaults to None.
        """
        self.name = name
        self.__type_resource = type_resource.lower()
        self.source = source.lower()
        self.station = station

    def __str__(self) -> str:
        """Return description info for primary resource.
        Returns:
            str: Info object primary resource.
        """
        return "Name: {}, Type: {}, Source: {} ".format(self.name, self.__type_resource, self.source)

    @property
    def data(self):
        return self.__data_df

    @property
    def type_resource(self):
        return self.__type_resource

    @property
    def date_start(self):
        return self.__date_start

    @property
    def date_end(self):
        return self.__date_end

    @property
    def data_info(self) -> str:
        return "Name: {}, time start: {}, time end: {}, frequency: {}, unit: {}".format(self.name, self.__date_start, self.__date_end, self.__frequency, self.__unit)

    def from_csv(self, path=None) -> bool:
        """Set info PrimaryResource from a csv file.
        Args:
            path (str, optional): Path csv file with info primary resource. Defaults to None.
        Returns:
            bool: True for successfully information extraction. 
        """
        if path is None:
            return False

        if self.source.lower() == 'ideam':
            __file_obj = read_ideam_data(
                path=path, _type=self.__type_resource, station=self.station)

        if self.source.lower() == 'pw_nasa':
            __file_obj = read_pw_nasa_data(
                path=path, _type=self.__type_resource)

        self.__date_start = __file_obj['info']['date_start']
        self.__date_end = __file_obj['info']['date_end']
        self.__frequency = __file_obj['info']['frequency']
        self.__unit = __file_obj['info']['unit']
        self.__data_df = __file_obj['data']
        return True

    def from_json(self, json=None):
        """Set info PrimaryResource from a JSON object.

        Args:
            json (JSON, optional): Data resource object: Include Name, times, _source and data. Defaults to None.
        """
        if json is None:
            pass

    def to_json(self):
        """Convert instance to JSON object.
        """
        pass

    def to_csv(self):
        """Write current instance info in csv file.
        """
        pass


class ResourceViability:
    __resource: object = None
    __viability: object = None
    y_hline: str = None

    def __init__(self, min_hydro=20, min_pv=3.8, min_wind=2.0, min_biomass=20) -> None:
        self.__min_hydro = min_hydro
        self.__min_pv = min_pv
        self.__min_wind = min_wind
        self.__min_biomass = min_biomass

    def evaluate_resource(self, resource):
        """Mesure the viability and variability resource (pv, hydro, wind, biomass).

        Args:
            resource (PrimaryResource Object): Object with info and historical data.
        """        
        self.__resource = resource
        status = self.read_type_resource(resource)
        if status:
            print(self.__viability.variability)
            print(self.__viability.autonomy)
            print(' ')
        # self.graph_viability(resource=resource)

    def read_type_resource(self, resource):
        if resource.type_resource == 'hydro':
            self.__viability = Hydro(resource.data)
        elif resource.type_resource == 'pv':
            self.y_hline = self.__min_pv
            self.__viability = Pv(resource.data, self.__min_pv)
        elif resource.type_resource == 'wind':
            self.y_hline = self.__min_wind
            self.__viability = Wind(resource.data, self.__min_wind)
        else:
            self.y_hline = self.__min_biomass
            self.__viability = Pv(resource.data, self.__min_pv)
        return True

    def graph_resource(self):        
        #fig = self.__viability.viability_graph
        #fig2 = self.__viability.variability_graph
        self.__viability.all_graph
        plt.show()
    
    def potential(self):
        return self.__viability.potential()
    
    def extra(self):
        self.__viability.graph_pdc()

    def electrical_demand(self, percentage_value=0.3):
        demand = pd.read_excel('./recursos/demand/Jamundi-XM-NR.xlsx', header=2)
        demand = demand.filter(
            items=['Fecha - Año', 'Fecha - Mes', 'Fecha - Día', 'Suma de Demanda Real'])
        demand = demand.rename(
            columns={'Fecha - Año': 'year', 'Fecha - Mes': 'month', 'Fecha - Día': 'day', 'Suma de Demanda Real': 'Valor'})

        m = {'enero':1, 'febrero':2, 'marzo':3, 'abril':4, 'mayo':5, 'junio':6, 'julio':7, 'agosto':8, 'septiembre':9, 'octubre':10, 'noviembre':11, 'diciembre':12}

        demand['month']= demand['month'].map(m)
        demand['Fecha'] = pd.to_datetime(demand[['year', 'month', 'day']]) 
        demand = demand.drop(['year', 'month', 'day'], axis=1)
        #demand = demand.set_index('Fecha')

        demand_month, demand_month_piv = get_data_month(demand)


        # Plot figure
        fig, (ax1, ax2) = plt.subplots(2, 1,  figsize=(10, 6))
        demand_month_piv.plot(kind='line', ax=ax1, alpha=0.4)

        # Mean chart
        demand_month_piv['mean'] = demand_month_piv.mean(axis=1)
        demand_month_piv['std'] = demand_month_piv.std(axis=1)
        demand_month_piv.plot(kind='line', y='mean', ax=ax1,
                            style='--k')
        ax1.fill_between(demand_month_piv.index, demand_month_piv['mean'] - demand_month_piv['std'], demand_month_piv['mean'] + demand_month_piv['std'],
                         alpha=.15)
        ax1.set_title('Electricity demand', fontdict=font)
        ax1.set_xlabel('Year', fontdict=font)
        ax1.set_ylabel('[MWh]', fontdict=font)

        demand_month['Mes'] = pd.to_datetime(
            demand_month.index.month, format="%m").month_name()

        # Boxplot chart
        sns.boxplot(data=demand_month, x='Mes', y='Valor', ax=ax2)
        ax2.set_title('Electricity demand', fontdict=font)
        ax2.set_xlabel('Year', fontdict=font)
        ax2.set_ylabel('[MWh]', fontdict=font)

        plt.subplots_adjust(hspace=0.5, bottom=0.1)

        demand_result = pd.DataFrame(index=demand_month_piv.index)
        demand_result['Valor'] = demand_month_piv['mean']

        def demand_percentage(x): return x*percentage_value
        return demand_result.apply(demand_percentage)


class Potential:
    def __init__(self) -> None:
        self.source_name = None
        self.description = None