# import os
# os.system('!pip install pyomo > /etc/null')

# !pip install pyomo > /etc/null #ส่งผลไปยัง null ทำให้ไม่แสดงข้อความ
# !apt-get install -y -qq coinor-cbc > /etc/null

import pyomo.environ as pyo
# import gurobipy

model = pyo.ConcreteModel()

model.x = pyo.Var([1,2], domain=pyo.NonNegativeReals)

model.OBJ = pyo.Objective(expr = 2*model.x[1] + 3*model.x[2])

model.Constraint1 = pyo.Constraint(expr = 3*model.x[1] + 4*model.x[2] >= 1)

pyo.SolverFactory('glpk').solve(model)

model.write("2.sol")