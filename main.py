import numpy as np
import overlap_sim

import brain
import brain_util as bu
import numpy as np
import copy
import simulations

import sys 

n=100000
k=317
p=0.05
beta=0.1
project_iter=10
number_firings=10
neurons_are_active_for = 10

def find_firing_neurons(n=100000,k=317,p=0.05,beta=0.1,project_iter=10,number_firings=10,neurons_are_active_for = 10):
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
    b.add_area("E",n,k,beta) # final project test area
    b.project({"stimA":["A"],"stimB":["B"],"stimC":["C"],"stimD":["D"]},{})
    # Create assemblies A,B,C,D to stability
    for i in range(0,9):
        b.project({"stimA":["A"],"stimB":["B"],"stimC":["C"],"stimD":["D"]}, 
                {"A":["A"],"B":["B"], "C":["C"],"D":["D"]})
    #print(b.areas["E"].winners_dict)
    #project assemblies to area of interest E must not be done at the same time
    b.project({"stimA":["A"]},{"A":["A","E"]})
    for i in range(0,9):
        b.project({"stimA":["A"]},{"A":["A","E"], "E":["E"]})
    b.project({"stimB":["B"]},{"B":["B","E"]})
    for i in range(0,9):
        b.project({"stimB":["B"]},{"B":["B","E"], "E":["E"]})
    b.project({"stimC":["C"]},{"C":["C","E"]})
    for i in range(0,9):
        b.project({"stimC":["C"]},{"C":["C","E"], "E":["E"]})
    b.project({"stimD":["D"]},{"D":["D","E"]})
    for i in range(0,9):
        b.project({"stimD":["D"]},{"D":["D","E"], "E":["E"]})

    overlap, winners_from_interesting_area = simulations.association_grand_sim_4_areas(b,n,k,p,beta,10,20)
    
    final_stim_dict = {}
    b.project({"stimA":["A"],"stimB":["B"],"stimC":["C"]}, 
                {"A":["A", "E"],"B":["B", "E"], "C":["C", "E"]})
    for i in range(0,1):
        b.project({"stimA":["A"],"stimB":["B"],"stimC":["C"]}, 
                {"A":["A", "E"],"B":["B", "E"], "C":["C", "E"], "E": ["E"]})

    total_overlap = {}
    winners = b.areas["E"].winners
    overlap_with_assembly_of_interest = bu.overlap(winners, winners_from_interesting_area)
    total_overlap[0] = float(overlap_with_assembly_of_interest)/float(k)
    for i in range(1,10):
        b.project({},{"E": ["E"]})
        winners = b.areas["E"].winners
        overlap_with_assembly_of_interest = bu.overlap(winners, winners_from_interesting_area)
        total_overlap[i] = float(overlap_with_assembly_of_interest)/float(k)
    
    print("Total overlap with d")
    print(total_overlap)

    simulations.plot_association_overlap(total_overlap)
    return



    


def find_firing_neurons_multiple_areas(n=100000,k=317,p=0.05,beta=0.1,project_iter=10,number_firings=10,neurons_are_active_for = 10, n_areas=4):
    print("RUNNING find_firing_neurons_multiple_areas")
    b = brain.Brain(p,save_winners=True)

    # area in which we will associate the assemblies
    target_area = str(chr(64+(n_areas+1)))

	# assembly we care about (the person we want to remember)
    important_area = str(chr(64+(n_areas)))
    important_stim_name = "stim" + important_area

    total_stim_dict = {}
    total_area_dict = {}

    # add stimuli and areas in brain b
    for i in range(1, n_areas+1):	
        area_name = str(chr(64+i))
        stim_name = "stim" + area_name
        b.add_stimulus(stim_name,k)
        b.add_area(area_name,n,k,beta)
        total_stim_dict[stim_name] = [area_name]
        total_area_dict[area_name] = [area_name]
    b.add_area(target_area,n,k,beta)
	
    b.project(total_stim_dict,{}) # stimuli projection
    # Create assemblies in each area to stability
    for i in range(0,9):
        b.project(total_stim_dict, total_area_dict)

    # Add target area in lists of area_dict
    for key, value in total_area_dict.items():
        total_area_dict[key].append(target_area)

    # Project the assembly of each area to the target area
    for i in range(1, n_areas+1):
        
        area_name = str(chr(64+i))
        stim_name = "stim" + area_name
        stim_dict = {stim_name:[area_name]}
        area_dict = {}
        area_dict[area_name] = total_area_dict[area_name]
        if i==1:
            print(stim_dict,area_dict)	
        b.project(stim_dict,area_dict)
        area_dict[target_area] = [target_area]
        for j in range(0,9):
            if i==1:
                print(stim_dict,area_dict)
            b.project(stim_dict,area_dict)
    
    # winners_from_interesting_area = the projection of the assembly we are interested in in the target area after the association
    overlap, winners_from_interesting_area = simulations.association_grand_sim_multiple_areas_not_together(b,n,k,p,beta,10,20,4)

    b_copy = {}
    b_copy_areas_winners = []
    b_copy[1] = copy.deepcopy(b)
    b_copy[2] = copy.deepcopy(b)
    b_copy[3] = copy.deepcopy(b)
    b_copy[4] = copy.deepcopy(b)
    
    b_copy[1].project({"stimA":["A"]},{})
    b_copy[1].project({},{"A":["E"]})
    b_copy_areas_winners.append(b_copy[1].areas["E"].winners)
    b_copy[2].project({"stimB":["B"]},{})
    b_copy[2].project({},{"B":["E"]})
    b_copy_areas_winners.append(b_copy[2].areas["E"].winners)
    b_copy[3].project({"stimC":["C"]},{})
    b_copy[3].project({},{"C":["E"]})
    b_copy_areas_winners.append(b_copy[3].areas["E"].winners)
    b_copy[4].project({"stimD":["D"]},{})
    b_copy[4].project({},{"D":["E"]})
    b_copy_areas_winners.append(b_copy[4].areas["E"].winners)

    o_a_d = bu.overlap(b_copy[1].areas["E"].winners, b_copy[4].areas["E"].winners)
    o_b_d = bu.overlap(b_copy[2].areas["E"].winners, b_copy[4].areas["E"].winners)
    o_c_d = bu.overlap(b_copy[3].areas["E"].winners, b_copy[4].areas["E"].winners)

    o = bu.overlap_multiple_lists(*b_copy_areas_winners)
    winners_from_interesting_area = b_copy[4].areas["E"].winners
    print("HERE MAIN")
    print("total overlap")
    print(float(o)/float(k))
    print("a-d overlap")
    print(float(o_a_d)/float(k))
    print("b-d overlap")
    print(float(o_b_d)/float(k))
    print("c-d overlap")
    print(float(o_c_d)/float(k))

    final_stim_dict = {}
    final_area_dict = {}
    for i in range(1, n_areas):
        area_name = str(chr(64+i))
        stim_name = "stim" + area_name
        final_stim_dict[stim_name] = [area_name]
        final_area_dict[area_name] = [area_name, target_area]

    b.project(final_stim_dict, final_area_dict)

    total_overlap = {}
    winners = b.areas[target_area].winners
    overlap_with_assembly_of_interest = bu.overlap(winners, winners_from_interesting_area)
    total_overlap[0] = float(overlap_with_assembly_of_interest)/float(k)
    for i in range(1,10):
        b.project({},{target_area: [target_area]})
        winners = b.areas[target_area].winners
        overlap_with_assembly_of_interest = bu.overlap(winners, winners_from_interesting_area)
        total_overlap[i] = float(overlap_with_assembly_of_interest)/float(k)
    
    print("Total overlap with d")
    print(total_overlap)
    
    simulations.plot_association_overlap(total_overlap)
    f.flush()
    return

if __name__ == "__main__":
    stdoutOrigin=sys.stdout 
    f= open("separate_auto.txt", "w",0)
    sys.stdout = f
    find_firing_neurons_multiple_areas()
    sys.stdout.close()
    f.close()
