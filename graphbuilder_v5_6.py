from hashlib import new
import json
from multiprocessing.connection import wait
import random
from random import choice
from sys import exc_info

from matplotlib.pyplot import eventplot
from numpy import empty

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


def checkPresenceOfLoop(graph,node):

    for destinations in graph[node]:
        if(destinations == node):
            return 1

    return 0

listPaths = []
'''A recursive function to print all paths from 'u' to 'd'.
visited[] keeps track of vertices in current path.
path[] stores actual vertices and path_index is current
index in path[]'''
def printAllPathsUtil(u, d, visited, path, newGraph):

    # Mark the current node as visited and store in path
    visited[u]=True
    path.append(u)

    # If current vertex is same as destination, then print
    # current path[]
    if u == d:

        newPath = path.copy()
        if(newPath not in listPaths):
            listPaths.append(newPath)
            print (path)

    else:
        # If current vertex is not destination
        # Recur for all the vertices adjacent to this vertex
        for i in newGraph[u]:
            if visited[i]==False:
                printAllPathsUtil(i, d, visited, path, newGraph)
                    
    # Remove current vertex from path[] and mark it as unvisited
    path.pop()
    visited[u]=False


# Prints all paths from 's' to 'd'
def printAllPaths(s, d, newGraph):

    # Mark all the vertices as not visited
    visited =[False]*(len(newGraph))

    # Create an array to store paths
    path = []

    # Call the recursive helper function to print all paths
    printAllPathsUtil(s, d, visited, path, newGraph)

"""
outputEdges = []
def DFS(graphN,state,graphVisit):
    
    graphVisit[state] = 1
    for i in range (0,len(graphN[state])):
        if([state,graphN[state][i]] not in outputEdges):
            outputEdges.append([state,i])

        print(i)
        if(graphVisit[graphN[state][i]] == 0):
            DFS(graphN,graphN[state][i],graphVisit)

    return
"""

#Click, if we have height and width we check where to click
#Otherwise we click on the element at the middle (Selenium will do this)
#CHECKBOX HTML (the event is "change" but what is needed is a simple click)
def Click(height,width):

    if(height!="auto" and width!="auto"):

        #Choose randomly a point to click
        xClick = random.randint(0,width-1)
        yClick = random.randint(0,height-1)

        return (xClick,yClick)

    else:

        return None

#PAN BRUSH
def PanBrush(directions,brushExtent,selectionExtent):

    #Dimension of the brushable area
    width = brushExtent[1][0] - brushExtent[0][0]
    height = brushExtent[1][1] - brushExtent[0][1]

    #Dimension of the pannable area of the brush
    widthBrush = selectionExtent[1][0] - selectionExtent[0][0]
    heightBrush = selectionExtent[1][1] - selectionExtent[0][1]

    #Starting,Ending and Middle point of the brushArea
    xStartBrush = selectionExtent[0][0]
    yStartBrush = selectionExtent[0][1]

    xEndBrush = xStartBrush + widthBrush
    yEndBrush = yStartBrush + heightBrush

    xMiddleBrush = xStartBrush + widthBrush/2
    yMiddleBrush = yStartBrush + heightBrush/2

    #print("xMiddle " + str(xMiddleBrush))

    xMove = None
    yMove = None

    if(directions == "xy"):

        #Here randomly is chosen where moving between "left/right" and "up/down"
        xMove = random.randint(0,1)
        yMove = random.randint(0,1)

        xDirections = ["right","left"]
        yDirections = ["up","down"]

        xMove = xDirections[xMove]
        yMove = yDirections[yMove]
    
    elif(directions == "x"):

        xMove = random.randint(0,1)

        xDirections = ["right","left"]

        xMove = xDirections[xMove]

    else:

        yMove = random.randint(0,1)

        yDirections = ["up","down"]

        yMove = yDirections[yMove]

    if(xMove == "right"):
        
        maxMovement = width - xEndBrush

        moveX = random.randint(0,maxMovement)
    
    elif(xMove == "left"):

        maxMovement = -xStartBrush

        moveX = random.randint(maxMovement,0)
    
    else:

        moveX = 0


    if(yMove == "up"):

        maxMovement = -yStartBrush

        moveY = random.randint(maxMovement,0)

    #This means we're moving down
    elif(yMove == "down"):

        maxMovement = height - yEndBrush

        moveY = random.randint(0,maxMovement)

    else: 

        moveY = 0

    return [int(moveX),int(moveY),xMiddleBrush,yMiddleBrush,width,height]

#BRUSH FUNCTION
def Brush(actionType,brushableInfo):
    
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
            xStartBrush = random.randint(0,widthBrush - int(widthBrush/4))
            yStartBrush = random.randint(0,heightBrush - int(heightBrush/4))

            #New selection extent
            newSelectionExtent = [[xStartBrush,yStartBrush],[xStartBrush + int(widthBrush/4),yStartBrush + int(heightBrush/4)]]
    

        elif(actionType == "M"):

            #In this case the area is 1/2 of the original

            #Find the starting points
            xStartBrush = random.randint(0,widthBrush - int(widthBrush/2))
            yStartBrush = random.randint(0,heightBrush - int(heightBrush/2))

            #New selection extent
            newSelectionExtent = [[xStartBrush,yStartBrush],[xStartBrush + int(widthBrush/2),yStartBrush + int(heightBrush/2)]]
        
        else:

            #In this case the area is 2/3 of the original

            #Find the starting points
            xStartBrush = random.randint(0,widthBrush - int(widthBrush*(2/3)))
            yStartBrush = random.randint(0,heightBrush - int(heightBrush*(2/3)))

            #New selection extent
            newSelectionExtent = [[xStartBrush,yStartBrush],[xStartBrush + int(widthBrush*(2/3)),yStartBrush + int(heightBrush*(2/3))]]

    elif(directions == "x"):

        #Dimension of the brushable area
        widthBrush = brushExtent[1][0] - brushExtent[0][0]
        heightBrush = brushExtent[1][1] - brushExtent[0][1]

        if(actionType == "L"):

            #In this case the area is 1/4 of the original

            #Find the starting points
            xStartBrush = random.randint(0,widthBrush - int(widthBrush/4))
            yStartBrush = int(heightBrush/2)

            #New selection extent
            newSelectionExtent = [[xStartBrush,yStartBrush],[xStartBrush + int(widthBrush/4),yStartBrush]]
    

        elif(actionType == "M"):

            #In this case the area is 1/2 of the original

            #Find the starting points
            xStartBrush = random.randint(0,widthBrush - int(widthBrush/2))
            yStartBrush = int(heightBrush/2)

            #New selection extent
            newSelectionExtent = [[xStartBrush,yStartBrush],[xStartBrush + widthBrush/2,yStartBrush]]
        
        else:

            #In this case the area is 2/3 of the original

            #Find the starting points
            xStartBrush = random.randint(0,widthBrush - int(widthBrush*(2/3)))
            yStartBrush = int(heightBrush/2)

            #New selection extent
            newSelectionExtent = [[xStartBrush,yStartBrush],[xStartBrush + int(widthBrush*(2/3)),yStartBrush]]

    else:

        #Dimension of the brushable area
        widthBrush = brushExtent[1][0] - brushExtent[0][0]
        heightBrush = brushExtent[1][1] - brushExtent[0][1]

        if(actionType == "L"):

            #In this case the area is 1/4 of the original

            #Find the starting points
            xStartBrush = int(widthBrush/2)
            yStartBrush = random.randint(0,heightBrush - int(heightBrush/4))

            #New selection extent
            newSelectionExtent = [[xStartBrush,yStartBrush],[xStartBrush,yStartBrush + int(heightBrush/4)]]
    

        elif(actionType == "M"):

            #In this case the area is 1/2 of the original

            #Find the starting points
            xStartBrush = int(widthBrush/2)
            yStartBrush = random.randint(0,heightBrush - int(heightBrush/2))

            #New selection extent
            newSelectionExtent = [[xStartBrush,yStartBrush],[xStartBrush,yStartBrush + int(heightBrush/2)]]
        
        else:

            #In this case the area is 2/3 of the original

            #Find the starting points
            xStartBrush = int(widthBrush/2)
            yStartBrush = random.randint(0,heightBrush - int(heightBrush*(2/3)))

            #New selection extent
            newSelectionExtent = [xStartBrush,yStartBrush],[xStartBrush,yStartBrush + int(heightBrush*(2/3))]
    
    
    return newSelectionExtent

#ZOOM and PANNINGZOOM FUNCTION
#This is probably used only in the case of the "wheel", since with "dbclick" we have a fixed scale
def Zoom(actionType,zoomInfo):

    width = zoomInfo["width"]
    height = zoomInfo["height"]

    #Starting point from which zooming 
    xStart = random.randint(0,width)
    yStart = random.randint(0,height)

    return [actionType,(xStart,yStart)]

#Returns an array with all the information
def PanZoom(actionType,panZoomInfo):

    if(panZoomInfo==None):

        return [actionType,None]

    else:

        height = panZoomInfo["height"]
        width = panZoomInfo["width"]

        #Starting point from which panning starts
        xStart = random.randint(0,width)
        yStart = random.randint(0,height)

        #Here randomly is chosen where moving between "left/right" and "up/down"
        xMove = random.randint(0,1)
        yMove = random.randint(0,1)

        xDirections = ["right","left"]
        yDirections = ["up","down"]

        xMove = xDirections[xMove]
        yMove = yDirections[yMove]

        return [actionType,(height,width),(xStart,yStart),(xMove,yMove)]

#SLIDER CHANGE HTML
#This is the case when class = "input" and type = "range"
def SliderHtml(sliderInfo):

    minValue = sliderInfo["min"]
    maxValue = sliderInfo["max"]
    
    #Per ora escludiamo di averlo
    # currentValue = sliderInfo["value"]

    width = sliderInfo["width"]

    return ["range",None,(minValue,maxValue,width)]

#SELECT DROPDOWN HTML
def selectDropdownHtml(selectInfo):

    possibleValues = selectInfo["value"]

    nextValueIndex = random.randint(0,len(possibleValues)-1)

    nextValue = possibleValues[nextValueIndex]["value"]

    return nextValue

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


def getNode(explSequence,xpath):
    for node in explSequence:
        if(node["xpath"] == xpath):
            return node["events"]

def retEdges(graph,stateCurr,nextState):
    listEdges = []
    for transition in graph[stateCurr]:
        if transition["leadsToState"] == nextState:
            listEdges.append(transition)

    return listEdges

allSequences = []
def ExplorationState(graph,stateCurrent,transition,exploration):
    global explorationSequence

    continueExploration = exploration.copy()
    
    if(checkPresenceOfLoop(newGraph,stateCurrent)):
    
        for edge in retEdges(graph,str(stateCurrent),stateCurrent):

            typeActions = ["L","M","B"]

            currentState = edge

            idNode = currentState["id"]
            xpathNode = currentState["xpath"]
            siblingsNode = currentState["siblings"]
            startingPathNode = currentState["startingPath"]
            eventNode  = currentState["event"]
            stylesNode = currentState["styles"]
            attributeNode = currentState["attributes"]
            tagNode = currentState["tag"]
            brushableNode = currentState["brushable"]
            zoomableNode = currentState["zoomable"]

            #UpdateScore(graph,state,idNode)

            """
            checkPresence = 0
            for element in explorationSequence:
                if(element["xpath"] == xpathNode):
                    checkPresence = 1

            if(checkPresence == 0):
                explorationSequence.append({"xpath":xpathNode,"css":idNode,"startingPath":int(startingPathNode),"siblings":siblingsNode,"events":[]})
            #print("STATE: "+ stateNumber + "| ID: "+ idNode)

            """

            if(eventNode == "click" or eventNode == "contextmenu"):

                #If the tag is button we don't need any other information
                if(tagNode == "button"):

                    explorationState = {"xpath":xpathNode,"css":idNode,"startingPath":int(startingPathNode),"siblings":siblingsNode,"event":eventNode,"info":None}

                    if(explorationState not in continueExploration):
                        continueExploration.append(explorationState)

                else:

                    width = stylesNode["width"]
                    height = stylesNode["height"]

                    infoClick = Click(height,width)

                    explorationState = {"xpath":xpathNode,"css":idNode,"startingPath":int(startingPathNode),"siblings":siblingsNode,"event":eventNode,"info":infoClick}
                    
                    if(explorationState not in continueExploration):
                        continueExploration.append(explorationState)

            #For the moment we try to not distinguish them "mouseover" and "mouseleave"
            elif(eventNode == "mouseover" or eventNode == "mouseenter"):

                explorationState = {"xpath":xpathNode,"css":idNode,"startingPath":int(startingPathNode),"siblings":siblingsNode,"event":eventNode,"info":None}

                if(explorationState not in continueExploration):
                        continueExploration.append(explorationState)

            elif(eventNode == "mouseout" or eventNode=="mouseleave"):

                infoOut = None

                #If it's a circle we know its radius
                if(tagNode == "circle"):

                    infoOut = float(attributeNode["r"])

                elif(stylesNode["height"]!=None or stylesNode["width"]!=None):

                    infoOut = (stylesNode["height"],stylesNode["width"])

                explorationState = {"xpath":xpathNode,"css":idNode,"startingPath":int(startingPathNode),"siblings":siblingsNode,"event":eventNode,"info":infoOut}

                if(explorationState not in continueExploration):
                        continueExploration.append(explorationState)

            elif(eventNode == "mousedown"):

                if(brushableNode==None and zoomableNode==None):

                    explorationState = {"xpath":xpathNode,"css":idNode,"startingPath":int(startingPathNode),"siblings":siblingsNode,"event":eventNode,"info":None}

                    if(explorationState not in continueExploration):
                        continueExploration.append(explorationState)

                elif(brushableNode!=None):

                    newBrushPosition = None

                    print(brushableNode["brush_extent"])
                    print(brushableNode["selection_extent"])

                    if(brushableNode["brush_extent"] == brushableNode["selection_extent"]):

                        explorationState = {"xpath":xpathNode,"css":idNode,"startingPath":int(startingPathNode),"siblings":siblingsNode,"event":"reset_brush","info":brushableNode["selection_extent"]}

                        continueExploration.append(explorationState)

                        brushableNode["selection_extent"] = None

                    for size in typeActions:

                        for i in range(0,10):

                            newSelectionExtent = Brush(size,brushableNode)

                            print("New selection_extent: ",end="")
                            print(newSelectionExtent)

                            infoPan = PanBrush(brushableNode["directions"],brushableNode["brush_extent"],newSelectionExtent)
                            #print("InfoPan ",end="")
                            #print(infoPan)

                            newBrushPosition = [[newSelectionExtent[0][0] + infoPan[0],newSelectionExtent[0][1] + infoPan[1]],[newSelectionExtent[1][0] + infoPan[0],newSelectionExtent[1][1] + infoPan[1]]]

                            #Info for panning the brushed area
                            explorationState = {"xpath":xpathNode,"css":idNode,"startingPath":int(startingPathNode),"siblings":siblingsNode,"event":"brush","info":[newSelectionExtent,[infoPan, newBrushPosition]]}

                            if(explorationState not in continueExploration):
                                continueExploration.append(explorationState)

                            #Position after the panning
                            #newBrushPosition = [[newSelectionExtent[0][0] + infoPan[0],newSelectionExtent[0][1] + infoPan[1]],[newSelectionExtent[1][0] + infoPan[0],newSelectionExtent[1][1] + infoPan[1]]]
                            #print("New brush pos ",end="")
                            #print(newBrushPosition)

                elif(zoomableNode!=None):

                    if(stylesNode["height"]!=None or stylesNode["width"]!=None):

                
                        panZoomInfo = {"xpath":xpathNode,"css":idNode,"startingPath":int(startingPathNode),"siblings":siblingsNode,"height":stylesNode["height"],"width":stylesNode["width"]}

                    else: 

                        panZoomInfo = None

                    for size in typeActions:
                        
                        retInfo = PanZoom(size,panZoomInfo)

                        explorationState = {"xpath":xpathNode,"css":idNode,"startingPath":int(startingPathNode),"siblings":siblingsNode,"event":"panzoom","info":retInfo}

                        if(explorationState not in continueExploration):
                            continueExploration.append(explorationState)
                            
            elif(eventNode == "wheel"):

                for size in typeActions:

                    #We make 10 for zoom in and 10 for zoom out handled directly in Selenium
                    for i in range(0,10):

                        if(stylesNode["height"]!=None or stylesNode["width"]!=None):
                    
                                zoomInfo = {"height":stylesNode["height"],"width":stylesNode["width"]}

                        else: 

                                zoomInfo = None
                            

                        retInfo = Zoom(size,zoomInfo)

                        explorationState = {"xpath":xpathNode,"css":idNode,"startingPath":int(startingPathNode),"siblings":siblingsNode,"event":eventNode,"info":["in",retInfo]}

                        if(explorationState not in continueExploration):
                            continueExploration.append(explorationState)
                        

                    for i in range(0,10):
            
                        if(stylesNode["height"]!=None or stylesNode["width"]!=None):
                    
                                zoomInfo = {"height":stylesNode["height"],"width":stylesNode["width"]}

                        else: 

                                zoomInfo = None
                            

                        retInfo = Zoom(size,zoomInfo)

                        explorationState = {"xpath":xpathNode,"css":idNode,"startingPath":int(startingPathNode),"siblings":siblingsNode,"event":eventNode,"info":["out",retInfo]}

                        if(explorationState not in continueExploration):
                            continueExploration.append(explorationState)
                        
            elif(eventNode == "mouseup"):

                explorationState = {"xpath":xpathNode,"css":idNode,"startingPath":int(startingPathNode),"siblings":siblingsNode,"event":eventNode,"info":None}

                if(explorationState not in continueExploration):
                        continueExploration.append(explorationState)

            elif(eventNode == "input"):

                if(attributeNode["type"]!=None):

                    if(attributeNode["type"]=="range"):

                        for size in typeActions:

                            for i in range(0,10):

                                sliderHtmlInfo = {"min":int(attributeNode["min"]),"max":int(attributeNode["max"]),"width":stylesNode["width"]}

                                retInfo = SliderHtml(sliderHtmlInfo)

                                retInfo[1]=size

                                explorationState = {"xpath":xpathNode,"css":idNode,"startingPath":int(startingPathNode),"siblings":siblingsNode,"event":eventNode,"info": retInfo}

                                if(explorationState not in continueExploration):
                                    continueExploration.append(explorationState)
                                

                    elif(attributeNode["type"]=="number"):

                        for i in range(0,10):

                            numberInfo = {"min":int(attributeNode["min"]),"max":int(attributeNode["max"]),"value":int(attributeNode["value"]),"step":int(attributeNode["step"])}

                            explorationState = {"xpath":xpathNode,"css":idNode,"startingPath":int(startingPathNode),"siblings":siblingsNode,"event":eventNode,"info": ["number",inputNumberHtml(numberInfo)]}

                            if(explorationState not in continueExploration):
                                continueExploration.append(explorationState)
                            

                    #We treat this case like it was a button
                    elif(attributeNode["type"] == "checkbox" or attributeNode["type"] == "radio"):

                        explorationState = {"xpath":xpathNode,"css":idNode,"startingPath":int(startingPathNode),"siblings":siblingsNode,"event":eventNode,"info":[attributeNode["type"],None]}

                        if(explorationState not in continueExploration):
                            continueExploration.append(explorationState)
                            
            elif(eventNode == "change"):

                if(tagNode == "input"):

                    if(attributeNode["type"] == "checkbox" or attributeNode["type"] == "radio"):
            
                        explorationState = {"xpath":xpathNode,"css":idNode,"startingPath":int(startingPathNode),"siblings":siblingsNode,"event":eventNode,"info":[attributeNode["type"],None]}

                        if(explorationState not in continueExploration):
                            continueExploration.append(explorationState)

            elif(eventNode == "facsimile_back"):

                #Since this is not a real event but just to go back to a state

                explorationState = {"xpath":xpathNode,"css":idNode,"startingPath":int(startingPathNode),"siblings":siblingsNode,"event":eventNode,"info":None}

                if(explorationState not in continueExploration):
                        continueExploration.append(explorationState)

    if(transition==[]):
        if(exploration not in allSequences):
            allSequences.append(continueExploration)
        return

    nextState = transition[0]

    for edge in retEdges(graph,str(stateCurrent),nextState):

        typeActions = ["L","M","B"]

        currentState = edge

        idNode = currentState["id"]
        xpathNode = currentState["xpath"]
        siblingsNode = currentState["siblings"]
        startingPathNode = currentState["startingPath"]
        eventNode  = currentState["event"]
        stylesNode = currentState["styles"]
        attributeNode = currentState["attributes"]
        tagNode = currentState["tag"]
        brushableNode = currentState["brushable"]
        zoomableNode = currentState["zoomable"]

        #UpdateScore(graph,state,idNode)

        """
        checkPresence = 0
        for element in explorationSequence:
            if(element["xpath"] == xpathNode):
                checkPresence = 1

        if(checkPresence == 0):
            explorationSequence.append({"xpath":xpathNode,"css":idNode,"startingPath":int(startingPathNode),"siblings":siblingsNode,"events":[]})
        #print("STATE: "+ stateNumber + "| ID: "+ idNode)

        """

        if(eventNode == "click" or eventNode == "contextmenu"):

            #If the tag is button we don't need any other information
            if(tagNode == "button"):

                explorationState = {"xpath":xpathNode,"css":idNode,"startingPath":int(startingPathNode),"siblings":siblingsNode,"event":eventNode,"info":None}

                continueExploration.append(explorationState)

            else:

                width = stylesNode["width"]
                height = stylesNode["height"]

                infoClick = Click(height,width)

                explorationState = {"xpath":xpathNode,"css":idNode,"startingPath":int(startingPathNode),"siblings":siblingsNode,"event":eventNode,"info":infoClick}
                
                continueExploration.append(explorationState)

        #For the moment we try to not distinguish them "mouseover" and "mouseleave"
        elif(eventNode == "mouseover" or eventNode == "mouseenter"):

            explorationState = {"xpath":xpathNode,"css":idNode,"startingPath":int(startingPathNode),"siblings":siblingsNode,"event":eventNode,"info":None}

            continueExploration.append(explorationState)

        elif(eventNode == "mouseout" or eventNode=="mouseleave"):

            infoOut = None

            #If it's a circle we know its radius
            if(tagNode == "circle"):

                infoOut = float(attributeNode["r"])

            elif(stylesNode["height"]!=None or stylesNode["width"]!=None):

                infoOut = (stylesNode["height"],stylesNode["width"])

            explorationState = {"xpath":xpathNode,"css":idNode,"startingPath":int(startingPathNode),"siblings":siblingsNode,"event":eventNode,"info":infoOut}

            continueExploration.append(explorationState)

        elif(eventNode == "mousedown"):

            if(brushableNode==None and zoomableNode==None):

                explorationState = {"xpath":xpathNode,"css":idNode,"startingPath":int(startingPathNode),"siblings":siblingsNode,"event":eventNode,"info":None}

                continueExploration.append(explorationState)

            elif(brushableNode!=None):

                newBrushPosition = None

                print(brushableNode["brush_extent"])
                print(brushableNode["selection_extent"])

                if(brushableNode["brush_extent"] == brushableNode["selection_extent"]):

                    explorationState = {"xpath":xpathNode,"css":idNode,"startingPath":int(startingPathNode),"siblings":siblingsNode,"event":"reset_brush","info":brushableNode["selection_extent"]}

                    continueExploration.append(explorationState)

                    brushableNode["selection_extent"] = None

                for size in typeActions:

                    for i in range(0,10):

                        newSelectionExtent = Brush(size,brushableNode)

                        print("New selection_extent: ",end="")
                        print(newSelectionExtent)

                        explorationState = {"xpath":xpathNode,"css":idNode,"startingPath":int(startingPathNode),"siblings":siblingsNode,"event":"brush","info":newSelectionExtent}

                        continueExploration.append(explorationState)

                        infoPan = PanBrush(brushableNode["directions"],brushableNode["brush_extent"],newSelectionExtent)
                        #print("InfoPan ",end="")
                        #print(infoPan)

                        newBrushPosition = [[newSelectionExtent[0][0] + infoPan[0],newSelectionExtent[0][1] + infoPan[1]],[newSelectionExtent[1][0] + infoPan[0],newSelectionExtent[1][1] + infoPan[1]]]

                        #Info for panning the brushed area
                        explorationState = {"xpath":xpathNode,"css":idNode,"startingPath":int(startingPathNode),"siblings":siblingsNode,"event":"panbrush","info":[infoPan, newBrushPosition]}

                        continueExploration.append(explorationState)

                        #Position after the panning
                        #newBrushPosition = [[newSelectionExtent[0][0] + infoPan[0],newSelectionExtent[0][1] + infoPan[1]],[newSelectionExtent[1][0] + infoPan[0],newSelectionExtent[1][1] + infoPan[1]]]
                        #print("New brush pos ",end="")
                        #print(newBrushPosition)

            elif(zoomableNode!=None):

                if(stylesNode["height"]!=None or stylesNode["width"]!=None):

            
                    panZoomInfo = {"xpath":xpathNode,"css":idNode,"startingPath":int(startingPathNode),"siblings":siblingsNode,"height":stylesNode["height"],"width":stylesNode["width"]}

                else: 

                    panZoomInfo = None

                for size in typeActions:
                    
                    retInfo = PanZoom(size,panZoomInfo)

                    explorationState = {"xpath":xpathNode,"css":idNode,"startingPath":int(startingPathNode),"siblings":siblingsNode,"event":"panzoom","info":retInfo}

                    continueExploration.append(explorationState)
                        
        elif(eventNode == "wheel"):

            for size in typeActions:

                #We make 10 for zoom in and 10 for zoom out handled directly in Selenium
                for i in range(0,10):

                    if(stylesNode["height"]!=None or stylesNode["width"]!=None):
                
                            zoomInfo = {"height":stylesNode["height"],"width":stylesNode["width"]}

                    else: 

                            zoomInfo = None
                        

                    retInfo = Zoom(size,zoomInfo)

                    explorationState = {"xpath":xpathNode,"css":idNode,"startingPath":int(startingPathNode),"siblings":siblingsNode,"event":eventNode,"info":["in",retInfo]}

                    continueExploration.append(explorationState)
                    

                for i in range(0,10):
        
                    if(stylesNode["height"]!=None or stylesNode["width"]!=None):
                
                            zoomInfo = {"height":stylesNode["height"],"width":stylesNode["width"]}

                    else: 

                            zoomInfo = None
                        

                    retInfo = Zoom(size,zoomInfo)

                    explorationState = {"xpath":xpathNode,"css":idNode,"startingPath":int(startingPathNode),"siblings":siblingsNode,"event":eventNode,"info":["out",retInfo]}

                    continueExploration.append(explorationState)
                    
        elif(eventNode == "mouseup"):

            explorationState = {"xpath":xpathNode,"css":idNode,"startingPath":int(startingPathNode),"siblings":siblingsNode,"event":eventNode,"info":None}

            continueExploration.append(explorationState)

        elif(eventNode == "input"):

            if(attributeNode["type"]!=None):

                if(attributeNode["type"]=="range"):

                    for size in typeActions:

                        for i in range(0,10):

                            sliderHtmlInfo = {"min":int(attributeNode["min"]),"max":int(attributeNode["max"]),"width":stylesNode["width"]}

                            retInfo = SliderHtml(sliderHtmlInfo)

                            retInfo[1]=size

                            explorationState = {"xpath":xpathNode,"css":idNode,"startingPath":int(startingPathNode),"siblings":siblingsNode,"event":eventNode,"info": retInfo}

                            continueExploration.append(explorationState)
                            

                elif(attributeNode["type"]=="number"):

                    for i in range(0,10):

                        numberInfo = {"min":int(attributeNode["min"]),"max":int(attributeNode["max"]),"value":int(attributeNode["value"]),"step":int(attributeNode["step"])}

                        explorationState = {"xpath":xpathNode,"css":idNode,"startingPath":int(startingPathNode),"siblings":siblingsNode,"event":eventNode,"info": ["number",inputNumberHtml(numberInfo)]}

                        continueExploration.append(explorationState)
                        

                #We treat this case like it was a button
                elif(attributeNode["type"] == "checkbox" or attributeNode["type"] == "radio"):

                    explorationState = {"xpath":xpathNode,"css":idNode,"startingPath":int(startingPathNode),"siblings":siblingsNode,"event":eventNode,"info":[attributeNode["type"],None]}

                    continueExploration.append(explorationState)
                        
        elif(eventNode == "change"):

            if(tagNode == "input"):

                if(attributeNode["type"] == "checkbox" or attributeNode["type"] == "radio"):
        
                    explorationState = {"xpath":xpathNode,"css":idNode,"startingPath":int(startingPathNode),"siblings":siblingsNode,"event":eventNode,"info":[attributeNode["type"],None]}

                    continueExploration.append(explorationState)

        elif(eventNode == "facsimile_back"):

            #Since this is not a real event but just to go back to a state

            explorationState = {"xpath":xpathNode,"css":idNode,"startingPath":int(startingPathNode),"siblings":siblingsNode,"event":eventNode,"info":None}

            continueExploration.append(explorationState)

        #print(transition)
        ExplorationState(graph,nextState,transition[1:],continueExploration)
        
    #return exploration


#Here we make a preprocessing of the JSON statechart
def statechartPreProcessing(statechart):

    newGraph = {}
    for state in statechart:

        #Add a node for each possible state
        newGraph[str(state["stateId"])] = []

        #print(state)

        for node in state["ieo"]:

            if(node["leadsToState"]!=-1):

                newNode = {}
                
                newNode["id"] = node["nodeSelector"]
                newNode["tag"] = node["tag"]
                newNode["event"] = node["event"]
                newNode["brushable"] = node["brushable"]
                newNode["zoomable"] = node["zoomable"]
                newNode["leadsToState"] = node["leadsToState"]
                newNode["siblings"] = node["siblings"]
                

                if(node["siblings"] != 0):
                 
                    positionXPath = node["nodeXPath"].rfind("[")
                    newNode["xpath"] = node["nodeXPath"][0:positionXPath]
                    newNode["startingPath"] = node["nodeXPath"][positionXPath:][1:-1]

                else:
                    newNode["xpath"] = node["nodeXPath"]
                    newNode["startingPath"] = -1

                if(node["selectValue"]!=None):
                    newNode["selectValue"] = node["selectValue"]

                #Here we add the attributes by preprocessing them
                #So creating a dictionary with as key their name
                #Convert to integer if height or width
                newNode["attributes"] = {}

                if(node["attributes"]!=None):

                    for key in node["attributes"]:
                        
                        if(key["name"] == "height" or key["name"] == "width"):
                        
                            newNode["attributes"][key["name"]] = int(key["value"])
                        
                        else:

                            newNode["attributes"][key["name"]] = key["value"]


                #Same for the styles but we need to remove "px"
                #at the end of the height and with and then convert to integer
                newNode["styles"] = {}
                for key in node["styles"]:
                    
                    if(key["name"] == "height" or key["name"] == "width"):

                        if(key["value"] != "auto"):
                    
                            newNode["styles"][key["name"]] = int(key["value"][:len(key["value"])-2])

                        else:

                            newNode["styles"][key["name"]] = key["value"]

                if(node["data"] == None):
                    newNode["data"] = None
                
                else:

                    newNode["data"] = {}
                    for key in node["data"]:
                        newNode["data"][key["name"]] = key["value"]

                #print(newNode)

                #Add this node to the state
                newGraph[str(state["stateId"])].append(newNode)



    return newGraph

def createGraphVisit(graph):
    
    newGraph = {}

    for state in graph:

        newGraph[int(state)] = 0

    return newGraph

#Update the graph of the visits
def UpdateScore(graphVisit,state,idNode):

    for node in graphVisit[state]:

        if(node["id"] == idNode):

            if(node["visit"]!=None):

                node["visit"]+=1

    return

if(__name__=="__main__"):

    nameVis = input("Insert name of the visualization: ")
    
    #open the statechart json file
    statechart_j=open('statecharts/statechart_'+nameVis+'.json')

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

    exit
    #Save graph on a file
    with open('postprocess_statecharts/ppstatehcart_'+nameVis+'.json', 'w') as fp:
        json.dump(graph, fp,  indent=4)

    print(transitionsList)
    print(eventsList)

    newGraph = {}

    counter = 0
    for node in graph:

        innerList = []
        for transition in graph[node]:

            #if(transition["leadsToState"] not in innerList):
            innerList.append(int(transition["leadsToState"]))

        newGraph[counter] = innerList
        counter+=1

    graphVisit = createGraphVisit(graph)
    print("Graph:",json.dumps(newGraph,indent=4))

    #print("GraphVisit:",json.dumps(graphVisit,indent=4))

    #DFS(newGraph,0,graphVisit)
    #print(outputEdges)

    for nodeEnd in newGraph:
        print("destination: " +str(nodeEnd))
        printAllPaths(0,nodeEnd,newGraph)

    #print(listPaths)
    print("-------------------------------------------")

    for transition in listPaths:
        ExplorationState(graph,0,transition[1:],[])
    
    """
    res = ExplorationState(graph,0,listPaths[10][1:],[])
    print(allSequences)
    print(len(allSequences))
    """

    #Save exploration sequence that will be passed to Selenium
    with open('explorations/exploration_'+nameVis+'.json', 'w') as fp:
        json.dump(allSequences, fp,  indent=4)

    print("------------------------------------------------------------------------------")