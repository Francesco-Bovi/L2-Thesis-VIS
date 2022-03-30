import json

graph={}

def add_state(s,check_rest):
    global graph
    if(check_rest is False):
        graph[s]=[['rest','MOUSEOUT']]
    else:
        graph[s]=[]

#open the statechart json file
statechart_j=open('xstate_visualization_statechart.json')

#returns the JSON object as a dictionary
statechart_dict=json.load(statechart_j)

#Print the JSON as a dictionary
#print(statechart_dict)

#List with all states except for rest
states_aux=[]

#Print states
for i in statechart_dict['states']:
    #Print name of all the states/interactions
    print(i)

    #If the state is not REST we can automatically add a transition to
    # REST with MOUSEOUT
    if(i!='rest'):
        add_state(i,False)
        states_aux.append(i)
    else:
        add_state(i,True)

print(states_aux)
#Here we add to REST all transition to other states with MOUSEOVER
for i in states_aux:
    temp = [i, 'MOUSEOVER']
    graph['rest'].append(temp)

#Print graph representation
print("Graph representation: ",graph)