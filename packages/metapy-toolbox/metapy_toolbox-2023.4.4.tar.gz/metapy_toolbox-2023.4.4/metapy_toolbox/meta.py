"""Algorithms module"""
import time
from multiprocessing import Pool

import numpy as np
import pandas as pd

import metapy_toolbox.common_library as metapyco


def metaheuristic_optmizer(setup):
    """_summary_

    Args:
        setup (_type_): _description_

    Returns:
        _type_: _description_
    """
    # Start variables
    initial_time = time.time()
    all_results_per_rep = []
    best_population_per_rep = []
    reports = []


    # try:
    #     if not isinstance(setup, dict):
    #         raise TypeError('The setup parameter must be a dictionary.')
    #     if len(setup) != 7:
    #         raise ValueError('The setup parameter must have 7 keys (N_REP, n_population, D, x_lower, x_upper, TYPE CODE, SEED CONTROL).')

    #     for key in setup.keys():
    #         if key not in ['N_REP', 'n_population', 'D', 'x_lower', 'x_upper', 'TYPE CODE', 'SEED CONTROL']:
    #             raise ValueError('The setup parameter must have 7 keys (N_REP, n_population, D, x_lower, x_upper, TYPE CODE, SEED CONTROL).')
        
    #     for key in setup.keys():
    #         if not isinstance(key, (int, list, float, str, type(None))):
    #             raise TypeError(f'Error type in key {key}.')
        
    # except TypeError as te:
    #     print(f'Error {te}')
    # except ValueError as ve:
    #     print(f'Error {ve}')

    # Initial population for each repetition
    population = metapyco.initial_pops(setup['number of repetitions'],
                                        setup['number of population'],
                                        setup['number of dimensions'],
                                        setup['x pop lower limit'],
                                        setup['x pop upper limit'],
                                        setup['type code'],
                                        setup['seed control'])

    # Algorithm selection and general results
    if setup['algorithm'] == 'hill_climbing_01':
        # Define the name of the model
        model_name = 'META_HC001_'
        # Multiprocess
        with Pool() as p:
            settings = [[setup, init_population, setup['seed control'][i]] for i, init_population in enumerate(population)]
            results = p.map_async(func=hill_climbing_01, iterable=settings)
            for result in results.get():
                all_results_per_rep.append(result[0])
                best_population_per_rep.append(result[1])
                reports.append(result[3])

    # Best results
    status_procedure = metapyco.summary_analysis(best_population_per_rep)
    best_result = best_population_per_rep[status_procedure]
    last_line = best_result.iloc[-1]  # Obtém a última linha do DataFrame
    best_of = last_line['OF BEST']
    design_variables = last_line.iloc[:setup['number of dimensions']].tolist()

    # Output details
    end_time = time.time()
    print(' Optimization results:', '\n')
    print(' - Best repetition id: ', status_procedure)
    print(' - Best of:             {:.10e}'.format(best_of))
    print(' - Design variables:   ', design_variables)
    print(' - Process time (s):    {:.6f}'.format(end_time - initial_time))

    return all_results_per_rep, best_population_per_rep, reports, status_procedure

def hill_climbing_01(settings):
    """
    Hill Climbing algorithm.

    See documentation in https://wmpjrufg.github.io/METAPY/FRA_ALG_.html
    
    Args:  
        settings (list): [0] setup (dict), [1] initial population (list), [2] seeds (int).
        setup keys:
            'number of population' (int): number of population.
            'number of iterations' (int): number of iterations.
            'number of dimensions' (int): Problem dimension.
            'x pop lower limit' (list): Lower limit of the design variables.
            'x pop upper limit' (list): Upper limit of the design variables.
            'none variable' (Object or None): None variable. Default is None. 
                                                Use in objective function.
            'objective function' (function): Objective function. 
                                                The Metapy user defined this function.                                                
            'algorithm parameters' (dict): Algorithm parameters.
                'sigma' (float): Control parameter for the Gaussian or Uniform 
                            distribution in percentage. In Gaussian or Uniform distribution, 
                            sigma equivalent to a standard deviation.
                'pdf' (str): Probability density function. 
                                Options: 'normal' or 'uniform'.
    
    Returns:
        df_all (dataframe): All data of the population.
        df_best (dataframe): Best data of the population.
        delta_time (float): Time of the algorithm execution in seconds.
        report (str): Report of the algorithm execution.
    """

    # setup config
    setup = settings[0]
    n_population = setup['number of population']
    n_iterations = setup['number of iterations']
    n_dimensions = setup['number of dimensions']
    x_lower = setup['x pop lower limit']
    x_upper = setup['x pop upper limit']
    none_variable = setup['none variable']
    obj_function = setup['objective function']
    seeds = settings[2]
    if seeds is None:
        pass
    else:
        np.random.seed(seeds)

    # algorithm_parameters
    algorithm_parameters = setup['algorithm parameters']
    std = algorithm_parameters['sigma']
    pdf = algorithm_parameters['pdf']

    # Creating variables in the iteration procedure
    of_pop = []
    fit_pop = []
    neof_count = 0

    # Storage values: columns names about dataset results
    columns_all_data = ['X_' + str(i) for i in range(n_dimensions)]
    columns_all_data.append('OF')
    columns_all_data.append('FIT')
    columns_all_data.append('ITERATION')
    columns_repetition_data = ['X_' + str(i) for i in range(n_dimensions)]
    columns_repetition_data.append('OF BEST')
    columns_repetition_data.append('FIT BET')
    columns_repetition_data.append('ID BEST')
    columns_worst_data  = ['X_' + str(i) for i in range(n_dimensions)]
    columns_worst_data.append('OF WORST')
    columns_worst_data.append('FIT WORST')
    columns_worst_data.append('ID WORST')
    columns_other_data = ['OF AVG', 'FIT AVG', 'ITERATION', 'neof']
    report = "Hill Climbing 01 - report \nInitial population\n\n"
    all_data_pop = []
    resume_result = []

    # Initial population and evaluation solutions
    x_pop = settings[1].copy()
    for i_pop in range(n_population):
        of_pop.append(obj_function(x_pop[i_pop], none_variable))
        fit_pop.append(metapyco.fit_value(of_pop[i_pop]))
        neof_count += 1
        i_pop_solution = metapyco.resume_all_data_in_dataframe(x_pop[i_pop], of_pop[i_pop],
                                                               fit_pop[i_pop], columns_all_data,
                                                               iteration=0)
        all_data_pop.append(i_pop_solution)

    # Best, average and worst values and storage
    repetition_data, best_id = metapyco.resume_process_in_dataframe(x_pop, of_pop, fit_pop,
                                                            columns_repetition_data,
                                                            columns_worst_data,
                                                            columns_other_data,
                                                            neof_count, iteration=0)
    resume_result.append(repetition_data)
    for i_pop in range(n_population):
        if i_pop == best_id:
            report += f'x{i_pop} = {x_pop[i_pop]} - best solution\n'
        else:
            report += f'x{i_pop} = {x_pop[i_pop]} \n'

    # Iteration procedure
    report += "\nIterations\n"
    for iter in range(n_iterations):
        report += f"\nIteration: {iter}\n"
        # Time markup
        initial_time = time.time()

        # Population movement
        for pop in range(n_population):
            report += f"Pop id: {pop}\n"
            # Hill Climbing particle movement
            report += f"    current x = {x_pop[pop]}, of = {of_pop[pop]}, fit = {fit_pop[pop]}\n"
            x_i_temp, of_i_temp, fit_i_temp, neof, \
                                        report = metapyco.mutation_01_movement(obj_function,
                                                                                x_pop[pop],
                                                                                x_lower, x_upper,
                                                                                n_dimensions,
                                                                                pdf, std, report,
                                                                                none_variable)
            i_pop_solution = metapyco.resume_all_data_in_dataframe(x_i_temp, of_i_temp,
                                                                   fit_i_temp,
                                                                   columns_all_data,
                                                                   iteration=iter+1)
            all_data_pop.append(i_pop_solution)

            # New design variables
            if fit_i_temp > fit_pop[pop]:
                report += "    fit_i_temp > fit_pop[pop] - accept this solution\n"
                x_pop[pop] = x_i_temp.copy()
                of_pop[pop] = of_i_temp
                fit_pop[pop] = fit_i_temp
            else:
                report += "    fit_i_temp < fit_pop[pop] - not accept this solution\n"

            # Update neof (Number of Objective Function Evaluations)
            neof_count += neof

        # Best, average and worst values and storage
        repetition_data, best_id = metapyco.resume_process_in_dataframe(x_pop, of_pop, fit_pop,
                                                                columns_repetition_data,
                                                                columns_worst_data,
                                                                columns_other_data,
                                                                neof_count,
                                                                iteration=iter+1)
        resume_result.append(repetition_data)
        report += "update solutions\n"
        for i_pop in range(n_population):
            if i_pop == best_id:
                report += f'x{i_pop} = {x_pop[i_pop]} - best solution\n'
            else:
                report += f'x{i_pop} = {x_pop[i_pop]} \n'

        # Time markup
        end_time = time.time()
        delta_time = end_time - initial_time

    # Storage all values in DataFrame
    df_all = pd.concat(all_data_pop, ignore_index=True)

    # Storage best values in DataFrame
    df_best = pd.concat(resume_result, ignore_index=True)

    return df_all, df_best, delta_time, report
