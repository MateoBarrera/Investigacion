import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

plt.style.use('seaborn-paper')
#plt.style.use('ggplot')

font = {'family': 'serif',
        'color':  'black',
        'weight': 'bold',
        'size': 10,
        }

class Hydro:
  """Analysis of the water resource through the flow permanence curve, resource variability and calculation of autonomy from historical monthly average flow data.

  Returns:
      Object: Hydro object
  """  
  __is_viability: bool = False
  __variability: float = None
  __autonomy: float = None
  
  def __init__(self, data) -> None:
    self.data = data
    self.q_data = pd.DataFrame(data)['Valor'].to_list()
    self.calculate_autonomy()    
    
  def flow_permanece_curve(self):
    """Evaluate the resource with the flow duration curve graph for the given data.
    """    
    q_data_sort = np.sort(self.q_data)[::-1]
    q_frequency = (np.arange(1.,len(q_data_sort)+1) / len(q_data_sort))*100

    #Plot figure
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 6))
    
    #Plot raw data
    self.data.plot(kind='line', x='Fecha', y='Valor', ax=ax1, label="Q")
    ax1.hlines(y=self.q_mean, xmin=self.data['Fecha'].min(), xmax=self.data['Fecha'].max(), colors='gray', linestyles='--',
               label="Qmean= {:.2f}".format(self.q_mean))
    ax1.hlines(y=self.q_sr, xmin=self.data['Fecha'].min(), xmax=self.data['Fecha'].max(), colors='red', linestyles='--',
                label="Qsr = {:.2f}".format(self.q_sr))
    
    ax1.set_title('Average monthly flow', fontdict=font)
    ax1.set_xlabel('Year', fontdict=font)
    ax1.set_ylabel('Q [m^3/s]', fontdict=font)
    ax1.legend(loc='upper left')

    #Flow permanence curve
    ax2.plot(q_frequency, q_data_sort)

    ax2.fill_between(q_frequency[0:self.q_sr_index], q_data_sort[0:self.q_sr_index], self.q_sr, alpha=0.2, color='b')
    ax2.fill_between(q_frequency[self.q_sr_index:],q_data_sort[self.q_sr_index:], self.q_sr, alpha=0.2, color='r')
    ax2.hlines(y=self.q_sr, xmin=q_frequency[0], xmax=q_frequency[-1], colors='red', linestyles='--',
               label="Qsr = {:.2f}".format(self.q_sr))
    ax2.set_xlabel("Percentage of occurrence [%]", fontdict=font)
    ax2.set_ylabel("Flow rate [m^3/s]", fontdict=font)
    ax2.set_title('Flow permanence curve', fontdict=font)
    ax2.legend(loc='upper right')
    plt.subplots_adjust(hspace=0.3, bottom=0.1)
    
    return fig

  def graph_variability(self):
    #Prepare data
    data_month = self.data.set_index('Fecha')
    data_month = data_month.asfreq('M', method='ffill')
    data_month['Año'] = data_month.index.year
    data_month['Mes'] = pd.to_datetime(
        data_month.index.month, format="%m")

    #Grouped year charts
    data_month_piv = pd.pivot_table(data_month, index=['Mes'], columns=[
                                    'Año'], values=['Valor'])
    data_month_piv.sort_index()
    #data_month_piv.sort_values('month')

    #Plot figure
    fig, (ax1, ax2) = plt.subplots(2, 1,  figsize=(10, 6))
    data_month_piv.plot(kind='line', ax=ax1, alpha=0.4)

    #Mean chart
    data_month_piv['mean'] = data_month_piv.mean(axis=1)
    data_month_piv['std'] = data_month_piv.std(axis=1)
    data_month_piv.plot(kind='line', y='mean', ax=ax1,
                        style='--k')
    ax1.fill_between(data_month_piv.index, data_month_piv['mean'] - data_month_piv['std'], data_month_piv['mean'] + data_month_piv['std'],
                     alpha=.15)
    ax1.hlines(y=self.q_sr, xmin=data_month_piv.index.min(), xmax=data_month_piv.index.max(), colors='red', linestyles='--',
               label="Qsr = {:.2f}".format(self.q_sr))
    ax1.set_title('River regime', fontdict=font)
    ax1.set_xlabel('Year', fontdict=font)
    ax1.set_ylabel('Q [m^3/s]', fontdict=font)

    data_month['Mes'] = pd.to_datetime(
        data_month.index.month, format="%m").month_name()
    
    #Boxplot chart
    sns.boxplot(data=data_month, x='Mes', y='Valor', ax=ax2)
    ax2.set_title('Average monthly flow', fontdict=font)
    ax2.set_xlabel('Year', fontdict=font)
    ax2.set_ylabel('Q [m^3/s]', fontdict=font)

    plt.subplots_adjust(hspace=0.5, bottom=0.1)
    return fig

  def calculate_autonomy(self):
    #Q parameters calculation
    q_data_sort = np.sort(self.q_data)[::-1]
    self.q_sr_index = int(len(q_data_sort)*0.7)
    self.q_sr = q_data_sort[self.q_sr_index]
    #q_max = q_data_sort[int(len(q_data_sort)*0.024)]
    self.q_mean = q_data_sort[int(len(q_data_sort)*0.5)]
    
    autonomy = 0

    #Prepare data
    data_month = self.data.set_index('Fecha')
    data_month = data_month.asfreq('M', method='ffill')
    data_month['Año'] = data_month.index.year
    data_month['Mes'] = pd.to_datetime(
        data_month.index.month, format="%m")

    data_month_piv = pd.pivot_table(data_month, index=['Mes'], columns=[
                                    'Año'], values=['Valor'])
    data_month_piv['mean'] = data_month_piv.mean(axis=1)
    data_month_piv.sort_index()
    cv = lambda x: np.std(x, ddof=1) / np.mean(x) * 100 
    self.__variability = data_month_piv.apply(cv).mean()
    q_month_mean = data_month_piv['mean'].to_list()

    for q_month_item in q_month_mean:
      if q_month_item > self.q_sr:
        autonomy += 1
    self.__autonomy = autonomy/12

  @property
  def viability_graph(self):
    return self.flow_permanece_curve()

  @property
  def is_viability(self):
    return self.__is_viability

  @property
  def variability(self):
    return self.__variability

  @property
  def variability_graph(self):
    return self.graph_variability()

  @property 
  def autonomy(self):
    return self.__autonomy
  
  @property
  def all_graph(self):
    self.flow_permanece_curve()
    self.graph_variability()
    return 
