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


def Input(element,infoInput,driver):

    actionType = infoInput[1]

    if(infoInput[0] == "range"):

        tupleInfo = infoInput[2]

        pixelsOffsetBack = GetPixelsBack(tupleInfo[0],tupleInfo[1],tupleInfo[2])

        pixelsOffset = GetPixelsToMove(tupleInfo[0],tupleInfo[1],tupleInfo[2],actionType)

        actions = ActionChains(driver)

        actions.move_to_element(element).click_and_hold().move_by_offset(pixelsOffsetBack,0).release().click_and_hold().move_by_offset(pixelsOffset,0).release().perform()

    elif(infoInput[0] == "number"):

        element.clear()
        element.send_keys(str(infoInput[1]))
    
    return
        

def Mouseout(element,driver):

    actions = ActionChains(driver)

    actions.move_to_element(element).release().perform()

    return

def Mousedown(element,driver):

    actions = ActionChains(driver)

    actions.move_to_element(element).click_and_hold().perform()

    return

def Mouseout(element,infoOut,driver):

    if(infoOut!=None):

        #Case in which we know the height and width
        if(type(infoOut) is tuple or type(infoOut) is list):

            actions = ActionChains(driver)

            actions.move_by_offset(infoOut[0]+1,infoOut[0]+1).perform()

        else:

            actions = ActionChains(driver)

            actions.move_by_offset(infoOut+1,infoOut+1).perform()
            
    
    else:

        actions = ActionChains(driver)

        actions.move_by_offset(100,100).perform()

    return

def Mouseover(element,driver):

    actions = ActionChains(driver)

    actions.move_to_element(element).perform()        

    return

def Click(element,clickInfo,driver):

    if(clickInfo == None):

        actions = ActionChains(driver)

        actions.move_to_element(element).click().release().perform()

    else:

        actions = ActionChains(driver)

        actions.move_to_element_with_offset(element,clickInfo[0],clickInfo[1]).click().release().perform()

    return

def Brush(element,infoBrush,driver):

    Start = infoBrush[0]
    End = infoBrush[1]

    xStart = Start[0]
    yStart = Start[1]

    xEnd = End[0]
    yEnd = End[1]

    actions = ActionChains(driver)

    actions.move_to_element_with_offset(element,xStart,yStart).click_and_hold().move_by_offset(xEnd-xStart,yEnd-yStart).release().perform()

if __name__ == "__main__":

    #open the statechart json file
    explorationSequence = open('explorationBrushMoreScatter.json')

    #returns the JSON object as a dictionary
    explorationSequence = json.load(explorationSequence)

    actionSequence = []

    driver = webdriver.Chrome()

    driver.get('http://127.0.0.1:5501/MatteoScript/brushmorescatter.html')
    driver.maximize_window()

    for state in explorationSequence:

        time.sleep(2)

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
            print(state["info"])

            if(event == "click"):

                Click(element,state["info"],driver)

            elif(event == "mouseover" or event == "mouseenter"):

                Mouseover(element,driver)

            elif(event == "mouseout" or event == "mouseleave"):

                Mouseout(element,state["info"],driver)

            elif(event == "mousedown"):

                if(state["info"]!=None):

                    Brush(element,state["info"],driver)

                else:

                    Mousedown(element,driver)
            
            elif(event == "mouseout"):

                Mouseout(element,driver)

            elif(event == "input"):

                Input(element,state["info"],driver)

            actionSequence.append(event)

    print(actionSequence)