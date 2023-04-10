# Martianeer
## Overview
Martianeer is the winning [Hack_NCState 2023](https://hackncstate.devpost.com/) project for the [Create the Future track](https://hackncstate.devpost.com/submissions/search?utf8=%E2%9C%93&filter%5Btrack+selection%5D%5B%5D=create+the+future) created by Brian Yngve, Joey Langhorst, and Simon Griggs. It is an idle tycoon game that uses real Mars climate data collected by the Curiosity rover to influence crop yields. Players are tasked with growing enough food to support a colony. We have decided to keep updating it since the conclusion of Hack_NCState. To play/see the version of the game as it was when it was submitted check out the [hack_ncstate2023 branch](https://github.com/sdgriggs/JLSGBY/tree/hack_ncstate2023).
 
## FAQ
### Is the weather data real time?
No, we take [the historical weather data](https://mars.nasa.gov/rss/api/?feed=weather&category=msl&feedtype=json) from NASA's Curiosity rover and aggregate it to get ranges for the different fields. For example, we would take every sol (a Martian day) 1 of every year that Curiosity has been on Mars and find the minimum lowest temperature and the maximum lowest temperature experienced on that sol. Then we pick a random value between those temperatures to be the lowest temperature for sol 1 in the game. Through this process we also get the highest temperature, the pressure, and sunrise and sunset times. Using the minimum and maximum temperatures for the sol, as well as the sunrise and sunset times, we generate variating temperature values for the sol. This process means that your production rates will change throughout the sol and you can experience seasons if you play for long enough!
### How did you make it?
Martianeer is made entirely made in python. For the GUI it uses pygame and the backend uses the requests library to get the most recent weather data from Curiosity (or, if you're offline, it pulls from a downloaded json file from 4/8/2023).

## What's new?
* We filled out our README!

## Upcoming Features
* Optimized rendering to improve performance in the end game
* Potentially other things from [here](https://github.com/sdgriggs/JLSGBY/wiki/New-Feature-and-Optimization-Ideas)
