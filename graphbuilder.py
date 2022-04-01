import json
import random
from textwrap import indent

def add_state(s,graph):
    sub_dict=[]
    graph[s]=sub_dict

    #print("Graph representation: ",graph)


def add_transitions(transitions,graph,parent=None):
    for t in transitions:
        target_array=transitions.get(t)
        for elem in target_array:
            if(elem['target']!="hover"):
                transition_array=[t,elem['target']]
                graph.append(transition_array)
            else:
                transition_array=[t,parent]
                graph.append(transition_array)

#Function to build the graph
def create_graph(states,graph,parent=None):
    global count
    for child in states:

        #Add node to graph
        if(child!="hover"):
            add_state(child,graph)

        if(states.get(child).get("on") is not None):
            if(child!="hover"):
                add_transitions(states.get(child).get('on'),graph[child],parent)
            else:
                add_transitions(states.get(child).get('on'),graph[parent])
        
        if(states.get(child).get('states') is not None):
            create_graph(states.get(child).get('states'),graph,child)

def explore_graph(graph,parent=None):
    start=random.randint(0,len(graph)-1)
    print(start)
    list_states=list(graph)
    initial_state=list_states[start]
    print(initial_state)
    explore_graph(graph,initial_state)

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

    print("---EXPLORE THE GRAPH---")

    #explore_graph(graph)