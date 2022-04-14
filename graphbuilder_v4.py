import json
import random
from textwrap import indent
from typing import List
from collections import deque

from cv2 import magnitude



#Function used to add a key in the dictionary
def AddState(state,graph,parent):

    #Crete a key in the dictionary based on the parent
    sub_dict=[]
    graph[state+"_"+parent]=sub_dict

    return state+"_"+parent


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
                    transition_array.append([t,elem["target"]+"_"+child])

    return transition_array

#Function to build the graph
def CreateGraph(states,graph,parent_tranistions=None,parent=None):
    transitions=[]
    for child in states:
        #print("CHILD:",child)
        #print("PARENT:",parent)
        #print("PARENT TRANS:",parent_tranistions)

        #We are not interested in hover or idle since we have considered them previoulsy
        if(child!="hover" and child!="idle"):

            #Case when it's not a Container state
            if(states.get(child).get("initial") is None):

                #Add the new key to the graph using the name of the parent (Container)
                child_name=AddState(child,graph,parent)

                #Check if it has transitions (and add them)
                if(states.get(child).get("on") is not None):
                    transitions=AddTransitions(states.get(child).get("on"),parent,child_name)
                    print(transitions)
                    for t in transitions:
                        graph[child_name].append(t)

                #Inheritance of transitions from container nodes
                if(parent_tranistions!=None):
                    for t in parent_tranistions:
                        graph[child_name].append(t)

                #print("TRANSITIONS:",transitions)

                #Add parent transitions to the transitions of the new state
                #Those will be inherited by the substates
                if(parent_tranistions!=None):
                    for t in parent_tranistions:
                        transitions.append(t)
                
                #print("TRANSITION UPDATE",transitions)
                #print("------------------------------------------------------------------------------")

                #Check if it has parallels
                if(states.get(child).get("type") is not None):
                    for node in states.get(child).get("states"):

                        graph[child_name].append(["MOUSEMOVE",node+"_"+child_name])

                #Go inside the substates
                if(states.get(child).get("states") is not None):
                    CreateGraph(states.get(child).get("states"),graph,transitions,child_name)
            
            #Case when the state is a Container
            else:

                #Name of the default initial state
                initial_state=states.get(child).get("initial")

                #Add the new key to the graph using the name of the parent (Container)
                child_name=AddState(child,graph,parent)

                #Check if it has transitions (and add them)
                if(states.get(child).get("on") is not None):
                    transitions=AddTransitions(states.get(child).get("on"),parent,child_name)
                    print(transitions)
                    for t in transitions:
                        graph[child_name].append(t)

                #In this case add also the transitions of the ipotetical initial state
                #Since we consider the actual state having the same transitions of its initial one
                if(states.get(child).get("states").get(initial_state).get("on") is not None):
                    transition_initial_state=AddTransitions(states.get(child).get("states").get(initial_state).get("on"),child_name,child_name)
                    for t in transition_initial_state:
                        graph[child_name].append(t)
            
                #Inheritance of transitions from container nodes
                if(parent_tranistions!=None):
                    for t in parent_tranistions:
                        graph[child_name].append(t)
        
                #print("TRANSITIONS:",transitions)

                #Add parent transitions to the transitions of the new state
                #Those will be inherited by the substates
                if(parent_tranistions!=None):
                    for t in parent_tranistions:
                        transitions.append(t)
                
                #print("TRANSITION UPDATE",transitions)
                #print("------------------------------------------------------------------------------")
                
                #Check if it has parallels
                if(states.get(child).get("type") is not None):
                    for node in states.get(child).get("states"):

                        graph[child_name].append(["MOUSEMOVE",node+"_"+child_name])
                
                #Go inside the substates
                if(states.get(child).get("states") is not None):
                    CreateGraph(states.get(child).get("states"),graph,transitions,child_name)

        #If we are in "hover" or "idle" we don't consider them because we have done it previously
        #So we just skip
        else:

            print("------------------------------------------------------------------------------")

#Function that help choosing next state based on the score
def ChooseNextState(graph_s,random_number,transactions):

    #I give priority to transactions with 0 score
    for t in transactions:
        possible_state=t[1]
        #print("POSSIBLE STATE:",possible_state,"SCORE",graph_s[possible_state])
        if(graph_s[possible_state]==0):
            return t

    #Otherwise I go random
    return transactions[random_number]
 
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
        

def Exploration(graph,graph_context,state):
    print()
    print("---CURRENT STATE: "+state+"---")
    print("Choose transitions to execute using numbers:")

    #Print all possible transitions
    counter=0
    list_tran=[]
    for trn in graph[state]:
        print(str(counter)+":",end="")
        print(trn)
        list_tran.insert(counter,trn)
        counter+=1

    #Insert transition to execute from the current state
    next_tran=int(input("Insert number: "))
    next_state=list_tran[next_tran][1]

    #Choose magnitude of transitions
    #print("Which magnitude of transition (low-medium-high)?\n")
    #magnitude=input()

    #if(graph_context[next_state]!=[]):

    Exploration(graph,graph_context,next_state)

if(__name__=="__main__"):

    #open the statechart json file
    statechart_j=open('xstate_visualization_statechart_context.json')

    #returns the JSON object as a dictionary
    statechart_dict=json.load(statechart_j)

    #Data structure for that will contain the graph
    graph={}

    CreateGraph(statechart_dict.get('states'),graph,None,"vis")

    #Print graph representation
    print("------------------------------------------------------------------------------")
    print("------------------------------------------------------------------------------")
    print("Graph:",json.dumps(graph,indent=4))

    #Data structure that contains context information
    graph_context={}

    #Extract Information of context
    #ExtractContextInfo(statechart_dict.get('states'),graph_context,"vis")
    
    for elem in statechart_dict.get('context'):
        if(statechart_dict.get('context').get(elem) is not None):
            graph_context[elem] = statechart_dict.get('context').get(elem)
    
    print("GRAPH_CONTEXT:",json.dumps(graph_context,indent=4))

    #Exploration(graph,graph_context,"rest_vis")

    print("------------------------------------------------------------------------------")