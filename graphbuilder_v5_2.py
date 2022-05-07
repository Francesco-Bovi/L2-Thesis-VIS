from hashlib import new
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

#Click, if we have height and width we check where to click
#Otherwise we click on the element at the middle (Selenium will do this)
def Click(height,width):

    if(height!="auto" and width!="auto"):

        #Choose randomly a point to click
        xClick = random.uniform(0,height-1)
        yClick = random.uniform(0,width-1)

        return (xClick,yClick)

    else:

        return None

#BRUSH FUNCTION
def Brush(brushableInfo):
    
    actionType = retTypeAction()

    directions = brushableInfo["directions"]

    brushExtent = brushableInfo["brush_extent"]

    selectionExtent = brushableInfo["selection_extent"]

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
            newSelectionExtent = [xStartBrush,yStartBrush],[xStartBrush,yStartBrush + heightBrush*(2/3)]

    return newSelectionExtent

#PANNINGBRUSH FUNCTION
def retBrush_PanBrush(actionType,width,height,xStartBrush,xEndBrush,yStartBrush,yEndBrush,xDirections,yDirections):

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

    xMove = xDirections[xMove]
    yMove = yDirections[yMove]


    newSelectionExtent = retBrush_PanBrush(actionType,width,height,xStartBrush,xEndBrush,yStartBrush,yEndBrush,xMove,yMove)

    print(newSelectionExtent)

    return newSelectionExtent

#ZOOM and PANNINGZOOM FUNCTION
#This is probably used only in the case of the "wheel", since with "dbclick" we have a fixed scale
def Zoom(zoomInfo):

    actionType = retTypeAction()

    width = zoomInfo["width"]
    height = zoomInfo["hieght"]

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

    xMove = xDirections[xMove]
    yMove = yDirections[yMove]

    return [actionType,(xStart,yStart),(xMove,yMove)]


#SLIDER CHANGE D3 (in which we know only the handler)
def SliderD3(sliderInfo):

    minValue = sliderInfo["aria-valuemin"]
    maxValue = sliderInfo["aria-valuemax"]
    currentValue = sliderInfo["aria-valuenow"]


#SLIDER CHANGE HTML
#This is the case when class = "input" and type = "range"
def SliderHtml(sliderInfo):

    minValue = sliderInfo["min"]
    maxValue = sliderInfo["max"]
    
    #Per ora escludiamo di averlo
    # currentValue = sliderInfo["value"]

    width = sliderInfo["width"]

    actionType = retTypeAction()

    return ["range",actionType,(minValue,maxValue,width)]


#SELECT DROPDOWN HTML
def selectDropdownHtml(selectInfo):

    possibleValues = selectInfo["value"]

    nextValueIndex = random.randint(0,len(possibleValues)-1)

    nextValue = possibleValues[nextValueIndex]["value"]

    return nextValue

#CHECKBOX HTML (the event is "change" but what is needed is a simple click)

#INPUT TYPE NUMER HTML
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


def retTypeAction():
    typeActions = ["L","M","H"]

    return typeActions[random.randint(0,2)]
    
def updateValue(graph,state,newValue):

    attributesList = graph[state]["attributes"]

    for elem in attributesList:
        if(elem["name"] == "value"):
            elem["value"] = newValue

#Check when interrupt the exploration
def CheckScore(graphVisit):

    for state in graphVisit:
        
        #print(state)
        for node in graphVisit[state]:

            if(node["visit"]!=None):
                print("STATE: "+state + " NODE: " + node["id"] + " visit: " + str(node["visit"]))
                if(node["visit"]==0):
                    return 0
    
    return 1

#Update the graph of the visits
def UpdateScore(graphVisit,state,idNode):

    for node in graphVisit[state]:

        if(node["id"] == idNode):

            if(node["visit"]!=None):

                node["visit"]+=1

    return

def retVisitNode(graphVisit,state,idNode):

    for node in graphVisit[state]:
    
        if(node["id"]== idNode):

            return node["visit"]

def ExplorationState(graph,graphVisit,state,stateNumber):
    global explorationSequence

    print(graphVisit)

    """
    if(CheckScore(graphVisit)):
        return

    nStates = len(state)

    currentState = None

    #We give priority to non visited nodes
    for node in state:
        idNode = node["id"]
        if(retVisitNode(graphVisit,stateNumber,idNode) == 0 and str(node["leadsToState"]) != "-1"):

            currentState = node

    #We must go random if we have already visited all the nodes in a state
    if(currentState==None):

        stateOk = 0
        while(not stateOk):

            #Go randomly
            randomState = random.randint(0,nStates-1)

            #current State by going randomly
            currentState = state[randomState]

            #-1 if the event cannot be triggered there
            if(str(currentState["leadsToState"]) != "-1"):
                stateOk = 1
    """

    currentState = state

    idNode = currentState["id"]
    eventNode  = currentState["event"]
    stylesNode = currentState["styles"]
    attributeNode = currentState["attributes"]
    tagNode = currentState["tag"]
    brushableNode = currentState["brushable"]
    zoomableNode = currentState["zoomable"]

    #print("STATE: "+ stateNumber + "| ID: "+ idNode)

    if(eventNode == "click"):

        #If the tag is button we don't need any other information
        if(tagNode == "button"):

            explorationState = {"selector":idNode,"event":eventNode,"info":None}

            explorationSequence.append(explorationState)
            UpdateScore(graphVisit,stateNumber,idNode)

        else:

            width = stylesNode["width"]
            height = stylesNode["height"]

            infoClick = Click(height,width)

            explorationState = {"selector":idNode,"event":eventNode,"info":infoClick}

            explorationSequence.append(explorationState)
            UpdateScore(graphVisit,stateNumber,idNode)

        #Now go to new state
        #ExplorationState(graph,graphVisit,graph[str(currentState["leadsToState"])],str(currentState["leadsToState"]))

    #For the moment we try to not distinguish them "mouseover" and "mouseleave"
    elif(eventNode == "mouseover" or eventNode == "mouseenter"):

        explorationState = {"selector":idNode,"event":eventNode,"info":None}

        explorationSequence.append(explorationState)
        UpdateScore(graphVisit,stateNumber,idNode)

        #Now go to new state
        #ExplorationState(graph,graphVisit,graph[str(currentState["leadsToState"])],str(currentState["leadsToState"]))

    elif(eventNode == "mouseout" or eventNode=="mouseleave"):

        infoOut = None

        #If it's a circle we know its radius
        if(tagNode == "circle"):

            infoOut = float(attributeNode["r"])

        elif(stylesNode["height"]!=None or stylesNode["width"]!=None):

            infoOut = (stylesNode["height"],stylesNode["width"])

        explorationState = {"selector":idNode,"event":eventNode,"info":infoOut}

        #explorationSequence.append(explorationState)
        UpdateScore(graphVisit,stateNumber,idNode)
        #ExplorationState(graph,graphVisit,graph[str(currentState["leadsToState"])],str(currentState["leadsToState"]))


    elif(eventNode == "mousedown"):

        if(brushableNode==None and zoomableNode==None):

            explorationState = {"selector":idNode,"event":eventNode,"info":None}

            explorationSequence.append(explorationState)
            UpdateScore(graphVisit,stateNumber,idNode)

            #ExplorationState(graph,graphVisit,graph[str(currentState["leadsToState"])],str(currentState["leadsToState"]))

        elif(brushableNode!=None):

            newSelectionExtent = Brush(brushableNode)

            explorationState = {"selector":idNode,"event":eventNode,"info":newSelectionExtent}

            explorationSequence.append(explorationState)
            UpdateScore(graphVisit,stateNumber,idNode)


    elif(eventNode == "mouseup"):

        explorationState = {"selector":idNode,"event":eventNode,"info":None}

        explorationSequence.append(explorationState)
        UpdateScore(graphVisit,stateNumber,idNode)

        #ExplorationState(graph,graphVisit,graph[str(currentState["leadsToState"])],str(currentState["leadsToState"]))

    elif(eventNode == "input"):

        if(attributeNode["type"]!=None):

            if(attributeNode["type"]=="range"):

                sliderHtmlInfo = {"min":int(attributeNode["min"]),"max":int(attributeNode["max"]),"width":stylesNode["width"]}

                explorationState = {"selector":idNode,"event":eventNode,"info": SliderHtml(sliderHtmlInfo)}

                explorationSequence.append(explorationState)
                UpdateScore(graphVisit,stateNumber,idNode)

            elif(attributeNode["type"]=="number"):

                numberInfo = {"min":int(attributeNode["min"]),"max":int(attributeNode["max"]),"value":int(attributeNode["value"]),"step":int(attributeNode["step"])}

                explorationState = {"selector":idNode,"event":eventNode,"info": ["number",inputNumberHtml(numberInfo)]}

                explorationSequence.append(explorationState)
                UpdateScore(graphVisit,stateNumber,idNode)
    
    #elif(eventNode == "change"):

    #    if(tagNode=="select"):



    #elif(eventNode == "facsimile_back"):

        #Since this is not a real event but just to go back to a state

        #explorationState = {"selector":idNode,"event":eventNode,"info":None}

        #explorationSequence.append(explorationState)
        #UpdateScore(graphVisit,stateNumber,idNode)

        #ExplorationState(graph,graphVisit,graph[str(currentState["leadsToState"])],str(currentState["leadsToState"]))
        
    return  


#Here we make a preprocessing of the JSON statechart
def statechartPreProcessing(statechart):

    newGraph = {}
    for state in statechart:

        #Add a node for each possible state
        newGraph[str(state["stateId"])] = []

        #print(state)

        for node in state["ieo"]:

            newNode = {}
            
            newNode["id"] = node["nodeSelector"]
            newNode["tag"] = node["tag"]
            newNode["data"] = node["data"]
            newNode["event"] = node["event"]
            newNode["brushable"] = node["brushable"]
            newNode["zoomable"] = node["zoomable"]
            newNode["leadsToState"] = node["leadsToState"]

            #Here we add the attributes by preprocessing them
            #So creating a dictionary with as key their name
            #Convert to integer if height or width
            newNode["attributes"] = {}
            for key in node["attributes"]:
                
                if(key["name"] == "height" or key["name"] == "width"):
                
                    newNode["attributes"][key["name"]] = float(key["value"])
                
                else:

                    newNode["attributes"][key["name"]] = key["value"]


            #Same for the styles but we need to remove "px"
            #at the end of the height and with and then convert to integer
            newNode["styles"] = {}
            for key in node["styles"]:
                
                if(key["name"] == "height" or key["name"] == "width"):

                    if(key["value"] != "auto"):
                
                        newNode["styles"][key["name"]] = float(key["value"][:len(key["value"])-2])

                    else:

                        newNode["styles"][key["name"]] = key["value"]


            print(newNode)

            #Add this node to the state
            newGraph[str(state["stateId"])].append(newNode)



    return newGraph



def createGraphVisit(graph):

    newGraph = {}

    for state in graph:

        newGraph[state] = []

        for node in graph[state]:

            newNode = {}
            newNode["id"] = node["id"]

            if(node["leadsToState"] != -1):

                newNode["visit"] = 0
            
            else:

                newNode["visit"] = None

            newGraph[state].append(newNode)

    return newGraph

if(__name__=="__main__"):
    
    #open the statechart json file
    statechart_j=open('C:/Users/Fran/Desktop/SAPIENZA/Engineering in Computer Science/Master Thesis/MatteoScript/material/statechart.json')

    #returns the JSON object as a dictionary
    statechart_dict=json.load(statechart_j)

    #Data structure for that will contain the graph
    graph = statechartPreProcessing(statechart_dict)

    #Print graph representation
    print("------------------------------------------------------------------------------")
    print("------------------------------------------------------------------------------")
    #print("Graph:",json.dumps(graph,indent=4))

    graphVisit = createGraphVisit(graph)
    print("GraphVisit:",json.dumps(graphVisit,indent=4))

    #Save graph on a file
    with open('statechart_v5_brushmorescatter.json', 'w') as fp:
        json.dump(graph, fp,  indent=4)

    print(transitionsList)
    print(eventsList)

    #Exploration of the graph
    #We know that "0" is the rest state, so the initial one
    #ExplorationState(graph,graphVisit,graph["0"],"0")

    #ExplorationState(graph,graphVisit,graph["0"],"0")

    for state in graph:

        for node in graph[state]:

            ExplorationState(graph,graphVisit,node,state)

    print(explorationSequence)
    
    #Save exploration sequence that will be passed to Selenium
    with open('explorationBrushMoreScatter.json', 'w') as fp:
        json.dump(explorationSequence, fp,  indent=4)

    print("------------------------------------------------------------------------------")