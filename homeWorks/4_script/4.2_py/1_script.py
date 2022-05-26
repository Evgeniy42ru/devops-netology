#!/usr/bin/env python3

a = 1
b = '2'

#c = a + b
#unsupported operand type(s) for +: 'int' and 'str'
#  File "/Users/Evgeniy/Projects/netology/devops-netology/homeWorks/4_script/4.2_py/1_script.py", line 4, in <module>
#    c = a + b

c3 = a + int(b)
c12 = str(a) + b

print(a, b, c3, c12)
