import numpy as np
import overlap_sim

import brain
import brain_util as bu
import numpy as np
import copy
import simulations

n=100000
k=317
p=0.05
beta=0.1
project_iter=10
number_firings=10
neurons_are_active_for = 10

print("RUNNING")
b = brain.Brain(p,save_winners=True)
b.add_stimulus("stimA",k)
b.add_area("A",n,k,beta)
b.add_stimulus("stimB",k)
b.add_area("B",n,k,beta)
b.add_stimulus("stimC",k)
b.add_area("C",n,k,beta)
b.add_stimulus("stimD",k)
b.add_area("D",n,k,beta)
b.add_area("E",n,k,0.0) # final project test area
b.project({"stimA":["A"],"stimB":["B"],"stimC":["C"],"stimD":["D"]},{})
# Create assemblies A,B,C,D to stability
for i in range(0,1):
    print("i = " + str(i))
    b.project({"stimA":["A"],"stimB":["B"],"stimC":["C"],"stimD":["D"]}, 
            {"A":["A"],"B":["B"], "C":["C"],"D":["D"]})
print(b.areas["E"].winners_dict)
#project assemblies to area of interest E must not be done at the same time
b.project({"stimA":["A"]},{"A":["A","E"]})
for i in range(0,1):
    b.project({"stimA":["A"]},{"A":["A","E"], "E":["E"]})
b.project({"stimB":["B"]},{"B":["B","E"]})
for i in range(0,1):
    b.project({"stimB":["B"]},{"B":["B","E"], "E":["E"]})
b.project({"stimC":["C"]},{"C":["C","E"]})
for i in range(0,1):
    b.project({"stimC":["C"]},{"C":["C","E"], "E":["E"]})
b.project({"stimD":["D"]},{"D":["D","E"]})
for i in range(0,1):
    b.project({"stimD":["D"]},{"D":["D","E"], "E":["E"]})
#sanity check print area["D"]saved_winners
overlap = simulations.association_grand_sim_multiple_areas(b,100000,317,0.05,0.1,10,20,4)
diction = {0:"A", 1:"B", 2:"C"} #E_b, E_a, E_c...
t=0 
print(b.areas["E"].winners_dict)
#how much time have the neurons left 
all_neurons=[]
for key, value in b.areas["E"].winners_dict.items(): 
    all_neurons.append(value)

all_neurons_flat = []
for neurons_list in all_neurons:
    for neuron in neurons_list:
        all_neurons_flat.append(neuron)

individual_neurons = set(all_neurons_flat)
print("length winners" +str(len(individual_neurons)))
firing_time_dict = dict.fromkeys(individual_neurons, 0)
print(firing_time_dict)
#start firing the A,B,C assemblies
for i in range(0,number_firings):
    if(i!=0):
        for key,value in firing_time_dict.items():
            firing_time_dict[key] = max(0,firing_time_dict[key]-1)
    ind = np.random.randint(0,2)
    area_firing = diction[ind]
    for neuron in b.areas["E"].winners_dict[area_firing]:
        firing_time_dict[neuron]=10
    comp ={}
    for key, value in b.areas["E"].winners_dict.items():
        comp[key]=0
        for neuron in value:
            if (firing_time_dict[neuron] > 0):
                comp[key] += 1

    area = max(comp, key=comp.get)
    print("initial area fired " + area_firing+  " assembly in E firing " + area)

print("Association overlap: " + str(overlap))