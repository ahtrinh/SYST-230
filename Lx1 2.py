'''
Alex Trinh
G01310551
SYST 230
Lab Section 203
'''

import help

numA = float(input("Enter number for a: "))
numB = float(input("Enter number for b: "))
numC = float(input("Enter number for c: "))

positive_quadratic_formula = (((-1*numB)) + (((numB ** 2) - 4*numA*numC) ** 0.5)) / 2 * numA
negative_quadratic_formula = (((-1*numB)) - (((numB ** 2) - 4*numA*numC) ** 0.5)) / 2 * numA

print(f"{positive_quadratic_formula} and {negative_quadratic_formula}")







