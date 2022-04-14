import json
import random


class StateMachine:
    def __init__(self, initial_state):
        self.initialState=initial_state


class State:
    def __init__(self, ID=None):
        self.ID = ID
        self.Transitions  = []
        self.Subsets = []
        self.Container = None
        self.Score=0
        self.initial = None

def CreateGraph(substates,state,parent_transitions=None):
    for child in substates:
        
        new_state=State(child)
        new_state.Container=state
        #print(new_state.ID)

        if(substates.get(child).get("initial") is not None):
            new_state.initial = substates.get(child).get("initial")

        if(substates.get(child).get("on") is not None):
            new_state.Transitions=AddTransitions(substates.get(child).get('on'))

        if(state.initial==child):
            state.initial=new_state

        #Inheritance of transitions by Container
        if(parent_transitions!=None):
            for t in parent_transitions:
                new_state.Transitions.append([t[0],t[1]])

        state.Subsets.append(new_state)
        #print(state)

        #Explore rest of graph
        if(substates.get(child).get("states") is not None):
            CreateGraph(substates.get(child).get("states"),new_state,new_state.Transitions)

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
        print(indentation,"PARENT:", state.Container.ID)
    print(indentation,"TRANSITIONS:",state.Transitions)
    print(indentation,"STATES:",state.Subsets)
    if(state.initial is not None):
        print(indentation,"INITIAL:",state.initial.ID)
    for item in state.Subsets:
        PrintGraph(item,level+1)

def PrintNode(state,level=1):
    print(state.ID)
    if(level!=0):
        print("PARENT:", state.Container.ID)
    print("TRANSITIONS:",state.Transitions)
    print("INITIAL:",state.initial)
    #print("SUBSET:")
    #print("\t",state.Subsets)
    for item in state.Subsets:
        print("\t",item.ID)

def findTransaction(state,id):
    for i in state.Subsets:
        if(i.ID==id):
            return i

#Function that update the LOG of the states
def addToLog(state):
    current_state=""
    while state!=None:

        #I am in VIS in this case
        if(state.Container==None):
            current_state=state.ID+current_state
        else:
            current_state=":{"+state.ID+current_state
        state=state.Container

    return current_state

def ExploreGraph(state):
    global log
    global log2
    log.append(state.ID)

    #Update score of the state
    state.Score=state.Score+1

    if(state.Score==30):
        return

    print("------------------------------------------------------------")
    PrintNode(state,0)
    print("------------------------------------------------------------")

    #Possible next states
    substates=state.Subsets
    transactions=state.Transitions
    container=state.Container

    #In each state I can go inside, at same level or at the container
    start=random.randint(0,2)

    if(start==0):

        if(substates!=[]):
            #Explore a random state
            start=random.randint(0,len(substates)-1)
            next_state=substates[start]
            
            #Print the state
            print("SUBSTATE")
            print("NEXT_STATE->",next_state.ID)

            #log2.append(log2[-1]+":{"+next_state.ID)
            log2.append(addToLog(next_state))
            ExploreGraph(next_state)
        
        elif(transactions!=[]):
            #Explore a random state
            start=random.randint(0,len(transactions)-1)
            next_state_id=transactions[start][1]
            next_state=findTransaction(container,next_state_id)

            #Print the state
            print("TRANSACTIONS")
            print("NEXT_STATE->",next_state.ID)

            log2.append(addToLog(next_state))
            ExploreGraph(next_state)

        else:
            next_state=state.Container
            #Print the state
            print("PARENT")
            print("NEXT_STATE->",next_state.ID)

            log2.append(addToLog(next_state))
            ExploreGraph(next_state)          
    
    elif(start==1):

        if(transactions!=[]):

            #Explore a random state
            start=random.randint(0,len(transactions)-1)
            next_state_id=transactions[start][1]
            next_state=findTransaction(container,next_state_id)
            
            #Print the state
            print("TRANSACTIONS")
            print("NEXT_STATE->",next_state.ID)
            
            log2.append(addToLog(next_state))
            ExploreGraph(next_state)

        elif(substates!=[]):
            #Explore a random state
            start=random.randint(0,len(substates)-1)
            next_state=substates[start]
            
            #Print the state
            print("SUBSTATE")
            print("NEXT_STATE->",next_state.ID)

            #log2.append(log2[-1]+":{"+next_state.ID)
            log2.append(addToLog(next_state))
            ExploreGraph(next_state)
        else:
            next_state=state.Container
            #Print the state
            print("PARENT")
            print("NEXT_STATE->",next_state.ID)

            log2.append(addToLog(next_state))
            ExploreGraph(next_state)
    
    else:
        if(container!=None):
            next_state=state.Container
            #Print the state
            print("PARENT")
            print("NEXT_STATE->",next_state.ID)

            log2.append(addToLog(next_state))
            ExploreGraph(next_state)

        elif(transactions!=[]):
    
            #Explore a random state
            start=random.randint(0,len(transactions)-1)
            next_state_id=transactions[start][1]
            next_state=findTransaction(container,next_state_id)
            
            #Print the state
            print("TRANSACTIONS")
            print("NEXT_STATE->",next_state.ID)

            log2.append(addToLog(next_state))
            ExploreGraph(next_state)
        
        elif(substates!=[]):
            #Explore a random state
            start=random.randint(0,len(substates)-1)
            next_state=substates[start]
            
            #Print the state
            print("SUBSTATE")
            print("NEXT_STATE->",next_state.ID)

            #log2.append(log2[-1]+":{"+next_state.ID)
            log2.append(addToLog(next_state))
            ExploreGraph(next_state)


def Exploration(state,container):
    print()
    print("---CURRENT STATE: "+state.ID+"---")
    print("Choose transitions to execute using numbers:")

    #Print all possible transitions
    counter=0
    list_tran=[]
    for trn in state.Transitions:
        print(str(counter)+":",end="")
        print(trn)
        list_tran.insert(counter,trn)
        counter+=1

    #Insert transition to execute from the current state
    next_tran=int(input("Insert number: "))
    next_state=list_tran[next_tran][1]

    next=None
    print(container.Subsets)
    for states in container.Subsets:
        if(states.ID==next_state):
            next=states

    if next.initial is not None:
        Exploration(next.initial,next)
    else:
        Exploration(next)


log=[]

log2=[]

if(__name__=="__main__"):

    #open the statechart json file
    statechart_j=open('xstate_visualization_statechart_context.json')

    #returns the JSON object as a dictionary
    statechart_dict=json.load(statechart_j)

    #Function to create the graph implementation
    #create_graph(statechart_dict.get('states'),graph)

    #if(child=="rest"):
    #    state_machine.initialState=new_state

    root_node=State("vis")
    state_machine=StateMachine(root_node)

    #root_node.Container=state_machine

    CreateGraph(statechart_dict.get('states'),root_node)
   
    #root_state.Subsets.append(State("scatter"))
    #root_state.Subsets.append(State("barchart"))

    print("----------------------------")
    print("Graph representation: ")
    PrintGraph(root_node)


    graph_context={}
    for elem in statechart_dict.get('context'):
        if(statechart_dict.get('context').get(elem) is not None):
            graph_context[elem] = statechart_dict.get('context').get(elem)
    
    print("GRAPH_CONTEXT:",json.dumps(graph_context,indent=4))


    Exploration(root_node.Subsets[0],root_node)

    #log2.append(root_node.ID)
    #ExploreGraph(root_node)

    #print("\n-------------LOG:-----------")
    #print(log)

    #print("\n-------------LOG2:-----------")
    #print(log2)