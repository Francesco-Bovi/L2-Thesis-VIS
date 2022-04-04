import json
import random
from textwrap import indent

from torch import initial_seed

def AddState(state,graph,parent=None):

    #Check if already exists a ley with that value
    if(parent!=None):
        sub_dict=[]
        graph[state+"_"+parent]=sub_dict

        return state+"_"+parent

    else:

        sub_dict=[]
        graph[state]=sub_dict

        return state


    #print("Graph representation: ",graph)


def AddTransitions(transitions,parent=None,child=None):
    transition_array=[]
    for t in transitions:
        target_array=transitions.get(t)
        for elem in target_array:

            #Reference to parent if we found a transition to hover
            if(elem["target"]=="hover" or elem["target"]=="idle"):
                transition_array.append([t,parent])
            else:
                if(parent!=None):
                    transition_array.append([t,elem["target"]+"_"+parent])
                else:
                    transition_array.append([t,elem["target"]+"_"+child])

    return transition_array

#Function to build the graph
def create_graph(states,graph,parent_tranistions=None,parent=None):
    transitions=None
    for child in states:
        print("CHILD:",child)
        print("PARENT:",parent)
        print("PARENT TRANS:",parent_tranistions)

        #We are not interested in hover since we have considered it previoulsy
        if(child!="hover" and child!="idle"):

            #Add state checking if it's a real state
            if(states.get(child).get("initial") is None):

                child_name=AddState(child,graph,parent)

                if(states.get(child).get("on") is not None):
                    transitions=AddTransitions(states.get(child).get("on"),parent,child_name)
                    print(transitions)
                    for t in transitions:
                        graph[child_name].append(t)

                #Inheritance of transitions from container nodes
                if(parent_tranistions!=None):
                    for t in parent_tranistions:
                        graph[child_name].append(t)

                print("TRANSITIONS:",transitions)

                if(transitions!=None and parent_tranistions!=None):
                    for t in parent_tranistions:
                        transitions.append(t)
                
                print("TRANSITION UPDATE",transitions)
                print("------------------------------------------------------------------------------")
                if(states.get(child).get("states") is not None):
                    create_graph(states.get(child).get("states"),graph,transitions,child_name)
            
            #Case when the state is a container
            else:
                initial_state=states.get(child).get("initial")
                child_name=AddState(child,graph,parent)

                if(states.get(child).get("on") is not None):
                    transitions=AddTransitions(states.get(child).get("on"),parent,child_name)
                    print(transitions)
                    for t in transitions:
                        graph[child_name].append(t)

                if(states.get(child).get("states").get(initial_state).get("on") is not None):
                    transition_initial_state=AddTransitions(states.get(child).get("states").get(initial_state).get("on"),None,child_name)
                    for t in transition_initial_state:
                        graph[child_name].append(t)
            
                #Inheritance of transitions from container nodes
                if(parent_tranistions!=None):
                    for t in parent_tranistions:
                        graph[child_name].append(t)
        
                print("TRANSITIONS:",transitions)

                if(transitions!=None and parent_tranistions!=None):
                    for t in parent_tranistions:
                        transitions.append(t)
                
                print("TRANSITION UPDATE",transitions)
                print("------------------------------------------------------------------------------")
                if(states.get(child).get("states") is not None):
                    create_graph(states.get(child).get("states"),graph,transitions,child_name)
if(__name__=="__main__"):
    #open the statechart json file
    statechart_j=open('xstate_visualization_statechart.json')

    #returns the JSON object as a dictionary
    statechart_dict=json.load(statechart_j)

    #Data structure for that will contain the graph
    graph={}

    create_graph(statechart_dict.get('states'),graph,"vis")

    #Print graph representation
    print("------------------------------------------------------------------------------")
    print("------------------------------------------------------------------------------")
    #print("Graph representation: ",graph)
    print("Graph:",json.dumps(graph,indent=4))
    with open('statechart.json', 'w') as fp:
        json.dump(graph, fp,  indent=4)