import json

graph={}

def add_node_parent(s):
    global graph
    #print("----Adding node:",s,"----")
    if(s!='rest'):
        graph[s+"_hover"]=[]
    else:
        graph[s]=[]

def add_state(s):
    global graph
    #print("----Adding node:",s,"----")
    graph[s]=[]

def traverse_json(node):
    global states_aux
    if(node.get('states') is None):
        return
    else:
        #If is not a parent node add it
        if(node.get('id') not in states_aux):
            add_state(node.get('id'))
        #Explore other childs
        for i in node.get('states'):
            traverse_json(node.get('states').get(i))

#open the statechart json file
statechart_j=open('xstate_visualization_statechart.json')

#returns the JSON object as a dictionary
statechart_dict=json.load(statechart_j)

#List with all states except for rest
states_aux=[]

for i in statechart_dict['states']:
    #Print name of all the states/interactions
    print(i)

    #Aux vector in order to not insert again parent nodes
    states_aux.append(i)

    #Add principal states with hovering
    add_node_parent(i)

    #Add child states
    traverse_json(statechart_dict.get('states').get(i))

#Print graph representation
print("Graph representation: ",graph)