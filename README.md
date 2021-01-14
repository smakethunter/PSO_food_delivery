Szkic projektu:
https://docs.google.com/document/d/1lzUxZjcf3DzIbYNxZNsbLj9RVE_VxoxeMv6Tvu__2jo/edit
#%%

import numpy as np

import matplotlib.pyplot as plt
from PSO import *
from delivery_swarm import *
working_path = os.pardir+'/'
%matplotlib inline

#%% md

## Utworzenie przypadku i zapis do pliku
1. przed utworzeniem zrestartuj kernel
2. przy tworzeniu nowego przypadku zastosuj ./cases/NazwaPrzypadku(liczba_kurierów)k(liczba_zamówień)z(liczba_restauracji)r.txt


#%%

particle = DeliveryService(nr_couriers = 2, nr_orders = 8, nr_restaurants = 4)
filename =  '2c8o4r.txt'
particle.save_to_file(filename)



#%% md

## Odtworzenie roju z pliku i eksperyment
Wykonaj eksperymenty dla różnych parametrów {inertia,cp,cg}

#%%

from summary import *

#%%

import warnings
import tqdm
warnings.filterwarnings('ignore')
from summary import *
filename = '2c8o4r.txt'
csv_file = '../data/summary.csv'
run_pso_and_save_summary(filename,20,0.1,0.2,0.3,30,draw_route=False,database=csv_file)

#%%

import pandas as pd
from IPython.display import Image

#%%

experiments_logs = pd.read_csv(csv_file)
print(experiments_logs.columns)
#%%

showcase = experiments_logs
showcase
#%%

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

#%%

