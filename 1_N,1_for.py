
N = [ i for i in range(1,10)] + [-1] +[ i for i in range(10,20)]+[ i for i in range(10,20)]
print(N)
"""
for i in range(len(N)):
    if N.count(N[i]) == 1:
        print(N[i])
"""
        
    
for i in range(len(N)):
    if N[len(N)-i-1] in N[0: len(N)-i-1]:
        N.remove(N[len(N)-i-1])
    else:
        print(N[len(N)-1 - i])
        break
       
        
        


    
     
    

