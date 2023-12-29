"""Module has as functions about all metaheuristics algorithms"""
import numpy as np
import pandas as pd


def initial_population_01(n_population, n_dimensions, x_lower, x_upper, seed=None):
    """  
    Generates a random population with defined limits. 
    Continuum variables generator.

    See documentation in https://wmpjrufg.github.io/METAPY/FRA_CO_.html
    
    Args:
        n_population (int): Number of population.
        n_dimensions (int): Problem dimension.
        x_lower (list): Lower limit of the design variables.
        x_upper (list): Upper limit of the design variables.
        seed (int or None): Random seed. Default is None.
    
    Returns:
        x_pop (list): Population design variables.
    """

    # Set random seed
    if seed is None:
        pass
    else:
        np.random.seed(seed)

    # Random variable generator
    x_pop = []
    for _ in range(n_population):
        aux = []
        for j in range(n_dimensions):
            random_number = np.random.random()
            value_i_dimension = x_lower[j] + (x_upper[j] - x_lower[j]) * random_number
            aux.append(value_i_dimension)
        x_pop.append(aux)

    return x_pop


def initial_population_02(n_population, n_dimensions, seed=None):
    """  
    The function generates a random population.
    Combinatorial variables generator.

    See documentation in https://wmpjrufg.github.io/METAPY/FRA_CO_.html
    
    Args:
        n_population (int): Number of population.
        n_dimensions (int): Problem dimension.
        seed (int or None): Random seed. Default is None.
    
    Returns:
        x_pop (list): Population design variables.
    """

    # Set random seed
    if seed is None:
        pass
    else:
        np.random.seed(seed)

    # Random variable generator
    nodes = list(range(n_dimensions))
    x_pop = [list(np.random.permutation(nodes)) for _ in range(n_population)]

    return x_pop


def initial_pops(n_repetitions, n_population, n_dimensions, x_lower, x_upper, type_pop, seeds):
    """
    This function randomly initializes a population of the metaheuristic algorithm
    for a given number of repetitions.

    See documentation in https://wmpjrufg.github.io/METAPY/FRA_CO_.html
    
    Args:
        n_repetitions (int): Number of repetitions.
        n_population (int): Number of population.
        n_dimensions (int): Problem dimension.
        x_lower (list or None): Lower limit of the design variables. Use None for combinatorial variables.
        x_upper (list or None): Upper limit of the design variables. Use None for combinatorial variables.
        type_pop (str): Type of population. Options: 'real code' or 'combinatorial code'.
        seeds (list or None): Random seed. Use None for random seed.
    
    Returns:
        population (list): Population design variables. All repetitions.
    """

    # Set random seed
    population = []
    # Random variable generator
    if type_pop.upper() == 'REAL CODE':
        for i in range(n_repetitions):
            if seeds[i] is None:
                population.append(initial_population_01(n_population, n_dimensions,
                                                        x_lower, x_upper))
            else:
                population.append(initial_population_01(n_population, n_dimensions,
                                                        x_lower, x_upper,
                                                        seed=seeds[i]))
    elif type_pop.upper() == 'COMBINATORIAL CODE':
        for i in range(n_repetitions):
            if seeds[i] is None:
                population.append(initial_population_02(n_population, n_dimensions))
            else:
                population.append(initial_population_02(n_population, n_dimensions,
                                                        seed=seeds[i]))  

    return population


def fit_value(of_i_value):
    """ 
    This function calculates the fitness of the i agent.

    See documentation in https://wmpjrufg.github.io/METAPY/FRA_CO_.html
    
    Args:
        of_i_value (float): Object function value of the i agent.
    
    Returns:
        fit_i_value (float): Fitness value of the i agent.
    """

    # Positive or zero OF value
    if of_i_value >= 0:
        fit_i_value = 1 / (1 + of_i_value)
    # Negative OF value
    elif of_i_value < 0:
        fit_i_value = 1 + abs(of_i_value)

    return fit_i_value


def check_interval_01(x_i_old, x_lower, x_upper):
    """
    This function checks if a design variable is out of the limits 
    established x_lower, x_upper and updates the variable if necessary.

    See documentation in https://wmpjrufg.github.io/METAPY/FRA_CO_.html
    
    Args:
        x_i_old (list): Current design variables of the i agent.
        x_lower (list): Lower limit of the design variables.
        x_upper (list): Upper limit of the design variables.
    
    Returns:
        x_i_new (list): Update variables of the i agent.
    """

    x_i_new = list(np.clip(x_i_old, x_lower, x_upper))

    return x_i_new


def best_values(x_pop, of_pop, fit_pop):
    """ 
    This function determines the best, best id, worst particle and worst id. 
    It also determines the average value (OF and FIT) of the population.

    See documentation in https://wmpjrufg.github.io/METAPY/FRA_CO_.html
    
    Args:
        x_pop (list): Population design variables.
        of_pop (list): Population objective function values.
        fit_pop (list): Population fitness values.
        
    Returns:
        best_id (int): Best id in population.
        worst_id (int): Worst id in population.
        x_best (list): Best design variables in population.
        x_worst (list): Worst design variables in population.
        of_best (float): Best objective function value in population.
        of_worst (float): Worst objective function value in population.
        fit_best (float): Best fitness value in population.
        fit_worst (float): Worst fitness value in population.
        of_avg (float): Average objective function value.
        fit_avg (float): Average fitness value.
    """

    # Best and worst ID in population
    best_id = of_pop.index(min(of_pop))
    worst_id = of_pop.index(max(of_pop))

    # Global best values
    x_best = x_pop[best_id].copy()
    of_best = of_pop[best_id]
    fit_best = fit_pop[best_id]

    # Global worst values
    x_worst = x_pop[worst_id].copy()
    of_worst = of_pop[worst_id]
    fit_worst = fit_pop[worst_id]

    # Average values
    of_avg = sum(of_pop) / len(of_pop)
    fit_avg = sum(fit_pop) / len(fit_pop)

    return best_id, worst_id, x_best, x_worst, of_best, of_worst, \
            fit_best, fit_worst, of_avg, fit_avg


def mutation_01_movement(obj_function, x_i_old, x_lower, x_upper,
                         n_dimensions, pdf, sigma, report = "",
                         none_variable=None):
    """ 
    This function mutates a solution using a Gaussian or Uniform distribution.
    
    See documentation in https://wmpjrufg.github.io/METAPY/COMMON.html
    
    Args:
        obj_function (function): Objective function. The Metapy user defined this function.
        x_i_old (list): Current design variables of the i agent.
        x_lower (list): Lower limit of the design variables.
        x_upper (list): Upper limit of the design variables.
        n_dimensions (int): Problem dimension.
        pdf (str): Probability density function. Options: 'gaussian' or 'uniform'.
        sigma (float): Control parameter for the Gaussian or Uniform 
                       distribution in percentage. In Gaussian or Uniform
                       distribution, sigma equivalent to a standard deviation.
        report (str): Report about the mutation process. Default is "".
        none_variable (Object or None): None variable. Default is None. Use in objective function.
    
    Returns:
        x_i_new (list): Update variables of the i agent.
        of_i_new (float): Update objective function value of the i agent.
        fit_i_new (float): Update fitness value of the i agent.
        neof (int): Number of evaluations of the objective function.
        report (str): Report about the mutation process.
    """

    # Start internal variables
    x_i_new = []
    of_i_new = 0
    fit_i_new = 0

    # Particle movement - Gaussian distribution or Uniform distribution
    report += "    Particle movement\n"
    for i in range(n_dimensions):
        mean_value = x_i_old[i]
        sigma_value = abs(mean_value * sigma / 100)
        if pdf.upper() == 'GAUSSIAN' or pdf.upper() == 'NORMAL':
            neighbor = np.random.normal(mean_value, sigma_value, 1)
        elif pdf.upper() == 'UNIFORM':
            neighbor = np.random.uniform(mean_value - sigma_value, mean_value + sigma_value, 1)
        x_i_new.append(neighbor[0])
        report += f"    Dimension {i}: mean = {mean_value}, sigma = {sigma_value} "
        report += f"neighbor = {neighbor[0]}\n"

    # Check bounds
    x_i_new = check_interval_01(x_i_new, x_lower, x_upper)

    # Evaluation of the objective function and fitness
    of_i_new = obj_function(x_i_new, none_variable)
    fit_i_new = fit_value(of_i_new)
    report += f"    update x = {x_i_new}, of = {of_i_new}, fit = {fit_i_new}\n"   
    neof = 1

    return x_i_new, of_i_new, fit_i_new, neof, report


def resume_all_data_in_dataframe(x_i_pop, of_i_pop, fit_i_pop, columns, iteration):
    """
    This function creates a dataframme with all values of the population.
    
    Args:
        x_i_pop (list): Design variables of the i agent.
        of_i_pop (float): Objective function value of the i agent.
        fit_i_pop (float): Fitness value of the i agent.
        columns (list): Columns names about dataset results.
        iteration (int): Current iteration number.
    
    Returns:
        i_pop_data (dataframe): Dataframe with all values of the i agent in j iteration.
    """

    # Dataframe creation
    aux = x_i_pop.copy()
    aux.append(of_i_pop)
    aux.append(fit_i_pop)
    aux.append(iteration)
    solution_list = [aux]
    i_pop_data = pd.DataFrame(solution_list, columns=columns)

    return i_pop_data


def resume_process_in_dataframe(x_pop, of_pop, fit_pop, column_best, column_worst,
                                other_columns, neof_count, iteration):
    """
    This function creates a dataframe with the best, worst and average values of 
    the population.
    
    Args:
        x_pop (list): Population design variables.
        of_pop (list): Population objective function values.
        fit_pop (list): Population fitness values.
        column_best (list): Columns names about dataset results.
        column_worst (list): Columns names about dataset results.
        other_columns (list): Columns names about dataset results.
        neof_count (int): Number of evaluations of the objective function.
        iteration (int): Current iteration number.
    
    Returns:
        data_resume (dataframe): Dataframe with the best, worst and average 
        values of in j iteration. 
        best_id (int): Best id in population.
    """

    # Best, average and worst values
    best_id, worst_id, x_best, x_worst, of_best, of_worst, fit_best, \
    fit_worst, of_avg, fit_avg = best_values(x_pop, of_pop, fit_pop)

    # Dataframe creation
    aux = x_best.copy()
    aux.append(of_best)
    aux.append(fit_best)
    aux.append(best_id)
    best_solution = pd.DataFrame([aux], columns = column_best)
    aux = x_worst.copy()
    aux.append(of_worst)
    aux.append(fit_worst)
    aux.append(worst_id)
    worst_solution = pd.DataFrame([aux], columns = column_worst)
    avg_solution = pd.DataFrame([[of_avg, fit_avg, iteration, neof_count]], columns = other_columns)
    data_resume = pd.concat([best_solution, worst_solution, avg_solution], axis = 1)

    return data_resume, best_id

def summary_analysis(df_best_results):
    """
    This function searches for the best result in result list.

    Args:
        df_best_results (list): List with the best results of each repetition.
    
    Returns:
        id_min_of (int): Best result id.
    """
    
    min_of = float('inf')
    id_min_of = None
    for index, df in enumerate(df_best_results):
        last_line = df.iloc[-1]
        min_of_atual = last_line['OF BEST']
        if min_of_atual < min_of:
            min_of = min_of_atual
            id_min_of = index

    return id_min_of

if __name__ == "__main__":

    # initial_population_01
    # Data
    nPop = 5
    xL = [1, 1, 2]
    xU = [4, 4, 4]
    d = len(xU) # or d = len(xL) or d = 3

    # Call function
    population = initial_population_01(nPop, d, xL, xU)

    # Output details
    print('particle 0: ', population[0])
    print('particle 1: ', population[1])
    print('particle 2: ', population[2])
    print('particle 3: ', population[3])
    print('particle 4: ', population[4])
    print('\n\n')

    # initial_population_02
    # Data
    nPop = 5
    d = 3

    # Call function
    population = initial_population_02(nPop, d)

    # Output details
    print('particle 0: ', population[0])
    print('particle 1: ', population[1])
    print('particle 2: ', population[2])
    print('particle 3: ', population[3])
    print('particle 4: ', population[4])
    print('\n\n')

    # initial_pops
    # Data
    nRep = 4
    nPop = 2
    d = 3
    xL = [1, 1, 1]
    xU = [3, 3, 3]
    typeCode = 'real code'
    seeds = [None, None, None, None]

    # Call function
    pops = initial_pops(nRep, nPop, d, xL, xU, typeCode, seeds)

    # Output details
    print('population repetition ID = 0: ', pops[0])
    print('population repetition ID = 1: ', pops[1])
    print('population repetition ID = 2: ', pops[2])
    print('population repetition ID = 3: ', pops[3])
    print('\n Agent example:')
    print('init. population rep. ID = 0 - agent id = 0: ', pops[0][0])
    print('init. population rep. ID = 0 - agent id = 1: ', pops[0][1])
    print('\n\n')

    # initial_pops
    # Data
    nRep = 4
    nPop = 2
    d = 3
    xL = [1, 1, 1]
    xU = [3, 3, 3]
    typeCode = 'real code'
    seeds = [10, 11, 10, 11]

    # Call function
    pops = initial_pops(nRep, nPop, d, xL, xU, typeCode, seeds)

    # Output details
    print('population repetition ID = 0: ', pops[0])
    print('population repetition ID = 1: ', pops[1])
    print('population repetition ID = 2: ', pops[2])
    print('population repetition ID = 3: ', pops[3])
    print('\n Agent example:')
    print('init. population rep. ID = 0 - agent id = 0: ', pops[0][0])
    print('init. population rep. ID = 0 - agent id = 1: ', pops[0][1])
    print('\n\n')
    
    # fit_value
    # Data
    ofI = 1

    # Call function
    fitI = fit_value(ofI)
    
    # Output details
    print(f'fit value i agent when OF = {ofI} is ', fitI)
    print('\n\n')

    # check_interval_01
    # Data
    xL = [1, 2, 3]
    xU = [5, 5, 5]
    xI = [6, -1, 2.5]

    # Call function
    xINew = check_interval_01(xI, xL, xU)
    
    # Output details
    print(xINew)
    print('\n\n')

    # best_values
    # Data
    xValues = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    ofValues = [10, 5, 8]
    fitValues = [0.09, 0.17, 0.11]

    # Call function
    bestPos, worstPos, xBest, xWorst, ofBest, ofWorst, fitBest, fitWorst, \
                ofAverage, fitAverage = best_values(xValues, ofValues, fitValues)

    # Output details
    print("Best position in the population:", bestPos)
    print("Worst position in the population:", worstPos)
    print("Best value of X:", xBest)
    print("Worst value of X:", xWorst)
    print("Best OF:", ofBest)
    print("Worst OF:", ofWorst)
    print("Best FIT:", fitBest)
    print("Worst FIT:", fitWorst)
    print("Average OF:", ofAverage)
    print("Average FIT:", fitAverage)
    print('\n\n')

    # mutation_01_movement
    # Data
    xL = [1, 1]
    xU = [5, 5]
    d = len(xL)
    sigma = 15 # 15%
    xI = [2, 2]
    pdf = 'uniform'

    # Objective function
    def obj_function(x, _):
        """Example objective function"""
        x0 = x[0]
        x1 = x[1]
        of = x0 ** 2 + x1 ** 2
        return of

    # Call function
    xII, ofINew, fitINew, neof, report = mutation_01_movement(obj_function, xI, xL, xU,
                                                              d, pdf, sigma)

    # Output details
    print('x New: ', xII)
    print('of New: ', ofINew)
    print('fit New: ', fitINew)
    print('number of evalutions objective function: ', neof)
    print('\n\n')

    # Report details
    arq = "report_example.txt"

    # Escrevendo o relatório no arquivo de texto
    with open(arq, "w") as file:
        file.write(report)
    