# L2-Thesis-VIS
Implementation of a semi-automatic mechanism for exploring the statechart of a web-based interface.

Master's thesis Sapienza-University of Rome.

## Report
The first action needed is to extract the JSON file representing the statechart of the interface with the different D3 widgets available on the browser. Once I got this file, my goal will be to create a program that simulates the random exploration of the interface. 

Given the output of the program, representing an ordered sequence of interactions, I reproduce it in the real browser visualization, in order to use the LOGs of the framework to understand where there can be latency problems.

### Statechart
The statechart is composed by state nodes organized hierarchically, indeed there are some nodes like ```range``` that contains subnodes representing the possible interactions executable in it, for example ```hover```, ```handleR```, ```handleL``` and ```handleLR```.

A state node can have a set of transitions that could be performed to reach another state on the same hierarchical level, so that state ```hover``` (substate of ```range```) has three possible transitions to reach ```handleR```, ```handleL``` and ```handleLR```.

A screenshot of the JSON file where there can be seen clearly transitions and subnodes is the following:
![image](https://user-images.githubusercontent.com/81032317/161439165-edb081fd-6e6f-43d8-b22a-6207119522e6.png)

where from ```range``` we can go to ```rest``` through MOUSEOUT in the ```on``` field, and in the field ```states``` we have the list of subnodes.

Among the problem that can arises using this file there are the fact that:
- Not all the field are present in all the state nodes (like the id, set of substates and set of transitions)
- Subnotes doesn't have a transition back to their "parent node", since they are not really child but represent the set of possible values (interactions) that the "parent node" can assume;

### v0
At the beginning my idea was to represent all the states at the same level, using a python dictionary where each key is the ID of the state and as value it contains an array with all possbile transitions. The output of the program is something like:

![image](https://user-images.githubusercontent.com/81032317/161448000-4d361bcc-f252-4569-a404-8c4c4a589074.png)

Obviously this representation is not good at all for many reason, the first is that many states have the same substate ```hover``` and we know that in a dictionary have unique keys, then another problem is that during the exploration of this dictionary we can remain stuck in nodes that haven't a set of transactions or in loops, even if a possible solution can be adding a transaction to the "parent node". The more relevant problem of this configuration is that we don't have an hierarchy, so I since the beginning I can go to any state and I will never move in deep.

### v1
In this second version the output of the program is a sort of clean version of the original JSON file where, for each state, we have only the list of possible substates and transactions:

![image](https://user-images.githubusercontent.com/81032317/161440339-bf90cf5a-e654-456b-9078-e293f994141e.png)

I noticed that in this case, during the exploration, problems arise when we arrive to a node that have no transitions and no substates, remaining stuck in that node. Even in this casa a possible solution could be to add a transition to the "parent node" when we arrive to this kind of states.

### v2
In this version of the program I create a class ```State``` with the following attributes:
- ID: The identifier of the state node;
- Transitions: An array containing the set of all possible transitions to a state at the same hierachical level;
- Subsets: An array containing the set of references to sub-states of the state node;
- Container: The reference to the container (if exists, otherwise None), so to the node that has the current state as one of its substates;
- Score: A score used in the exploration phase;
I create an istance of the class ```State``` with the proper attributes every time I need to add a node during the exploration of the JSON. It's important to higlight that in the attributes Subsets and Container I don't have a string but a real reference to the istances representing the states. 

This configuration helps a lot during a random scanning of the statechart's graph, indeed for each node I choose randomly, taking a number from zero to two, how to proceed:

0: Continue the exploration going to a state in the set of Subsets;

1: Continue the exploration going to a state in the set of Transitions;

2: Continue the exploration going back to the Container;

If some nodes has one of those attributes empty, the choice will obviously be to one of the others, in order to avoid remaining stuck.
