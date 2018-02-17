import math as math

def fact(pr_n):
    if pr_n <= 4: raise AssertionError("N < 5")
    if pr_n == 5: return 120
    return pr_n * fact(pr_n-1)



try:
    print(fact(7))
except:
    print("Error en factorial")
finally:
    print("Ultima cosa que se hace")