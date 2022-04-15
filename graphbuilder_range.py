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

            #Reference to parent if we found a transition to hover or idle
            if(elem["target"]=="hover" or elem["target"]=="idle"):
                if(parent!=None):
                    transition_array.append([t,parent])
            else:

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

 
def ExtractContextInfo(states,graph,parent,parent_context=None):
    for child in states:
        if(child!="hover" and child!="idle"):
        
                #Case when it's not a Container state
                if(states.get(child).get("initial") is None):

                    #Add the new key to the graph using the name of the parent (Container)
                    child_name=AddState(child,graph,parent)

                    if(states.get(child).get("context") is not None):
                        graph[child_name]=states.get(child).get("context")

                    if(parent_context!=None):
                        for key in parent_context:
                            graph[child_name]

                    #Go inside the substates
                    if(states.get(child).get("states") is not None):
                        ExtractContextInfo(states.get(child).get("states"),graph,child_name)
                
                #Case when the state is a Container
                else:

                    #Name of the default initial state
                    initial_state=states.get(child).get("initial")

                    #Add the new key to the graph using the name of the parent (Container)
                    child_name=AddState(child,graph,parent)

                    if(states.get(child).get("context") is not None):
                        graph[child_name]=states.get(child).get("context")
                    
                    #Go inside the substates
                    if(states.get(child).get("states") is not None):
                        ExtractContextInfo(states.get(child).get("states"),graph,child_name)

        #If we are in "hover" or "idle" we don't consider them because we have done it previously
        #So we just skip
        else:

            print("------------------------------------------------------------------------------")
        

def Range(graph,state):
    global exploration_sequence

    #Check if we are not in Range interaction anymore
    out=0
    print("Now you are in the range slider")

    #In case the slider is range
    handleL=None
    handleR=None

    #Save max and min values
    max=None
    min=None

    #Get the context information
    context=graph[state]["context"]
    if(context["type"]=="range"):
        handleL=context["handleL"]
        handleR=context["handleR"]
        min=context["min"]
        max=context["max"]

    prev=None

    #Loop until you go out of the RANGE interaction
    while(out!=1):
        if(graph[state]["initial"] is not None):
            state=graph[state]["initial"]
        
        exploration_sequence.append(state)

        if("idle" in state):
            #Save the previous state
            prev=state

        print(f"Values are:\nhandleL:{handleL} - handleR:{handleR}")

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

        exploration_sequence.append(state)

        if("range" not in state):
            out=1

        #Here if we are dragging
        if("drag" in state):

            if("left" in state and "dragLR" in state):
        
                if(handleL<=min):
                    print("You are already at the MIN")
                else:
                    handleL-=0.1
                    handleR-=0.1

            elif("right" in state and "dragLR" in state):

                if(handleR>=max):
                    print("You are already at the MIN")
                else:
                    handleL+=0.1
                    handleR+=0.1

            #Check if we are going to LEFT with DRAGL
            elif("left" in state and "dragL" in state):
                
                if(handleL<=min):
                    print("You are already at the MIN")
                else:
                    handleL-=0.1
                
            #Check if we are going to LEFT with DRAGR
            elif("left" in state and "dragR" in state):

                if(handleR<=min):
                    print("You are already at the MIN")
                else:
                    handleR-=0.1

            #Check if we are going to RIGHT with DRAGL
            elif("right" in state and "dragL" in state):

                if(handleL>=max):
                    print("You are already at the MAX")
                else:
                    handleL+=0.1

            #Check if we are going to RIGHT with DRAGR
            else:

                if(handleR>=max):
                    print("You are already at the MAX")
                else:
                    handleR+=0.1
        
            #Update the statechart
            graph["range"]["context"]["handleR"]=handleR
            graph["range"]["context"]["handleL"]=handleL

            if(prev!=None):
                state=prev
            
    return state


def Exploration(graph,state):
    global exploration_sequence

    print()
    print("---CURRENT STATE: "+state+"---")
    print("Choose transitions to execute using numbers:")


    #Add to state
    exploration_sequence.append(state)

    #CHECK IF YOU ARE IN DRAGGING
    if("drag" in state):
        Range(graph,state)

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

    if(next_state=="range"):
        next_state=Range(graph,next_state)

    Exploration(graph,next_state)



exploration_sequence=[]


if(__name__=="__main__"):

    #open the statechart json file
    statechart_j=open('xstate_range.json')

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
    with open('statechart_range.json', 'w') as fp:
        json.dump(graph, fp,  indent=4)


    Exploration(graph,"rest")

    print(exploration_sequence)

    print("------------------------------------------------------------------------------")