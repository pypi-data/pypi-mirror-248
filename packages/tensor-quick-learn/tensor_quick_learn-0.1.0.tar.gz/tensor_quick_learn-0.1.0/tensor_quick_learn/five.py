import inspect
def func():

    '''
    import numpy as np
import csv
import pandas as pd
from pgmpy.models import BayesianModel
from pgmpy.estimators import MaximumLikelihoodEstimator
from pgmpy.inference import VariableElimination

heartDisease = pd.read_csv('heart.csv')
heartDisease = heartDisease.replace('?',np.nan)
Model=BayesianModel([('age','trestbps'),('age','fbs'),('sex','trestbps'),('exang','trestbps'),
                     ('trestbps','target'),('fbs','target'),('target','restecg'),
                     ('target','thalach'),('target','chol')])
print('\n Learning CPD using Maximum likelihood estimators')
Model.fit(heartDisease,estimator = MaximumLikelihoodEstimator)
print('\n Inferencing with Bayesian Network:')
HeartDisease_infer = VariableElimination(Model)

print('\n 1. Probability of HeartDisease given Age=52')
q1 = HeartDisease_infer.query(variables=['target'],evidence={'age':52})
print(q1)

print('\n 2. Probability of HeartDisease given cholesterol=149')
q2 = HeartDisease_infer.query(variables=['target'],evidence={'chol':149})
print(q2)
   '''
   
def px():
    code=inspect.getsource(func)
    print(code)

