import json
import random
from textwrap import indent

#Function to give priority to some states
def PrioritySet(transition_list,graph_transition):
    print("The set of all transactions is:")
    for tran in graph_transition:
        print("|"+tran+"|",end="")
    input_tran=input("\nChoose to which transaction give priority and press ENTER (otherwise press N): ")
    print(input_tran)
    if(input_tran=="N"):
        return
    elif(input_tran not in graph_transition):
        print("------TRANSITION INSERTED DOESN'T EXIST, TRY AGAIN------")
        PrioritySet(transition_list,graph_transition)
    else:
        print("------TRANSITION INSERTED------")
        if(input_tran not in transition_list):
            transition_list.append(input_tran)
        PrioritySet(transition_list,graph_transition)

#Function used to add a key in the dictionary
def AddState(state,graph,parent):

    #Crete a key in the dictionary based on the parent
    sub_dict=[]
    graph[state+"_"+parent]=sub_dict

    return state+"_"+parent


#Add transitions or update to graph of transitions
def UpdateGraphTransition(tran):
    global graph_transition

    if tran in graph_transition:
        graph_transition[tran]+=1
    else:
        graph_transition[tran]=1

def AddTransitions(transitions,parent=None,child=None):
    transition_array=[]
    for t in transitions:
        target_array=transitions.get(t)
        for elem in target_array:

            UpdateGraphTransition(t)

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
        print("CHILD:",child)
        print("PARENT:",parent)
        print("PARENT TRANS:",parent_tranistions)

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

                print("TRANSITIONS:",transitions)

                #Add parent transitions to the transitions of the new state
                #Those will be inherited by the substates
                if(parent_tranistions!=None):
                    for t in parent_tranistions:
                        transitions.append(t)
                
                print("TRANSITION UPDATE",transitions)
                print("------------------------------------------------------------------------------")

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
        
                print("TRANSITIONS:",transitions)

                #Add parent transitions to the transitions of the new state
                #Those will be inherited by the substates
                if(parent_tranistions!=None):
                    for t in parent_tranistions:
                        transitions.append(t)
                
                print("TRANSITION UPDATE",transitions)
                print("------------------------------------------------------------------------------")
                
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
def ChooseNextState(graph_s,random_number,transactions,priority_tran):

    #I give priority to transactions with 0 score
    for t in transactions:
        possible_state=t[1]

        if(graph_s[possible_state]==0):
            return t

    #If there are no transitions among the one chosen by user
    #Go to the node not visited yet
    for t in transactions:
        possible_transition=t[0]

        #Give priority to transitions set by users
        if(possible_transition in priority_tran):
            return t

    #Otherwise I go random
    return transactions[random_number]

#Check if all states have been visited
def CheckScore(graph_s):
    for elem in graph_s:
        if(graph_s[elem]==0):
            return False
    return True

#Exploration of the Graph
def ExploreGraph(graph,graph_s,state,priority_tran):

    #Update score of a state
    graph_s[state]+=1

    #Check if we have vistied all states at least once
    if not CheckScore(graph_s):

        #List of all possible transitions from the current state
        list_possible_transitions=graph[state]
        len_list=len(list_possible_transitions)-1

        #Randon number for the possible next state (if all have been visited yet)
        ran_number=random.randint(0,len_list)

        next_transaction=ChooseNextState(graph_s,ran_number,list_possible_transitions,priority_tran)
        print("NEXT TRANSITION:",next_transaction[0]," TO:",next_transaction[1])

        #Continue the exploration
        ExploreGraph(graph,graph_s,next_transaction[1],priority_tran)
    
    else:

        #If all states have been visted at least once stop exploring the dictionary
        return


#Data structure that saves each transitions and how many times can be performed
#So how many times in each state we can find that transition
graph_transition=None

if(__name__=="__main__"):

    #open the statechart json file
    statechart_j=open('xstate_visualization_statechart_aux.json')

    #returns the JSON object as a dictionary
    statechart_dict=json.load(statechart_j)

    #Data structure for that will contain the graph
    graph={}

    #Data structure that saves each transitions and how many times can be performed
    #So how many times in each state we can find that transition
    graph_transition={}

    CreateGraph(statechart_dict.get('states'),graph,None,"vis")

    #Print graph representation
    print("------------------------------------------------------------------------------")
    print("------------------------------------------------------------------------------")
    print("Graph:",json.dumps(graph,indent=4))

    #Save graph on a file
    with open('statechartv3_2.json', 'w') as fp:
        json.dump(graph, fp,  indent=4)

    #Create auxiliar dictionary to store the score for each state
    graph_score=graph.copy()
    for key in graph_score:
        graph_score[key]=0

    #Print graph with scores
    print(graph_score)

    #Print graph with transitions
    print("Graph:",json.dumps(graph_transition,indent=4))


    #Data structure to save transitions and state with
    #Higher priority during the exploration
    priority_transaction=[]
    priority_states={}

    #Give priority to some states
    PrioritySet(priority_transaction,graph_transition)
    print(priority_transaction)

    #Choosa randomly the first state to visit
    start=random.randint(0,len(statechart_dict.get('states'))-1)
    list_graph=list(statechart_dict.get('states'))

    #Print inital state
    initial_state=list_graph[start]+"_vis"
    print("FIRST STATE:",initial_state)

    #Start the exploration of the graph
    ExploreGraph(graph,graph_score,initial_state,priority_transaction)

    print("------------------------------------------------------------------------------")
    print("Score Graph:",json.dumps(graph_score,indent=4))
    print("All states visited at least once")