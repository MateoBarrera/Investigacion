from potentials.source import *
from potentials.graph import *
import matplotlib.pyplot as plt


#### Jamundi PV ####
test_obj = PrimaryResource(name='Irradiance',
                           type_resource='pv', source='pw_nasa')
test_obj.from_csv('./recursos/pv/PV-Jamundi-H.csv')

print("Jamundi PV\n{}".format(test_obj.data_info))

viability_obj = ResourceViability()
viability_obj.evaluate_resource(test_obj)
viability_obj.graph_resource()
#viability_obj.extra()
p_pv = viability_obj.potential()


plt.style.use('seaborn-v0_8')
#plt.style.use('ggplot')

font = {'family': 'serif',
        'color':  'black',
        'weight': 'bold',
        'size': 10,
        }


plt.show()











###############################
#test_obj = PrimaryResource(name='Wind speed',                    type_resource='wind', source='Ideam', station=26055110)
#test_obj.from_csv('./recursos/wind/Wind-Jamundi-D.csv.csv')


""" #### POTRERITO - Hydro ####
test_obj = PrimaryResource(name='Caudal medio mensual',
                           type_resource='hydro', source='Ideam', station=26057030)
test_obj.from_csv('./recursos/hydro/caudal_medio_mensual/Valle.csv.csv')
print("\nStation 26057030-POTRERITO")

print(test_obj.data_info)

viability_obj = ResourceViability()
viability_obj.evaluate_resource(test_obj)
viability_obj.graph_resource() """
