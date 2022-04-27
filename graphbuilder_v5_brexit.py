import json
from multiprocessing.connection import wait
import random
from sys import exc_info
from selenium import webdriver
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

from matplotlib.pyplot import eventplot

eventsList = [
"click", 
"dbclick",
"change",
"keydown",
"mousemove", #When moving inside a widget
"mousedown", #A pointing device button is pressed while the pointer is inside the element
"mouseup", #When the pointing device is released (opposite of MOUSEDOWN)
"mouseenter", #triggered when the mouse pointer enters the element
"mouseover", #is triggered when the mouse pointer enters the element, and its child
"mouseleave", #opposite of MOUSEOVER
"wheel" #opposite of MOUSEOUT
]

#Can we consider MOUSEDOWN + MOVE = DRAGSTART and then MOUSEUP = DRAGEND ?
#Can we consider WHEEL = ZOOM and DBCLICK also

transitionsList = []
explorationSequence = []


def retTypeAction():
    typeActions = ["L","M","H"]

    return typeActions[random.randint(0,2)]
    
def updateValue(graph,state,newValue):

    attributesList = graph[state]["attributes"]

    for elem in attributesList:
        if(elem["name"] == "value"):
            elem["value"] = newValue

def ExplorationState(stateName,state,driver):
    global explorationSequence

    print("State: ",stateName)

    events = state["events"]
    #print("Events: ",events)

    element = driver.find_element(by=By.CSS_SELECTOR, value = state["tag"]+stateName)

    explorationSequence.append(stateName)
    time.sleep(2)


    #In the Brexit Visualization the events possible are
    # click-mouseover-mouseout-contextmenu
    for event in events:

        explorationSequence.append(event)

        print("performing "+event)

        if(event == "click"):

            actions = ActionChains(driver)
            actions.move_to_element(element).click().release().perform()

        elif(event == "contextmenu"):

            actions = ActionChains(driver)
            actions.move_to_element(element).context_click().release().perform()
        
        elif(event == "mouseover"):

            actions = ActionChains(driver)
            actions.move_to_element(element).perform()

        time.sleep(1)
                    
def Exploration(graph,driver):

    for state in graph:
        ExplorationState(state,graph[state],driver)


def PreProcessJSON(graph):

    newGraph = {}
    for node in graph:

        if(node["selector"] not in newGraph):
            newGraph[node["selector"]] = {}
            newGraph[node["selector"]]["events"] = []
            newGraph[node["selector"]]["brushable"] = node["brushable"]
            newGraph[node["selector"]]["zoomable"] = node["zoomable"]
            newGraph[node["selector"]]["tag"] = node["tag"]
            newGraph[node["selector"]]["attributes"] = node["attributes"]


            newGraph[node["selector"]]["styles"] = {}
            for pair in node["styles"]:

                newGraph[node["selector"]]["styles"][pair["name"]] = pair["value"]

        newGraph[node["selector"]]["events"].append(node["event"])

    return newGraph


if(__name__=="__main__"):
    
    #open the statechart json file
    statechart_j=open('brexitOutput.json')

    #returns the JSON object as a dictionary
    statechart_dict=json.load(statechart_j)

    #Data structure for that will contain the graph
    graph={}

    graph = PreProcessJSON(statechart_dict)

    #Print graph representation
    print("------------------------------------------------------------------------------")
    print("------------------------------------------------------------------------------")
    #print("Graph:",json.dumps(graph,indent=4))

    #Save graph on a file
    with open('statechart_brexit.json', 'w') as fp:
        json.dump(graph, fp,  indent=4)

    print(transitionsList)
    print(eventsList)

    driver = webdriver.Chrome()
    driver.get("http://localhost:8000/brexitVisualization.html")
    driver.maximize_window()

    #Exploration of th graph
    Exploration(graph,driver)

    driver.close()

    print(explorationSequence)
    
    print("------------------------------------------------------------------------------")