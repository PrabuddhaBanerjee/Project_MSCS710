# AIRservices

## Overview
AIRService is a program designed to predict flight delays/cacellations and allow users to create an account with our service to find the best airports to fly out of, given a certain date. The user can also view graphs about cancellations and type of weather cancellations.

## Tools used
The UI was built with HTML/CSS and Javascript. The API was built using a Swagger server stub and the model predictions were built using Python and Jupyter notebook. The database integrated with this program is Mongodb. 

## Folder Breakdown
air_env - Was used to for intial testing of data <br>
aieline_data - All airline data stored in csv files <br>
database - Transfering airline and weather data to Mongodb <br>
IATA_codes_data - Airline airport codes for reference <br>
Login_v1 - The UI for the program <br>
modeling - The modeling for the airline predictions <br>
notebooks - Jupyter notebooks for modeling <br>
swagger_server - The REST API <br>
utilites - Utilites for modeling <br>
weather_data - Weather data used to compare weather to flight cancellation <br>

## Requirements
Python 3.5.2+ <br>
Docker


## Running with Docker

To run the server on a Docker container, please execute the following from the root directory:

```bash
# building the image
docker build -t swagger_server .

# starting up a container
docker run -p 8080:8080 swagger_server
```
To run the ui on a Docker container, please execute the following from the Login_v1 directory:

```bash
# building the image
docker build -t app .

# starting up a container
docker run -it --rm -p 8081:80 --name web app
```
## Contributors 
Johnathon Hoste <br>
Prabudhha Banerjee <br>
Dayna Eidle <br>
Christian Sumano <br>
Prof. Michael Gildein <br>
