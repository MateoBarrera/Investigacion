from potentials.source import *
from potentials.graph import *
import matplotlib.pyplot as plt


viability_obj = ResourceViability()
demand = viability_obj.electrical_demand(percentage_value=0.15)

plt.show()