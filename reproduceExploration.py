from xml.dom.minidom import Element
from selenium import webdriver
import time
import random

from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains



consoleScript = "eventsList = ['click', 'dbclick','change','keydown','mousemove','mousedown','mouseup', 'mouseover','mouseleave','wheel'];\n\
                eventsList.forEach(event => {\n\
                    document.addEventListener(event, function handleClick(event) {\n\
                        console.time('tempo');\n\
                    });\n\
                });"


def GetPixelsToMove(Slider,Amount,SliderMax,SliderMin):
    pixels = 0
    print(Slider.size)
    tempPixels = 300
    tempPixels = tempPixels / (SliderMax - SliderMin)
    tempPixels = tempPixels * (Amount - SliderMin)
    pixels = int(tempPixels)
    return pixels


if __name__ == "__main__":
    driver = webdriver.Chrome()

    inputString = input("Inserisci tipo di visualizzazione da testare: ")

    if(inputString == "brush"):
        #BRUSH

        driver.get("https://bl.ocks.org/cmgiven/raw/abca90f6ba5f0a14c54d1eb952f8949c/?raw=true") 
        time.sleep(2)
        element = driver.find_element(by=By.CSS_SELECTOR, value="#scatterplot svg g g.brush") #Id unique
        dimElement = [390,300]

        xStart = random.uniform(0,dimElement[0])
        xEnd = random.uniform(0,dimElement[0] - xStart)

        yStart = random.uniform(0,dimElement[1])
        yEnd = random.uniform(0,dimElement[1] - yStart)

        actions = ActionChains(driver)
        actions.move_to_element_with_offset(element,xStart,yStart).click_and_hold().move_by_offset(xEnd,yEnd).release().perform()

    elif(inputString == "slider"):
        #SLIDER

        driver.get("https://bl.ocks.org/johnwalley/raw/e1d256b81e51da68f7feb632a53c3518/?raw=true")
        time.sleep(2)
        element = driver.find_element_by_css_selector("#slider-fill > svg > g > g.slider > g > path")

        pixelsToMove = GetPixelsToMove(element,0.0125,0.025,0)

        actions = ActionChains(driver)
        actions.move_to_element(element).click_and_hold().move_by_offset((-180),0).move_by_offset(pixelsToMove,0).release().perform()

    elif(inputString == "zoom1"):
        #ZOOM
    
        driver.get("https://bl.ocks.org/aleereza/raw/d2be3d62a09360a770b79f4e5527eea8/?raw=true")
        time.sleep(5)
        element = driver.find_element(by=By.CSS_SELECTOR,value="body > svg > rect")
        dimElement = [400,400]
        actions = ActionChains(driver)
        xPoint = random.uniform(0,dimElement[0])
        yPoint = random.uniform(0,dimElement[1])
        print(xPoint,yPoint)
        #actions.move_to_element(element).double_click().perform()  #Raddoppia lo scale
        #actions.move_to_element_with_offset(element,xPoint,yPoint).scroll(0,0,0,100).perform()
        actions.move_to_element(element).click().scroll(200,200,0,-110).release().perform()

        """
        #Per il panning potremmo fare move by offset
        time.sleep(2)
        xOffset = random.uniform(0,dimElement[0] - xPoint)
        yOffset = random.uniform(0,dimElement[0] - yPoint)
        actions.move_to_element_with_offset(element,xPoint,yPoint).click_and_hold().move_by_offset(xOffset,yOffset).perform()
        """

    elif(inputString == "zoom2"):
        #ZOOM2

        driver.get("https://bl.ocks.org/kkdd/raw/c13a7d51b2f2afe297dbd7712853ebbb/?raw=true")
        time.sleep(5)
        actions = ActionChains(driver)
        element = driver.find_element(by=By.CSS_SELECTOR,value="#canvas > svg")
        #actions.move_to_element(element).double_click().perform()  #Raddoppia lo scale
        #actions.move_to_element_with_offset(element,xPoint,yPoint).scroll(0,0,0,100).perform()
        actions.move_to_element(element).scroll(0,0,0,-100).release().perform()

    elif(inputString == "zoom3"):

        driver.get("https://bl.ocks.org/deristnochda/raw/1ffe16ccf8bed2035ea5091ab9bb53fb/?raw=true")
        time.sleep(5)
        actions = ActionChains(driver)
        element = driver.find_element(by=By.CSS_SELECTOR,value="body > div > svg")
        #actions.move_to_element(element).double_click().perform()  #Raddoppia lo scale
        #actions.move_to_element_with_offset(element,xPoint,yPoint).scroll(0,0,0,100).perform()
        actions.move_to_element(element).scroll(450,200,0,-110).release().perform()


    elif(inputString == "crossfilter"):

        #CROSSFILTER

        driver.get("https://bl.ocks.org/micahstubbs/raw/66db7c01723983ff028584b6f304a54a/?raw=true")
        time.sleep(2)
        elements_selector = ["#hour-chart > svg > g > g.brush","#delay-chart > svg > g > g.brush","#distance-chart > svg > g > g.brush","#date-chart > svg > g > g.brush"]
        dimensions_histo = {
            "#hour-chart > svg > g > g.brush":240,
            "#delay-chart > svg > g > g.brush":210,
            "#distance-chart > svg > g > g.brush":400,
            "#date-chart > svg > g > g.brush":900
        }
        for element in elements_selector:
            elementReference = driver.find_element(by=By.CSS_SELECTOR, value=element)
            actions = ActionChains(driver)
            xStart = random.uniform(0,dimensions_histo[element])
            xEnd = random.uniform(0,dimensions_histo[element]-xStart)
            actions.move_to_element_with_offset(elementReference,xStart,0).click_and_hold().move_by_offset(xEnd,0).release().perform()

    #driver.close()