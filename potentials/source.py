import pandas as pd
import matplotlib.pyplot as plt
from .viability import Hydro, Pv
from .extract.load import read_ideam_data, read_pw_nasa_data


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
            type_resource (str, optional): Type of resource (Solar, Hydro, Wind, Biomas, etc). Defaults to None.
            source (str, optional): Information source. Defaults to None.
        """
        self.name = name
        self.__type_resource = type_resource
        self.source = source
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
            print("New function...")
            __file_obj = read_ideam_data(path=path, station=self.station)

        if self.source.lower() == 'pw_nasa':
            print("New function... 2")
            __file_obj = read_pw_nasa_data(path=path)

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

    def __init__(self, min_hydro=20, min_pv=3.0, min_wind=3, min_biomass=20) -> None:
        self.__min_hydro = min_hydro
        self.__min_pv = min_pv
        self.__min_wind = min_wind
        self.__min_biomass = min_biomass

    def evaluate_resource(self, resource):
        self.__resource = resource
        self.read_type_resource(resource)
        # self.graph_viability(resource=resource)

    def read_type_resource(self, resource):
        if resource.type_resource == 'hydro':
            self.__viability = Hydro(resource.data)
        elif resource.type_resource == 'pv':
            self.y_hline = self.__min_pv
            self.__viability = Pv(resource.data, self.__min_pv)
        elif resource.type_resource == 'wind':
            self.y_hline = self.__min_wind
        else:
            self.y_hline = self.__min_biomass

    def graph_resource(self):
        print(":: Variability Resource: {:.2f}% ::".format(
            self.__viability.variability))
        print("Average monthly variation coefficient")
        print(":: Autonomy Resource: {:.2f}% ::".format(
            self.__viability.autonomy*100))
        print("Months higher than the ecological flow.")
        #fig = self.__viability.viability_graph
        #fig2 = self.__viability.variability_graph
        self.__viability.all_graph
        plt.show()


class Potential:
    def __init__(self) -> None:
        self.source_name = None
        self.description = None
