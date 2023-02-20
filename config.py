import numpy as np
from itertools import product
from prettytable import PrettyTable

from tabulate import tabulate


def generate_scenarios(list_resources=[1, 1, 1, 1]):
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

  New_Ex = list(dict.fromkeys(New_Ex))
  New_Ex = [eval(i) for i in New_Ex]

  describe_scenarios(New_Ex, list_resources, seed)
  return New_Ex


def describe_scenarios(scenarios, list_resources, seed):
  info = PrettyTable()
  info.title = "Scenarios summary"
  info.field_names = ["Total scenarios", "{}".format(len(scenarios))]
  info.add_row(["Resources", "Included"])
  for resource in zip(["Pv", "Wind", "PCH", "Biomass"],list_resources):
    if resource[1] == 1:
      info.add_row([resource[0], u'\N{check mark}'])
    else:
      info.add_row([resource[0], u'\N{Ballot X}'])
  percentage_info = PrettyTable()
  percentage_info.title = "% Penetration for demand coverage"
  percentage_info.field_names = ["{} %".format(x*100) for x in seed]
  Ex = PrettyTable()
  Ex.field_names = ["Pv", "Wind", "PCH", "Biomass"]
  Ex.title = "Scenarios"
  for scenario in scenarios:
    scenario = list(map(lambda x: "{} %".format(x*100) , scenario))
    Ex.add_row(scenario)
  print(info)
  print(percentage_info)
  print(Ex)

scenarios = generate_scenarios()
