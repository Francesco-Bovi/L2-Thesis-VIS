# L2-Thesis-VIS
Implementation of a semi-automatic mechanism for exploring the statechart of a web-based interface.

Master's thesis Sapienza-University of Rome.

## Report
The first action needed is to extract the JSON file representing the statechart of the interface with the different D3 widgets available on the browser. Once I got this file, my goal will be to create a program that simulates the random exploration of the interface. 

Given the output of the program, representing an ordered sequence of interactions, I reproduce it in the real browser visualization, in order to use the LOGs of the framework to understand where there can be latency problems.

### Statechart ([link here](https://github.com/Francesco-Bovi/L2-Thesis-VIS/blob/main/xstate_visualization_statechart.json))
The statechart is composed by state nodes organized hierarchically, indeed there are some nodes like ```range``` that contains subnodes representing the possible interactions executable in it, for example ```hover```, ```handleR```, ```handleL``` and ```handleLR```.

A state node can have a set of transitions that could be performed to reach another state on the same hierarchical level, so that state ```hover``` (substate of ```range```) has three possible transitions to reach ```handleR```, ```handleL``` and ```handleLR```.

A screenshot of the JSON file where there can be seen clearly transitions and subnodes is the following:
![image](https://user-images.githubusercontent.com/81032317/161439165-edb081fd-6e6f-43d8-b22a-6207119522e6.png)

where from ```range``` we can go to ```rest``` through MOUSEOUT in the ```on``` field, and in the field ```states``` we have the list of subnodes.

Among the problem that can arises using this file there are the fact that:
- Not all the field are present in all the state nodes (like the id, set of substates and set of transitions)
- Subnotes doesn't have a transition back to their "parent node", since they are not really child but represent the set of possible values (interactions) that the "parent node" can assume;

---

### v0 ([link here](https://github.com/Francesco-Bovi/L2-Thesis-VIS/blob/main/graphbuilder_v0.py))
At the beginning my idea was to represent all the states at the same level, using a python dictionary where each key is the ID of the state and as value it contains an array with all possbile transitions. The output of the program is something like:

[Output of version 0](https://github.com/Francesco-Bovi/L2-Thesis-VIS/blob/main/statechartv0.json)

Obviously this representation is not good at all for many reason, the first is that many states have the same substate ```hover``` and we know that in a dictionary have unique keys, then another problem is that during the exploration of this dictionary we can remain stuck in nodes that haven't a set of transactions or in loops, even if a possible solution can be adding a transaction to the "parent node". The more relevant problem of this configuration is that we don't have an hierarchy, so I since the beginning I can go to any state and I will never move in deep.

---

### v1 ([link here](https://github.com/Francesco-Bovi/L2-Thesis-VIS/blob/main/graphbuilder_v1.py))
In this second version the output of the program is a sort of clean version of the original JSON file where, for each state, we have only the list of possible substates and transactions:

[Output of version 1](https://github.com/Francesco-Bovi/L2-Thesis-VIS/blob/main/statechartv1.json)

I noticed that in this case, during the exploration, problems arise when we arrive to a node that have no transitions and no substates, remaining stuck in that node. Even in this casa a possible solution could be to add a transition to the "parent node" when we arrive to this kind of states.

### v2 ([link here](https://github.com/Francesco-Bovi/L2-Thesis-VIS/blob/main/graphbuilder_v2.py))
In this version of the program I create a class ```State``` with the following attributes:
- ID: The identifier of the state node;
- Transitions: An array containing the set of all possible transitions to a state at the same hierachical level;
- Subsets: An array containing the set of references to sub-states of the state node;
- Container: The reference to the container (if exists, otherwise None), so to the node that has the current state as one of its substates;
- Score: A score used in the exploration phase;
I create an istance of the class ```State``` with the proper attributes every time I need to add a node during the exploration of the JSON. It's important to higlight that in the attributes Subsets and Container I don't have a string but a real reference to the istances representing the states. 

[Output of version 2](https://github.com/Francesco-Bovi/L2-Thesis-VIS/blob/main/statechartv2.txt)

This configuration helps a lot during a random scanning of the statechart's graph, indeed for each node I choose randomly, taking a number from zero to two, how to proceed:

0: Continue the exploration going to a state in the set of Subsets;

1: Continue the exploration going to a state in the set of Transitions;

2: Continue the exploration going back to the Container;

If a node has some of those attributes empty, the choice will obviously be to one of the others, in order to avoid remaining stuck.

---

### Meet 04/04

During the Meet of April 4th what emerged is that hierarchy only complicates the structure, since it was just a convenience for the JSON but it's not fundamental, in fact as we have seen previously there are sono states, that we call **Container** that are not real states since they enter directly in an initial state representing its initial value, like  ```Range``` that goes directly in ```hover```. Given these premises the best idea would be to unroll the hierarchy of the JSON representing the statechart, in this way we would have all the states at the same level. The implementation of this structure has been done in the 3rd version of the program described in the next paragraph.

---

### v3 ([link here](https://github.com/Francesco-Bovi/L2-Thesis-VIS/blob/main/graphbuilder_v3_2.py))
This version of the program aims to produce as output a dictionary in which all the states are at the same hierarchical level, the differences between this version and v0 arise from the fact that:
- Since we are using a python dictionary it cannot contains duplicates, so in order to avoid overwriting states with the same name, but belonging to different containers, we save each state with key:  ```state_name + _ + container_name```, where ```state_name``` represents the name of the current state and ```container_name``` represents the name of the Container in which the state belongs;
- **Container** states, which have always an initial state (usually *hover* or *idle*), represents automatically this initial state, incorporating its transitions. Indeed if we enter, for example, the state ```Range```, we can consider ourselves as in ```Range:{hover```.
- In this version all the internal states inherit transitions from their Containers, in this way we can avoid using an hierarchy. As an example we want to have the possibility to move from any internal state to the state ```Rest```, since all principal Containers like ```Range, Scatter and Barchart``` have a transition **MOUSEOUT** to ```Rest```;

Once this structure (represented as a dictionary) has been created, we create another dictionary with the same keys in which we will store a score that we will increment, when we traverse that node, during the exploration (so we initialize all the keys with value 0 at the beginning).

In the exploration of this structure of the statechart, at first a random number representing the possible initila states is used (this number must be between 0 and 3 in our case, since we have 4 possible initial states: ```Rest, Range, Scatter or Barchart```), then we give priority to states which have 0 as score (which means they have not been visited yet) and, if all the possible next states already have been visited, we choose randomly. In this way out program will visit all the states at least once and will stop when all the states have been visited, obviously at the end of the execution the states with the highest score will be the Container nodes, considering the fact that they are the ones from which we can visit the majority of other states.

[Output of version 3](https://github.com/Francesco-Bovi/L2-Thesis-VIS/blob/main/statechartv3_2.json)

During the implementation of this version some problems emerged, here we list which have been solved (and how) which not:
- [x] Some states, like ```brush``` in our case,  are of type ```parallel```, which means it allows the execution of substates at the same time (the substate ```x``` and ```y``` in this case), which in turn can assume different values based on their structure (```right```,```left``` for x and ```up```,```down``` for y). We "solved" this problem by creating a key in the dictionary for each substates, so allowing the state with type parallel to go to one of this substates one by one and not contemporary;
- [x] There are states like ```zoom``` and ```click``` that are not real states, in fact they goes back automatically to their Container node after 100ms of their execution. In order to abstract this in our structure we have modified the original JSON to an auxiliar version ([auxiliar version](https://github.com/Francesco-Bovi/L2-Thesis-VIS/blob/main/xstate_visualization_statechart_aux.json)) in which we replace those states with a transition from their Container node to themselves (like for example in ```scatter``` we add a transition [ZOOM,```scatter```]);
- [ ] In our program we don't have implemented any control or conditions, states like ```brushRegion``` or ```brushBorder``` can be visited only once a ```brush``` has been performed. Furthermore some states cannot be performed forever like ```dragR:{right``` when I arrived to ```dragR:{max```;