import random
import sys
import math
from multiprocessing import Pool, cpu_count
from tqdm import tqdm

def generate_hash(input, formula_index):
    """
    Generate a hash using non-conventional mathematical formulas.
    Different formulas are applied based on the formula_index.
    
    :param input: Integer value to hash.
    :param formula_index: Index to select the mathematical formula.
    :return: The calculated hash value.
    """
    if formula_index == 0:
        hash_value = ((input * 123456789) ^ 987654321) % (1 << 32)
    elif formula_index == 1:
        hash_value = (pow(input, 5, 2**32) * 2654435761) % (1 << 32)
    elif formula_index == 2:
        hash_value = (math.sin(input) * 2**31) % (1 << 32)
    elif formula_index == 3:
        base = random.randint(1, 1000)
        giant_step = 2**16
        baby_step = int(math.sqrt(giant_step))
        baby_steps = {}
        for j in range(baby_step):
            baby_steps[(base * pow(2, j, giant_step)) % giant_step] = j
        for i in range(giant_step):
            rhs = (input * pow(base, i, giant_step)) % giant_step
            if rhs in baby_steps:
                x = i * baby_step + baby_steps[rhs]
                hash_value = x
                break
        else:
            hash_value = -1
    elif formula_index == 4:
        def pollards_rho(n):
            x = random.randint(1, n-1)
            y = x
            c = random.randint(1, n-1)
            g = 1
            while g == 1:
                x = (pow(x, 2, n) + c) % n
                y = (pow(y, 2, n) + c) % n
                y = (pow(y, 2, n) + c) % n
                g = math.gcd(abs(x - y), n)
            return g
        hash_value = pollards_rho(input)
    else:
        raise ValueError("Unsupported formula index.")
    
    return hash_value

def evaluate_formula(formula, target):
    """
    Apply a formula to the input and calculate the resulting hash.
    
    :param formula: Tuple containing (input, formula_index)
    :param target: The target hash we want to match.
    :return: True if the formula generates the target hash.
    """
    hash_value = generate_hash(formula[0], formula[1])
    return hash_value == target

def evaluate_population(population, target_hash):
    """
    Evaluate all formulas in the population and return the formula that matches the target hash.
    
    :param population: A list of formulas.
    :param target_hash: The target hash to match.
    :return: The formula that matches the target hash or None if not found.
    """
    for formula in population:
        if evaluate_formula(formula, target_hash):
            return formula
    return None

def main(target_hash):
    """
    Main function to evolve formulas and find the one that produces the target hash.
    
    :param target_hash: The hash that the program is trying to find.
    """
    population_size = 1000
    max_generations = 2000000
    min_value = 0
    max_value = (1 << 32) - 1
    
    population = [(random.randint(min_value, max_value), random.randint(0, 4)) for _ in range(population_size)]
    
    found = False
    generation = 0
    
    progress_bar = tqdm(total=max_generations, desc='Progress', file=sys.stdout, unit=' iterations')
    
    while not found and generation < max_generations:
        num_cpus = cpu_count()
        chunk_size = len(population) // num_cpus
        population_chunks = [population[i:i + chunk_size] for i in range(0, len(population), chunk_size)]
        
        with Pool(processes=num_cpus) as pool:
            results = pool.map(evaluate_population_wrapper, [(chunk, target_hash) for chunk in population_chunks])
        
        for result in results:
            if result is not None:
                print(f"Found formula that produces the hash {target_hash}: {result}")
                found = True
                break
        
        progress_bar.update(1)
        
        if found:
            break
        
        new_population = []
        for formula in population:
            mutated_formula = (formula[0] + random.randint(-1000000, 1000000), formula[1])
            new_population.append(mutated_formula)
        
        population = new_population
        generation += 1
    
    progress_bar.close()
    
    if not found:
        print(f"Failed to find a formula that produces the hash {target_hash} after {max_generations} generations.")

def evaluate_population_wrapper(args):
    """
    Wrapper function to evaluate the population in parallel.
    
    :param args: Tuple containing (population_chunk, target_hash)
    :return: The formula if found, otherwise None.
    """
    population_chunk, target_hash = args
    return evaluate_population(population_chunk, target_hash)

if __name__ == "__main__":
    target_hash = int(input("Enter the target hash (number between 0 and 4294967295): "))
    main(target_hash)
