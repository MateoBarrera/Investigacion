import pandas as pd
import matplotlib.pyplot as plt

def graph(obj):
  plt.figure(figsize=(10, 5))
  ax = plt.gca()
  pd.DataFrame(obj.data).plot(
      kind='line', x='Fecha', y='Valor', ax=ax)
  plt.title('Autograph method')
  plt.show()
