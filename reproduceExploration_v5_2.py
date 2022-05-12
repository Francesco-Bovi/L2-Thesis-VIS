from re import S
from xml.dom.minidom import Element
from selenium import webdriver
import time
import random
import json

from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

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

    actions = ActionChains(driver)
    actions.move_to_element_with_offset(element,xStart,yStart)
    
    start = time.time()
    actions.click_and_hold().move_by_offset(spaceHorizontal*divisor,spaceVertical*divisor).release().perform()
    end = time.time()

    return end-start
    

def Zoom(element,infoInput,driver):

    actionType = infoInput[0]

    xPoint=infoInput[1][0]
    yPoint=infoInput[1][1]

    scrollSize = None

    if(actionType == "L"):

        scrollSize = -100

    elif(actionType == "M"):

        scrollSize = -200
    
    else:

        scrollSize = -300

    actions = ActionChains(driver)

    actions.move_to_element(element)
    
    start = time.time()
    actions.scroll(xPoint,yPoint,0,scrollSize).release().perform()
    end = time.time()

    return end-start

def Input(element,infoInput,driver):

    actionType = infoInput[1]

    if(infoInput[0] == "range"):

        tupleInfo = infoInput[2]

        pixelsOffsetBack = GetPixelsBack(tupleInfo[0],tupleInfo[1],tupleInfo[2])

        pixelsOffset = GetPixelsToMove(tupleInfo[0],tupleInfo[1],tupleInfo[2],actionType)

        actions = ActionChains(driver)

        actions.move_to_element(element).click_and_hold().move_by_offset(pixelsOffsetBack,0).release()

        start = time.time()
        actions.click_and_hold().move_by_offset(pixelsOffset,0).release().perform()
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
        actions.click().release().perform()
        end = time.time()
    
    return end-start
        

#For now we don't consider the "mousedown" when we don't have any other information
"""
def Mousedown(element,driver):

    actions = ActionChains(driver)

    actions.move_to_element(element).click_and_hold().perform()

    return
"""

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

    start = time.time()
    actions.move_to_element(element).perform()
    end = time.time()     

    return end-start

def Click(element,clickInfo,driver):

    if(clickInfo == None):

        actions = ActionChains(driver)

        #At first we go on the element
        actions.move_to_element(element)
        
        #Then we perform the click on that element
        start = time.time()
        actions.click().release().perform()
        end = time.time()

    else:

        actions = ActionChains(driver)

        #At first we go on the element
        actions.move_to_element_with_offset(element,clickInfo[0],clickInfo[1])
        
        #Then we perform the click on that element
        start = time.time()
        actions.click().release().perform()
        end = time.time()

    #Return the latency time
    return end-start

def Brush(element,infoBrush,driver):

    Start = infoBrush[0]
    End = infoBrush[1]

    xStart = Start[0]
    yStart = Start[1]

    xEnd = End[0]
    yEnd = End[1]

    actions = ActionChains(driver)

    actions.move_to_element_with_offset(element,xStart,yStart).perform()

    start = time.time()
    actions.click_and_hold().move_by_offset(xEnd-xStart,yEnd-yStart).release().perform()
    end = time.time()

    #In order to refresh the brush
    #actions.move_to_element_with_offset(element,0,0).click().release().perform()

    return end-start

def PanBrush(element,infoBrush,driver):
    
    directions = infoBrush["directions"]

    brushExtent = infoBrush["brush_extent"]

    selectionExtent = infoBrush["selection_extent"]

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


    actions = ActionChains(driver)

    #actions.move_to_element_with_offset(element,xStartBrush,yStartBrush).click_and_hold().move_by_offset(xEndBrush-xStartBrush,yEndBrush-yStartBrush).release().perform()

    if(xMove == "right"):
        
        maxMovement = width - xEndBrush

        moveX = random.uniform(0,maxMovement)
    
    elif(xMove == "left"):

        maxMovement = -xStartBrush

        moveX = random.uniform(maxMovement,0)
    
    else:

        moveX = 0


    if(yMove == "up"):

        maxMovement = -yStartBrush

        moveY = random.uniform(maxMovement,0)

    #This means we're moving down
    elif(yMove == "down"):

        maxMovement = height - yEndBrush

        moveY = random.uniform(0,maxMovement)

    else: 

        moveY = 0

    #actions.move_to_element_with_offset(element,0,0).perform()
    actions.move_to_element_with_offset(element,xMiddleBrush,yMiddleBrush).perform()

    start = time.time()
    actions.click_and_hold().move_by_offset(moveX,moveY).release().perform()
    end = time.time()

    #In order to refresh the brush
    #actions.move_to_element_with_offset(element,0,0).click().perform()

    return end-start

if __name__ == "__main__":

    #open the statechart json file
    explorationSequence = open('explorations/exploration_brush.json')

    #returns the JSON object as a dictionary
    explorationSequence = json.load(explorationSequence)

    actionSequence = []

    driver = webdriver.Chrome()

    driver.get('http://127.0.0.1:5501/MatteoScript/brushmorescatter.html')
    driver.maximize_window()
    
    finalSummary = {}

    for state in explorationSequence:

        time.sleep(2)

        #driver.refresh()

        latency = None
        #time.sleep(2)

        selector = state["selector"]
        event = state["event"]

        #Explicit wait
        try:
            element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR,selector))
            )
        except:
            print("Element not found")
        else:

            print("STATE: " + selector + " EVENT: " + event)
            #print(state["info"])

            if(selector not in finalSummary):
                finalSummary[selector] = {}

            if(event not in finalSummary[selector]):
                finalSummary[selector][event] = []

            if(event == "click"):

                latency = Click(element,state["info"],driver)

            elif(event == "mouseover" or event == "mouseenter"):

                latency = Mouseover(element,driver)

            elif(event == "mouseout" or event == "mouseleave"):

                latency = Mouseout(element,state["info"],driver)

            elif(event == "mousedown"):

                if(state["info"][0] == "brush"):

                    latency = Brush(element,state["info"][1],driver)

                elif(state["info"][0] == "zoom"):

                    latency = PanZoom(element,state["info"][1],driver)

            elif(event == "wheel"):

                latency = Zoom(element,state["info"],driver)

            elif(event == "mouseout"):

                latency = Mouseout(element,driver)

            elif(event == "input"):

                latency = Input(element,state["info"],driver)
            
            elif(event == "panbrush"):

               latency = PanBrush(element,state["info"],driver)
               driver.refresh()

            print(latency)
            actionSequence.append([event,latency])
            finalSummary[selector][event].append([state["info"],latency])

    
    with open('summaries/summary_brush.json', 'w') as fp:
        json.dump(finalSummary, fp,  indent=4)
    
    driver.close()
    print(actionSequence)