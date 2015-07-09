## Max's 2015 Summer Internship

###Random Walkers - 06/25/2015

Random walkers pick a single point from a variety of possible points, then move to it, creating a random path that can be displayed as a graph.  I made program to create random walkers along diagonal axes, using numpy for random generation and array organization and matplotlib for plotting the data.  I then made a similar program that ran random walkers along vertical and horizontal axes.  Depeding on input, they can both be run in two or three dimensions; however, since there is no function for user input, this must be accomplished through editing value in the file.

![vertical axes 2D random walker, line format](/RandomWalk/RandWalk2D.png)
![vertical axes 3D random walker, dot format](/RandomWalk/RandWalkDot.png)

###Mapping - 07/03/2015

The past week, I made program that reads data from a .csv file and plots on a Leaflet map using MarkerCluster.  I later modified it to give each ship a different color using MakiMarkers, and to input and retrieve data from a MySQL database using MySQLdb.  
I had to learn SQL (MySQL), as well as refresh my knowledge of HTML and Javascript, in order to complete this.

![zoomed out map to display markerclusters](/mapping/ZoomedOut.png)
![zoomed in map to display ship color differentiation](/mapping/ZoomedIn.png)

####07/06/2015
Added constraints system, which supports functions such as limiting the ships displayed based on name, timestamp (as a range), or latitude and longitude (also as ranges).  Also, experimented with doctests, but removed them due to the fact that there was too large a variety of returns on each function or method.

![map with data limited by two time ranges and two ship names](/mapping/Constrained.png)

###Linear Algebra - 07/09/2015
I've been learning (very) basic linear algebra this week.  I made a python file with several linear algebra-related methods, such as a gauss-jordan solver.  The solver occassionally fails, possibly when finding infinite sets of solutions.  I made a different file that created a noisy graph, then could find the slope of its line of best fit.  It can also generate linear graphs (no exponential graphs) for this purpose.  
Later, I added functionality of graphing.  This is an example graph that filters noise through the two filter methods that I added: least squares and moving average window.

![graph - filtering out noise through least squares and moving average window](/LinearAlgebra/NoiseFilter.png)
