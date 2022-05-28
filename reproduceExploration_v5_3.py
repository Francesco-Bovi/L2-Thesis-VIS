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
#Intro-backgorund-requirements-implementazione-parte chiave

#According to https://drive.google.com/drive/u/0/folders/1ARGI_CIR3V3FvrhttgFNfXWiIpaFqNeV

#Referring to Pan/Drag/Brush
StartLatency = 200.0
EndLatency = 1000.0

latencyLimits = {"click":200.0, "change":200.0, "contextclick": 200.0, "mouseover":200.0 , "mouseenter": 200.0, "mousemove": 200.0 , "mouseleave": 1000.0 , "mouseout": 1000.0, "wheel": 1000.0, "dbclick": 1000.0}

def GetPixelsBack(min,max,width):

    return -width/2

def GetPixelsToMove(min,max,width,actionType):

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

    actions = ActionChains(driver,duration=10)
    actions.move_to_element_with_offset(element,xStart,yStart).perform()

    actions.click_and_hold()
    
    moveX = int(spaceHorizontal*divisor)
    moveY = int(spaceVertical*divisor)

    xStart = 0
    yStart = 0
    while(xStart != moveX or yStart != moveY):
        #print("Cicling...")
        
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

        #print("moveX :" + str(xStart) + " moveY: " +str(yStart))

    start = time.time()
    actions.release().perform()
    end = time.time()

    print("arriveX :" + str(moveX) + " arriveY: " +str(moveY))

    return end-start
    
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
    
            scrollSize = +100

        elif(actionType == "M"):

            scrollSize = +200
        
        else:

            scrollSize = +300

    actions = ActionChains(driver,duration = 0)

    actions.move_to_element(element).perform()

    actions.scroll(xPoint,yPoint,0,scrollSize)
    
    start = time.time()
    actions.perform()
    end = time.time()

    return end-start

def Input(element,infoInput,driver):

    actionType = infoInput[1]

    if(infoInput[0] == "range"):

        tupleInfo = infoInput[2]

        pixelsOffsetBack = GetPixelsBack(tupleInfo[0],tupleInfo[1],tupleInfo[2])

        pixelsOffset = GetPixelsToMove(tupleInfo[0],tupleInfo[1],tupleInfo[2],actionType)

        actions = ActionChains(driver,duration=10)

        actions.move_to_element(element).click_and_hold().move_by_offset(pixelsOffsetBack,0).release().click_and_hold().perform()

        pixelStart=0
        while(pixelStart<int(pixelsOffset)):
            pixelStart+=1
            actions.move_by_offset(1,0)
            
        start = time.time()
        actions.release().perform()
        end = time.time()

    elif(infoInput[0] == "number"):

        element.clear()

        start = time.time()
        element.send_keys(str(infoInput[1]))
        end = time.time()

    elif(infoInput[0] == "checkbox" or infoInput[0] == "radio"):

        actions = ActionChains(driver)

        actions.move_to_element(element)
        
        start = time.time()
        actions.click().perform()
        end = time.time()
    
    return end-start

def Mouseout(element,infoOut,driver):

    if(infoOut!=None):

        #Case in which we know the height and width
        if(type(infoOut) is tuple or type(infoOut) is list):

            actions = ActionChains(driver)

            start = time.time()
            actions.move_by_offset(infoOut[0]+1,infoOut[0]+1).perform()
            end = time.time()

        else:

            actions = ActionChains(driver)

            start = time.time()
            actions.move_by_offset(infoOut+1,infoOut+1).perform()
            end = time.time()
    
    #For now we don't consider the "mouseout" when we don't have any other information
    """
    else:

        actions = ActionChains(driver)

        actions.move_by_offset(100,100).perform()
    """

    return end-start

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

        actions = ActionChains(driver)
        
        actions.move_to_element(element).perform()

        actions.click()

        #Then we perform the click on that element
        start = time.time()
        actions.perform()
        end = time.time()

    else:

        actions = ActionChains(driver)

        xClick = random.randint(0,element.size["width"]) 
        yClick = random.randint(0,element.size["height"])

        #At first we go on the element
        actions.move_to_element_with_offset(element,xClick,yClick).perform()
        
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

        actions.context_click()

        #Then we perform the click on that element
        start = time.time()
        actions.perform()
        end = time.time()

    else:

        actions = ActionChains(driver)

        #At first we go on the element
        actions.move_to_element_with_offset(element,clickInfo[0],clickInfo[1]).perform()
        
        actions.context_click()

        #Then we perform the click on that element
        start = time.time()
        actions.perform()
        end = time.time()

    #Return the latency time
    return (end-start)

def Brush(element,infoBrush,driver):

    Start = infoBrush[0]
    End = infoBrush[1]

    xStart = int(Start[0])
    yStart = int(Start[1])

    xEnd = int(End[0])
    yEnd = int(End[1])

    #print("Brushed: [" + str(xStart)+","+str(yStart)+"],["+str(xEnd)+","+str(yEnd)+"]" )

    actions = ActionChains(driver,duration=1)

    actions.move_to_element_with_offset(element,xStart,yStart).click_and_hold().perform()

    listMoveLatency = [] 

    while(xStart<xEnd and yStart<yEnd):
        xStart+=1
        yStart+=1
        actions.move_by_offset(1,1)
        start = time.time()
        actions.perform()
        end = time.time()
        listMoveLatency.append(str((end-start)*1000))

    actions.release().perform()
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

    actions = ActionChains(driver,duration=10)

    #actions.move_to_element_with_offset(element,0,0).perform()
    actions.move_to_element_with_offset(element,xMiddleBrush,yMiddleBrush).click_and_hold()

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

        #print("moveX :" + str(xStart) + " moveY: " +str(yStart))

    start = time.time()
    actions.release().perform()
    end = time.time()

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

    return end-start

if __name__ == "__main__":

    #open the statechart json file
    explorationSequence = open('explorations/exploration_nemesis.json')

    #returns the JSON object as a dictionary
    explorationSequence = json.load(explorationSequence)

    actionSequence = []

    violationRespected = "V"
    violationNotRespected = "X"

    driver = webdriver.Chrome()

    driver.get('http://awareserver.dis.uniroma1.it/nemesis/')
    driver.maximize_window()
    
    finalSummary = {}

    for state in explorationSequence:

        xpath = state["xpath"]
        events = state["events"]
        siblings = state["siblings"]
        starting = state["startingPath"]

        #css = state["id"]
    

        for i in range(siblings + 1):

            latency = None

            #Explicit wait
            try:

                if(siblings != 0):
                    
                    element = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH,xpath + "[" + str(starting + i) + "]")))
                
                else:

                    element = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH,xpath)))

            except:

                if(siblings == 0):

                    print("Element not found :" + xpath)

                else:

                    print("Element not found :" + xpath + "[" + str(starting + i) + "]")
            else:

                if(siblings == 0):

                    print("----------ANALYZING " + xpath + "------------")

                else:
                    
                    print("----------ANALYZING " + xpath + "[" + str(starting + i) + "]------------")
                
                for event in events:

                    eventName = event["event"]

                    if(xpath not in finalSummary):
                        finalSummary[xpath] = {}

                    if(eventName not in finalSummary[xpath]):
                        finalSummary[xpath][eventName] = []

                    if(eventName == "click"):

                        latency = Click(element,event["info"],driver)

                    if(eventName == "contextmenu"):

                        #latency = ContextClick(element,event["info"],driver)
                        latency = None

                    elif(eventName == "mouseover" or eventName == "mouseenter"):

                        latency = Mouseover(element,driver)

                    elif(eventName == "mouseout" or eventName == "mouseleave"):

                        #latency = Mouseout(element,event["info"],driver)
                        latency = None

                    elif(eventName == "mousedown"):

                        #Do nothing here, since we don't know what doing if we don't have info
                        time.sleep(0.1)
                    
                    elif(eventName == "brush"):

                        latency = Brush(element,event["info"],driver)

                    elif(eventName == "panzoom"):

                        latency = PanZoom(element,event["info"],driver)

                    elif(eventName == "wheel"):

                        latency = Zoom(element,event["info"],driver)

                    elif(eventName == "mouseout"):

                        latency = Mouseout(element,driver)

                    elif(eventName == "input"):

                        latency = Input(element,event["info"],driver)
                    
                    elif(eventName == "panbrush"):

                        latency = PanBrush(element,event["info"],driver)

                    elif(eventName == "facsimile_back"):

                        latency = None

                    if(latency != None):

                        if(type(latency) is not list):

                            #Convert in milliseconds
                            latency = latency * 1000
                            
                            print("STATE: " + xpath + " EVENT: " + eventName + " LATENCY: " + str(latency) + " ms")
                            actionSequence.append([eventName,latency])
                            finalSummary[xpath][eventName].append([event["info"],latency, violationRespected if latencyLimits[eventName] > latency else violationNotRespected])

                        #Case of brushing
                        else:

                            for latencyTime in latency:
                                #Convert in milliseconds
                                print("STATE: " + xpath + " EVENT: " + "mousemove" + " LATENCY: " + latencyTime + " ms")
                                actionSequence.append([eventName,latencyTime])
                                finalSummary[xpath][eventName].append([event["info"],latencyTime , violationRespected if latencyLimits["mousemove"] > latency else violationNotRespected])


                    else:

                        print("STATE: " + xpath + " EVENT: " + eventName + " LATENCY: None")
                        actionSequence.append([eventName,latency])
                        #finalSummary[xpath][eventName].append([event["info"],latency])

                print("-------------------------------------------------------")
            
    with open('summaries/summary_nemesis.json', 'w') as fp:
        json.dump(finalSummary, fp,  indent=4)
    
    driver.close()
    print(actionSequence)