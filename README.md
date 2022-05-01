# L2-Thesis-VIS
Implementation of a semi-automatic mechanism for exploring the statechart of a web-based interface.

Master's thesis Sapienza-University of Rome.

---



## Report
The first action needed is to extract the JSON file representing the statechart of the interface with the different D3 widgets available on the browser. Once I got this file, my goal will be to create a program that simulates a random exploration of the interface. 

Given the output of this program, representing an ordered sequence of interactions over the graphical elements of the interface, I will reproduce it in the real browser visualization, in order to obtain the LOGs from a framework for exploratory data systems, and use them to understand where there can be latency problems and solve them with the most suitable optimization technique (improving performances).

### Statechart ([link here](https://github.com/Francesco-Bovi/L2-Thesis-VIS/blob/main/xstate_visualization_statechart.json))
The statechart is composed by state nodes organized hierarchically, indeed there are some nodes, that we will denote as **Container** (like ```range```), which contains subnodes representing the possible interactions that can be performed inside it, for example ```hover```, ```handleR```, ```handleL``` and ```handleLR```.

Every node (Container or not) can have a set of transitions, which are executed to reach another state on the same hierarchical level, for example that state ```hover``` (substate of ```range```), through the same action **MOUSEMOVE** reach one among ```handleR```, ```handleL``` and ```handleLR```.

A screenshot of the JSON file, where there can be seen clearly transitions and subnodes, is the following:

![image](https://user-images.githubusercontent.com/81032317/161439165-edb081fd-6e6f-43d8-b22a-6207119522e6.png)

where from ```range``` we can go to ```rest``` through the **MOUSEOUT** transition in the ```on``` field, and in the field ```states``` we have the list of subnodes.

Among the problem that can arises using this file there are the fact that:
- Not all the nodes have the same fileds (like the ```id```, ```states``` and ```on```)
- Subnotes doesn't have a transition back to their Container node, since they are not really child but represent the set of possible values (interactions) that the it can assume;

---

### v0 ([link here](https://github.com/Francesco-Bovi/L2-Thesis-VIS/blob/main/graphbuilder_v0.py))
At the beginning my idea was to represent all the states at the same level, using a python dictionary where each key is the ID of the state and its value is an array with all possbile transitions. The output of the program would be:

[Output of version 0](https://github.com/Francesco-Bovi/L2-Thesis-VIS/blob/main/statechartv0.json)

Obviously this representation is not good at all for many reason: the first is that many states have the same substates ```hover``` and ```idle```, so since we know that in a dictionary have unique keys this will lead to information loss; Then another problem is that during the exploration of this dictionary we can remain stuck in nodes that haven't a set of transactions, or, in loops, even if a simple solution could be adding to each key a transaction to its Container node.

---

### v1 ([link here](https://github.com/Francesco-Bovi/L2-Thesis-VIS/blob/main/graphbuilder_v1.py))
In this second version the output of the program is a sort of clean version of the original JSON file where, for each state, we have only the list of possible substates and transactions, so differently from version 0 in this case I maintained the hierarchical structure of the nodes:

[Output of version 1](https://github.com/Francesco-Bovi/L2-Thesis-VIS/blob/main/statechartv1.json)

I noticed, during the exploration, that problems arise when we arrive to a node that have no transitions and no substates, remaining stuck. Even in this casa a possible solution could be to add a transition to the Container node once arrived to this kind of states.

---

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

During the Meet of April 4th what emerged is that hierarchy only complicates the structure, since it was just a convenience for the JSON but it's not fundamental, in fact as we have seen previously there are sono states, that we call **Container** that are not real states since they enter directly in an initial state representing its initial value, like  ```range``` that goes directly in ```hover```. Given these premises the best idea would be to unroll the hierarchy of the JSON representing the statechart, in this way we would have all the states at the same level. The implementation of this structure has been done in the 3rd version of the program described in the next paragraph.

---

### v3 ([link here](https://github.com/Francesco-Bovi/L2-Thesis-VIS/blob/main/graphbuilder_v3_2.py))
This version of the program aims to produce as output a dictionary in which all the states are at the same hierarchical level, the differences between this version and v0 arise from the fact that:
- Since we are using a python dictionary it cannot contains duplicates, so in order to avoid overwriting states with the same name, but belonging to different containers, we save each state with key:  ```state_name + _ + container_name```, where ```state_name``` represents the name of the current state and ```container_name``` represents the name of the Container in which the state belongs;
- **Container** states, which have always an initial state (usually *hover* or *idle*), represents automatically this initial state, incorporating its transitions. Indeed if we enter, for example, the state ```range```, we can consider ourselves as in "range:{hover".
- In this version all the internal states inherit transitions from their Containers, in this way we can avoid using an hierarchy. As an example we want to have the possibility to move from any internal state to the state ```rest```, since all principal Containers like ```range, scatter and barchart``` have a transition **MOUSEOUT** to ```rest```;

Once this structure (represented as a dictionary) has been created, we create another dictionary with the same keys in which we will store a score that we will increment, when we traverse that node, during the exploration (so we initialize all the keys with value 0 at the beginning).

In the exploration of this structure of the statechart, at first a random number representing the possible initila states is used (this number must be between 0 and 3 in our case, since we have 4 possible initial states: ```rest, range, scatter or barchart```), then we give priority to states which have 0 as score (which means they have not been visited yet) and, if all the possible next states already have been visited, we choose randomly. In this way out program will visit all the states at least once and will stop when all the states have been visited, obviously at the end of the execution the states with the highest score will be the Container nodes, considering the fact that they are the ones from which we can visit the majority of other states.

[Output of version 3](https://github.com/Francesco-Bovi/L2-Thesis-VIS/blob/main/statechartv3_2.json)

During the implementation of this version some problems emerged, here we list which have been solved (and how) which not:
- [x] Some states, like ```brush``` in our case,  are of type ```parallel```, which means it allows the execution of substates at the same time (the substate ```x``` and ```y``` in this case), which in turn can assume different values based on their structure (```right```,```left``` for x and ```up```,```down``` for y). We "solved" this problem by creating a key in the dictionary for each substates, so allowing the state with type parallel to go to one of this substates one by one and not contemporary;
- [x] There are states like ```zoom``` and ```click``` that are not real states, in fact they goes back automatically to their Container node after 100ms of their execution. In order to abstract this in our structure we have modified the original JSON to an auxiliar version ([auxiliar version](https://github.com/Francesco-Bovi/L2-Thesis-VIS/blob/main/xstate_visualization_statechart_aux.json)) in which we replace those states with a transition from their Container node to themselves (like for example in ```scatter``` we add a transition [ZOOM,```scatter```]);
- [ ] In our program we don't have implemented any control or conditions, states like ```brushRegion``` or ```brushBorder``` can be visited only once a ```brush``` has been performed. Furthermore some states cannot be performed forever like "dragR:{right" when I arrived to "dragR:{max";

---

### v3.3 ([states](https://github.com/Francesco-Bovi/L2-Thesis-VIS/blob/main/graphbuilder_v3_3_states.py) - [transitions](https://github.com/Francesco-Bovi/L2-Thesis-VIS/blob/main/graphbuilder_v3_3_transition.py))
Version 3 of the program has two different subversions, one for the states and the other for transitions. What we want to achieve in this case is the customization of the exploration, giving priority to some transitions rathen than other or setting for some states how many times they must be visited before the algorithm ends.
(TODO better because for certain parameters goes to Maximum Recursion).

---

### v3.4 ([link here](https://github.com/Francesco-Bovi/L2-Thesis-VIS/blob/main/graphbuilder_v3_4.py))
This version of the program uses the same structure of the version 3 for representing the JSON statechart, but in this case we have a different type of exploration. In fact, given from user's input a state ```initial_state``` and a number ```input_n```, the program will print on screen all the possible paths of length ```input_n``` with source node ```initial_state```. In order to achieve this goal we use a queue data structure in which we store a list with all the states for each possible path, so at each iteration we update the lists, we will stop and print them when they reach length ```input_n```.

---

### Meet 11/04

April 11th meet was held with the presence of Professor Angelini, who clarified the path for the realization of the project, including which steps to tackle individually and which together Matteo and I, the workflow can be analyzed [here](https://github.com/Francesco-Bovi/L2-Thesis-VIS/blob/main/WorkFlow.jpg).

About the exploration what emerged is that currently we have an uninformed one, so we can visit all the states once randomly, or we can find all the possible paths of length N starting from a state, but we don't use any information about the context of the interactions that we are performing on the visualization, in this way we can find only some ciritical issues of latency. What we want now is to have an informed exploration in such a way that it can be more realistic, in a smarter way, in order to find other kind of critical points, based on the type of interaction performed. We can categorize the interactions into three orders of magnitude: low, medium and big, in order to understand, which parts of the data can create latency problems. 

Once this phase is over, the next phase consists in creating an automatic program that performs the exploration directly on the browser, so to collect the information arising from the framework and then applying the optimization techniques for improving performances.

---

### v3.5 ([slider](https://github.com/Francesco-Bovi/L2-Thesis-VIS/blob/main/graphbuilder_range.py) - [scatter](https://github.com/Francesco-Bovi/L2-Thesis-VIS/blob/main/graphbuilder_scatter.py) - [barchart](https://github.com/Francesco-Bovi/L2-Thesis-VIS/blob/main/graphbuilder_histogram.py))

I create 3 custom JSON, each containing only one main state other than that of ```rest```, then I add a filed ```context``` in each of these states in order to have information that can help me for the informed exploration:
- **slider**: What we need is the type of slider (if range, so with 2 handlers or not), the position of the handler/s  and the maximum and minimum value that they can reach. In this way when I'm dragging I can update the position of the handlers and check if they are in the min or max value;
- **barchart**: This is maybe the easiest interaction, what we need is the length of the x or y axes (depends on how the rectangles are oriented) and the width of each rectangle, in order to know how many are them. During the CLICK interaction when a bin is selected it's index is saved in a variable, so when a new bin is selected this variable is updated or when one is deselected the value will be None;
- **scatter**: The scatter plot is probably the most difficult one to handle, in fact we need a lot of information: the default values on the x and y axes, their minimum and maximum values and the default zoomLevel. During the panning I change the current values on the x and y axes, in such a way that if I perform a BRUSHING I can selected the intervals for the points of the rectangle I'm brushing corretly (the value of these point must be in the interval of the x and y axes). While for the ZOOM is used a variable that increments its value if zooming in or decrements if zooming out.

---

### v4([link here](https://github.com/Francesco-Bovi/L2-Thesis-VIS/blob/main/graphbuilder_v4.py))

In this version I create another custom JSON, in which for each Container node a new field ```context``` is added, where a set of predefined information is presented, same for all the nodes. Those information are:

- **xwidth**: Width of the x-axis;
- **ywidth**: Width of the y-axis;
- **xstart**: Value of the origin of the x-axis;
- **ystart**: Value of the origin of the y-axis;
- **panstep**: How much the axis move during a panning;
- **zoomlevel**: Current level of zoom (default is 0);
- **rangezoomlevels**: Range of values that the zoomlevel can assume [min,max] (it can go from negative to positive, representing zoomout and zoomin);
- **zoomstep**: How much the axes shrink or widen (in the case of zoomout) at each step;
- **binsize**: Width of a bin (in this case we probably have a bin chart);
- **itemselected**: Integer or ID of the bin selected (if selection with click is possible);
- **numitems**: Number of bins;
- **handleL**: Position of the left handle in a slider;
- **handleR**: Position of the right handle in a slider (if it's not a range slider this field is null);
- **brushx**: Starting and ending point in the x-axis of a brush area ([xstart,xend]);
- **brushy**: Starting and ending point in the y-axis of a brush area ([ystart,yend]);

Those are all the information needed to execute all the different transitions in a statchart, for example given a state in which the only information are **xwidth**, **handleL** and/or **handleR**, we can consider that state a slider, if the information are instead **binsize**, **itemselected**, **numitems**, **handleL** and **handleR** we are in a scatterplot where we can perform brushing and zooming. 

In this way during the exploration of the statechart, when performing a transition we have to update the value of the variables in the context presented above, simulating a real exploration, like one performed by an user.

---

### Meet 21/04

The most interesting aspects that emerged during this meet are:
- The possibility that the designer of the visualization tells us what kind of interactors are present;
- Differentiate the interactors using a field **type** in the statechart;
- All the information that will be used for the informed exploration are passed in the statchart by Matteo's program;

---

After that meet I decided to use Matteo's script to start looking at all the fields it returns and how to use them in my program during the informed exploration. What Matteo's script returns is a list of fields describes as follow:

- **node**: The object for the current node;
- **tag**: String of the element tag name;
- **id**: String of the element id (null if absent);
- **class**: List of the strings of the element classes (null if no class is there);
- **parents**: List of objects {tag, id, class} for each container node going outwards from the current one, stopping right before the 'body' tag (null if no eligible one is there);
- **attributes**: List of objects {name, value} for each element attribute (excluded 'id', 'class' and 'style');
- **styles**: List of objects {name, value} for each element style (including default ones though);
- **data**: List of objects {name, value} for each element attached data (null if there is none);
- **event**: String of the currently considered event of the element;
- **eventFunction**: String of the function triggered by the aforementioned event;
- **brushable**: Object {handles, directions, brush_extent, selection_extent} with brush informations (null if the event is not brush-related);
- **zoombale**: Object {scale, translate_x, translate_y} with zoom informations (null if the event is not zoom-related);
- **leadsToState**:Integer indicating to which state triggering this event will bring you, with respect to the ids used in the states global list (at first they are all initialized to 0, the rest state id);

Testing this script on different d3.js visualizations ([listed here](https://github.com/Francesco-Bovi/L2-Thesis-VIS/blob/main/d3Visualizations.txt)) many interesting aspects emerged:

- When an element is brushable, the events triggered can be "mousedown" or "touchstart" (but we can exlude this case, since we are not working with touch screen devices);
- Once a brush area is created, in order to move it the event triggered is a "mousedown" performed inside that area and then move the cursor;
- The events that manage the zoom on an element are "wheel", "dbclick" (that double the zoom scale every time is performed, while with wheel we have a high granularity);
- A zoomable element is also pannable and it's handled by the "mousedown" events that changes the translate_x and translate_y values;
- It's not possible that a brushable element is also zoomable, because the "mousedown" event creates collision, the only solution would be change the default configuration of brushing or zooming using another event instead of the "mousedown";
- A slider can be modelled in very different ways (html type input, d3.slider, customized or with brushing for example);
- When a slider is modelled using d3.sliderBottom (or sliderVertical) we can use the information in the styles fields "aria-valuemax", "aria-valuemin" and "aria-valuenow";
- With high probability we can assume that when the "mousedown" event is present on an element, but the latter is not brushable or zoomable, then the action that is performed is a dragging. In this case a problem can be the fact that I have to know what interactor is to move in the correct direction;

### Meet 28/04

Prior to this meet the problems encountered were:

1. Since Selenium (the framework through which the automatic exploration of the browser is performed) moves the element in the screen by using pixels coordinate, a problem could be moving the sliders by a certain amount of values;
2. How handle the cases in which the events are not the default ones but they're customized (like the "contextmenu" for panning);
3. Is it possible to simulate the zoom only by using the double click interaction during the automatic exploration? Since I was struggling to simulate the wheel for zooming;
4. Problem when a slider has a predefined step and/or when the value it can assume are not numeric (like dates);

After the meet those problems were solved using the following methods:

1. Using a function that, given the width of the slider, the max and min values it can assume, makes the proportion to find by how many pixels the handler needs to be moved to achieve a certain value;
2. For now we try to handle only the default event, unless a certain configuration even if it's not the default one is very popular;
3. It's better to simulate the wheel since it has a greater granularity and is the most used by the users (porblem solved);
4. That cases don't need to be handled since they don't create dynamic queries that can affect the performances of the visualization;

One of the goals that emerged from this meet is to be able to isolate the latency due to the automation of Selenium during the browser exploration of the visualization
