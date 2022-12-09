import numpy as np
from itertools import product
from collections import deque

def generate_scenarios(list_resources=[1,1,1,1]):
  y_pv, y_w, y_pch, y_bio = list_resources
  
  seed = [1.0, 0.5, 0.25, 0]
  all_combinations = list(product(*[seed]*4))

  weight_scenarios = np.array(all_combinations)
  y_resources = np.array([y_pv, y_w, y_pch, y_bio])

  Ex = weight_scenarios * y_resources
  New_Ex = list()
  for items in Ex:
    if sum(items)==1:
      New_Ex.append(str(list(items)))

  print("Ex matrix")
  New_Ex = list(dict.fromkeys(New_Ex))
  New_Ex = [eval(i) for i in New_Ex]
  print("# of scenarios {}".format(len(New_Ex)))
  return New_Ex

scenarios = generate_scenarios()
print(scenarios)

