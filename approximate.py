import mip
import re
import json
from flask import Flask, render_template, url_for, request, redirect

# app = Flask(__name__)


class Solver:
    
    def __init__(self
                ,components
                ,target
                ,series
                ,tolerance
                ,resistor):
        
        self.components = components
        self.target = target
        self.series = series
        self.tolerance = tolerance
        self.resistor = resistor


    def equivalent_tol(self):
        """Return list of components which in series/parallel are within tolerance
         of the target value, minimising the number of components in use.
        Args:
            components: float values of the resistors/capacitors to choose from. A component
                value can be used as many times as it occurs in this list.
            target: The target value.
            series: True for series, false for parallel.
            tol: Solved resistance will be in range [(1-tol)*target, (1+tol)*target, %
            resistor: True for resistors and inductors, False for capacitors
        Returns:
            Optimal component values, or empty list if no solution.
        """
        
        tol = self.tolerance/100
        
        # This is what sets the different parallel and series combination 
        # depending on the component type. Reasoning = Boolean algebra.
        condition = (not self.resistor and not self.series) or (self.series and self.resistor)
        _target = self.target if condition else 1/self.target
        _components = self.components if condition else [1/x for x in self.components]
        lower = (1-tol) * self.target if condition else 1/((1+tol) * self.target)
        upper = (1+tol) * self.target if condition else 1/((1-tol) * self.target)
    
        m = mip.Model()  # Create new mixed integer/linear model.
    
        r_in_use = [m.add_var(var_type=mip.BINARY) for _ in _components]
        opt_r = sum([b * r for b, r in zip(r_in_use, _components)])  
        m += opt_r >= lower
        m += opt_r <= upper
    
        m.objective = mip.minimize(mip.xsum(r_in_use))
        m.verbose = False  
        sol_status = m.optimize()
        if sol_status != mip.OptimizationStatus.OPTIMAL:
            print('No solution found')
            return []
    
        r_in_use_sol = [float(v) for v in r_in_use]
        r_to_use = [r for r, i in zip(self.components, r_in_use_sol) if i > 0]
        
        solved_values = sum(x for x in r_to_use) if condition else 1/sum(1/x for x in r_to_use)
        solved_error = 100 * (solved_values - self.target) / self.target
            
        print(f'{"Resistors/Inductors" if self.resistor else "Capacitors"}; {r_to_use} in {"series" if self.series else "parallel"} '
              
              f'will produce {"resistance/inductance" if self.resistor else "capacitance"} = {solved_values:.3f}'\
              f' {"R/I" if self.resistor else "C"}. Aiming for {"R/I" if self.resistor else "C"} = {self.target:.3f}, '
              
              f'error of {solved_error:.2f}%')
        return r_to_use
    
    @staticmethod
    def list_process(list_r):
        """
        Turns a list of strings with SI unit multipliers and number multilpiers into a list of floats.
        For example will turn ["5kx5"] into [5000.0 for i in range(5)]
        Idea behind this is that user input can be accepted as strings and the two multipliers will save them time given components
        usually come 5's or 10's in most packages and the equivalent tol function works assuming there is the same number of inputs at specified. 
        
        """
        replace_dict = {'a': '1e-18', 'f': '1e-15', 'p': '1e-12',
                    'n': '1e-9',  'u': '1e-6',  'm': '1e-3',
                    'c': '1e-2',  'd': '1e-1', 'da': '1e1',
                    'h': '1e2',   'k': '1e3',   'M': '1e6',
                    'G': '1e9',   'T': '1e12',  "P": '1e15',
                    'E': '1e18'}
        
        regex = re.compile(r"([0-9]+\.?[0-9]*)([^x]+)(x[0-9]+)?")
        regex_nox = re.compile(r"([0-9]+\.?[\d]*)([^\d]*)")
        list_numbers = []
        for item in list_r:
            if type(item) != str:
                list_numbers.append(float(item))
                continue
            if 'x' in item:
                parsed = re.findall(regex, item)[0]
                n = 1 if parsed[2] == '' else int(parsed[2].replace('x', ''))
                list_numbers += [float(parsed[0]) * eval(replace_dict[parsed[1]])] * n 
            else:
                parsed = re.findall(regex_nox, item)[0]
                n = 1 if parsed[1] == '' else eval(replace_dict[parsed[1]])
                list_numbers += [n*float(parsed[0])] 
                
        return list_numbers
    
    def minimize(self):
        self.components = self.list_process(self.components)
        self.equivalent_tol()
        
# @app.route("/<data>",methods = ['GET','POST'])
# def root(data):
#     res = request.json
#     print(res)
#     return 'Hello BITCH'

    
    
if __name__ == "__main__":
          
    # app.run()
    a = Solver([1, '2kx5', 3, 4, 5, 6, 7], 11, True, 10,True)
    a.minimize()
    
    # Run this code block to test.
    
    # processed_list = list_process(["1kx5",2000,'1'])
    
    # print()
    # sol = equivalent_tol(processed_list, 5000, True, 10,True)
    # print()
    # # sol = equivalent_tol([1, 2, 3, 4, 5, 6, 7], 11, True, 10,True)
    # # print()
    # # sol = equivalent_tol([1, 2, 3, 4, 5, 6, 7], 11, False, 10,False)
    
    
    
    