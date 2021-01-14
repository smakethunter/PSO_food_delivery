Szkic Projektu: 

https://docs.google.com/document/d/1UBqcbSAs76G2SIo3GzXs6zvLel50BhM28p_pVsCWDSU/edit#heading=h.5a2lndih0ivk
```python

```


```python
import numpy as np

import matplotlib.pyplot as plt
from PSO import *
from delivery_swarm import *
working_path = os.pardir+'/'
%matplotlib inline
```

## Utworzenie przypadku i zapis do pliku
1. przed utworzeniem zrestartuj kernel
2. przy tworzeniu nowego przypadku zastosuj ./cases/NazwaPrzypadku(liczba_kurierów)k(liczba_zamówień)z(liczba_restauracji)r.txt



```python
particle = DeliveryService(nr_couriers = 2, nr_orders = 8, nr_restaurants = 4)
filename =  '2c8o4r.txt'
particle.save_to_file(filename)


```

## Odtworzenie roju z pliku i eksperyment
Wykonaj eksperymenty dla różnych parametrów {inertia,cp,cg}


```python
from summary import *
```


```python
import warnings
import tqdm
warnings.filterwarnings('ignore')
from summary import *
filename = '2c8o4r.txt'
csv_file = '../data/summary.csv'
run_pso_and_save_summary(filename,20,0.1,0.2,0.3,30,draw_route=False,database=csv_file)
```


    
https://github.com/smakethunter/PSO_food_delivery/blob/master/changes_per_epoch_plots/przypadek10k200z20r10_01_01_01_20.png
    



    
![png](output_6_1.png)
    



    
![png](output_6_2.png)
    



    
![png](output_6_3.png)
    



    
![png](output_6_4.png)
    



```python
import pandas as pd
from IPython.display import Image
```


```python
experiments_logs = pd.read_csv(csv_file)
print(experiments_logs.columns)
```

    Index(['case_name', 'PSO_time', 'avg_v_computation', 'avg_move_time',
           'avg_epoch_time', 'avg_fitness_calculation_time', 'loss', 'nr_changes',
           'nr_orders', 'nr_restaurants', 'nr_couriers', 'nr_particles',
           'nr_epochs', 'inertia', 'cp', 'cg', 'particles_history_plot',
           'loss_history_plot', 'best_path_plot', 'changes_per_epoch_plot',
           'experiment_documentation'],
          dtype='object')



```python
showcase = experiments_logs
showcase
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>case_name</th>
      <th>PSO_time</th>
      <th>avg_v_computation</th>
      <th>avg_move_time</th>
      <th>avg_epoch_time</th>
      <th>avg_fitness_calculation_time</th>
      <th>loss</th>
      <th>nr_changes</th>
      <th>nr_orders</th>
      <th>nr_restaurants</th>
      <th>...</th>
      <th>nr_particles</th>
      <th>nr_epochs</th>
      <th>inertia</th>
      <th>cp</th>
      <th>cg</th>
      <th>particles_history_plot</th>
      <th>loss_history_plot</th>
      <th>best_path_plot</th>
      <th>changes_per_epoch_plot</th>
      <th>experiment_documentation</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>2c8o4r.txt</td>
      <td>1.063884</td>
      <td>0.001414</td>
      <td>0.000103</td>
      <td>0.035351</td>
      <td>0.000108</td>
      <td>33.609727</td>
      <td>5</td>
      <td>8</td>
      <td>4</td>
      <td>...</td>
      <td>20</td>
      <td>30</td>
      <td>0.1</td>
      <td>0.2</td>
      <td>0.3</td>
      <td>swarm_loss_plots/2c8o4r20_01_02_03_30.png</td>
      <td>loss_history_plots/2c8o4r20_01_02_03_30.png</td>
      <td>best_path_plots/2c8o4r20_01_02_03_30.png</td>
      <td>changes_per_epoch_plots/2c8o4r20_01_02_03_30.png</td>
      <td>experiments_documentation/2c8o4r.txt</td>
    </tr>
  </tbody>
</table>
<p>1 rows × 21 columns</p>
</div>




```python
from scipy.stats import zscore
fig, ax =plt.subplots()
ax.set(title = 'Rozkład funkcji kosztu dla wywołanych przypadków')
showcase.boxplot('loss',ax = ax)
showcase['z_scores'] = zscore(showcase['loss'])
filtered_entries = showcase[abs(showcase['z_scores'])<3]
fig2, ax2 =plt.subplots()
filtered_entries.loss.hist(ax = ax2, bins = 30)
ax2.set(title = 'Rozłkad po usunięciu wartości odstających', xlabel = 'koszt', ylabel = 'ilość')
ax2.axvline(showcase.loss.mean(), c = 'red')
ax2.axvline(showcase.loss.mean()-showcase.loss.std(),c = 'red')
ax2.axvline(showcase.loss.mean()+showcase.loss.std(),c = 'red')
```


```python

```
