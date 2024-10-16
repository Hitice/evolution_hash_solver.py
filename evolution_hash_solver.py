import math
import random
from multiprocessing import Pool, cpu_count
from tqdm import tqdm

def baby_step_giant_step(base, target, prime):
    """
    Solves the discrete logarithm problem using the Baby-Step Giant-Step method.
    Finds `x` such that base^x ≡ target (mod prime).

    :param base: The base of the logarithm (g in g^x mod p).
    :param target: The result of the logarithm (h in g^x ≡ h mod p).
    :param prime: The prime modulus.
    :return: The value of x or -1 if not found.
    """
    m = math.isqrt(prime) + 1  # Size of the baby steps
    baby_steps = {}

    # Baby step: Calculate and store base^j mod prime for j = 0, 1, ..., m-1
    baby_step = 1
    for j in range(m):
        baby_steps[baby_step] = j
        baby_step = (baby_step * base) % prime

    # Giant step: Check if any base^(m * i) * target mod prime is in baby_steps
    inv_base_m = pow(base, prime - m - 1, prime)  # base^(-m) mod prime
    giant_step = target
    for i in range(m):
        if giant_step in baby_steps:
            return i * m + baby_steps[giant_step]
        giant_step = (giant_step * inv_base_m) % prime

    return -1

def pollards_rho(base, target, prime):
    """
    Pollard's Rho algorithm for solving the discrete logarithm problem.
    Finds `x` such that base^x ≡ target (mod prime).

    :param base: The base of the logarithm (g in g^x mod p).
    :param target: The result of the logarithm (h in g^x ≡ h mod p).
    :param prime: The prime modulus.
    :return: The value of x or -1 if not found.
    """
    def f(x, a, b):
        if x % 3 == 0:
            return (x * x % prime, a * 2 % (prime - 1), b * 2 % (prime - 1))
        elif x % 3 == 1:
            return (x * base % prime, (a + 1) % (prime - 1), b)
        else:
            return (x * target % prime, a, (b + 1) % (prime - 1))

    x, a, b = 1, 0, 0
    X, A, B = x, a, b
    for _ in range(prime):
        x, a, b = f(x, a, b)
        X, A, B = f(*f(X, A, B))

        if x == X:
            r = (b - B) % (prime - 1)
            if r == 0:
                return -1
            return (A - a) * pow(r, prime - 2, prime - 1) % (prime - 1)

    return -1

def solve_discrete_log(base, target, prime, method="baby-step"):
    """
    Attempts to solve the discrete logarithm problem using different methods.

    :param base: The base of the logarithm (g in g^x mod p).
    :param target: The result of the logarithm (h in g^x ≡ h mod p).
    :param prime: The prime modulus.
    :param method: The method to use: 'baby-step' or 'pollard'.
    :return: The value of x or -1 if not found.
    """
    if method == "baby-step":
        return baby_step_giant_step(base, target, prime)
    elif method == "pollard":
        return pollards_rho(base, target, prime)
    else:
        raise ValueError("Unsupported method: Choose 'baby-step' or 'pollard'.")

def main():
    """
    Main program to solve the discrete logarithm problem.
    Asks for user input for the base, target, and prime.
    """
    base = int(input("Enter the base (g in g^x mod p): "))
    target = int(input("Enter the target (h in g^x ≡ h mod p): "))
    prime = int(input("Enter the prime modulus (p): "))

    method = input("Choose a method ('baby-step' or 'pollard'): ").strip().lower()

    print(f"Solving the discrete log problem for base={base}, target={target}, prime={prime} using {method} method...")
    
    x = solve_discrete_log(base, target, prime, method=method)

    if x != -1:
        print(f"Solution found: x = {x}")
    else:
        print("No solution found.")

if __name__ == "__main__":
    main()
