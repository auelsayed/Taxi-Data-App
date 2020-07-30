# Taxi-Data-App

# Description

This is a web app developed using Flask as the backend that displays some interesting data regarding taxi rides taken in NYC yellow taxis. The map is generated using d3.js and much of the DOM manipulation uses d3.js as well.

# How to use

Hovering over any of the zones (or regions) pops us a helpful tooltip with the name of each zone. Clicking on any zone will show the zone as twice the size in an information card that displays the number of taxi rides in a specific year that either had this zone as a pickup point of the ride or as a dropoff point. Hovering over either of these numbers will highlight the respective zones on the map. Hovering over or clicking on the left "button" will highlight the zones where the currently selected zone served as the pickup zone (i.e. it displays where the all rides starting at this zone ended). Hovering over or clicking on the right "button" will highlight the zones where the currently selected zone served as the dropoff zone (i.e. it displays where the all rides ending at this zone started). Hovering over these "buttons" will temporarily highlight the results, while clicking on them will keep them highlighted until another region is selected, the year of the data is changed, or the button is clicked again. If both buttons are clicked or one is highlighed and the other is clicked, the areas overlapping are highlighted in green. The year of the data can be changed by a dropdown menu available in the menu card with the options being 2017, 2018, and 2019. The datasets are available for far earlier years, but the system of using zones instead of actual latitude and logitude for pickup and dropoff locations began in 2017. The default is set to be 2019 (the latest dataset available).


# Things to note

To give some context, the taxi rides datasets give pickup and dropoff locations (the main 2 columns used in this project) as zones. These zones are described by the NYC Open Data site as the following: "The taxi zones are roughly based on NYC Department of City Planning’s Neighborhood Tabulation Areas (NTAs) and are meant to approximate neighborhoods, so you can see which neighborhood a passenger was picked up in, and which neighborhood they were dropped off in."
These zones are what make up the map displayed on the website. An issue that popped up was that the taxi rides datasets go up to zone 265 for various rides as pickup or dropoff locations. However, the "NYC Taxi Zones" (found [here](https://data.cityofnewyork.us/Transportation/NYC-Taxi-Zones/d3c5-ddgc)) gives information upto zone 262. Without the information provided by this dataset, I am unable to graph rides that involve zones 263-265. Therefore, I had to filter out rides that used zones within that range. Other rides that were filtered out are ones that had the total cost of the ride (aptly named total_amount in the datasets) below $0. This was done to avoid rides that were either unrealistic or some sort of error. As far as I am aware, there isn't a way to have a negative cost ride but there are some negative costs that are well into the hundreds or thousands of dollars. Of course, this could be an error on my part and I would be more than glad to fix it if pointed out as such. I would've liked to do some more filtering and "cleaning" the data, but this is my first time doing any sort of data analysis and I hope to learn from this experience.

# Data generation

As mentioned in the credits section, the datasets use the public taxi rides data provided by NYC. After numerous attempts to get these large datasets for analysis, I settled on simply having queries on the datasets using the Socrata API mentioned as an option on the datasets. Doing this every time the website is loaded or specific information is requested would be rather costly computationally (these are datasets with 100M+ rows) and simply unnecessary. My main goal was using pickup and dropoff locations for my visualization, so I was able to compute all the necessary information for each specific zone, which are then requested using GET requests. In order to avoid computing this data every time, I computed it once using the "data.py" script and saved the outputs into csv files that are turned in Pandas Dataframes as needed by the GET requests. Therefore, "data.py" is not actually called anywhere in the web app, but is run on its own to generated the needed csv files.

# Credit 

Massive credit to NYC for the numerous public data sets available for various aspects of life in NYC. These can be found here: https://data.cityofnewyork.us/. Moreover, credit to NYC's Taxi & Limousine Commission (TLC) for collecting and publishing these large datasets of ride data.
<br>
Credit to the following font named "Taxi Driver Font" for the font used in this web app: https://www.dafont.com/taxidriver.font. I liked how it looked and felt that it fit the theme of the site (and it had the perfect name for it!).
