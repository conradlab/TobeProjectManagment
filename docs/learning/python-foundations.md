# Python Foundations for Research

This guide covers core Python concepts essential for scientific computing and research software development.

## Overview

Python has become the de facto standard language for scientific research, data analysis, and machine learning. In the Conrad Lab, we use Python for:

- Image processing and computer vision
- Statistical analysis and data manipulation
- Machine learning model development
- Workflow automation and reproducibility scripts
- Scientific visualization

This guide covers the minimum Python knowledge needed to participate effectively in research projects.

## Table of Contents

1. [Environment Setup](#environment-setup)
2. [Core Language Concepts](#core-language-concepts)
3. [Data Structures and Manipulation](#data-structures-and-manipulation)
4. [Functions and Modules](#functions-and-modules)
5. [NumPy and Scientific Computing](#numpy-and-scientific-computing)
6. [File I/O and Data Formats](#file-io-and-data-formats)
7. [Debugging and Testing](#debugging-and-testing)
8. [Recommended Resources](#recommended-resources)

## Environment Setup

### Virtual Environments

A Python virtual environment is an isolated directory containing a specific Python interpreter and set of packages. This prevents conflicts between projects.

```bash
# Create a virtual environment
python3 -m venv myenv

# Activate it
source myenv/bin/activate  # macOS/Linux
# or
myenv\Scripts\activate  # Windows

# Install packages
pip install numpy scipy matplotlib scikit-learn

# Deactivate when done
deactivate
```

**Why this matters:** Different projects need different package versions. Virtual environments keep them separate.

### Package Management with pip

`pip` is Python's package installer. Always use it within a virtual environment:

```bash
pip install package_name==1.2.3      # Specific version
pip install package_name              # Latest version
pip list                              # Show installed packages
pip freeze > requirements.txt         # Save dependencies
pip install -r requirements.txt       # Restore dependencies
```

**Reproducibility:** Always commit `requirements.txt` to version control.

## Core Language Concepts

### Variables and Types

```python
# Integers and floats
count = 10
value = 3.14

# Strings
name = "Tobe"
description = f"This is {name}'s code"  # f-strings (Python 3.6+)

# Lists (ordered, mutable)
measurements = [1.2, 2.3, 3.1]

# Tuples (ordered, immutable)
coordinates = (x, y, z)

# Dictionaries (key-value pairs)
metadata = {"experiment": "SATINN", "date": "2025-01-15"}

# Checking types
type(count)  # <class 'int'>
isinstance(count, int)  # True
```

### Control Flow

```python
# Conditionals
if value > threshold:
    print("Above threshold")
elif value == threshold:
    print("Equal to threshold")
else:
    print("Below threshold")

# Loops
for i in range(10):
    print(i)

for item in measurements:
    print(item)

while condition:
    # Do something
    pass

# Break and continue
for i in range(10):
    if i == 5:
        break  # Exit loop
    if i == 3:
        continue  # Skip to next iteration
```

### Exception Handling

```python
try:
    result = 10 / divisor
except ZeroDivisionError as e:
    print(f"Cannot divide by zero: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
finally:
    # Always runs, good for cleanup
    file.close()
```

## Data Structures and Manipulation

### Lists

```python
# Creating lists
numbers = [1, 2, 3, 4, 5]
empty = []
mixed = [1, "two", 3.0, [4, 5]]

# Indexing (0-based)
first = numbers[0]  # 1
last = numbers[-1]  # 5

# Slicing
subset = numbers[1:4]  # [2, 3, 4]
reverse = numbers[::-1]  # [5, 4, 3, 2, 1]

# Methods
numbers.append(6)
numbers.extend([7, 8])
numbers.remove(3)
numbers.sort()
```

### Dictionaries

```python
# Creating dictionaries
config = {
    "model": "ResNet50",
    "epochs": 100,
    "batch_size": 32
}

# Accessing values
model_name = config["model"]
batch = config.get("batch_size", 16)  # Default if missing

# Adding/updating
config["learning_rate"] = 0.001
config.update({"optimizer": "Adam"})

# Iterating
for key, value in config.items():
    print(f"{key}: {value}")
```

## Functions and Modules

### Defining Functions

```python
def calculate_mean(values):
    """Calculate the mean of a list of values.
    
    Args:
        values: List of numeric values
        
    Returns:
        Float: The arithmetic mean
    """
    if not values:
        return 0
    return sum(values) / len(values)

# Using the function
result = calculate_mean([1, 2, 3, 4, 5])

# Default arguments
def plot_histogram(data, bins=10, title="Histogram"):
    pass

# Returning multiple values
def get_statistics(values):
    return min(values), max(values), calculate_mean(values)

min_val, max_val, mean_val = get_statistics(data)
```

### Modules and Imports

```python
# Importing entire modules
import numpy as np
result = np.array([1, 2, 3])

# Importing specific functions
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y)

# Importing with alias
from matplotlib import pyplot as plt
plt.plot([1, 2, 3])

# Importing all (usually avoid)
from utils import *  # Not recommended; explicitly import what you need
```

### Creating Your Own Module

```python
# mymodule.py
def helper_function(x):
    return x * 2

class DataProcessor:
    def __init__(self, input_path):
        self.input_path = input_path

# main.py
from mymodule import helper_function, DataProcessor
result = helper_function(5)
processor = DataProcessor("data.csv")
```

## NumPy and Scientific Computing

NumPy is the foundation for numerical computing in Python. It provides:

- **Arrays:** Efficient multi-dimensional containers
- **Operations:** Element-wise math, linear algebra, statistics
- **Performance:** C-optimized computations (faster than pure Python)

### Creating and Manipulating Arrays

```python
import numpy as np

# Creating arrays
a = np.array([1, 2, 3])
b = np.zeros((3, 3))  # 3x3 matrix of zeros
c = np.ones((2, 4))   # 2x4 matrix of ones
d = np.arange(10)     # [0, 1, 2, ..., 9]
e = np.linspace(0, 1, 11)  # 11 evenly spaced values from 0 to 1

# Shape and size
matrix = np.array([[1, 2, 3], [4, 5, 6]])
print(matrix.shape)  # (2, 3)
print(matrix.size)   # 6

# Data types
int_array = np.array([1, 2, 3], dtype=np.int32)
float_array = np.array([1, 2, 3], dtype=np.float32)
```

### Element-wise Operations

```python
a = np.array([1, 2, 3])
b = np.array([4, 5, 6])

# Arithmetic
c = a + b          # [5, 7, 9]
d = a * b          # [4, 10, 18]
e = np.sqrt(a)     # [1, 1.414, 1.732]

# Broadcasting (automatic expansion)
f = a + 10         # [11, 12, 13]
```

### Statistical Functions

```python
data = np.array([1, 2, 3, 4, 5])

mean = np.mean(data)
std = np.std(data)
maximum = np.max(data)
percentile = np.percentile(data, 75)
```

## File I/O and Data Formats

### Reading and Writing Text Files

```python
# Writing
with open("results.txt", "w") as f:
    f.write("Result 1: 42\n")
    f.write("Result 2: 3.14\n")

# Reading
with open("results.txt", "r") as f:
    content = f.read()  # Entire file
    # or
    lines = f.readlines()  # List of lines

# Processing line-by-line
with open("data.txt", "r") as f:
    for line in f:
        print(line.strip())
```

### CSV Files

```python
import csv

# Writing CSV
data = [["Name", "Score"], ["Alice", 95], ["Bob", 87]]
with open("scores.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerows(data)

# Reading CSV
with open("scores.csv", "r") as f:
    reader = csv.DictReader(f)  # Read as dictionaries
    for row in reader:
        print(row["Name"], row["Score"])
```

### JSON Files

```python
import json

# Writing
data = {"name": "Tobe", "experiment": "SATINN", "status": "active"}
with open("metadata.json", "w") as f:
    json.dump(data, f, indent=2)

# Reading
with open("metadata.json", "r") as f:
    loaded = json.load(f)
```

### Images and NumPy Arrays

```python
from PIL import Image
import numpy as np

# Loading an image
img = Image.open("sample.png")
array = np.array(img)  # Convert to NumPy array

# Processing
processed = array * 0.5  # Darken image
result_img = Image.fromarray(processed)
result_img.save("output.png")
```

## Debugging and Testing

### Print Debugging

```python
value = 42
print(f"Value is {value}")
print(f"Type: {type(value)}, Shape: {np.array(value).shape}")
```

### Using the Python Debugger

```python
import pdb

def my_function(x):
    pdb.set_trace()  # Execution pauses here
    result = x * 2
    return result
```

In the debugger:
- `l` (list) - Show code around current line
- `n` (next) - Execute next line
- `c` (continue) - Resume execution
- `p variable` - Print variable value
- `q` (quit) - Exit debugger

### Unit Testing

```python
import unittest

class TestMeanCalculation(unittest.TestCase):
    def test_mean_of_normal_list(self):
        result = calculate_mean([1, 2, 3, 4, 5])
        self.assertAlmostEqual(result, 3.0)
    
    def test_mean_of_empty_list(self):
        result = calculate_mean([])
        self.assertEqual(result, 0)
    
    def test_mean_with_floats(self):
        result = calculate_mean([1.5, 2.5, 3.5])
        self.assertAlmostEqual(result, 2.5)

if __name__ == "__main__":
    unittest.main()
```

Run tests:
```bash
python -m unittest test_module.py
```

## Recommended Resources

### Official Documentation
- Python Official Tutorial: https://docs.python.org/3/tutorial/
- NumPy Documentation: https://numpy.org/doc/
- SciPy Tutorial: https://docs.scipy.org/doc/scipy/tutorial/

### Online Learning
- Real Python: https://realpython.com/
- Python Data Science Handbook: https://jakevdp.github.io/PythonDataScienceHandbook/

### Books
- "Fluent Python" by Luciano Ramalho (advanced)
- "Python for Data Analysis" by Wes McKinney (pandas, data science)

## Next Steps

Once you're comfortable with these foundations, explore:

1. **Pandas** - Data manipulation and analysis
2. **Matplotlib/Seaborn** - Data visualization
3. **Scikit-learn** - Machine learning
4. **TensorFlow/PyTorch** - Deep learning

In the Conrad Lab curriculum, these topics are covered starting in Week 4.
