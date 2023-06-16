# Dinner-Decider
A python project I designed to help me pick where to eat when I can't decide for myself. Uses Pygame BeautifulSoup and Tkinter.
The main bulk of the project are the various GUI windows created with Tkinter. The user is greeted and then prompted to enter their address and preference for how they would 
like to receive the food(delivery or pickup). The user is then prompted to either pick a type of food they are interested in or push the random button. Pushing the random
button opens a pygame window which displays a colorful wheel that spins until a random option is chosen. The user is taken to the final screen with two buttons (Show Results,
and Start Over). Show results activates a function that uses BeautifulSoup to scrape Yelp for the top 10 results for the given food and the specified address, that offers the
desired receiving method. Those results are then displayed to the user along with how far, in miles, the resturant is from the user. If the user pushes the start over button
the results of the initial search are wiped and the user is brought back to the page that prompts for the user's address and receival method.
