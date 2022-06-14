from re import S
from xml.dom.minidom import Element
from selenium import webdriver
import time
import random
from random import choice
import json


import scipy.interpolate as si
import numpy as np
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.events import EventFiringWebDriver, AbstractEventListener
from selenium.common.exceptions import ElementClickInterceptedException, ElementNotInteractableException
#Intro-backgorund-requirements-implementazione-parte chiave

#According to https://drive.google.com/drive/u/0/folders/1ARGI_CIR3V3FvrhttgFNfXWiIpaFqNeV

#Referring to Pan/Drag/Brush
StartLatency = 200.0
EndLatency = 1000.0

latencyLimits = {"click":200.0, "change":200.0, "contextmenu": 200.0,"mousedown":200.0, "mouseup":1000.0, "mouseover":200.0 , "mouseenter": 200.0, "mousemove": 200.0 , "mouseleave": 1000.0 , "mouseout": 1000.0, "wheel": 1000.0, "dbclick": 1000.0}

def GetPixelsBack(width):

    return -width/2

def GetPixelsToMove(width,actionType):

    divisor = None
    if(actionType == "L"):

        divisor = 1/3
    
    elif(actionType == "M"):

        divisor = 1/2

    else:

        divisor = 2/3

    pixels = width*divisor
    return pixels

def PanZoom(element,zoomInfo,driver):

    actionType = zoomInfo[0]

    divisor = None
    if(actionType == "L"):

        divisor = 1/3
    
    elif(actionType == "M"):

        divisor = 1/2

    else:

        divisor = 2/3

    #Retrieve all the information for performing the panning
    height = zoomInfo[1][0]
    width = zoomInfo[1][1]

    xStart = zoomInfo[2][0]
    yStart = zoomInfo[2][1]

    xMove = zoomInfo[3][0]
    yMove = zoomInfo[3][1]

    print("StartingX: " + str(xStart) + " " + "StartingY: " + str(yStart))

    #Here we calculate the space that we have horizontally
    #and vertically in order to perform the panning
    if(xMove == "right"):

        spaceHorizontal = width - xStart
    
    else:

        spaceHorizontal = -xStart

    if(yMove == "down"):

        spaceVertical = height - yStart

    else:

        spaceVertical = -yStart

    actions = ActionChains(driver,duration=1)
    actions.move_to_element_with_offset(element,xStart,yStart).perform()

    actions.click_and_hold()

    listMoveLatency = []

    start = time.time()
    actions.perform()
    end = time.time()

    listMoveLatency.append((end-start)*1000)
    
    moveX = int(spaceHorizontal*divisor)
    moveY = int(spaceVertical*divisor)

    xStart = 0
    yStart = 0
    while(xStart != moveX or yStart != moveY):
        
        if(xStart == moveX):

            if(yStart < moveY):
                yStart+=1
                actions.move_by_offset(0,1)
            else:
                yStart-=1
                actions.move_by_offset(0,-1)

        elif(xStart < moveX):

            if(yStart < moveY):
                yStart+=1
                xStart+=1
                actions.move_by_offset(1,1)
            elif(yStart > moveY):
                yStart-=1
                xStart+=1
                actions.move_by_offset(1,-1)
            else:
                xStart+=1
                actions.move_by_offset(1,0)

        else:

            if(yStart < moveY):
                yStart+=1
                xStart-=1
                actions.move_by_offset(-1,1)
            elif(yStart > moveY):
                yStart-=1
                xStart-=1
                actions.move_by_offset(-1,-1)
            else:
                xStart-=1
                actions.move_by_offset(-1,0)

        start = time.time()
        actions.perform()
        end = time.time()
        listMoveLatency.append((end-start)*1000)

    actions.release()

    start = time.time()
    actions.perform()
    end = time.time()

    listMoveLatency.append((end-start)*1000)

    return listMoveLatency
    
def Zoom(element,infoInput,driver):

    #Check if zoom in or zoom out
    typeZoom = infoInput[0]

    infoInput = infoInput[1]
    actionType = infoInput[0]

    xPoint=infoInput[1][0]
    yPoint=infoInput[1][1]

    scrollSize = None

    if(typeZoom == "in"):

        if(actionType == "L"):

            scrollSize = -100

        elif(actionType == "M"):

            scrollSize = -200
        
        else:

            scrollSize = -300
    
    else:

        if(actionType == "L"):
    
            scrollSize = 100

        elif(actionType == "M"):

            scrollSize = 200
        
        else:

            scrollSize = 300

    actions = ActionChains(driver,duration = 1)

    actions.move_to_element(element).perform()

    listWheelLatency = []

    countScroll = 0

    if(scrollSize > 0):

        while(countScroll < scrollSize):
            actions.scroll(xPoint,yPoint,0,10)

            start = time.time()
            actions.perform()
            end = time.time()

            listWheelLatency.append((end-start)*1000)

            countScroll+=1

    else:

        while(countScroll > scrollSize):
            actions.scroll(xPoint,yPoint,0,-10)

            start = time.time()
            actions.perform()
            end = time.time()

            listWheelLatency.append((end-start)*1000)

            countScroll-=1

    return listWheelLatency

def Input(element,infoInput,driver):

    actionType = infoInput[1]

    if(infoInput[0] == "range"):

        tupleInfo = infoInput[2]

        pixelsOffsetBack = GetPixelsBack(tupleInfo[2])

        pixelsOffset = GetPixelsToMove(tupleInfo[2],actionType)

        actions = ActionChains(driver,duration=10)

        actions.move_to_element(element).click_and_hold().move_by_offset(pixelsOffsetBack,0).release().perform()
        
        actions.click_and_hold()

        pixelStart=0

        listMoveLatency = []

        start = time.time()
        actions.perform()
        end = time.time()

        listMoveLatency.append((end-start)*1000)

        while(pixelStart<int(pixelsOffset)):
            pixelStart+=1
            actions.move_by_offset(1,0)

            start = time.time()
            actions.perform()
            end = time.time()

            listMoveLatency.append((end-start)*1000)

        actions.release()

        start = time.time()
        actions.perform()
        end = time.time()

        return listMoveLatency

    elif(infoInput[0] == "number"):

        element.clear()

        start = time.time()
        element.send_keys(str(infoInput[1]))
        end = time.time()

    elif(infoInput[0] == "checkbox" or infoInput[0] == "radio"):

        actions = ActionChains(driver,duration = 0)

        actions.move_to_element(element).perform()

        actions.click()
        
        start = time.time()
        actions.perform()
        end = time.time()
    
    return end-start

def Mouseout(driver):

    #Move to the 1,1 point of the HTML/BODY
    actions.move_to_element_with_offset(mouseOutElement,1,1)
    
    start = time.time()
    actions.perform()
    end = time.time()

    return (end-start) - timeOut

def Mouseover(element,driver):

    actions = ActionChains(driver)

    #It's like a jump
    actions.move_to_element(element)

    start = time.time()
    actions.perform()
    end = time.time()     

    return (end-start) - 0.250

def Click(element,clickInfo,driver):

    if(clickInfo == None):

        actions = ActionChains(driver, duration = 0)
        
        actions.move_to_element(element).perform()

        actions.click()

        #Then we perform the click on that element

        try:

            start = time.time()
            element.click()
            end = time.time()
        
        except ElementClickInterceptedException:

            start = time.time()
            actions.perform()
            end = time.time()

        except:

            start=0
            end=0
        

    else:

        actions = ActionChains(driver, duration = 0)

        #At first we go on the element
        actions.move_to_element_with_offset(element,clickInfo[0],clickInfo[1]).perform()
        
        actions.click()
        
        #Then we perform the click on that element
        start = time.time()
        actions.perform()
        end = time.time()

    #Return the latency time
    return (end-start)

def ContextClick(element,clickInfo,driver):
    
    if(clickInfo == None):

        actions = ActionChains(driver)
        
        actions.move_to_element(element).perform()

    else:

        actions = ActionChains(driver)

        #At first we go on the element
        actions.move_to_element_with_offset(element,clickInfo[0],clickInfo[1]).perform()
        
        actions.context_click()

    try:

            #Then we perform the click on that element
            start = time.time()
            actions.perform()
            end = time.time()

    except:

            start=0
            end=0

    #Return the latency time
    return (end-start)

def Brush(element,infoBrush,driver):

    Start = infoBrush[0]
    End = infoBrush[1]

    xStart = Start[0]
    yStart = Start[1]

    xEnd = End[0]
    yEnd = End[1]

    listMoveLatency = []

    actions = ActionChains(driver,duration=1)

    actions.move_to_element_with_offset(element,xStart,yStart).perform()
    
    actions.click_and_hold()
    
    start = time.time()
    actions.perform() 
    end = time.time()

    listMoveLatency.append((end-start)*1000)

    if(xStart != xEnd and yStart != yEnd):

        while(xStart<xEnd and yStart<yEnd):
            xStart+=1
            yStart+=1
            actions.move_by_offset(1,1)

            start = time.time()
            actions.perform()
            end = time.time()
            
            listMoveLatency.append((end-start)*1000)

    #This is the case in which we move only in the "x" direction
    elif(xStart != xEnd and yStart == yEnd):

        while(xStart<xEnd):
            xStart+=1
            actions.move_by_offset(1,0)

            start = time.time()
            actions.perform()
            end = time.time()
            
            listMoveLatency.append((end-start)*1000)

    #Case in which we move only in the "y" direction
    else:

        while(yStart<yEnd):
            yStart+=1
            actions.move_by_offset(0,1)

            start = time.time()
            actions.perform()
            end = time.time()
            
            listMoveLatency.append((end-start)*1000)

    actions.release()
    
    start = time.time()
    actions.perform()
    end = time.time()

    listMoveLatency.append((end-start)*1000)
    #In order to refresh the brush
    #actions.move_to_element_with_offset(element,0,0).click().release().perform()

    return listMoveLatency

def PanBrush(element,infoPan,driver):

    newBrushAfterPan = infoPan[1]
    infoPan = infoPan[0]

    width = infoPan[4]
    height = infoPan[5]

    xMiddleBrush = infoPan[2]
    yMiddleBrush = infoPan[3]

    actions = ActionChains(driver,duration=1)

    listLatency = []

    #actions.move_to_element_with_offset(element,0,0).perform()
    actions.move_to_element_with_offset(element,xMiddleBrush,yMiddleBrush).perform()
    
    actions.click_and_hold()

    start = time.time()
    actions.perform()
    end = time.time()

    listLatency.append((end-start)*1000)

    moveX = infoPan[0]
    moveY = infoPan[1]

    xStart = 0
    yStart = 0
    while(xStart != moveX or yStart != moveY):
        
        if(xStart == moveX):

            if(yStart < moveY):
                yStart+=1
                actions.move_by_offset(0,1)
            else:
                yStart-=1
                actions.move_by_offset(0,-1)

        elif(xStart < moveX):

            if(yStart < moveY):
                yStart+=1
                xStart+=1
                actions.move_by_offset(1,1)
            elif(yStart > moveY):
                yStart-=1
                xStart+=1
                actions.move_by_offset(1,-1)
            else:
                xStart+=1
                actions.move_by_offset(1,0)

        else:

            if(yStart < moveY):
                yStart+=1
                xStart-=1
                actions.move_by_offset(-1,1)
            elif(yStart > moveY):
                yStart-=1
                xStart-=1
                actions.move_by_offset(-1,-1)
            else:
                xStart-=1
                actions.move_by_offset(-1,0)

        start = time.time()
        actions.perform()
        end = time.time()
        listLatency.append((end-start)*1000)


    actions.release()

    start = time.time()
    actions.perform()
    end = time.time()

    listLatency.append((end-start)*1000)

    #print("Panning... " + str(moveX) + " " + str(moveY))

    #This part of the code is useful to cancel the brushed zone and prepare a new brush
    listExcludeX = []
    listExcludeY = []

    for i in range(int(newBrushAfterPan[0][0]),int(newBrushAfterPan[1][0])):
        listExcludeX.append(i)

    for j in range(int(newBrushAfterPan[0][1]),int(newBrushAfterPan[1][1])):
        listExcludeY.append(j)

    xWhereClick = choice(list(set([x for x in range(0,int(width))]) - set(listExcludeX)))
    yWhereClick = choice(list(set([x for x in range(0,int(height))]) - set(listExcludeY)))

    actions.move_to_element_with_offset(element,xWhereClick,yWhereClick).click().perform()
    #print("X and Y to click: " + str(xWhereClick) + " " + str(yWhereClick))

    return listLatency

def ResetBrush(element,infoReset,driver):

    actions = ActionChains(driver,duration = 10)

    #Dimension of the brushable area
    widthBrush = infoReset[1][0] - infoReset[0][0]
    heightBrush = infoReset[1][1] - infoReset[0][1]

    actions.move_to_element_with_offset(element,widthBrush,heightBrush/2).click_and_hold().move_by_offset(-widthBrush/2,0).perform()

    actions.move_to_element_with_offset(element,widthBrush*2/3,heightBrush/2).click().perform

def EventHandle(element,eventName,transition,driver,pathNumber,pathElement):

    latency = None

    if(eventName == "click" or eventName == "change"):
    
        latency = Click(element,transition["info"],driver)

    elif(eventName == "contextmenu"):

        latency = ContextClick(element,transition["info"],driver)

    elif(eventName == "mouseover" or eventName == "mouseenter"):

        latency = Mouseover(element,driver)

    elif(eventName == "mouseout" or eventName == "mouseleave"):

        latency = Mouseout(driver)

    elif(eventName == "mousedown"):

        #Do nothing here, since we don't know what doing if we don't have info
        time.sleep(0.1)
    
    elif(eventName == "brush"):

        print("brush start")

        latency = Brush(element,transition["info"][0],driver)

        #print("STATE: " + xpath + " EVENT: " + "mousedown" + " LATENCY: " + str(latency[1]) + " ms")
        actionSequence.append(["mousedown",latency[1]])
        finalSummary[pathNumber].append([pathElement,"mousedown",transition["info"][0],latency[1] , violationRespected if latencyLimits["mousedown"] > latency[1] else violationNotRespected])


        for latencyTime in latency[1:-1]:
            #Convert in milliseconds
            #print("STATE: " + xpath + " EVENT: " + "mousemove" + " LATENCY: " + str(latencyTime) + " ms")
            actionSequence.append(["mousemove",latencyTime])
            finalSummary[pathNumber].append([pathElement,"mousemove",transition["info"][0],latencyTime , violationRespected if latencyLimits["mousemove"] > latencyTime else violationNotRespected])

        #print("STATE: " + xpath + " EVENT: " + "mouseup" + " LATENCY: " + str(latency[-1]) + " ms")
        actionSequence.append(["mouseup",latency[-1]])
        finalSummary[pathNumber].append([pathElement,"mouseup",transition["info"][0],latency[-1] , violationRespected if latencyLimits["mouseup"] > latency[-1] else violationNotRespected])

        print("panning start")

        latency = PanBrush(element,transition["info"][1],driver)

        #print("STATE: " + xpath + " EVENT: " + "mousedown" + " LATENCY: " + str(latency[1]) + " ms")
        actionSequence.append(["mousedown",latency[1]])
        finalSummary[pathNumber].append([pathElement,"mousedown",transition["info"][1],latency[1] , violationRespected if latencyLimits["mousedown"] > latency[1] else violationNotRespected])


        for latencyTime in latency[1:-1]:
            #Convert in milliseconds
            #print("STATE: " + xpath + " EVENT: " + "mousemove" + " LATENCY: " + str(latencyTime) + " ms")
            actionSequence.append(["mousemove",latencyTime])
            finalSummary[pathNumber].append([pathElement,"mousemove",transition["info"][1],latencyTime , violationRespected if latencyLimits["mousemove"] > latencyTime else violationNotRespected])

        #print("STATE: " + xpath + " EVENT: " + "mouseup" + " LATENCY: " + str(latency[-1]) + " ms")
        actionSequence.append(["mouseup",latency[-1]])
        finalSummary[pathNumber].append([pathElement,"mouseup",transition["info"][1],latency[-1] , violationRespected if latencyLimits["mouseup"] > latency[-1] else violationNotRespected])

    elif(eventName == "panzoom"):

        latency = PanZoom(element,transition["info"],driver)

    elif(eventName == "wheel"):

        latency = Zoom(element,transition["info"],driver)

        for latencyTime in latency:

            #print("STATE: " + xpath + " EVENT: " + "mousemove" + " LATENCY: " + str(latencyTime) + " ms")
            actionSequence.append([eventName,latencyTime])
            finalSummary[pathNumber].append([pathElement,eventName,transition["info"],latencyTime , violationRespected if latencyLimits[eventName] > latencyTime else violationNotRespected])

    elif(eventName == "mouseout"):

        latency = Mouseout(element,driver)

    elif(eventName == "reset_brush"):

        ResetBrush(element,transition["info"],driver)

    elif(eventName == "input"):

        latency = Input(element,transition["info"],driver)

    elif(eventName == "facsimile_back"):

        latency = None

    if(latency != None):

        if(type(latency) is not list):

            #Convert in milliseconds
            latency = latency * 1000
            
            print("STATE: " + xpath + " EVENT: " + eventName + " LATENCY: " + str(latency) + " ms")
            actionSequence.append([eventName,latency])
            finalSummary[pathNumber].append([pathElement,eventName,transition["info"],latency, violationRespected if latencyLimits[eventName] > latency else violationNotRespected])

        elif(eventName in ["panzoom","input"]):
    
            #print("STATE: " + xpath + " EVENT: " + "mousedown" + " LATENCY: " + str(latency[1]) + " ms")
            actionSequence.append(["mousedown",latency[1]])
            finalSummary[pathNumber].append([pathElement,"mousedown",transition["info"][1],latency[1] , violationRespected if latencyLimits["mousedown"] > latency[1] else violationNotRespected])


            for latencyTime in latency[1:-1]:
                #Convert in milliseconds
                #print("STATE: " + xpath + " EVENT: " + "mousemove" + " LATENCY: " + str(latencyTime) + " ms")
                actionSequence.append(["mousemove",latencyTime])
                finalSummary[pathNumber].append([pathElement,"mousemove",transition["info"][1],latencyTime , violationRespected if latencyLimits["mousemove"] > latencyTime else violationNotRespected])

            #print("STATE: " + xpath + " EVENT: " + "mouseup" + " LATENCY: " + str(latency[-1]) + " ms")
            actionSequence.append(["mouseup",latency[-1]])
            finalSummary[pathNumber].append([pathElement,"mouseup",transition["info"][1],latency[-1] , violationRespected if latencyLimits["mouseup"] > latency[-1] else violationNotRespected])

    else:

        print("STATE: " + xpath + " EVENT: " + eventName + " LATENCY: None")
        actionSequence.append([eventName,latency])

mouseOutElement = None
actionSequence = []
finalSummary = {}
violationRespected = "V"
violationNotRespected = "X"
timeOut = None

if __name__ == "__main__":

    #open the statechart json file
    explorationSequence = open('explorations/exploration_brexit.json')

    #returns the JSON object as a dictionary
    explorationSequence = json.load(explorationSequence)

    driver = webdriver.Chrome()

    sleepValue = 1
    pathNumber = 0
    problemsFound = []

    driver.get('http://localhost:8000/brexitVisualization.html')
    driver.maximize_window()

    for path in explorationSequence["0"]:

        explorationPerformed = []

        driver.get('http://localhost:8000/brexitVisualization.html')
        driver.maximize_window()

        mouseOutElement = driver.find_element(By.XPATH,"/html/body")
        actions = ActionChains(driver,duration = 0)

        #Move to the 1,1 point of the HTML/BODY
        actions.move_to_element_with_offset(mouseOutElement,1,1)
        
        start = time.time()
        actions.perform()
        end = time.time()

        timeOut = end-start
        
        finalSummary[pathNumber] = []
        print("PATH: " + str(pathNumber))

        if(path == None):
            print("None found")

        else:

            indexState = 0
            for transition in path:

                explorationPerformed.append(transition)

                """
                elementsInPage = driver.find_elements(By.CSS_SELECTOR,"*")

                print(len(elementsInPage))

                for element in elementsInPage:
                    WebDriverWait(driver, 5).until_not(EC.staleness_of(element))
                """


                xpath = transition["xpath"]
                event = transition["event"]
                siblings = transition["siblings"]
                starting = transition["startingPath"]
                nextState = transition["leadsToState"]

                siblings = int((siblings*10)/100)

                pathElement = ""
            

                for i in range(siblings + 1):

                    if(siblings != 0):

                        pathElement = xpath + "[" + str(starting + i) + "]"
                    
                    else:

                        pathElement = xpath
                        
                    print("---ANALYZING " + pathElement + "---")

                    try:

                        element = WebDriverWait(driver, 2).until(EC.visibility_of_element_located((By.XPATH,pathElement)))

                    except:

                            print("Element not found: " + pathElement)

                            #Save the paths in which problems arises
                            if(pathNumber not in problemsFound):
                                problemsFound.append(pathNumber)

                    else:

                        print("-----Event: " + event)

                        EventHandle(element,event,transition,driver,pathNumber,pathElement)

                    indexState+=1

                print("Check")
                print(str(nextState))
                #Perform sub explorations
                if(str(nextState) in explorationSequence and explorationSequence[str(nextState)] != None):

                    for subpath in explorationSequence[str(nextState)]:

                        print()
                        print("--------SUBPATH OF STATE " +str(nextState))

                        subdriver = webdriver.Chrome()
                        subdriver.get(driver.current_url)
                        subdriver.maximize_window()

                        mouseOutElement = subdriver.find_element(By.XPATH,"/html/body")
                        actions = ActionChains(subdriver,duration = 0)

                        #Move to the 1,1 point of the HTML/BODY
                        actions.move_to_element_with_offset(mouseOutElement,1,1)
                        
                        start = time.time()
                        actions.perform()
                        end = time.time()

                        timeOut = end-start

                        for subtransition in explorationPerformed:

                            xpath = subtransition["xpath"]
                            subevent = subtransition["event"]
                            siblings = subtransition["siblings"]
                            starting = subtransition["startingPath"]

                            siblings = int((siblings*10)/100)

                            SubpathElement = ""

                            for i in range(siblings + 1):

                                if(siblings != 0):

                                    SubpathElement = xpath + "[" + str(starting + i) + "]"
                                
                                else:

                                    SubpathElement = xpath
                                    
                                print("------------ANALYZING ELEMENT" + SubpathElement + "------------")

                                try:

                                    subelement = WebDriverWait(subdriver, 2).until(EC.visibility_of_element_located((By.XPATH,SubpathElement)))

                                except:

                                        print("Element not found: " + SubpathElement)

                                        #Save the paths in which problems arises
                                        if(pathNumber not in problemsFound):
                                            problemsFound.append(pathNumber)

                                else:

                                    print("------------Repeat Event: " + subevent)

                                    EventHandle(subelement,subevent,subtransition,subdriver,pathNumber,SubpathElement)
                                    print()


                        for subtransition in subpath:

                            xpath = subtransition["xpath"]
                            subevent = subtransition["event"]
                            siblings = subtransition["siblings"]
                            starting = subtransition["startingPath"]

                            siblings = int((siblings*10)/100)

                            SubpathElement = ""

                            for i in range(siblings + 1):

                                if(siblings != 0):

                                    SubpathElement = xpath + "[" + str(starting + i) + "]"
                                
                                else:

                                    SubpathElement = xpath
                                    
                                print("------------ANALYZING SUBELEMENT" + SubpathElement + "------------")

                                try:

                                    subelement = WebDriverWait(subdriver, 2).until(EC.visibility_of_element_located((By.XPATH,SubpathElement)))

                                except:

                                        print("Element not found: " + SubpathElement)

                                        #Save the paths in which problems arises
                                        if(pathNumber not in problemsFound):
                                            problemsFound.append(pathNumber)

                                else:

                                    print("------------SubEvent: " + subevent)

                                    EventHandle(subelement,subevent,subtransition,subdriver,pathNumber,SubpathElement)
                                    print()

                        subdriver.close()            

            print("************************************************************")

        pathNumber+=1
    

    with open('summaries/summary_brexit.json', 'w') as fp:
        json.dump(finalSummary, fp,  indent=4)
    
    print(actionSequence)
    print(problemsFound)

    driver.close()