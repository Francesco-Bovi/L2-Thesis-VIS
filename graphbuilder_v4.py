import json
from queue import Empty
import random


class StateMachine:
    def __init__(self, initial_state):
        self.initialState=initial_state


class Container:
    def __init__(self, ID=None):
        self.ID = ID
        self.Transitions  = []
        self.Subsets = []
        self.Parent = None

def CreateGraph(states,container):
    for child in states:
        
        new_container=Container(child)
        new_container.Parent=container
        #print(new_container.ID)

        if(states.get(child).get("on") is not None):
            new_container.Transitions=AddTransitions(states.get(child).get('on'))

        container.Subsets.append(new_container)
        #print(container)

        #Explore rest of graph
        if(states.get(child).get("states") is not None):
            CreateGraph(states.get(child).get("states"),new_container)

def AddTransitions(transitions):
    transition_array=[]
    for t in transitions:
        target_array=transitions.get(t)
        for elem in target_array:
            transition_array.append([t,elem["target"]])
    return transition_array

def PrintGraph(state,level=0):
    indentation = '\t' * level
    print(indentation,state.ID)
    if(level!=0):
        print(indentation,"PARENT:", state.Parent.ID)
    print(indentation,"TRANSITIONS",state.Transitions)
    for item in state.Subsets:
        PrintGraph(item,level+1)

def PrintNode(state,level=1):
    print(state.ID)
    if(level!=0):
        print("PARENT:", state.Parent.ID)
    print("TRANSITIONS",state.Transitions)
    print("SUBSET:")
    print("\t",state.Subsets)
    for item in state.Subsets:
        print("\t",item.ID)

def findTransaction(state,id):
    for i in state.Subsets:
        if(i.ID==id):
            return i

def ExploreGraph(state):
    PrintNode(state,0)

    #Possible next states
    substates=state.Subsets
    transactions=state.Transitions
    parent=state.Parent

    #In each state I can go inside, at same level or at the parent
    start=random.randint(0,2)

    if(start==0):

        if(substates!=[]):
            #Explore a random state
            start=random.randint(0,len(substates)-1)
            next_state=substates[start]
            
            #Print the state
            print("SUBSTATE")
            print("NEXT_STATE->",next_state.ID)
            ExploreGraph(next_state)
        
        elif(transactions!=[]):
            #Explore a random state
            start=random.randint(0,len(transactions)-1)
            next_state_id=transactions[start][1]
            next_state=findTransaction(parent,next_state_id)

            #Print the state
            print("TRANSACTIONS")
            print("NEXT_STATE->",next_state.ID)
            ExploreGraph(next_state)

        else:
            next_state=state.Parent
            #Print the state
            print("PARENT")
            print("NEXT_STATE->",next_state.ID)
            ExploreGraph(next_state)          
    
    elif(start==1):

        if(transactions!=[]):

            #Explore a random state
            start=random.randint(0,len(transactions)-1)
            next_state_id=transactions[start][1]
            next_state=findTransaction(parent,next_state_id)
            
            #Print the state
            print("TRANSACTIONS")
            print("NEXT_STATE->",next_state.ID)
            ExploreGraph(next_state)

        elif(substates!=[]):
            #Explore a random state
            start=random.randint(0,len(substates)-1)
            next_state=substates[start]
            
            #Print the state
            print("SUBSTATE")
            print("NEXT_STATE->",next_state.ID)
            ExploreGraph(next_state)
        else:
            next_state=state.Parent
            #Print the state
            print("PARENT")
            print("NEXT_STATE->",next_state.ID)
            ExploreGraph(next_state)
    
    else:
        if(parent!=None):
            next_state=state.Parent
            #Print the state
            print("PARENT")
            print("NEXT_STATE->",next_state.ID)
            ExploreGraph(next_state)

        elif(transactions!=[]):
    
            #Explore a random state
            start=random.randint(0,len(transactions)-1)
            next_state_id=transactions[start][1]
            next_state=findTransaction(parent,next_state_id)
            
            #Print the state
            print("TRANSACTIONS")
            print("NEXT_STATE->",next_state.ID)
            ExploreGraph(next_state)
        
        elif(substates!=[]):
            #Explore a random state
            start=random.randint(0,len(substates)-1)
            next_state=substates[start]
            
            #Print the state
            print("SUBSTATE")
            print("NEXT_STATE->",next_state.ID)
            ExploreGraph(next_state)

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

    #root_node.Parent=state_machine

    CreateGraph(statechart_dict.get('states'),root_node)
   
    #root_container.Subsets.append(Container("scatter"))
    #root_container.Subsets.append(Container("barchart"))

    print("----------------------------")
    print("Graph representation: ")
    #PrintGraph(root_node)

    ExploreGraph(root_node)