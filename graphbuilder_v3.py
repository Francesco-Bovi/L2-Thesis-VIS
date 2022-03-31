import json
import random
from textwrap import indent

def add_state(s,graph):
    sub_dict={}
    graph[s]=sub_dict

    #print("Graph representation: ",graph)


def add_transitions(transitions,graph):
    graph['transitions']=[]
    for t in transitions:
        target_array=transitions.get(t)
        for elem in target_array:
            transition_array=[t,elem['target']]
            graph['transitions'].append(transition_array)

#Function to build the graph
def create_graph(states,graph):
    for child in states:

        #Add principal states with hovering
        add_state(child,graph)

        #Add child states
        if(states.get(child).get('states') is not None):
            create_graph(states.get(child).get('states'),graph[child])

        #Add transition
        if(states.get(child).get('on') is not None):
            add_transitions(states.get(child).get('on'),graph[child])


def explore_graph(graph,parent=None):
    start=random.randint(0,len(graph)-1)
    print(start)
    list_states=list(graph)
    initial_state=list_states[start]
    print(initial_state)
    if(initial_state=='transitions'):
        start=random.randint(0,len(graph['transitions'])-1)
        print("TRANSITION FOUND:",start)
        list_states=list(graph['transitions'][start])
        print(list_states[1])
        explore_graph(parent[list_states[1]],parent)
    else:
        explore_graph(graph[initial_state],graph)



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