from potentials.source import *
from potentials.graph import *

#### TIMBA - Hydro ####
test_obj = PrimaryResource(name='Caudal medio mensual',
                           type_resource='hydro', source='Ideam', station=26057040)
test_obj.from_csv('./recursos/hydro/caudal_medio_mensual/Valle.csv.csv')
print("Station 26057040-TIMBA")
print(test_obj.data_info)

viability_obj = ResourceViability()
viability_obj.evaluate_resource(test_obj)

#### POTRERITO - Hydro ####
test_obj = PrimaryResource(name='Caudal medio mensual',
                           type_resource='hydro', source='Ideam', station=26057030)
test_obj.from_csv('./recursos/hydro/caudal_medio_mensual/Valle.csv.csv')
print("Station 26057030-POTRERITO")

print(test_obj.data_info)

viability_obj = ResourceViability()
viability_obj.evaluate_resource(test_obj)
viability_obj.graph_resource()