#Importing of all the necessary libraries for the project
import kivy
import pymongo
import os
import sys
from difflib import SequenceMatcher
from kivy.core.audio import SoundLoader
from kivy.clock import Clock
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.gridlayout import GridLayout
from kivy.graphics import Rectangle, Color
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.label import Label
from kivy.uix.checkbox import CheckBox
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.progressbar import ProgressBar
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.uix.floatlayout import FloatLayout
from data_base_testing import adding
from bson.objectid import ObjectId
from kivy.event import EventDispatcher
import math
Window.size = (720*0.65, 1280*0.65) #Setting the window size in terms of pixels
import random
kivy.require('1.11.1') #Project will not run for any version of the kivy library before 1.11.1
Window.clearcolor = 'FFD5A6' #Background
bg_music = SoundLoader.load('Computer_Science_Internal_Assessment/2 Min Jazz Timer.mp3') #Background Music
if bg_music: #Constantly play the background music
    bg_music.play()

#Initialization of a variety of global variables used in different classes and functions later
global score
global passcode 
global once 
global answer_field
global button_sound
button_sound = SoundLoader.load('Computer_Science_Internal_Assessment/bwuaaap.wav') #Button Sound
once = 1
passcode = "passcode" #Teacher Password
score = 0
looper = True
global quiz_kind #mc, fr, cw, ow, rw, grammar, vocabulary, syntax, #random #<-- names for different quiz types
quiz_kind = ""
global task_list
global actual_tasks
#variables for database and editing
global current_drill
global current_drill_id
global myupdate
global full_task_list
myupdate = False
global tags
tags = []
global mytype
mytype = ""
global questiondb
questiondb = ""
global optiondb
optiondb = 1
global all_optionsdb
all_optionsdb = []
global correctdb
correctdb = []
global exp_db
exp_db = ""
#

class Home(GridLayout): #Home Screen
    def login(self): #Login Button Function for Moving to Teacher Login Screen
        global button_sound
        button_sound.play()
        latinapp.screen_manager.current = "TeacherLogin" #Change the screen to the teacher login
    def begin(self, kind): #Button to begin any exercise
        global quiz_kind
        quiz_kind = kind
        Exercice.build 
        latinapp.screen_manager.current = "Exercice" #Change the screen to the Exercise screen
        global button_sound
        button_sound.play()

class Results(GridLayout):
    def home(self): #Home Button Function for Moving to Home Screen
        global button_sound
        button_sound.play()
        latinapp.screen_manager.current = "Home" #Change the screen to the Home screen
    def change_stats(self): #Function to take the Original Widgets and adjust them according to the user's score
        global score
        self.clear_widgets() #Clears all the preset widgets
        self.rows = 4 #Build the propper structure to add the new widgets with the updated statistics
        self.padding = (10,10)
        self.spacing = (10,10)
        
        text_score_label = Label(
            text="",
            font_size=40,
            color='5D3B23'
        )
        if score >= 90: #Different Text depending on the performance
            text_score_label.text =  "Excellent"
            sound = SoundLoader.load('Computer_Science_Internal_Assessment/c.wav')
            sound.play()
        elif score >= 75 and score <90:
            text_score_label.text =  "Good Job"
        elif score >= 30 and score <75:
            text_score_label.text =  "Ok Performance"
        else:
            text_score_label.text =  "You can do better"
        #Adding all necessary widgets to build the screen's UI
        #Adding Label to display percentage score
        num_score_label = Label(
            color='5D3B23',
            text= str(score)+"%",
            font_size=80,
        )
        #Adding progress bar to display percentage as a loading widget
        progress_bar = ProgressBar(
            # color= 'B27B3E' ,
            # back_color= 'B27B3E' ,
            max=100,
            value= score
        )
        #Adding button to return to home
        home = Button(
            text="Home",
            font_size=40,
            border=(2, 2, 2, 2),
            background_color='B27B3E',
            background_normal='',
        )
        #Adding all the afformentioned widgets
        self.add_widget(text_score_label)
        self.add_widget(num_score_label)
        self.add_widget(progress_bar)
        self.add_widget(home)
        home.on_press = self.home
        
class TeacherDashboard(GridLayout): #Teacher_Dashboard_Screen
    def add(self): #for_button_to_take_to_add_page
        global button_sound
        button_sound.play()
        latinapp.screen_manager.current = "AddDrill"
    def drills(self): #for_button_to_take_to_drill_list_page
        global button_sound
        button_sound.play()
        latinapp.screen_manager.current = "DrillList"
    def home(self): #Home Button Function for Moving to Home Screen #for_button_to_take_to_home_page
        global button_sound
        button_sound.play()
        latinapp.screen_manager.current = "Home"

class DrillList(GridLayout): #Screen for the Drill List where the teacher can enter an exercice and change it
    def build(self, instance):
        global button_sound
        button_sound.play() #play sound
        self.ids.carousel.clear_widgets() #clear all widgets inside the "carousel" component
        myclient = pymongo.MongoClient("mongodb://localhost:27017/") #connect to database
        mydb = myclient["IA"]
        mycol = mydb["Exercices"]
        mylist = list(mycol.find())
        for i in mylist: #build all exercices in the database
            self.ids.carousel.add_widget(Button(text = i["question_text"]+"\n"+str(i["_id"]), 
                                                font_size = 20, background_color = 'B27B3E',
                                                  background_normal='', on_press = self.update))
    def home(self): #Home Button Function for Moving to Home Screen
        global button_sound
        button_sound.play()
        latinapp.screen_manager.current = "Home"
    def add(self): #Function for add button to move to AddDrill Screen
        global button_sound
        button_sound.play()
        latinapp.screen_manager.current = "AddDrill"
    def update(self, instance): #Function for when an exercice is clicked to move to Modify it
        global button_sound
        button_sound.play()
        global current_drill_id #Get the id of the currently selected exercise
        current_drill_id = instance.text[instance.text.find('\n')+1:]  #find where the id number of the currently selected drill in a button widget and store it
        global myupdate
        myupdate = True 
        latinapp.screen_manager.current = "ModifyDrill"
        ModifyDrill.update(ModifyDrill()) #Call for the update to happen in the ModifyDrill class

class ModifyDrill(GridLayout): #Screen for Modifying a Drill
    global myupdate
    def update(self):
        global current_drill_id
        global current_drill
        global myupdate
        global tags
        if myupdate: #If there has been an update
            myclient = pymongo.MongoClient("mongodb://localhost:27017/")
            mydb = myclient["IA"]
            mycol = mydb["Exercices"]
            current_drill = [i for i in mycol.find({"_id": ObjectId(current_drill_id)})] #get the object with the current drill id
    def delete_from_db(self): #delete currently selected exercice from db
        global current_drill
        mycol.delete_one(current_drill[0]) #delete the exercice from the collection in the database
    def add_to_db(self): #add the new exercice to db
        global tags
        global mytype
        global questiondb
        global optiondb
        global all_optionsdb
        global correctdb
        global exp_db
        global button_sound
        button_sound.play()
        myclient = pymongo.MongoClient("mongodb://localhost:27017/")
        mydb = myclient["IA"]
        mycol = mydb["Exercices"]
        #
        questiondb = self.ids.question_text.text
        exp_db = self.ids.explanation_text.text
        optiondb = self.ids.option_slider.value
        #Get all necessary information that the user inputs for the exercise through the widgets
        adding(mytype,tags,questiondb, optiondb, all_optionsdb, correctdb, exp_db) #adds the current exercise in the database through the imported function of the data_base_testing.py file
        global current_drill
        mycol.delete_one(current_drill[0]) #delete the previous exercise with the same id (thus creating the illusion of updating it)
    def addremove_tag(self, value, active): #Function to handle adding and removing exercice tags
        global button_sound
        button_sound.play()
        global tags
        if active: #If a tag value is clicked by the viewer
            tags.append(value) #add is as a tag
        else: #If unclicked
            tags.remove(value) #remove it from the tags
    def delete_from_alloptions(self): #Function for deleting exercice options
        global button_sound
        button_sound.play()
        global all_optionsdb
        if all_optionsdb: #if there is a value to be deleted
            all_optionsdb.pop() #delete it
        self.ids.all_options.text = str(all_optionsdb) #update text to display all options
        pass
    def add_to_alloptions(self): #Function for adding exercice options
        global button_sound
        button_sound.play()
        global all_optionsdb
        all_optionsdb.append(self.ids.one_option.text) #add the value from the widget to all options
        self.ids.all_options.text = str(all_optionsdb)
    def delete_from_allanswers(self): #Function for deleting correct answers
        global button_sound
        button_sound.play()
        global correctdb
        if correctdb: #if there is a value to be deleted
            correctdb.pop()#delete it
        self.ids.all_answers.text = str(correctdb) #update text to display all correct answers
        pass
    def add_to_allanswers(self): #Function for adding correct answers
        global button_sound
        button_sound.play()
        global correctdb
        correctdb.append(self.ids.one_answer.text) #add the value from the widget to all correct answers
        self.ids.all_answers.text = str(correctdb)
    def home(self): #Home Button Function for Moving to Home Screen
        global button_sound
        button_sound.play()
        latinapp.screen_manager.current = "Home"
    def change_type(self, value): #Function for handling changing the exercice type
        global button_sound
        button_sound.play()
        global mytype
        mytype = value
        mytype = str(mytype)
        if mytype == "true_false" or mytype == "free": #If true or false or free response question
            self.ids.option_slider.value = 1 #Remove the options slider
            self.ids.option_slider.disabled = True #Disable the slider since it is useless
        else:
            self.ids.option_slider.disabled = False #Enable the slider for input of number of options
    def slider(self,value): #Function for handling amount of available options
        global optiondb
        optiondb = value 
        self.ids.options.text = "Options " + str(value) #Change text so that it matches the number of possible options that the user has selected with the slider

class AddDrill(GridLayout): #Adding new drill Screen
    #Functions extremely similarly to the Modify Drill class
    def add_to_db(self): #add the new exercice to db
        global button_sound
        button_sound.play()#Play button popping sound through kivy
        #Retrieve all necessary exercice values from widgets or globals
        global tags
        global mytype
        global questiondb
        global optiondb
        global all_optionsdb
        global correctdb
        global exp_db
        questiondb = self.ids.question_text.text
        exp_db = self.ids.explanation_text.text
        optiondb = self.ids.option_slider.value
        adding(mytype,tags,questiondb, optiondb, all_optionsdb, correctdb, exp_db) 
        #Use imported script to insert new entry into the database
    def addremove_tag(self, value, active):#Function to handle adding and removing exercice tags
        global button_sound
        button_sound.play()
        global tags
        if active:
            tags.append(value)
        else:
            tags.remove(value)
    def delete_from_alloptions(self):#Function for deleting exercice options
        global button_sound
        button_sound.play()
        global all_optionsdb
        if all_optionsdb:
            all_optionsdb.pop()
        self.ids.all_options.text = str(all_optionsdb)
        pass
    def add_to_alloptions(self): #Function for adding exercice options
        global button_sound
        button_sound.play()
        global all_optionsdb
        all_optionsdb.append(self.ids.one_option.text)
        self.ids.all_options.text = str(all_optionsdb)
    def delete_from_allanswers(self): #Function for deleting correct answers
        global button_sound
        button_sound.play()
        global correctdb
        if correctdb:
            correctdb.pop()
        self.ids.all_answers.text = str(correctdb)
        pass
    def add_to_allanswers(self): #Function for adding correct answers
        global button_sound
        button_sound.play()
        global correctdb
        correctdb.append(self.ids.one_answer.text)
        self.ids.all_answers.text = str(correctdb)
    def home(self): #Home Button Function for Moving to Home Screen
        global button_sound
        button_sound.play()
        latinapp.screen_manager.current = "Home"
    def change_type(self, value): #Function for handling changing the exercice type
        global button_sound
        button_sound.play()
        global mytype
        mytype = value
        mytype = str(mytype)
        if mytype == "true_false" or mytype == "free": #If true or false or free response question
            self.ids.option_slider.value = 1 #Remove the options slider
            self.ids.option_slider.disabled = True
        else:
            self.ids.option_slider.disabled = False
    def slider(self,value): #Function for handling amount of available options
        global optiondb
        optiondb = value
        self.ids.options.text = "Options " + str(value)

class TeacherLogin(GridLayout): # Screen for Teacher Login area
    def home(self): #Home Button Function for Moving to Home Screen
        global button_sound
        button_sound.play()
        latinapp.screen_manager.current = "Home"
    def dashboard(self): #Function to move to Teacher Dashboard screen and handle wrong passwords
        global button_sound
        button_sound.play()
        global passcode
        if self.ids.input.text == passcode: #If the correct password is inputted
            latinapp.screen_manager.current = "TeacherDashboard" #Move to the respective screen
        else:
            self.ids.credential.text = "Sorry, wrong credential" #Display wrong credential

class Exercice(GridLayout):
    global quiz_kind
    exp_text = ""
    #connection to database
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["IA"]
    global mycol
    mycol = mydb["Exercices"]
    global task_amount
    global full_task_list
    global task_list
    global actual_tasks
    task_list = []
    def get_random_tag_document(self,collection):
        global full_task_list
        global random_index
        global quiz_kind
        random_index = random.randint(0, len(full_task_list)-1) #get a random index
        random_document = full_task_list.pop(random_index) #remove it from the list and store it
        return random_document
        #Provide a randomized document from the database only containing entries of certain exercice type
    def get_random_type_document(self,collection): 
        global full_task_list
        global random_index
        global quiz_kind
        random_index = random.randint(0, len(full_task_list)-1) # Generate a random index within the range of document count
        random_document = full_task_list.pop(random_index) #Remove selected index from list so no duplicates
        return random_document #Return the selected document picked at random
    def get_random_document(self,collection): #Provide a randomized document from the full task list
        global full_task_list
        global random_index
        random_index = random.randint(0, len(full_task_list)-1)  # Generate a random index within the range of document count
        random_document = full_task_list.pop(random_index)
        return random_document #Return the selected document picked at random
    global current_object
    global current_index
    current_index = 0
    global right_answers
    right_answers = 0
    def build(self): #Building exercices
        global button_sound
        button_sound.play()
        global mycol
        global task_amount
        global current_object
        global exp_text
        global Explanation
        global current_answer
        global Options
        global Next
        global Submit
        global current_index
        global right_answers
        global myclient
        global mydb
        global mycol
        global current_object
        global current_answer
        global task_amount
        global full_task_list
        global task_list
        global actual_tasks
        global once
        exp_text = ""
        myclient = pymongo.MongoClient("mongodb://localhost:27017/")
        mydb = myclient["IA"]
        mycol = mydb["Exercices"]
        full_task_list = list(mycol.find()) #put all collection into list
        task_amount = len(full_task_list)
        if once == 1:
            if task_amount < 10:
                if quiz_kind == "random": # If random quiz
                    for i in range(1,len(full_task_list)+1): # Add as many exercices in task list as there are total tasks in the database
                        task_list.append(self.get_random_document(mycol))
                        actual_tasks = len(task_list)
                #For a multiple choice quiz
                if quiz_kind == "multiple_choice" or quiz_kind == "true_false" or quiz_kind == "free" or quiz_kind == "connecting" or quiz_kind == "ordering":
                    #Switch the full database entries list to one only containing the exercices tagged multiple_choice
                    full_task_list = list(mycol.find({"exercice_type":quiz_kind})) #put all entries of certain quiz kind into list
                    #Add as many exercices in task list as there are total tasks in the database
                    for i in range(1,len(full_task_list)+1): 
                        task_list.append(self.get_random_type_document(mycol))
                        actual_tasks = len(task_list)
                if quiz_kind == "grammar" or quiz_kind == "syntax" or quiz_kind == "vocabulary": #If quiz is of certain content
                    full_task_list = list(mycol.find({"exercice_tags":quiz_kind})) #search for all exercises correctly tagged
                    for i in range(1,len(full_task_list)+1): #and get the correct amount of random documents from it
                        task_list.append(self.get_random_type_document(mycol))
                        actual_tasks = len(task_list)
            else:
                if quiz_kind == "random": # Logic for random quiz
                    for i in range(1,11): #Add random documents disregarding their exercise type
                        task_list.append(self.get_random_document(mycol))
                        actual_tasks = 10
                if quiz_kind == "multiple_choice" or quiz_kind == "true_false" or quiz_kind == "free" or quiz_kind == "connecting" or quiz_kind == "ordering": # Logic for quiz types
                    full_task_list = list(mycol.find({"exercice_type":quiz_kind}))
                    for i in range(1,len(full_task_list)+1): #Add the correct amount of random documents of the respective quiz kind
                        task_list.append(self.get_random_type_document(mycol))
                        actual_tasks = len(task_list)
                if quiz_kind == "grammar" or quiz_kind == "syntax" or quiz_kind == "vocabulary":# Logic for quiz tags
                    full_task_list = list(mycol.find({"exercice_tags":quiz_kind}))
                    for i in range(1,len(full_task_list)+1): #Add the correct amount of random documents based on quiz content
                        task_list.append(self.get_random_type_document(mycol))
                        actual_tasks = len(task_list)
            once = 0
            current_index = 0
            right_answers = 0
            current_object = task_list[current_index]
            #Variables to handle logic
        current_answer = "" #Set current answer to nothing
        self.clear_widgets() #Clear widgets to build the quizes in an empty screen

        #Multiple Choice
        if current_object["exercice_type"] == "multiple_choice":  
            #if the exercice type that is currently selected is multiple choice
            self.add_widget(Label(text = current_object["question_text"], color = '5D3B23', font_size = 20)) 
            #add a label with the exercice's question text
            Options = GridLayout(rows = current_object["options"], cols = 1, spacing=(10,10),padding=(10,10)) 
            #set a grid of rows equal to the available options
            self.add_widget(Options) #add it
            for i in current_object["all_options"]:  
                #add button on grid for each of the available multiple choice options
                Options.add_widget(ToggleButton(group="v", state = "normal", text = str(i), background_color='B27B3E',
                                                background_normal ='', on_press = self.get_answer, font_size = 20))
            Explanation = Label(text = "", color = '5D3B23', font_size = 20)
            exp_text = current_object["explanation"] #get the current exercice's explanation text
            self.add_widget(Explanation) #add widget
            Buttons = GridLayout(cols = 2, spacing=(10,10),padding=(10,10)) #Set grid for buttons 
            self.add_widget(Buttons) #Add grid
            #Set Submit and Next Buttons
            Submit = Button(text="Submit",font_size = 20, border= (2,2,2,2), halign="center",
                             background_color='B27B3E', background_normal ='', on_press = self.reveal_answer, disabled = True)
            Next = Button(text="Next",font_size = 20, border= (2,2,2,2), halign="center",
                           background_color='B27B3E', background_normal ='', disabled = True, on_press = self.next_task)
            Buttons.add_widget(Submit) #Add Submit and Next Buttons on the grid
            Buttons.add_widget(Next)
            if current_answer != "": #Control when the user can click the Next and Submit buttons
                Next.disabled = False
                Submit.disabled = False    
        
        #True_False
        elif current_object["exercice_type"] == "true_false":
            #Add the nexessary widgets including Labels, Buttons and the button to toggle through true and false
            self.add_widget(Label(text = current_object["question_text"], color = '5D3B23', font_size = 20))
            Options = GridLayout(rows = current_object["options"], cols = 1, spacing=(10,10),padding=(10,10))
            self.add_widget(Options)
            Options.add_widget(ToggleButton(group="v", state = "normal", text = "False", background_color='B27B3E',background_normal ='', on_press = self.get_answer, font_size = 20))
            Explanation = Label(text = "", color = '5D3B23', font_size = 20)
            exp_text = current_object["explanation"]
            self.add_widget(Explanation)
            Buttons = GridLayout(cols = 2, spacing=(10,10),padding=(10,10))
            self.add_widget(Buttons)
            Submit = Button(text="Submit",font_size = 20, border= (2,2,2,2), halign="center", background_color='B27B3E', background_normal ='', on_press = self.reveal_answer, disabled = False)
            Next = Button(text="Next",font_size = 20, border= (2,2,2,2), halign="center", background_color='B27B3E', background_normal ='', disabled = True, on_press = self.next_task)
            Buttons.add_widget(Submit)
            Buttons.add_widget(Next)
            if current_answer != "": #if the student has inputted an answers
                Next.disabled = False #allow them to submit it
                Submit.disabled = False
        
        #Free Response & Ordering Words & Connecting Words
        #if the current quiz that the user selected is of any of the types below
        elif current_object["exercice_type"] == "free" or current_object["exercice_type"] == "connecting" or current_object["exercice_type"] == "ordering":
            global answer_field
            #Add all necessary widgets to interact with free response including labels for the question and a text box for input from user
            self.add_widget(Label(text = current_object["question_text"], color = '5D3B23', font_size = 20))
            Options = GridLayout(rows = current_object["options"], cols = 1, spacing=(10,10),padding=(10,10))
            self.add_widget(Options)
            answer_field = TextInput(text = "", hint_text = "Place response here...", hint_text_color = 'FFFFFF', multiline = False, font_size = 20,
                                      color = 'FFFFFF', foreground_color = 'FFFFFF', background_color = 'B27B3E')
            answer_field.bind(on_text_validate=self.get_answer)
            Options.add_widget(answer_field)
            Explanation = Label(text = "", color = '5D3B23', font_size = 20)
            exp_text = current_object["explanation"]
            self.add_widget(Explanation)
            Buttons = GridLayout(cols = 2, spacing=(10,10),padding=(10,10))
            self.add_widget(Buttons)
            Submit = Button(text="Submit",font_size = 20, border= (2,2,2,2), halign="center", background_color='B27B3E', background_normal ='', on_press = self.reveal_answer, disabled = False)
            #Upon pressing the Submit Button call the reveal answer function
            Next = Button(text="Next",font_size = 20, border= (2,2,2,2), halign="center", background_color='B27B3E', background_normal ='', disabled = True, on_press = self.next_task)
            #Upon pressing the Next Button call the next task function
            Buttons.add_widget(Submit)
            Buttons.add_widget(Next)
            #If there is an answer enable the Next and Submit buttons
            if current_answer != "":
                Next.disabled = False
                Submit.disabled = False
    
    def similarity(self,first,second): #Check the similarity ratio between two strings (used in free response)
        return SequenceMatcher(None, first, second).ratio() #Check similarity between first (user's response) and second (correct response)
    
    def reveal_answer(self, instance): #Function for revealing answer after question has been submitted and determining whether user was correct
        #Get all necessary global variables
        global button_sound
        button_sound.play() #Play button sound 
        global Explanation
        global answer_field
        global exp_text
        global current_object
        global current_answer
        global Options
        global Submit
        global Next
        global right_answers
        if current_object["exercice_type"] == "connecting" or current_object["exercice_type"] == "ordering": # if the quiz is of these types
            current_answer = answer_field.text #get the inputted answer by the user and store it
        elif current_object["exercice_type"] == "free": #for free response quizzes
            current_answer = answer_field.text
            #store the xurrently inputted answer
            #make the slightly wrong current answer equal to the propper answer  
            for i in current_object["correct_answer"]: #Loop for every element in the correct answers
                if self.similarity(current_answer,i) > 0.75: #If the user's answer has a similarity index of above 0.75 with any
                    current_answer = current_object["correct_answer"][0] #Set the user's answer equal to an answer guaranteed to be correct
        Next.disabled = False
        for child in Options.children: #Disable all options since the user has already answered
            child.disabled = True
        Submit.disabled = True #disallow the user from submitting
        if current_answer in current_object["correct_answer"]: #if correct answer after submit
            Explanation.text = "Good Job. "+"\n"+exp_text #show explanation
            right_answers += 1 #incriment right response
        else: #else
            Explanation.text = "Not Quite. "+"\n"+exp_text #show explanation without incrimenting
    def get_answer(self, instance): #Function to handle setxting the current_answer variable by getting data from different UI
        global button_sound
        button_sound.play()
        global current_object
        global Next
        global Submit
        global Explanation
        global current_answer
        if current_object["exercice_type"] == "multiple_choice": #For multiple choise exercises
            if instance.state == "down": #Set the current answer to the text of the option the user has chosen through the toggleable widget
                current_answer = instance.text
            else:
                current_answer = "" #Set answer to nothing
            if current_answer != "":
                Submit.disabled = False #Enable the submit button
            else:
                Next.disabled = True
                Submit.disabled = True #Disable buttons for submission
        elif current_object["exercice_type"] == "true_false": #for true or false questions
            if instance.state == "normal":
                current_answer = "False" #Set the answer as false
                instance.text = "False"
            else:
                current_answer = "True"
                instance.text = "True" #Set the answer as true
            if current_answer != "": #if no answer
                Submit.disabled = False #Enable submition
            else:
                Next.disabled = True #else disable it
        elif current_object["exercice_type"] == "free": #for free response questions
            Submit.disabled = False
            current_answer = instance.text #grab the user unputted text and store it
    def next_task(self, instance): #Function for iterating through the list and moving to the next exercice
        global button_sound
        button_sound.play()
        global mycol
        global task_amount
        global current_object
        global task_list
        global current_index
        global right_answers
        global actual_tasks
        global score
        current_index += 1 #Iterate to the next question
        if current_index == actual_tasks: #If there are no more questions
            score = math.ceil((right_answers/actual_tasks)*100) #Calculate Percentage of right answers and round to nearest whole number
            latinapp.screen_manager.current = "Results" #Move user to results screen
        else: #if there are more questions
            current_object = task_list[current_index] #iterate to the next one
            self.build() #and build it

class MainApp(App): #Class for the Main Application, used for connecting all the pages together and handling restarts
    def build(self):
        self.title = "Astaxulator"
        self.screen_manager = ScreenManager()

        #Initialization of all the pages necessary for movement between different screens to work properly

        self.connect_page = Home()
        screen = Screen(name="Home")
        screen.add_widget(self.connect_page)
        self.screen_manager.add_widget(screen)

        self.connect_page = Results()
        screen = Screen(name="Results")
        screen.add_widget(self.connect_page)
        self.screen_manager.add_widget(screen)

        self.connect_page = TeacherLogin()
        screen = Screen(name="TeacherLogin")
        screen.add_widget(self.connect_page)
        self.screen_manager.add_widget(screen)

        self.connect_page = Exercice()
        screen = Screen(name="Exercice")
        screen.add_widget(self.connect_page)
        self.screen_manager.add_widget(screen)

        self.connect_page = TeacherDashboard()
        screen = Screen(name="TeacherDashboard")
        screen.add_widget(self.connect_page)
        self.screen_manager.add_widget(screen)

        self.connect_page = AddDrill()
        screen = Screen(name="AddDrill")
        screen.add_widget(self.connect_page)
        self.screen_manager.add_widget(screen)

        self.connect_page = DrillList()
        screen = Screen(name="DrillList")
        screen.add_widget(self.connect_page)
        self.screen_manager.add_widget(screen)

        self.connect_page = ModifyDrill()
        screen = Screen(name="ModifyDrill")
        screen.add_widget(self.connect_page)
        self.screen_manager.add_widget(screen)
        return (self.screen_manager)
        

if __name__ == "__main__": #Run the application
    latinapp = MainApp() 
    latinapp.run() #run

