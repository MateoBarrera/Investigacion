from potentials.source import *
from potentials.graph import *
import matplotlib.pyplot as plt


viability_obj = ResourceViability()
demand = viability_obj.electrical_demand(percentage_value=0.15)

#### TIMBA - Hydro ####
test_obj = PrimaryResource(name='Caudal medio mensual',
                           type_resource='hydro', source='Ideam', station=26057040)
test_obj.from_csv('./recursos/hydro/caudal_medio_mensual/Jamundi.csv.csv')

print("Jamundi Hydro - Station 26057040-TIMBA\n{}".format(test_obj.data_info))

viability_obj = ResourceViability()
viability_obj.evaluate_resource(test_obj)
#viability_obj.graph_resource()
p_hydro = viability_obj.potential()


#### Jamundi PV ####
test_obj = PrimaryResource(name='Irradiance',
                           type_resource='pv', source='pw_nasa')
test_obj.from_csv('./recursos/pv/PV-Jamundi-H.csv')

print("Jamundi PV\n{}".format(test_obj.data_info))

viability_obj = ResourceViability()
viability_obj.evaluate_resource(test_obj)
#viability_obj.graph_resource()
p_pv = viability_obj.potential()


#### Jamundi wind ####
test_obj = PrimaryResource(name='Wind speed',
                           type_resource='wind', source='pw_nasa')
test_obj.from_csv('./recursos/wind/Wind-Jamundi-D-Nasa.csv')

print("Jamundi Wind\n{}".format(test_obj.data_info))

viability_obj = ResourceViability()
viability_obj.evaluate_resource(test_obj)
#viability_obj.graph_resource()
p_wind = viability_obj.potential()

plt.style.use('seaborn-v0_8')
#plt.style.use('ggplot')

font = {'family': 'serif',
        'color':  'black',
        'weight': 'bold',
        'size': 10,
        }

fig, ax  = plt.subplots(2, 2, figsize=(10, 10))
p_hydro.plot(kind='line', ax=ax[0][0], label="Hydro")
p_pv.plot(kind='line', ax=ax[0][1], label="Pv")
p_wind.plot(kind='line', ax=ax[1][0], label="Wind")
demand.plot(kind='line', ax=ax[1][1], label="Demand")

ax[0][0].set_title('Power generation - monthly average', fontdict=font)
ax[0][0].set_xlabel('Year', fontdict=font)
ax[0][0].set_ylabel('Wh/month', fontdict=font)
ax[0][0].legend(loc='upper left')
ax[0][0].set_ylim(bottom=0)

ax[0][1].set_title('Power generation - monthly average irradiance', fontdict=font)
ax[0][1].set_xlabel('Year', fontdict=font)
ax[0][1].set_ylabel('Wh/month', fontdict=font)
ax[0][1].legend(loc='upper left')
ax[0][1].set_ylim(bottom=0)

ax[1][0].set_title('Power generation - monthly average wind', fontdict=font)
ax[1][0].set_xlabel('Year', fontdict=font)
ax[1][0].set_ylabel('Wh/month', fontdict=font)
ax[1][0].legend(loc='upper left')
ax[1][0].set_ylim(bottom=0)

ax[1][1].set_title('Electricity demand', fontdict=font)
ax[1][1].set_xlabel('Year', fontdict=font)
ax[1][1].set_ylabel('[MWh]', fontdict=font)
ax[1][1].legend(loc='upper left')
ax[1][1].set_ylim(bottom=0)
plt.subplots_adjust(hspace=0.5, bottom=0.1)
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
