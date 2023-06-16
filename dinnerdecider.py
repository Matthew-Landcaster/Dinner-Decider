
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import getpass
import pygame
import random
from re import S
from urllib import request
from xml.etree.ElementInclude import include
from bs4 import BeautifulSoup
from random import randrange
import requests

class DinnerDecider(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        # Variables storing info from the different windows to be used in the results window
        self.addr = None
        self.recv = None
        self.food = None
        #self.dist = None

        windWidth = 800 # Desired width of the program window
        windHeight = 600 # Desired height of the program window

        screenWidth = self.winfo_screenwidth() # Width of the user's screen
        screenHeight = self.winfo_screenheight() # Height of the user's screen

        # Determines the center point of the screen in regards to the user's screen
        xCenter = int((screenWidth/2)-(windWidth/2))
        yCenter = int((screenHeight/2)-(windHeight/2))

        self.geometry(f"{windWidth}x{windHeight}+{xCenter}+{yCenter}") # Centers the program window

        # Configures a frame for all the windows so they appear uniform when stacked
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        

        self.frames = {} # Dictionary to hold the frames

        # Iterates through all the pages of the app, creates each frame/window, 
        # and stores them in the dictionary for easier access
        for wind in (StartPage,InfoPage, FoodOptionsPage, ResultPage):
            page_name = wind.__name__
            frame = wind(container, self)
            self.frames[page_name] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.showFrame("StartPage") # Starts the program on the start page

    # Parameters: The class object itself, the name of the page we want to see
    # Raises the desired page to the top of the frame stack using tkraise
    def showFrame(self, pageName):
        frame = self.frames[pageName]
        frame.tkraise()

class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.config(background="pink")
        self.controller = controller
        header = tk.Label(self, text="Hello " + getpass.getuser().title(), font=("Cooper Black",30), background="pink") # User greeting
        subheader = tk.Label(self, text="Welcome to Dinner Decider!", font=("Cooper Black",25), background="pink") # Welcome statement
        startButton = tk.Button(self, text="Start", command=lambda: controller.showFrame("InfoPage"), height=2, width=50, font=("Cooper Black", 12)) # Jump to next window

        # Window formatting
        header.place(relx=0.5, rely=0.4, anchor="center")
        subheader.place(relx=0.5, rely=0.5, anchor="center")
        startButton.place(relx=0.5, rely=0.6, anchor="center")

class InfoPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.config(bg="pink")
        # Variables that will be collected from widgets and set in the parent class
        recvVar = tk.StringVar()
        addrVar = tk.StringVar()
        #distVar = tk.StringVar()

        # Lists to be read by combobox widgets
        #distanceList = ["Bird's-eye View", "Driving (5 mi.)", "Biking (2 mi.)", "Walking (1 mi.)", "Within 4 Blocks"]
        receiveList = ["Pickup", "Delivery"]

        # Widgets that collect user's preferred method of receiving, address, and distance(info not used) willing to travel
        recvLabel = tk.Label(self, text="Pickup/Delivery: ", pady=0, font=("Cooper Black", 15), background="pink")
        recvDrop = ttk.Combobox(self, values=receiveList, textvariable=recvVar, state='readonly',width=26, height=3, font=("Cooper Black", 15))
        addrLabel = tk.Label(self, text="Address: ", pady=0, font=("Cooper Black", 15), background="pink")
        addrEntry = tk.Entry(self, textvariable=addrVar, width=28, font=("Cooper Black", 15))
        #distLabel = tk.Label(self, text="Distance: ", pady=0, font=("Cooper Black", 15))
        #distDrop = ttk.Combobox(self, values=distanceList, textvariable=distVar, state='readonly', width=26, height=3, font=("Cooper Black", 15))
        submitButton = tk.Button(self, text="Submit", command=lambda: self.onSubmit(recvVar.get(), addrVar.get(), controller), width=15, height=2, font=("Cooper Black", 10))
        backButton = tk.Button(self, text="Back", command=lambda: controller.showFrame("StartPage"), width=15, height=2, font=("Cooper Black", 10))

        # Formatting
        recvLabel.place(relx=0.5, rely=0.3, anchor="center")
        recvDrop.place(relx=0.5, rely=0.35, anchor="center")
        addrLabel.place(relx=0.5, rely=0.4, anchor="center")
        addrEntry.place(relx=0.5, rely=0.45, anchor="center")
        #distLabel.place(relx=0.5, rely=0.5, anchor="center")
        #distDrop.place(relx=0.5, rely=0.55, anchor="center")
        submitButton.place(relx=0.41, rely=0.63, anchor="center")
        backButton.place(relx=0.59, rely=0.63, anchor="center")

    def onSubmit(self, recv, addr, controller):
        # If user does not provide input do not let them move on
        if recv == '' or addr == '':
            messagebox.showerror("Error", "Please Fill Out All Fields")

        else:
        # Set variables in parent class to be used in yelp request link
            controller.addr = addr
            controller.recv = recv
            #controller.dist = dist

            controller.showFrame("FoodOptionsPage") # Go to next page

        

        

class FoodOptionsPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.config(bg="pink")
        # Variable to be collected from radio button widgets or random button and stored in parent
        foodVar = tk.StringVar()

        # Food options
        # Tristatevalue changed to be different from default value of foodVar so no radio button is selected on startup
        burgerButton = tk.Radiobutton(self, text="Burger", variable=foodVar, value="Burger", tristatevalue="x", font=("Cooper Black", 15), background="pink")
        pizzaButton = tk.Radiobutton(self, text="Pizza", variable=foodVar, value="Pizza", tristatevalue="x", font=("Cooper Black", 15), pady=10, background="pink")
        sandwichButton = tk.Radiobutton(self, text="Sandwich", variable=foodVar, value="Sandwich", tristatevalue="x", font=("Cooper Black", 15), background="pink")
        pastaButton = tk.Radiobutton(self, text="Pasta", variable=foodVar, value="Pasta", tristatevalue="x", font=("Cooper Black", 15), background="pink")
        chickenButton = tk.Radiobutton(self, text="Chicken", variable=foodVar, value="Chicken", tristatevalue="x", font=("Cooper Black", 15), background="pink")
        seafoodButton = tk.Radiobutton(self, text="Seafood", variable=foodVar, value="Seafood", tristatevalue="x", font=("Cooper Black", 15), background="pink")
        dessertButton = tk.Radiobutton(self, text="Dessert", variable=foodVar, value="Dessert", tristatevalue="x", font=("Cooper Black", 15), background="pink")
        indianButton = tk.Radiobutton(self, text="Indian", variable=foodVar, value="Indian", tristatevalue="x", font=("Cooper Black", 15), background="pink")
        ethiopianButton = tk.Radiobutton(self, text="Ethiopian", variable=foodVar, value="Ethiopian", tristatevalue="x", font=("Cooper Black", 15), background="pink")
        chineseButton = tk.Radiobutton(self, text="Chinese", variable=foodVar, value="Chinese", tristatevalue="x", font=("Cooper Black", 15), background="pink")
        japaneseButton = tk.Radiobutton(self, text="Japanese", variable=foodVar, value="Japanese", tristatevalue="x", font=("Cooper Black", 15), background="pink")
        bbqButton = tk.Radiobutton(self, text="BBQ", variable=foodVar, value="BBQ", tristatevalue="x", font=("Cooper Black", 15), background="pink")
        mexicanButton = tk.Radiobutton(self, text="Mexican", variable=foodVar, value="Mexican", tristatevalue="x", font=("Cooper Black", 15), background="pink")
        thaiButton = tk.Radiobutton(self, text="Thai", variable=foodVar, value="Thai", tristatevalue="x", font=("Cooper Black", 15), background="pink")
        vegetarianButton = tk.Radiobutton(self, text="Vegetarian", variable=foodVar, value="Vegetarian", tristatevalue="x", font=("Cooper Black", 15), background="pink")
        mediterranianButton = tk.Radiobutton(self, text="Mediterranian", variable=foodVar, value="Mediterranian", tristatevalue="x", font=("Cooper Black", 15), background="pink")
        randomButton = tk.Button(self, text="Random", command=lambda: self.onRandom(controller), width=25, height=3, font=("Cooper Black", 10))
        submitButton = tk.Button(self, text="Submit", command=lambda: self.onSubmit(foodVar.get(), controller), width=25, height=3, font=("Cooper Black", 10))
        backButton = tk.Button(self, text="Back", command=lambda: controller.showFrame("InfoPage"),width=25, height=3, font=("Cooper Black", 10))

        # Formatting
        burgerButton.place(relx=0.05, rely=0.05, anchor="w")
        pizzaButton.place(relx=0.05, rely=0.15, anchor="w")
        sandwichButton.place(relx=0.05, rely=0.25, anchor="w")
        pastaButton.place(relx=0.05, rely=0.35, anchor="w")
        chickenButton.place(relx=0.05, rely=0.45, anchor="w")

        seafoodButton.place(relx=0.4, rely=0.05, anchor="w")
        dessertButton.place(relx=0.4, rely=0.15, anchor="w")
        indianButton.place(relx=0.4, rely=0.25, anchor="w")
        ethiopianButton.place(relx=0.4, rely=0.35, anchor="w")
        chineseButton.place(relx=0.4, rely=0.45, anchor="w")
        japaneseButton.place(relx=0.4, rely=0.55, anchor="w")

        bbqButton.place(relx=0.75, rely=0.05, anchor="w")
        mexicanButton.place(relx=0.75, rely=0.15, anchor="w")
        thaiButton.place(relx=0.75, rely=0.25, anchor="w")
        vegetarianButton.place(relx=0.75, rely=0.35, anchor="w")
        mediterranianButton.place(relx=0.75, rely=0.45, anchor="w")

        randomButton.place(relx=0.2, rely=0.7, anchor="w")
        submitButton.place(relx=0.47, rely=0.8, anchor="center")
        backButton.place(relx=0.75, rely=0.7, anchor="e")

    def onSubmit(self, foodOpt, controller):
        # If user does not select a radio button or random button throw error
        if foodOpt == "":
            messagebox.showerror("Error", "Please Select A Button")

        else:
            # Set variable and move to next page
            controller.food = foodOpt
            controller.showFrame("ResultPage")

    '''
    Input: Parent object

    Output: None

    When user presses the randomo button the spin wheel function is called
    and whatever it lands on is set in the parent and the next page is raised to
    the top of the stack.
    '''
    def onRandom(self, controller):
        foodOpt = self.spinWheel()
        controller.food = foodOpt
        controller.showFrame("ResultPage")

    '''
    Input: An integer that represents an angle on the random wheel

    Output: Food Choosen

    function takes in an integer representing an angle on the wheel of food choices
    and outputs what option that angle corresponds with.

    '''
    def choosen(self, stopPoint):
        if 0 <= stopPoint < 23:
            return "Chinese"

        elif 23 <= stopPoint < 45:
            return "Japanese"

        elif 45 <= stopPoint < 68:
            return "BBQ"

        elif 68 <= stopPoint < 90:
            return "Mexican"

        elif 90 <= stopPoint < 113:
            return "Thai"

        elif 113 <= stopPoint < 135:
            return "Vegetarian"

        elif 135 <= stopPoint < 158:
            return "Mediterranean"

        elif 158 <= stopPoint < 180:
            return "Burger"

        elif 180 <= stopPoint < 203:
            return "Pizza"

        elif 203 <= stopPoint < 225:
            return "Sandwich"

        elif 225 <= stopPoint < 248:
            return "Pasta"

        elif 248 <= stopPoint < 270:
            return "Chicken"

        elif 270 <= stopPoint < 293:
            return "Seafood"

        elif 293 <= stopPoint < 315:
            return "Dessert"

        elif 315 <= stopPoint < 338:
            return "Indian"

        elif 338 <= stopPoint <= 360:
            return "Ethiopian"


    def spinWheel(self):
        '''
        Creates a spinning wheel with random food choices that simulates a random choice.
        A random whole degree is chosen on the wheel before it spins and that is where the
        wheel will eventually stop after about 15 seconds. The wheel will spin for about
        10 seconds and then eventually correct itself by one degree until it reached the 
        previously chosen stop position.
        '''
        self.update_idletasks()
        pygame.init()

        running = True

        screen = pygame.display.set_mode([800,600]) # Oblong screen to keep arrown in frame
        wheel = pygame.image.load("RandomWheel-removebg-preview.png").convert() # Random choice wheel
        arrow = pygame.image.load("revisedarrow.png").convert() # Arrow to help end user determine where wheel stops

        rotAngle = 0 # Keeps track of how far the wheel has rotated in degrees
        stopTime = random.randint(10000, 15000)
        stopPos = random.randint(0, 360) # Position randomly choosen for where the wheel will stop
        choosenFood = self.choosen(stopPos)
        old_center = wheel.get_rect().center
        wheelRect = wheel.get_rect()
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            wheelRot = pygame.transform.rotate(wheel, rotAngle)
            '''
            Whenever image rotates in a loop it gets bigger than the original and the resize causes
            the position of the image to change. The next line resets the image back to the
            same position as the original image.

            Better explanation: https://stackoverflow.com/questions/4183208/how-do-i-rotate-an-image-around-its-center-using-pygame
            '''
            wheelRect = wheelRot.get_rect(center=wheel.get_rect(topleft = (50, 50)).center) 

            # if the program has been running for less than 10 seconds rotate the wheel by one degree
            if pygame.time.get_ticks() <= 10000:
                rotAngle = (rotAngle + 1) % 360

            # if the wheel has been spinning for more than 10 seconds and the position of the wheel is not where it should be adjust it by one degree
            else:
                if rotAngle > stopPos or rotAngle < stopPos:
                    rotAngle = (rotAngle + 1) % 360

            # if the program has been running for more than 15 seconds shut the program down
                elif pygame.time.get_ticks() >= 15000:
                    running = False


            screen.blits([(wheelRot, wheelRect),(arrow,(548,175))])
            pygame.display.flip()
        pygame.display.quit()
        pygame.quit()
        return choosenFood

class ResultPage(tk.Frame):
    # NOT SURE HOW TO INCORPERATE DISTANCE INTO QUERY STRING NO EXPLANATION ONLINE
    # NUMBERS ARE INCONSISTENT (KNOW POINT OF ORIGIN TO CALC RADIUS)
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        
        self.config(bg="pink")

        # Webpage header
        header = tk.Label(self, text="Results", font=("Cooper Black", 20), background="pink")
        header.pack()

        # Buttons for showing the results and going back to the beginning of the program
        self.resultsButton = tk.Button(self, text="Show Results", command=lambda: self.getResults(controller), font=("Cooper Black", 10), width=20, height=2)
        returnButton = tk.Button(self, text="Start Over", command=lambda: self.startOver(controller), font=("Cooper Black",10), width=20, height=2)
        self.resultsButton.pack()
        returnButton.pack()

        self.resultsFrame = tk.Frame(self, background="pink")
        self.resultsFrame.pack()



    def startOver(self, controller):
        for widget in self.resultsFrame.winfo_children():
            widget.destroy()

        self.resultsFrame.pack_forget()
        self.resultsButton.config(relief="raised")
        self.resultsButton.config(state="active")
        self.resultsFrame = tk.Frame(self, background="pink")
        self.resultsFrame.pack()
        controller.showFrame("StartPage")

        #controller.showFrame("InfoPage")
    """
    Input: Parent object

    Output None

    Displays the results of the webscrape to the user
    """
    def getResults(self, controller):
        # Disables 'Show Results' button so user cant repeatedly show results
        self.resultsButton.config(relief="sunken")
        self.resultsButton.config(state=tk.DISABLED)

        # Gets variables that were stored in the parent object
        foodOpt = controller.food
        recvOpt = controller.recv
        homeAddr = controller.addr
        
        # Calls webscrape function to get list of resturant options
        optionsList,distanceList = self.yelpScraper(foodOpt, homeAddr, recvOpt)
        
        # Displays options on screen
        for i in range(len(optionsList)):
            result = tk.Label(self.resultsFrame, text= optionsList[i]+" ["+distanceList[i]+"]", font=("Cooper Black", 15), background="pink")
            result.pack()

# If there is an issue with the yelp webscrape the problem is most likely that 
# yelp has changed their divs so the class id for the h3 tag or the a tag will
# most likely have to be updated.
    def yelpScraper(self, food, loc, recv):
        yelpRequestStr = f"https://www.yelp.com/search?find_desc={food}&find_loc={loc}&attrs=Restaurants{recv}"

        yelpResponse = requests.get(yelpRequestStr).text

        # String Format f"https://www.yelp.com/search?find_desc={PARSED FOOD OPTION}&find_loc={Parsed ADDRESS}&attrs=Restaurants{METHOD OF RECIEVING FOOD}"

        # Scrapes Yelp For Restaurants
        resultsList = []
        distanceList = []
        soup = BeautifulSoup(yelpResponse, "lxml")
        divTag = soup.find_all("h3", class_ = "css-1agk4wl")
        pTag = soup.find_all("p", class_="tagText__09f24__ArEfy iaTagText__09f24__Gv1CO css-chan6m")
        for food in divTag:
            aTag = food.find("a", class_ = "css-19v1rkv").text
            resultsList.append(aTag)

        for dist in pTag:
            spanTag = dist.find("span", class_="raw__09f24__T4Ezm").text
            try: # For some reason delivery specs are also kept in this div class
                float(spanTag[0]) # If the first item in the string is a number append it to the list
                distanceList.append(spanTag)
            except ValueError:
                continue
        return resultsList, distanceList

def main():
    program = DinnerDecider()
    program.mainloop()

if __name__ == "__main__":
    main()



