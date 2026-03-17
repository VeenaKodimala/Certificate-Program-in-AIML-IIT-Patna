import numpy as np
import time

print("----------------------TASK-1----------------------------")
temps_celsius = np.array([22, 25, 28, 24, 26])
print(f"temps_celsius:: {temps_celsius}")

temp_Fahrenheit = np.add(np.multiply(temps_celsius,1.8),32)
print(f"temp_Fahrenheit:: {temp_Fahrenheit}")

print(f"Average temperature in Fahrenheit::{np.average(temp_Fahrenheit)} ")

print("----------------------TASK-2----------------------------")

test_scores = np.array([85, 90, 78, 92, 88, 76, 95, 82, 89, 91, 87, 84])
print(f"Shape of test_scores:: {np.shape(test_scores)}")
print(f"Highest score: {np.max(test_scores)}")
print(f"Lowest score: {np.min(test_scores)}")
print(f"Range: {np.max(test_scores)-np.min(test_scores)}")

print("----------------------TASK-3----------------------------")

numpyArr = np.arange(1, 50001)
pythonList = list(range(1, 50001))

start = time.time()
print(f"NumPy sum: {np.sum(numpyArr)}")
numpyTime = time.time()-start

start = time.time()
print(f"Python sum: {sum(pythonList)}")
pythonTime = time.time()-start

print(f"NumPy time: {numpyTime :.4f} seconds")
print(f"Python time: {pythonTime :.4f} seconds")
print(f"NumPy is {pythonTime/numpyTime:.4f} x faster")
