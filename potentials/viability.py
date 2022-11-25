import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

class Hydro:
  __is_viability: bool = False
  __viability_graph: object = None
  __variability: float = None
  __variability_graph: object = None
  __autonomy: float = None
  def __init__(self, data) -> None:
    self.data = data
    self.q_data = pd.DataFrame(data)['Valor'].to_list()
    self.flow_permanece_curve()
    self.calculate_variability()
    
  def flow_permanece_curve(self):
    """Evaluate the resource with the flow duration curve graph for the given data.
    """    
    q_data_sort = np.sort(self.q_data)[::-1]
    q_frequency = (np.arange(1.,len(q_data_sort)+1) / len(q_data_sort))*100

    #Q parameters calculation
    q_sr_index = int(len(q_data_sort)*0.7)
    q_sr = q_data_sort[q_sr_index]
    q_max =q_data_sort[int(len(q_data_sort)*0.024)]
    q_mean = q_data_sort[int(len(q_data_sort)*0.5)]

    #Plot figure
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 6))
    
    #Plot raw data
    self.data.plot(kind='line', x='Fecha', y='Valor', ax=ax1, label="Q")

    ax1.hlines(y=q_mean, xmin=self.data['Fecha'].min(), xmax=self.data['Fecha'].max(), colors='gray', linestyles='--',
               label="Qmean= {:.2f}".format(q_mean))
    ax1.hlines(y=q_sr, xmin=self.data['Fecha'].min(), xmax=self.data['Fecha'].max(), colors='red', linestyles='--',
                label="Qsr = {:.2f}".format(q_sr))
    ax1.set_title('Average monthly flow')
    ax1.set_xlabel('months')
    ax1.set_ylabel('flow [m^3/s]')
    ax1.legend(loc='upper left')

    #Flow permanence curve
    ax2.plot(q_frequency, q_data_sort)

    ax2.fill_between(q_frequency[0:q_sr_index], q_data_sort[0:q_sr_index], q_sr, alpha=0.2, color='b')
    ax2.fill_between(q_frequency[q_sr_index:],q_data_sort[q_sr_index:], q_sr, alpha=0.2, color='r')
    ax2.hlines(y=q_sr, xmin=q_frequency[0], xmax=q_frequency[-1], colors='red', linestyles='--',
               label="Qsr = {:.2f}".format(q_sr))
    ax2.set_xlabel("Percentage of occurrence [%]")
    ax2.set_ylabel("Flow rate [m^3/s]")
    ax2.set_title('Flow permanence curve')
    ax2.legend(loc='upper right')
    #result = self.calculate_potential(q_sr, q_mean)

    self.__viability_graph = fig

  def calculate_variability(self):
    #Prepare data
    data_month = self.data.set_index('Fecha')
    data_month = data_month.asfreq('M', method='ffill')
    data_month['Año'] = data_month.index.year
    data_month['Mes'] = pd.to_datetime(
        data_month.index.month, format="%m")

    #Plot figure
    fig, (ax1, ax2) = plt.subplots(2, 1,  figsize=(10, 6))
    #Grouped year charts
    data_month_piv = pd.pivot_table(data_month, index=['Mes'], columns=[
                                    'Año'], values=['Valor'])
    data_month_piv.sort_index()
    #data_month_piv.sort_values('month')
    data_month_piv.plot(kind='line', ax=ax1, alpha=0.4)
    

    #Mean chart
    data_month_piv['mean'] = data_month_piv.mean(axis=1)
    data_month_piv['std'] = data_month_piv.std(axis=1)
    data_month_piv.plot(kind='line', y='mean', ax=ax1,
                        style='--k')
    ax1.fill_between(data_month_piv.index, data_month_piv['mean'] - data_month_piv['std'], data_month_piv['mean'] + data_month_piv['std'],
                     alpha=.15)

    data_month['Mes'] = pd.to_datetime(
        data_month.index.month, format="%m").month_name()
    #Boxplot chart
    sns.boxplot(data=data_month, x='Mes', y='Valor', ax=ax2)
    self.__variability_graph = fig

  @property
  def viability_graph(self):
    return self.__viability_graph

  @property
  def is_viability(self):
    return self.__is_viability

  @property
  def variability(self):
    return self.__variability

  @property
  def variability_graph(self):
    return self.__variability_graph
