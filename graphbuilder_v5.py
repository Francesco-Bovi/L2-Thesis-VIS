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

#BRUSH FUNCTION
"""
def Brush(brushableInfo):
    
    actionType = retTypeAction()

    directions = brushableInfo["directions"]

    brushExtent = brushableInfo["brushExtent"]

    selectionExtent = brushableInfo["selectionExtent"]

    #Object to return with the new selection extent
    newSelectionExtent = None

    #Case when the brushing can be done in all the dimensions
    if(directions == "xy"):

        #Dimension of the brushable area
        widthBrush = brushExtent[1][0] - brushExtent[0][0]
        heightBrush = brushExtent[1][1] - brushExtent[0][1]

        if(actionType == "L"):

            #In this case the area is 1/4 of the original

            #Find the starting points
            xStartBrush = random.uniform(0,widthBrush - widthBrush/4)
            yStartBrush = random.uniform(0,heightBrush - heightBrush/4)

            #New selection extent
            newSelectionExtent = [[xStartBrush,yStartBrush],[xStartBrush + widthBrush/4,yStartBrush + heightBrush/4]]
    

        elif(actionType == "M"):

            #In this case the area is 1/2 of the original

            #Find the starting points
            xStartBrush = random.uniform(0,widthBrush - widthBrush/2)
            yStartBrush = random.uniform(0,heightBrush - heightBrush/2)

            #New selection extent
            newSelectionExtent = [[xStartBrush,yStartBrush],[xStartBrush + widthBrush/2,yStartBrush + heightBrush/2]]
        
        else:

            #In this case the area is 2/3 of the original

            #Find the starting points
            xStartBrush = random.uniform(0,widthBrush - widthBrush*(2/3))
            yStartBrush = random.uniform(0,heightBrush - heightBrush*(2/3))

            #New selection extent
            newSelectionExtent = [[xStartBrush,yStartBrush],[xStartBrush + widthBrush*(2/3),yStartBrush + heightBrush*(2/3)]]

    elif(directions == "x"):

        #Dimension of the brushable area
        widthBrush = brushExtent[1][0] - brushExtent[0][0]
        heightBrush = brushExtent[1][1] - brushExtent[0][1]

        if(actionType == "L"):

            #In this case the area is 1/4 of the original

            #Find the starting points
            xStartBrush = random.uniform(0,widthBrush - widthBrush/4)
            yStartBrush = heightBrush/2

            #New selection extent
            newSelectionExtent = [[xStartBrush,yStartBrush],[xStartBrush + widthBrush/4,yStartBrush]]
    

        elif(actionType == "M"):

            #In this case the area is 1/2 of the original

            #Find the starting points
            xStartBrush = random.uniform(0,widthBrush - widthBrush/2)
            yStartBrush = heightBrush/2

            #New selection extent
            newSelectionExtent = [[xStartBrush,yStartBrush],[xStartBrush + widthBrush/2,yStartBrush]]
        
        else:

            #In this case the area is 2/3 of the original

            #Find the starting points
            xStartBrush = random.uniform(0,widthBrush - widthBrush*(2/3))
            yStartBrush = heightBrush/2

            #New selection extent
            newSelectionExtent = [[xStartBrush,yStartBrush],[xStartBrush + widthBrush*(2/3),yStartBrush]]

    else:

        #Dimension of the brushable area
        widthBrush = brushExtent[1][0] - brushExtent[0][0]
        heightBrush = brushExtent[1][1] - brushExtent[0][1]

        if(actionType == "L"):

            #In this case the area is 1/4 of the original

            #Find the starting points
            xStartBrush = widthBrush/2
            yStartBrush = random.uniform(0,heightBrush - heightBrush/4)

            #New selection extent
            newSelectionExtent = [[xStartBrush,yStartBrush],[xStartBrush,yStartBrush + heightBrush/4]]
    

        elif(actionType == "M"):

            #In this case the area is 1/2 of the original

            #Find the starting points
            xStartBrush = widthBrush/2
            yStartBrush = random.uniform(0,heightBrush - heightBrush/2)

            #New selection extent
            newSelectionExtent = [[xStartBrush,yStartBrush],[xStartBrush,yStartBrush + heightBrush/2]]
        
        else:

            #In this case the area is 2/3 of the original

            #Find the starting points
            xStartBrush = widthBrush/2
            yStartBrush = random.uniform(0,heightBrush - heightBrush*(2/3))

            #New selection extent
            newSelectionExtent = [[xStartBrush,yStartBrush],[xStartBrush,yStartBrush + heightBrush*(2/3)]]

    return newSelectionExtent
"""

#PANNINGBRUSH FUNCTION

"""

def retBrush_PanBrush(actionType,width,height,xStartBrush,xEndBrush,yStartBrush,yEndBrush):

    #It depends by the type of action
    divisor = None

    #What we must return
    newSelectionExtent = None

    if(actionType == "L"):

        divisor = 1/2
    
    elif(actionType == "M"):

        divisor = 1/4

    else:

        divisor = 2/3

    if(xDirections == "right"):
    
            maxMovement = width - xEndBrush

            moveRight = maxMovement*divisor

            if(yDirections == "up"):

                maxMovement = height - xStartBrush

                moveUp = maxMovement*divisor

                #Update in new selection extent position (when going up we substract, while going right we add)
                newSelectionExtent = [[xStartBrush + moveRight,yStartBrush - moveUp],[xEndBrush + moveRight, yEndBrush - moveUp]]

            #This means we're moving down
            else:

                maxMovement = height - xEndBrush

                moveDown = maxMovement*divisor

                #Update in new selection extent position (when going down we add, while going right we add)
                newSelectionExtent = [[xStartBrush + moveRight,yStartBrush + moveDown],[xEndBrush + moveRight, yEndBrush + moveDown]]

        #Means we are going left
        else:
            
            maxMovement = width - xStartBrush

            moveLeft = maxMovement*divisor

            if(yDirections == "up"):
    
                maxMovement = height - xStartBrush

                moveUp = maxMovement*divisor

                #Update in new selection extent position (when going up we substract, while going left we substract)
                newSelectionExtent = [[xStartBrush - moveLeft,yStartBrush - moveUp],[xEndBrush - moveLeft, yEndBrush - moveUp]]

            #This means we're moving down
            else:

                maxMovement = height - xEndBrush

                moveDown = maxMovement*divisor

                #Update in new selection extent position (when going down we add, while going left we substarct)
                newSelectionExtent = [[xStartBrush - moveLeft,yStartBrush + moveDown],[xEndBrush - moveLeft, yEndBrush + moveDown]]

    return newSelectionExtent

def PanBrush(brushableInfo):
    
    actionType = retTypeAction()

    directions = brushableInfo["directions"]

    brushExtent = brushableInfo["brushExtent"]

    selectionExtent = brushableInfo["selectionExtent"]

    #Variable to update
    newSelectionExtent = None

    #Dimension of the brushable area
    width = brushExtent[1][0] - brushExtent[0][0]
    height = brushExtent[1][1] - brushExtent[0][1]

    #Dimension of the pannable area of the brush
    widthBrush = brushExtent[1][0] - brushExtent[0][0]
    heightBrush = brushExtent[1][1] - brushExtent[0][1]

    #Starting,Ending and Middle point of the brushArea
    xStartBrush = brushExtent[0][0]
    yStartBrush = brushExtent[0][1]

    xEndBrush = xStartBrush + widthBrush
    yEndBrush = yStartBrush + heightBrush

    xMiddleBrush = xStartBrush + widthBrush/2
    yMiddleBrush = yStartBrush + heightBrush/2

    #Here randomly is chosen where moving between "left/right" and "up/down"
    xMove = random.randint(0,1)
    yMove = random.randint(0,1)

    xDirections = ["right","left"]
    yDirections = ["up","down"]

    xMove = xDirections[XMove]
    yMove = yDirections[yMove]


    newSelectionExtent = retBrush_PanBrush(actionType,width,height,xStartBrush,xEndBrush,yStartBrush,yEndBrush)

    print(newSelectionExtent)

    return newSelectionExtent

"""

#ZOOM and PANNINGZOOM FUNCTION
#This is probably used only in the case of the "wheel", since with "dbclick" we have a fixed scale
"""
def Zoom():

    actionType = retTypeAction()

    #Starting point from which zooming 
    xStart = random.uniform(0,width)
    yStart = random.uniform(0,height)

    return [actionType,(xStart,yStart)]

#Returns an array with all the information
def PanZoom(height,width):

    actionType = retTypeAction()

    #Starting point from which panning starts
    xStart = random.uniform(0,width)
    yStart = random.uniform(0,height)

    #Here randomly is chosen where moving between "left/right" and "up/down"
    xMove = random.randint(0,1)
    yMove = random.randint(0,1)

    xDirections = ["right","left"]
    yDirections = ["up","down"]

    xMove = xDirections[XMove]
    yMove = yDirections[yMove]

    return [actionType,(xStart,yStart),(xMove,yMove)]

"""

#SLIDER CHANGE D3 (in which we know only the handler)

"""

def SliderD3(sliderInfo):

    minValue = sliderInfo["aria-valuemin"]
    maxValue = sliderInfo["aria-valuemax"]
    currentValue = sliderInfo["aria-valuenow"]

"""


#SLIDER CHANGE HTML
#This is the case when class = "input" and type = "range"
"""

def SliderHtml(sliderInfo):

    minValue = sliderInfo["min"]
    maxValue = sliderInfo["max"]
    currentValue = sliderInfo["value"]

    width = sliderInfo["width"]

    actionType = retTypeAction()

    return [actionType,minValue,maxValue,currentValue,width]

"""

#SELECT DROPDOWN HTML
"""

def selectDropdownHtml(selectInfo):

    possibleValues = selectInfo["value"]

    nextValueIndex = random.randint(0,len(possibleValues)-1)

    nextValue = possibleValues[nextValueIndex]["value"]

    return nextValue

"""

#CHECKBOX HTML (the event is "change" but what is needed is a simple click)

#INPUT TYPE NUMER HTML
"""

def inputNumberHtml(inputInfo):

    minValue = inputInfo["min"]
    maxValue = inputInfo["max"]
    currentValue = inputInfo["value"]

    step = inputInfo["step"]

    possibleValues = []
    for i in range(minValue,maxValue,step):
        possibleValues.append(i)
    
    possibleValues.append(maxValue)

    nextValue = random.randint(0,len(possibleValues)-1)

    return nextValue

"""
def retTypeAction():
    typeActions = ["L","M","H"]

    return typeActions[random.randint(0,2)]
    
def updateValue(graph,state,newValue):

    attributesList = graph[state]["attributes"]

    for elem in attributesList:
        if(elem["name"] == "value"):
            elem["value"] = newValue

def ExplorationState(graph,state):
    global explorationSequence

    print("State: ",state)

    events = graph[state]["events"]
    #print("Events: ",events)

    for event in events:

        explorationSequence.append(state)
        explorationSequence.append(event)

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

                    #Update the area of brushing
                    graph[state]["brushable"]["selection_extent"] = [[xStartBrush,yStartBrush],[xStartBrush + xBrushDimension,yStartBrush + yBrushDimension]]

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
                    graph[state]["brushable"]["selection_extent"] = [[xStartBrush,0],[xStartBrush + xBrushDimension,yDimension]]

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
                    graph[state]["brushable"]["selection_extent"] = [[0,yStartBrush],[xDimension,yStartBrush + yBrushDimension]]

            #In this case we are doing a panning
            elif(graph[state]["zoomable"]!=None):
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
                for elem in graph[state]["attributes"]:

                    if(elem["name"] == "select"):
                        for nestedElem in elem["value"]:
                            
                            possibleValues.append(nestedElem["value"])

                newValue = possibleValues[random.randint(0,len(possibleValues)-1)]

                #Update value in graph
                for elem in graph[state]["attribute"][0]:
                    if(elem["value"] == newValue):
                        elem["selected"] = True

                    else:

                        elem["selected"] = False

            #Maybe can be radio button (?) (https://d3-graph-gallery.com/graph/interactivity_button.html)
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

                    #Update value
                    graph[state]["value"] = newValue

        elif(event == "input"):

            tagElement = graph[state]["tag"]

            if(tagElement == "input"):

                attributeValues = graph[state]["attributes"]

                typeElement = None
                currentValue = None

                for elem in attributeValues:
                    if(elem["name"] == "type"):
                        typeElement = elem["value"]

                    elif(elem["name"] == "value"):
                        currentValue = elem["value"]

                #Specific time when we have a number
                if(typeElement == "number"):

                    actionType = retTypeAction()

                    if(actionType == "L"):

                        newValue = float(currentValue) + 1

                    elif(actionType == "M"):

                        newValue = float(currentValue) + 2
                    
                    else: 

                        newValue = float(currentValue) + 3

                    #Update value
                    updateValue(graph,state,newValue)

        #This is the case for example in the sliders (https://bl.ocks.org/johnwalley/raw/e1d256b81e51da68f7feb632a53c3518/?raw=true)
        elif(event == "keydown"):

            tagElement = graph[state]["tag"]

            #This is probably the case in which we have a slider and the path is an handler
            if(tagElement == "path"):

                attributeValues = graph[state]["attributes"]

                minValue = None
                maxValue = None
                currentValue = None

                for field in attributeValues:

                    if(field["name"] == "aria-valuemax"):

                        maxValue = float(field["value"])

                    elif(field["name"] == "aria-valuemin"):

                        minValue = float(field["value"])
                    
                    elif(field["name"] == "aria-valuenow"):

                        currentValue = float(field["value"])

                    #TODO: Handle case when values are not float, like dates

                
    return

                    
def Exploration(graph):

    for state in graph:
        ExplorationState(graph,state)

        if(graph[state]["child"]!=None):
            Exploration(graph[state]["child"])

if(__name__=="__main__"):
    
    #open the statechart json file
    statechart_j=open('crossfilter_visualization_statechart_htmlinfo.json')

    #returns the JSON object as a dictionary
    statechart_dict=json.load(statechart_j)

    #Data structure for that will contain the graph
    graph={}
    graph=statechart_dict

    #Print graph representation
    print("------------------------------------------------------------------------------")
    print("------------------------------------------------------------------------------")
    #print("Graph:",json.dumps(graph,indent=4))

    #Save graph on a file
    with open('statechart_v5.json', 'w') as fp:
        json.dump(graph, fp,  indent=4)

    print(transitionsList)
    print(eventsList)

    #Exploration of th graph
    Exploration(graph)

    print(explorationSequence)
    print("Graph:",json.dumps(graph,indent=4))

    print("------------------------------------------------------------------------------")