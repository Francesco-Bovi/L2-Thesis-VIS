import json
import random
from textwrap import indent

from torch import initial_seed

def AddState(state,graph):
    sub_dict=[]
    graph[state]=sub_dict

    #print("Graph representation: ",graph)


def AddTransitions(transitions):
    transition_array=[]
    for t in transitions:
        target_array=transitions.get(t)
        for elem in target_array:
            transition_array.append([t,elem["target"]])
    return transition_array

#Function to build the graph
def create_graph(states,graph,parent_tranistions=None):
    transitions=None
    for child in states:

        #Add state checking if it's a real state
        if(states.get(child).get("initial") is None):

            AddState(child,graph)

            if(states.get(child).get("on") is not None):
                transitions=AddTransitions(states.get(child).get("on"))
                graph[child]=transitions

            #Inheritance of transitions from container nodes
            if(parent_tranistions!=None):
                for transition in parent_tranistions:
                    graph[child].append(transition)
        
        #Case when the state is a container
        else:
            initial_state=states.get(child).get("initial")
            AddState(child,graph)

            if(states.get(child).get("on") is not None):
                transitions=AddTransitions(states.get(child).get("on"))
                graph[child]=transitions

            if(states.get(child).get("states").get(initial_state).get("on") is not None):
                transition_initial_state=AddTransitions(states.get(child).get("states").get(initial_state).get("on"))
                for transition in transition_initial_state:
                    graph[child].append(transition)

            #Inheritance of transitions from container nodes
            if(parent_tranistions!=None):
                for transition in parent_tranistions:
                    graph[child].append(transition)

        if(states.get(child).get("states") is not None):
            create_graph(states.get(child).get("states"),graph,transitions)

if(__name__=="__main__"):
    #open the statechart json file
    statechart_j=open('xstate_visualization_statechart.json')

    #returns the JSON object as a dictionary
    statechart_dict=json.load(statechart_j)

    #Data structure for that will contain the graph
    graph={}

    create_graph(statechart_dict.get('states'),graph)

    #Print graph representation
    print("----------------------------")
    #print("Graph representation: ",graph)
    print("Graph:",json.dumps(graph,indent=4))