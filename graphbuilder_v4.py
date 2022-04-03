import json


class StateMachine:
    def __init__(self, initial_state):
        self.initialState=initial_state


class Container:
    def __init__(self, ID=None):
        self.ID = ID
        self.Transitions  = []
        self.Subsets = []
        self.Parent = None 

"""
class State:
    def __init__(self, Contenuto=None, ProssimoNodo=None):
        self.Contenuto = Contenuto
        self.ProssimoNodo  = ProssimoNodo
    
    def __str__(self):
        return str(self.Contenuto)
"""

def create_graph(states,container):
    for child in states:
        
        new_container=Container(child)
        print(new_container.ID)

        if(states.get(child).get("on") is not None):
            new_container.Transitions=add_transitions(states.get(child).get('on'))

        container.append(new_container)
        print(container)

        #Explore rest of graph
        if(states.get(child).get("states") is not None):
            create_graph(states.get(child).get("states"),new_container.Subsets)

def add_transitions(transitions):
    transition_array=[]
    for t in transitions:
        target_array=transitions.get(t)
        for elem in target_array:
            transition_array.append([t,elem["target"]])
    return transition_array

def PrintGraph(state,level=0):
    indentation = '\t' * level
    print(indentation,state.ID)
    print(indentation,"TRANSITIONS",state.Transitions)
    for item in state.Subsets:
        PrintGraph(item,level+1)


if(__name__=="__main__"):

    #open the statechart json file
    statechart_j=open('xstate_visualization_statechart.json')

    #returns the JSON object as a dictionary
    statechart_dict=json.load(statechart_j)

    #Function to create the graph implementation
    #create_graph(statechart_dict.get('states'),graph)

    #if(child=="rest"):
    #    state_machine.initialState=new_container

    root_node=Container("vis")
    state_machine=StateMachine(root_node)

    create_graph(statechart_dict.get('states'),root_node.Subsets)
   
    #root_container.Subsets.append(Container("scatter"))
    #root_container.Subsets.append(Container("barchart"))

    print("----------------------------")
    print("Graph representation: ")
    print("VIS: ")
    print("TRANSITIONS:",root_node.Subsets)

    print("----PRINT----")
    PrintGraph(root_node)