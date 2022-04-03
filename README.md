# L2-Thesis-VIS
Implementation of a semi-automatic mechanism for exploring the statechart of a web-based interface.

Master's thesis Sapienza-University of Rome.

### Report
The first action needed is to extract the JSON file representing the statechart of the interface with the different D3 widgets available on the browser. Once I got this file, my goal will be to create a program that simulates the random exploration of the interface. 

Given the output of the program, representing an ordered sequence of interactions, I reproduce it in the real browser visualization, in order to use the LOGs of the framework to understand where there can be latency problems.

### Statechart
The statechart is composed by state nodes organized hierarchically, indeed there are some nodes like ```range ``` that contains subnodes representing the possible interactions executable in ```range ```, for example ```hover```, ```handleR```, ```handleL``` and ```handleLR```. 
