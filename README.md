# Intelligent-Transit
Transit REST API written with Python Django

!The Server is still in development! 

The Intelligent transit project is a project that helps making transit routing easier. It includes an API that takes as input three JSON files:
  • Markers: A list of nodes where the bus passes by.
  •Crosses: A list of stations where a person can change buses at.
  •Routes: The combination of markers and crosses that form a route.

The API will take as input the source and destination as coordinates and using these information it will compute the shortest path including traffic and least cost from the source to the destination.

The application “3al Khat” is a demo of the API. It shows the map of Beirut and gives the user the ability to select his source and his destination. Then the app uses the information returned by the API to display the path proposed by the API. The whole system does not rely on google API it uses a graph built on the server to return the nodes. Then these nodes are used as markers to query the google API to draw the polyline (route).
Link to 3alKhat Project : https://github.com/JadCham/3alKhat-TransitApp

The web panel is used to edit the JSON files. It is the crucial part of the project. It manages the data that is used to build the graph: the markers, the routes and the crosses.
Link to the Web Panel Project : https://github.com/JadCham/Intelligent-Transit-Web-Panel

b. Features:
The features of the application include:
• Shortest path using transit routes
• Take traffic into consideration
• Least Cost
• Generic
• Adaptable
• Works in cities with no proper infrastructures

c. Solved Problems:

When we worked on the project we had in mind solving a well known problem.
We decided to work on a project to encourage people use buses instead of taking their cars.In Beirut the traffic jams are becoming a bigger problem everyday.
On the other side the city has a transit system but without a proper infrastructure. This project gives this transit system a shot to become a better system.
