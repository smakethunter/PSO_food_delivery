from pso.delivery_swarm import *
import csv
import os


def run_pso_and_save_summary(filename: str, nr_particles: int, inertia: float, cp: float, cg: float, nr_epochs: int,
                             draw_route: bool = False, database = None):
    filename_to_run = os.pardir+'/cases/' + filename
    swarm:DeliverySwarm = DeliverySwarm(DeliverySwarmGenerator(nr_particles=nr_particles, from_file=True,
                                                               filename=filename_to_run))
    history = History(swarm.time_table)
    pso = PSO(inertia, cp, cg, nr_epochs , history)
    pso.fit(swarm)
    main_path = os.pardir
    name = filename.split('/')[-1]
    filename_png = name.split('.')[-2]+(f'{nr_particles}_{inertia}_{cp}_{cg}_{nr_epochs}').replace('.','')+'.png'
    filename_txt = name.split('.')[-2]+(f'{nr_particles}_{inertia}_{cp}_{cg}_{nr_epochs}').replace('.','')+'.txt'
    pso.history.draw_particles_history(main_path+'/swarm_loss_plots/' + filename_png)
    pso.history.draw_loss(main_path+'/loss_history_plots/' + filename_png)
    if draw_route:
        pso.history.draw_best_path(main_path+'/best_path_plots/'+ filename_png)
    pso.history.draw_changes_per_epoch(main_path + '/changes_per_epoch_plots/' + filename_png)
    pso.to_file(main_path+'/experiments_documentation/' + filename_txt)

    pso.history.draw_mobility_per_epoch(main_path + '/mobility_plots/' + filename_png)

    pso.history.draw_avg_swarm_loss(main_path + '/draw_avg_swarm_loss_plots/' + filename_png)

    row_to_csv = {}
    row_to_csv['case_name'] = name
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
    isEmpty = False
    filename = database if database is not None else 'statistics.csv'
    try:
        with open(filename, 'r', newline='') as csvfile:

            if len(csvfile.readline())==0:
                isEmpty = True
    except (FileNotFoundError,RuntimeError):
        isEmpty = True


    if isEmpty:
        with open(filename, 'w', newline='') as csvfile:

            writer = csv.DictWriter(csvfile, fieldnames = fieldnames)
            writer.writeheader()
    with open(filename, 'a', newline='') as csvfile:

            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writerow(row_to_csv)

    del pso
    del swarm
    del history

def GridSearchPSO(filename,params):
    for parameter in zip(params['nr_particles'], params['inertia'], params['cp'], params['cg'], params['nr_epochs']):

        run_pso_and_save_summary(filename, parameter[0], parameter[1], parameter[2], parameter[3], parameter[4])
