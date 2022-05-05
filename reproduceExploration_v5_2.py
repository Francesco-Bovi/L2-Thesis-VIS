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

def GetPixelsToMove(Slider,Amount,SliderMax,SliderMin):
    pixels = 0
    tempPixels = 129

    """
    tempPixels = tempPixels / (SliderMax - SliderMin)
    tempPixels = tempPixels * (Amount - SliderMin)
    pixels = tempPixels
    """

    pixels = (tempPixels*Amount)/SliderMax
    return pixels


def Mouseout(element,infoOut,driver):

    if(infoOut!=None):

        actions = ActionChains(driver)

        actions.move_by_offset(infoOut*2,infoOut*2)
    
    else:

        actions = ActionChains(driver)

        actions.move_by_offset(100,100)

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

if __name__ == "__main__":

    #open the statechart json file
    explorationSequence = open('explorationSequenceMouseEvents.json')

    #returns the JSON object as a dictionary
    explorationSequence = json.load(explorationSequence)

    actionSequence = []

    driver = webdriver.Chrome()

    driver.get("http://bl.ocks.org/WilliamQLiu/raw/76ae20060e19bf42d774/?raw=true")
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

            if(event == "click"):

                Click(element,state["info"],driver)

            elif(event == "mouseover"):

                Mouseover(element,driver)

            elif(event == "mouseout"):

                Mouseout(element,state["info"],driver)

            actionSequence.append(event)

    print(actionSequence)