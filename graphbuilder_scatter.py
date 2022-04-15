import json
import random
from textwrap import indent
from typing import List
from collections import deque

from cv2 import magnitude



#Function used to add a key in the dictionary
def AddState(state,graph,parent):

    if(parent!=None):
        #Crete a key in the dictionary based on the parent
        sub_dict={}
        graph[state+"_"+parent]=sub_dict

        return state+"_"+parent
    
    else:
        sub_dict={}
        graph[state]=sub_dict

        return state

def AddTransitions(transitions,parent=None,child=None):
    transition_array=[]
    for t in transitions:
        target_array=transitions.get(t)
        for elem in target_array:
            #If is a substate
            if(parent!=None):
                transition_array.append([t,elem["target"]+"_"+parent])
            
            #If is not a substate
            else:
                transition_array.append([t,elem["target"]])

    return transition_array

#Function to build the graph
def CreateGraph(states,graph,parent_tranistions=None,parent=None):
    transitions=[]
    for child in states:

        #Add the new key to the graph using the name of the parent (Container)
        child_name=AddState(child,graph,parent)

        if(states.get(child).get("initial") is not None):
            graph[child_name]["initial"] = states.get(child).get("initial")+"_"+child_name
        else:
            graph[child_name]["initial"] = None

        graph[child_name]["transitions"] = []
        graph[child_name]["values"] = []

        if(states.get(child).get("states") is not None):
            for value in states.get(child).get("states"):
                graph[child_name]["values"].append(value+"_"+child_name)            

        if(states.get(child).get("on") is not None):
            transitions=AddTransitions(states.get(child).get("on"),parent,child_name)
            print(transitions)
            for t in transitions:
                graph[child_name]["transitions"].append(t)


        if(states.get(child).get("context") is not None):
            graph[child_name]["context"] = states.get(child).get("context")

        #Inheritance of transitions from container nodes
        if(parent_tranistions!=None):
            for t in parent_tranistions:
                graph[child_name]["transitions"].append(t)

        #Add parent transitions to the transitions of the new state
        #Those will be inherited by the substates
        if(parent_tranistions!=None):
            for t in parent_tranistions:
                transitions.append(t)

        #Go inside the substates
        if(states.get(child).get("states") is not None):
            CreateGraph(states.get(child).get("states"),graph,transitions,child_name)


def Scatter(graph,state):
    print("------You are now in the scatter-------")

    #At first I will be in hovering
    state=graph[state]["initial"]

    exploration_sequence.append(state)

    #By default 0 zoom levels, positive if ZoomIn, negative if ZoomOut
    zoomLevels=0

    #PanningLR for left/right, then panningUD for up/down
    #Positive: right-up
    #Negative: left-down
    panningLR=0
    panningUD=0
    min=-10
    max=10

    #variables for the brushing transition
    # "x" can be left/right
    # "y" can be up/down
    # Both start with idle
    x="idle"
    y="idle"

    #Variable used to exit Scatter interaction
    out=0
    while(out!=1):

        print(f"Values are:\n zoomLevel:{zoomLevels}\npanningLR:{panningLR}\npanningUD:{panningUD}\nx:{x}\ny:{y}")

        #Print all possible transitions
        counter=0
        list_tran=[]
        for trn in graph[state]["transitions"]:
            print(str(counter)+":",end="")
            print(trn)
            list_tran.insert(counter,trn)
            counter+=1

        #Insert transition to execute from the current state
        next_tran=int(input("Insert number: "))
        state=list_tran[next_tran][1]
        action=list_tran[next_tran][0]

        if(next_tran==-1):
            out=1

        exploration_sequence.append(action)
        exploration_sequence.append(state)

        #Check the transitions we are performing
        if(action=="ZOOMIN"):
            zoomLevels+=1

        elif(action=="ZOOMOUT"):
            zoomLevels-=1

        #Here we are in panning
        elif(action=="MOUSEDOWN"):
            panningLR=random.randint(min,max)
            panningUD=random.randint(min,max)
            #Do MOUSEUP SINCE ATOMIC
            state=graph[state]["transitions"][0]
            exploration_sequence.append(state[0])
            exploration_sequence.append(state[1])
            state=state[1]

    return state


def Exploration(graph,state):
    global exploration_sequence

    print()
    print("---CURRENT STATE: "+state+"---")
    print("Choose transitions to execute using numbers:")


    #Add to state
    exploration_sequence.append(state)

    #Print all possible transitions
    counter=0
    list_tran=[]
    for trn in graph[state]["transitions"]:
        print(str(counter)+":",end="")
        print(trn)
        list_tran.insert(counter,trn)
        counter+=1

    #Insert transition to execute from the current state
    next_tran=int(input("Insert number: "))

    #Return with -1 from input
    if(next_tran==-1):
        return
    
    next_state=list_tran[next_tran][1]

    if(next_state=="scatter"):
        next_state=Scatter(graph,next_state)

    Exploration(graph,next_state)


exploration_sequence=[]


if(__name__=="__main__"):

    #open the statechart json file
    statechart_j=open('xstate_scatter.json')

    #returns the JSON object as a dictionary
    statechart_dict=json.load(statechart_j)

    #Data structure for that will contain the graph
    graph={}

    CreateGraph(statechart_dict.get('states'),graph,None)

    #Print graph representation
    print("------------------------------------------------------------------------------")
    print("------------------------------------------------------------------------------")
    print("Graph:",json.dumps(graph,indent=4))

    #Save graph on a file
    with open('statechart_scatter.json', 'w') as fp:
        json.dump(graph, fp,  indent=4)


    Exploration(graph,"rest")

    print(exploration_sequence)

    print("------------------------------------------------------------------------------")