import json
from textwrap import indent

def add_state(s,graph):
    sub_dict={}
    graph[s]=sub_dict

    print("Graph representation: ",graph)


def add_transition(transitions,parent):
    global graph
    print("PARENT-",parent)
    for t in transitions:
        print("DEBUG ACTION -",t,"-",transitions.get(t))
        target_array=transitions.get(t)
        for elem in target_array:
            print("TARGET-->",elem['target'])
            transition_array=[t,elem['target']]
            graph[parent].append(transition_array)

#Function to build the graph
def traverse_inner(states,graph):
    for child in states:
        #Print name of all the states/interactions
        print(child)

        #Add principal states with hovering
        add_state(child,graph)

        #Add child states
        #traverse_json(statechart_dict.get('states').get(i),i)
        if(states.get(child).get('states') is not None):
            traverse_inner(states.get(child).get('states'),graph[child])

if(__name__=="__main__"):
    #open the statechart json file
    statechart_j=open('xstate_visualization_statechart.json')

    #returns the JSON object as a dictionary
    statechart_dict=json.load(statechart_j)

    #Data structure for that will contain the graph
    graph={}

    traverse_inner(statechart_dict.get('states'),graph)

    #Print graph representation
    print("----------------------------")
    print("Graph representation: ",graph)
    print("Graph:",json.dumps(graph,indent=4))