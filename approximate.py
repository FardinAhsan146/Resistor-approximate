
import mip
from typing import List
import re
import pandas as pd


def equivalent_tol(components: List[float], target: float, series: bool, tolerance: float, resistor: bool) -> List[float]:
    """Return list of components which in series/parallel are within tolerance
     of the target value, minimising the number of components in use.

    Args:
        components: float values of the resistors/capacitors to choose from. A resistor
            value can be used as many times as it occurs in this list.
        target: The target value.
        series: True for series, false for parallel.
        tol: Solved resistance will be in range [(1-tol)*target, (1+tol)*target, %
        resistor: True for resistors and inductors, False for capacitors

    Returns:
        Optimal component values, or empty list if no solution.
    """
    
    tol = tolerance/100
    
    if resistor:
        
        _target = target if series else 1/target
        _components = components if series else [1/x for x in components]
        lower = (1-tol) * target if series else 1/((1+tol) * target)
        upper = (1+tol) * target if series else 1/((1-tol) * target)
        
    else:
        
        _target = target if not series else 1/target
        _components = components if not series else [1/x for x in components]
        lower = (1-tol) * target if not series else 1/((1+tol) * target)
        upper = (1+tol) * target if not series else 1/((1-tol) * target)
               
    m = mip.Model()  # Create new mixed integer/linear model.


    r_in_use = [m.add_var(var_type=mip.BINARY) for _ in _components]
    opt_r = sum([b * r for b, r in zip(r_in_use, _components)])  
    m += opt_r >= lower
    m += opt_r <= upper


    m.objective = mip.minimize(mip.xsum(r_in_use))
    m.verbose = False  
    sol_status = m.optimize()
    if sol_status != mip.OptimizationStatus.OPTIMAL:
        print(f'No solution found')
        return []


    r_in_use_sol = [float(v) for v in r_in_use]


    r_to_use = [r for r, i in zip(components, r_in_use_sol) if i > 0]
    
    if resistor:
        solved_values = sum(x for x in r_to_use) if series\
            else 1/sum(1/x for x in r_to_use)
        solved_error = 100 * (solved_values - target) / target
        
    else:
        solved_values = sum(x for x in r_to_use) if not series\
            else 1/sum(1/x for x in r_to_use)
        solved_error = 100 * (solved_values - target) / target
        
    
    print(f'{"Resistors" if resistor else "Capacitors"} {r_to_use} in {"series" if series else "parallel"} '
          
          f'will produce {"resistance" if resistor else "capacitance"} = {solved_values:.3f}. Aiming for {"R" if resistor else "C"} = {target:.3f}, '
          
          f'error of {solved_error:.2f}%')
    return r_to_use


if __name__ == "__main__":
    
    #df['Val'].replace({'K': '*1e3', 'M': '*1e6', 'm': '*1e-3', 'u': '*1e-6', 'n': '*1e-9', 'p': '*1e-12', 'f': , 
                   #}, regex=True).map(pd.eval).astype(float)

    sol = equivalent_tol([1, 2, 3, 4, 5, 6, 7], 11, True, 10,True)
    sol = equivalent_tol([1, 2, 3, 4, 5, 6, 7], 11, False, 10,False)


    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
