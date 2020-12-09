from system import *
from PSO import *
from delivery_swarm import *
from delivery_service import Courier
import csv
import os

main_path = '/'.join(os.getcwd().split('/')[:-1])
def run_pso_and_save_summary(filename,nr_particles, inertia,cp,cg, nr_epochs ):
    swarm:DeliverySwarm = DeliverySwarm(DeliverySwarmGenerator(nr_particles=nr_particles, from_file=True, filename=filename))
    history = History(swarm.time_table)
    pso = PSO(inertia, cp, cg, nr_epochs , history)
    filename_png = filename.split('.')[-2]+f'{nr_particles}_{inertia}_{cp}_{cg}_{nr_epochs}'+'.png'
    filename_txt = filename.split('.')[-2]+f'{nr_particles}_{inertia}_{cp}_{cg}_{nr_epochs}'+'.txt'
    print(pso.fit(swarm))
    history.draw_particles_history(main_path + '/swarm_loss_plots/' + filename_png)
    print(pso.history.time_performance)
    history.draw_loss(main_path + '/loss_history_plots/' + filename_png)
    # history.draw_path_search()
    print(pso.history.epochs_with_change)
    pso.history.draw_best_path(main_path+'/best_path_plots/'+ filename_png)
    pso.to_file(main_path + '/experiments_documentation/' + filename_txt)
    pso.history.draw_changes_per_epoch(main_path + '/changes_per_epoch_plots/' + filename_png)
    row_to_csv = {}
    row_to_csv['case_name'] = filename.split('.')[0]
    nr_changes=0
    for _, v in pso.history.epochs_with_change.items():
        nr_changes += v
    for k, v in pso.history.time_performance.items():
        row_to_csv[k]=v

    row_to_csv['loss'] = pso.history.best_history[-1]
    row_to_csv['nr_changes'] = nr_changes
    particle: DeliveryService = swarm.swarm[-1]
    row_to_csv['nr_orders'] = particle.nr_orders
    row_to_csv['nr_restaurants'] = particle.nr_restaurants
    row_to_csv['nr_couriers'] = particle.nr_couriers
    row_to_csv['nr_particles'] = nr_particles
    row_to_csv['nr_epochs'] = nr_epochs
    row_to_csv['inertia'] = inertia
    row_to_csv['cp'] = cp
    row_to_csv['cg'] = cg
    row_to_csv['particles_history_plot'] =  'swarm_loss_plots/' + filename_png
    row_to_csv['loss_history_plot'] = 'loss_history_plots/' + filename_png
    row_to_csv['best_path_plot'] = 'best_path_plots/'+ filename_png
    row_to_csv['changes_per_epoch_plot'] = 'changes_per_epoch_plots/' + filename_png
    row_to_csv['experiment_documentation'] = 'experiments_documentation/' + filename
    fieldnames = [k for k,v in row_to_csv.items()]

    with open('../summary.csv', 'a', newline='') as csvfile:

        writer = csv.DictWriter(csvfile, fieldnames = fieldnames )

        #writer.writeheader()
        writer.writerow(row_to_csv)
    del pso
    del swarm
    del history

def GridSearchPSO(filename,params):
    for parameter in zip(params['nr_particles'], params['inertia'], params['cp'], params['cg'], params['nr_epochs']):

        run_pso_and_save_summary(filename, parameter[0], parameter[1], parameter[2], parameter[3], parameter[4])
