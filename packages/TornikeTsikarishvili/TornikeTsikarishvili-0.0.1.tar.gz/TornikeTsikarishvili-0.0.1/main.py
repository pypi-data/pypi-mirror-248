#1
import os
print(os.getcwd())

#2
import numpy as np

ki=np.array([[1,2,3],[141,4124,12],[3,31,31]])
if [0,0,0] not in ki:
    print(f'{[0,0,0]} araa matricashi')
else:
    print(f'{0,0,0} ari matrica')


#3
try:
    import opps
except ImportError:
    print('arasworad gaq sheyvanili failis saxeli')

#4
from math_operations import add, subtract
result_add = add(5, 3)
print("Addition result:", result_add)
result_subtract = subtract(10, 4)
print("Subtraction result:", result_subtract)

#5
from math import sqrt
print(sqrt(25))

#6 გამოიყენება 4 სფეისი.
class MyClass:
    def my_method(self):
        if condition:
            do_something()
        else:
            do_something_else()

#7 არ არსებობს ლიმიტი კოდისთვის.

#8
# main.py
from math_operations_1 import MathOperations, module_function, module_variable

# Function call
result_add = MathOperations.add(5, 3)
print("Function call - Addition result:", result_add)

# Class call
math_instance = MathOperations()
result_subtract = math_instance.subtract(10, 4)
print("Class call - Subtraction result:", result_subtract)

# Variable call
print("Variable call -", module_variable)

# Function call
result_function = module_function()
print("Function call -", result_function)
