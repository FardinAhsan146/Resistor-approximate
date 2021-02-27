

def series_equivalance(R,target,tolerance):
    """
    R = list of resistors present
    target = target value
    tolerance = range += % of target that is acceptable 
    This function returns a list of 
    """

    tol = tolerance/100 #converting tolerance to decimal
    
    if target < min(R):
        return "Your target is too small for series equivalence, Try parallel equivalence"
    
    else:
        r = R #dummy/copy R
        toriginal = target #dummy values for arguments made to not change arguments 
        approximate = 0 #this is for exit condition, target in and of itself could be used but that would make algo unstable
        resistors_list = [] #list to return at the end
        
        while True: #Infinite loop because multiple exit conditions
        
            if (approximate >= (1-tol)*target and approximate <= (1+tol)*target)  :#exit condition
                break
            
            if len(R) == 0: #If all values are used up
                return "All values used up, list: {}, approximate: {},%Δ of ".format(resistors_list,sum(resistors_list),percentage_difference(target,int(sum(resistors_list))))
     
            difference_from_target = [abs(toriginal-i) for i in R] #finding absolute difference of target from list of R values
            
            for i,v in enumerate(difference_from_target):
                if v == min(difference_from_target): #adding lowest differences to list
                    approximate += r[i] #increment approximate by value from resistors with least difference
                    toriginal -= r[i] #remove that from target dummy target
                    resistors_list.append(r[i]) #adding to list to be returned
                    r.remove(r[i]) 
                    break
            
        return_string =  "Resistors to use are {}, Approximated value: {}, %Δ of {}%".format(resistors_list,sum(resistors_list),percentage_difference(target,int(sum(resistors_list))))
        return return_string



    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    