# L2-Thesis-VIS
Implementation of a semi-automatic mechanism for exploring the statechart of a web-based interface.

Master's thesis Sapienza-University of Rome.

### Report
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

![image](https://user-images.githubusercontent.com/81032317/161439724-39943927-14de-42d2-a6c1-632567bac9dc.png)

Obviously this representation is not good at all for many reason, the first is that many states have the same substate ```hover``` and we know that in a dictionary have unique keys, then another relevant problem is that during the exploration of this dictionary we can remain stuck in nodes that haven't a set of transactions or in loops, even if a possible solution can be adding a transaction to the "parent node".
