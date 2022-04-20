import json
import random
from sys import exc_info

from matplotlib.pyplot import eventplot

eventsList = [
"CLICK", 
"DBCLICK",
"MOUSEMOVE", #When moving inside a widget
"MOUSEDOWN", #A pointing device button is pressed while the pointer is inside the element
"MOUSEUP", #When the pointing device is released (opposite of MOUSEDOWN)
"MOUSEENTER", #triggered when the mouse pointer enters the element
"MOUSEOVER", #is triggered when the mouse pointer enters the element, and its child
"MOUSELEAVE", #opposite of MOUSEOVER
"MOUSEOUT", #opposite of MOUSEOUT
"WHEEL",
"ZOOM",
"BRUSHTART",
"BRUSHEND"]

#Can we consider MOUSEDOWN + MOVE = DRAGSTART and then MOUSEUP = DRAGEND ?
#Can we consider WHEEL = ZOOM and DBCLICK also

transitionsList = []
explorationSequence = []
explorationStates = []
explorationActions = []

#Function used to add a key in the dictionary
def AddState(state,graph,parent):

    if(parent!=None):
        #Crete a key in the dictionary based on the parent
        sub_dict={}
        graph[state+"_"+parent]=sub_dict

        return state+"_"+parent
    
    else:
        sub_dict={}
        graph[state]=sub_dict

        return state

def AddTransitions(transitions,parent=None,child=None):
    global transitionsList

    transition_array=[]
    for t in transitions:
        target_array=transitions.get(t)
        for elem in target_array:

            if(t not in transitionsList):
                transitionsList.append(t)

            #If is a substate
            if(parent!=None):
                transition_array.append([t,elem["target"]+"_"+parent])
            
            #If is not a substate
            else:
                transition_array.append([t,elem["target"]])

    return transition_array

#Function to build the graph
def CreateGraph(states,graph,parent_tranistions=None,parent_context=None,parent=None):
    transitions=[]
    context={}
    for child in states:

        #Add the new key to the graph using the name of the parent (Container)
        child_name=AddState(child,graph,parent)

        if(states.get(child).get("initial") is not None):
            graph[child_name]["initial"] = states.get(child).get("initial")+"_"+child_name
        else:
            graph[child_name]["initial"] = None

        graph[child_name]["transitions"] = []
        graph[child_name]["values"] = []

        if(states.get(child).get("states") is not None):
            for value in states.get(child).get("states"):
                graph[child_name]["values"].append(value+"_"+child_name)            

        if(states.get(child).get("on") is not None):
            transitions=AddTransitions(states.get(child).get("on"),parent,child_name)
            #print(transitions)
            for t in transitions:
                graph[child_name]["transitions"].append(t)


        if(states.get(child).get("context") is not None):
            graph[child_name]["context"] = states.get(child).get("context")
            context = states.get(child).get("context")
        
        else:
            graph[child_name]["context"] = parent_context
            context = parent_context

        #Inheritance of transitions from container nodes
        if(parent_tranistions!=None):
            for t in parent_tranistions:
                graph[child_name]["transitions"].append(t)

        #Add parent transitions to the transitions of the new state
        #Those will be inherited by the substates
        if(parent_tranistions!=None):
            for t in parent_tranistions:
                transitions.append(t)

        #Go inside the substates
        if(states.get(child).get("states") is not None):
            CreateGraph(states.get(child).get("states"),graph,transitions,context,child_name)

#Check if all states have been visited
def CheckScore(graph_s):
    #print(json.dumps(graph_s,indent=4))
    for elem in graph_s:
        if(graph_s[elem]==0):
            return False
    return True

def Exploration(graph,graph_score,state):
    global explorationSequence
    global explorationActions
    global explorationStates

    while not CheckScore(graph_score):
        #print("---Current state: " + state +"---")

        graph_score[state]+=1

        if(graph[state]["initial"]!=None):
            state = graph[state]["initial"]
            graph_score[state]+=1
            explorationSequence.append(state)

        #Print all possible transitions
        counter=0
        list_tran=[]
        for trn in graph[state]["transitions"]:
            #print(str(counter)+":",end="")
            #print(trn)
            list_tran.insert(counter,trn)
            counter+=1

        #Next state and action chosen
        next_tran = random.randint(0,counter-1)
        state = list_tran[next_tran][1]
        action = list_tran[next_tran][0]

        #Add state to exploration
        explorationSequence.append(action)
        explorationActions.append(action)

        explorationSequence.append(state)
        explorationStates.append(state)

    return


def ContextAnalysis(graph):
    global explorationActions
    global explorationSequence
            

    """
    #Get context info
    context = graph[state]["context"]

    #Here I'am assuming that the CLICK action is used only to select something
    #So I can assume that I don't have NULL in "itemselected" and "numitems" 
    #of the context
    if(action=="CLICK"):
        #print("CHANGE CONTEXT AFTER CLICK")
        #print("Previous context: ",end="")
        #print(context)

        context["itemselected"] = random.randint(0,context["numitems"]-1)
        graph[state]["context"] = context

        #print("New context: ",end="")
        #print(context)
    
    #Assume here that the WHEEL action is used for zooming
    elif(action=="ZOOM" or action=="WHEEL"):
        #print("CHANGE CONTEXT AFTER ",action)
        #print("Previous context: ",end="")
        #print(context)

        zoomLevels = context["rangezoomlevels"]
        newZoomLevel = random.randint(zoomLevels[0],zoomLevels[1])

        diffZoomLevel = newZoomLevel - context["zoomlevel"]

        context["xstart"] = context["xstart"] + diffZoomLevel*context["zoomstep"]
        context["ystart"] = context["ystart"] + diffZoomLevel*context["zoomstep"]
        context["xwidth"] = context["xwidth"] - diffZoomLevel*context["zoomstep"]*2 #left and right
        context["ywidth"] = context["ywidth"] - diffZoomLevel*context["zoomstep"]*2

        context["zoomlevel"] = newZoomLevel

        graph[state]["context"] = context

        #print("New context: ",end="")
        #print(context)
        """

if(__name__=="__main__"):
    
    #open the statechart json file
    statechart_j=open('xstate_visualization_statechart_context.json')

    #returns the JSON object as a dictionary
    statechart_dict=json.load(statechart_j)

    #Data structure for that will contain the graph
    graph={}

    CreateGraph(statechart_dict.get('states'),graph,None,None)

    #Create auxiliar dictionary to store the score for each state
    graph_score=graph.copy()
    for key in graph_score:
        graph_score[key]=0

    #Print graph representation
    print("------------------------------------------------------------------------------")
    print("------------------------------------------------------------------------------")
    #print("Graph:",json.dumps(graph,indent=4))

    #Save graph on a file
    with open('statechart_v4.json', 'w') as fp:
        json.dump(graph, fp,  indent=4)

    print(transitionsList)
    print(eventsList)


    Exploration(graph,graph_score,"rest")

    print(explorationStates)
    print(explorationActions)

    print("------------------------------------------------------------------------------")