import json
from multiprocessing.connection import wait
import random
from sys import exc_info

from matplotlib.pyplot import eventplot

eventsList = [
"click", 
"dbclick",
"mousemove", #When moving inside a widget
"mousedown", #A pointing device button is pressed while the pointer is inside the element
"mouseup", #When the pointing device is released (opposite of MOUSEDOWN)
"mouseenter", #triggered when the mouse pointer enters the element
"mouseover", #is triggered when the mouse pointer enters the element, and its child
"mouseleave", #opposite of MOUSEOVER
"wheel", #opposite of MOUSEOUT
"zoom",
"brushstart",
"brushend"]

#Can we consider MOUSEDOWN + MOVE = DRAGSTART and then MOUSEUP = DRAGEND ?
#Can we consider WHEEL = ZOOM and DBCLICK also

transitionsList = []
explorationSequence = []


def retTypeAction():
    typeActions = ["L","M","H"]

    return typeActions[random.randint(0,2)]

def ExplorationState(graph,state):
    global explorationSequence

    events = graph[state]["events"]

    for event in events:

        explorationSequence.append(state)
        explorationSequence.append(events)

        if(event == "mousedown" or event=="touchstart"):

            #Check if the element is brushable
            if(graph[state]["brushable"]!=None):
                
                brushInfo = graph[state]["brushable"]

                #Check if brushing is only one direction or not
                if(brushInfo["directions"] == "xy"):

                    actionType = retTypeAction()

                    areaDimension = brushInfo["brush_extent"]

                    #Dimension of the brushable area
                    xDimension = areaDimension[1][0] - areaDimension[0][0]
                    yDimension = areaDimension[1][1] - areaDimension[0][1] 

                    if(actionType == "L"):

                        #Since type of action is "L" we divide by 4
                        xBrushDimension = random.uniform(0,xDimension/4)
                        yBrushDimension = random.uniform(0,yDimension/4)

                    elif(actionType == "M"):

                        #Since type of action is "M" we divide by 2
                        xBrushDimension = random.uniform(0,xDimension/2)
                        yBrushDimension = random.uniform(0,yDimension/2)

                    else:

                        #Since type of action is "H" we multiply to 2/3
                        xBrushDimension = random.uniform(0,xDimension*(2/3))
                        yBrushDimension = random.uniform(0,yDimension*(2/3))

                    #Now update info
                    xStartBrush = random.uniform(0,xDimension - xBrushDimension)
                    yStartBrush = random.uniform(0,yDimension - yBrushDimension)

                    graph[state]["brushable"]["brush_extent"] = [[xStartBrush,yStartBrush],[xStartBrush + xBrushDimension,yStartBrush + yBrushDimension]]

                elif(brushInfo["directions"] == "x"):

                    actionType = retTypeAction()

                    areaDimension = brushInfo["brush_extent"]

                    #Dimension of the brushable area
                    xDimension = areaDimension[1][0] - areaDimension[0][0]
                    yDimension = areaDimension[1][1] - areaDimension[0][1] 

                    if(actionType == "L"):

                        #Since type of action is "L" we divide by 4
                        xBrushDimension = random.uniform(0,xDimension/4)

                    elif(actionType == "M"):

                        #Since type of action is "M" we divide by 2
                        xBrushDimension = random.uniform(0,xDimension/2)

                    else:

                        #Since type of action is "H" we multiply to 2/3
                        xBrushDimension = random.uniform(0,xDimension*(2/3))

                    #Now update info
                    xStartBrush = random.uniform(0,xDimension - xBrushDimension)

                    #In this case we take all the "y area"
                    graph[state]["brushable"]["brush_extent"] = [[xStartBrush,0],[xStartBrush + xBrushDimension,yBrushDimension]]

                else:

                    actionType = retTypeAction()

                    areaDimension = brushInfo["brush_extent"]

                    #Dimension of the brushable area
                    xDimension = areaDimension[1][0] - areaDimension[0][0]
                    yDimension = areaDimension[1][1] - areaDimension[0][1] 

                    if(actionType == "L"):

                        #Since type of action is "L" we divide by 4
                        yBrushDimension = random.uniform(0,yDimension/4)

                    elif(actionType == "M"):

                        #Since type of action is "M" we divide by 2
                        yBrushDimension = random.uniform(0,yDimension/2)

                    else:

                        #Since type of action is "H" we multiply to 2/3
                        yBrushDimension = random.uniform(0,yDimension*(2/3))

                    #Now update info
                    yStartBrush = random.uniform(0,yDimension - yBrushDimension)

                    #In this case we take all the "y area"
                    graph[state]["brushable"]["brush_extent"] = [[0,yStartBrush],[xBrushDimension,yStartBrush + yBrushDimension]]

            #In this case we are doing a panning
            elif(graph[state]["zoombale"]!=None):
                #TODO: Check if zoomable and brushable together
                #with mousedown exists
                wait(1)
            
            else:
                #TODO: This is the case of dragging??
                #What info can we use in this case?
                wait(1)
                
        elif(event == "wheel" or event=="dbclick"):
            
            if(graph[state]["zoomable"]!=None):

                zoomInfo = graph[state]["zoomable"]

                if(actionType == "L"):
    
                    zoomInfo["scale"] = 1.2
                    #TODO: Vedere come cambiano anche translate_x e translate_y
                    #Ci serve??

                elif(actionType == "M"):

                    zoomInfo["scale"] = 1.4

                else:

                    zoomInfo["scale"] = 1.6

                #Update info
                graph[state]["zoomable"] = zoomInfo
        
        elif(event == "change"):

            tagElement = graph[state]["tag"]

            #When we have the select dropdown
            if(tagElement == "select"):

                possibleValues = []
                for elem in graph[state]["node"]:
                    possibleValues.append(elem["__data__"])

                newValue = possibleValues[random.randint(0,len(possibleValues)-1)]

                graph[state]["value"] = newValue

            #Maybe chan be radio button (?)
            elif(tagElement == "div"):
                #TODO: If there's a method since in div we have
                #a list of <input type="radio">
                wait(1)

            elif(tagElement == "input"):

                typeElement = graph[state]["type"]

                if(typeElement == "range"):

                    minValue = graph[state]["min"]
                    maxValue = graph[state]["max"]

                    newValue = random.randint(minValue,maxValue)

                    #Update value<<<
                    graph[state]["value"] = newValue

        elif(event == "input"):

            tagElement = graph[state]["tag"]

            if(tagElement == "input"):

                typeElement = graph[state]["type"]

                if(typeElement == "number"):

                    value = graph[state]["value"]

                    actionType = retTypeAction()

                    if(actionType == "L"):

                        newValue = value + 1

                    elif(actionType == "M"):

                        newValue = value + 2
                    
                    else: 

                        newValue = value + 3

                    #Update value
                    graph[state]["value"] = newValue



                    


if(__name__=="__main__"):
    
    #open the statechart json file
    statechart_j=open('xstate_visualization_statechart_context.json')

    #returns the JSON object as a dictionary
    statechart_dict=json.load(statechart_j)

    #Data structure for that will contain the graph
    graph={}

    #Print graph representation
    print("------------------------------------------------------------------------------")
    print("------------------------------------------------------------------------------")
    #print("Graph:",json.dumps(graph,indent=4))

    #Save graph on a file
    with open('statechart_v4.json', 'w') as fp:
        json.dump(graph, fp,  indent=4)

    print(transitionsList)
    print(eventsList)

    Exploration(graph,"rest")

    print(explorationSequence)

    print("------------------------------------------------------------------------------")