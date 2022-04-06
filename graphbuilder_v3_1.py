import json
import random
from textwrap import indent

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
                if(parent!=None):
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

        #We are not interested in hover or idle since we have considered them previoulsy
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


                """"
                #Check if it has parallels
                if(states.get(child).get("parallel") is not None):
                    for node in states.get(child).get("states"):

                        create_graph(states.get(node).get("states"),graph,transitions,parent)
                """

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
                    transition_initial_state=AddTransitions(states.get(child).get("states").get(initial_state).get("on"),child_name,child_name)
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

#Check if all states have been visited
def CheckScore(graph_s):
    for elem in graph_s:
        if(graph_s[elem]==0):
            return False
    return True

#Exploration of the Graph
def ExploreGraph(graph,graph_s,state):

    #Update score of a state
    graph_s[state]+=1

    print("Score Graph:",json.dumps(graph_s,indent=4))

    #Check if we have vistied all states at least once
    if not CheckScore(graph_s):

        list_possible_transitions=graph[state]
        len_list=len(list_possible_transitions)-1

        ran_number=random.randint(0,len_list)

        next_transaction=ChooseNextState(graph_s,ran_number,list_possible_transitions)
        print("NEXT TRANSITION:",next_transaction[0]," TO:",next_transaction[1])

        ExploreGraph(graph,graph_s,next_transaction[1])
    
    else:
        return


if(__name__=="__main__"):
    #open the statechart json file
    statechart_j=open('xstate_visualization_statechart.json')

    #returns the JSON object as a dictionary
    statechart_dict=json.load(statechart_j)

    #Data structure for that will contain the graph
    graph={}

    create_graph(statechart_dict.get('states'),graph,None,"vis")

    #Print graph representation
    print("------------------------------------------------------------------------------")
    print("------------------------------------------------------------------------------")
    #print("Graph representation: ",graph)
    #print("Graph:",json.dumps(graph,indent=4))

    #Save graph on a file
    with open('statechartv3_1.json', 'w') as fp:
        json.dump(graph, fp,  indent=4)

    #Create auxiliar dictionary to store the score for each state
    graph_score=graph.copy()
    for key in graph_score:
        graph_score[key]=0

    #Print graph with scores
    print(graph_score)

    start=random.randint(0,len(statechart_dict.get('states'))-1)
    print(statechart_dict.get('states'))
    list_graph=list(statechart_dict.get('states'))

    initial_state=list_graph[start]+"_vis"
    print("FIRST STATE:",initial_state)

    #ExploreGraph(graph,graph_score,initial_state)

    print("------------------------------------------------------------------------------")
    print("All states visited at least once")