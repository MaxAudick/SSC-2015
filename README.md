## Max's 2015 Summer Internship

###Random Walkers - 06/25/2015

Made program to create random walkers along diagonal axes, using numpy for random generation and array organization and matplotlib for plotting the data.  Also made similar program that created random walkers along vertical axes.  Can run in 2 or 3 dimensions, depending on how file is edited.

![vertical axes 2D random walker, line format](/RandomWalk/RandWalk2D.png)
![vertical axes 3D random walker, dot format](/RandomWalk/RandWalkDot.png)

###Mapping - 07/06/2015

Made program that reads data from a csv file and plots on a Leaflet map using MarkerCluster.  Modified to give each ship a different color using MakiMarkers, and to input and retrieve data from a MySQL database using MySQLdb.

![zoomed out map to display markerclusters](/mapping/ZoomedOut.png)
![zoomed in map to display ship color differentiation](/mapping/ZoomedIn.png)

####07/06/2015
Added constraints system, which supports functions such as limiting the ships displayed based on name, timestamp (as a range), or latitude and longitude (also as ranges).  Also, experimented with doctests, but removed them due to the fact that there was too large a variety of returns on each function or method.

![map with data limited by two time ranges and two ship names](/mapping/Constrained.png)
