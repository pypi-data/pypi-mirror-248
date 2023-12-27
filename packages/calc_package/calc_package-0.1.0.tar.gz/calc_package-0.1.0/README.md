
# Mycounter

The project basically works as a calculator's principle. It can do addition, subtraction, multiplication, division as well as take a root with selected level(y). It has it's own memory and function to reset memory to 0.



## Functions:
- add(x, y) - addition of two numbers (x, y);
- sub(x, y) - subtraction of two numbers (x, y);
- mul(x, y) - multiplication of two numbers (x, y);
- div(x, y) - division of two numbers (x, y);
- roo(x, y) - root with selected level(y) of number x;
- memory() - returns last calculated number;
- reset() - resets number to 0.


## Installation

Install "mycounter" project using pip install:

```bash
  !pip install git+https://github.com/ShariYo/mycounter.git
```
    
## Usage/Examples

```python
import mycounter from Calculator

a = Calculator().add(2, 2)
print(a)
>>> 4
b = Calculator().sub(3, 2)
print(b)
>>> 1
c = Calculator().mul(5, 2)
print(c)
>>> 10
d = Calculator().div(8, 2)
print(d)
>>> 4
e = Calculator().roo(25, 2)
print(e)
>>> 5
a = Calculator().add(2, 2)
mem = Calculator.memory
print(mem)
>>> 4
res = Calculator().reset
print(res)
>>> 0
```

