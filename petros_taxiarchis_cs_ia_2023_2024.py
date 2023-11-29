import kivy
import pymongo
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
Window.size = (720*0.65, 1280*0.65)
import random
kivy.require('1.11.1')
Window.clearcolor = 'FFD5A6' #Background
global score
global passcode 
global once 
global answer_field
global button_sound
button_sound = SoundLoader.load('Computer_Science_Internal_Assessment/bwuaaap.wav') #Button Soun
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
        latinapp.screen_manager.current = "TeacherLogin"
    def begin(self, kind):
        global quiz_kind
        quiz_kind = kind
        latinapp.screen_manager.current = "Exercice"
        global button_sound
        button_sound.play()

class Results(GridLayout):
    def home(self): #Home Button Function for Moving to Home Screen
        global button_sound
        button_sound.play()
        App.get_running_app().restart()
        latinapp.screen_manager.current = "Home"
    def change_stats(self): #Function to take the Original Widgets and adjust them according to the user's score
        global score
        self.clear_widgets()
        self.rows = 4
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
        num_score_label = Label(
            color='5D3B23',
            text= str(score)+"%",
            font_size=80,
        )
        progress_bar = ProgressBar(
            # color= 'B27B3E' ,
            # back_color= 'B27B3E' ,
            max=100,
            value= score
        )
        home = Button(
            text="Home",
            font_size=40,
            border=(2, 2, 2, 2),
            background_color='B27B3E',
            background_normal='',
        )
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
        App.get_running_app().restart()
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
        
        App.get_running_app().restart()
        latinapp.screen_manager.current = "Home"
    def add(self): #Function for add button to move to AddDrill Screen
        global button_sound
        button_sound.play()
        latinapp.screen_manager.current = "AddDrill"
    def update(self, instance): #Function for when an exercice is clicked to move to Modify it
        global button_sound
        button_sound.play()
        global current_drill_id
        current_drill_id = instance.text[instance.text.find('\n')+1:]
        global myupdate
        myupdate = True 
        latinapp.screen_manager.current = "ModifyDrill"
        ModifyDrill.update(ModifyDrill())

class ModifyDrill(GridLayout): #Screen for Modifying a Drill
    global myupdate
    def update(self):
        global current_drill_id
        global current_drill
        global myupdate
        global tags
        if myupdate: #If there has not been an update
            myclient = pymongo.MongoClient("mongodb://localhost:27017/")
            mydb = myclient["IA"]
            mycol = mydb["Exercices"]
            current_drill = [i for i in mycol.find({"_id": ObjectId(current_drill_id)})]
            # if "grammar" in current_drill[0]["exercice_tags"]:
            #     self.ids.grammar.active = True
            #     tags.append("grammar")
            # elif "syntax" in current_drill[0]["exercice_tags"]:
            #     self.ids.syntax.active = True
            #     tags.append("syntax")
            # elif "vocabulary" in current_drill[0]["exercice_tags"]:
            #     self.ids.vocabulary.active = True
            #     tags.append("vocabulary")
            # else: 
            #     pass
            # self.ids.question_text.text = current_drill[0]["question_text"]
    def delete_from_db(self): #delete currently selected exercice from db
        global current_drill
        mycol.delete_one(current_drill[0])
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
        questiondb = self.ids.question_text.text
        exp_db = self.ids.explanation_text.text
        optiondb = self.ids.option_slider.value
        adding(mytype,tags,questiondb, optiondb, all_optionsdb, correctdb, exp_db)
        global current_drill
        mycol.delete_one(current_drill[0])
    def addremove_tag(self, value, active): #Function to handle adding and removing exercice tags
        global button_sound
        button_sound.play()
        global tags
        if active:
            tags.append(value)
        else:
            tags.remove(value)
    def delete_from_alloptions(self): #Function for deleting exercice options
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
        
        App.get_running_app().restart()
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
    # ev = MyEventDispatcher()
    # ev.bind(on_test=update)
    # ev.do_something('pwease')

class AddDrill(GridLayout): #Adding new drill Screen
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
        
        App.get_running_app().restart()
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
        
        App.get_running_app().restart()
        latinapp.screen_manager.current = "Home"
    def dashboard(self): #Function to move to Teacher Dashboard screen and handle wrong passwords
        global button_sound
        button_sound.play()
        global passcode
        if self.ids.input.text == passcode:
            latinapp.screen_manager.current = "TeacherDashboard"
        else:
            self.ids.credential.text = "Sorry, wrong credential"

class Exercice(GridLayout):
    global quiz_kind
    exp_text = ""
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["IA"]
    global mycol
    mycol = mydb["Exercices"]
    global task_amount
    # task_amount = (len(list(mycol.find())))
    global full_task_list
    # full_task_list = list(mycol.find())
    global task_list
    global actual_tasks
    task_list = []
    def get_random_tag_document(self,collection):
        global full_task_list
        global random_index
        global quiz_kind
        random_index = random.randint(0, len(full_task_list)-1)
        random_document = full_task_list.pop(random_index)
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
                    full_task_list = list(mycol.find({"exercice_type":quiz_kind})) 
                    #Add as many exercices in task list as there are total tasks in the database
                    for i in range(1,len(full_task_list)+1): 
                        task_list.append(self.get_random_type_document(mycol))
                        actual_tasks = len(task_list)
                if quiz_kind == "grammar" or quiz_kind == "syntax" or quiz_kind == "vocabulary":
                    full_task_list = list(mycol.find({"exercice_tags":quiz_kind}))
                    for i in range(1,len(full_task_list)+1):
                        task_list.append(self.get_random_type_document(mycol))
                        actual_tasks = len(task_list)
            else:
                if quiz_kind == "random": # Logic for random quiz
                    for i in range(1,11):
                        task_list.append(self.get_random_document(mycol))
                        actual_tasks = 10
                if quiz_kind == "multiple_choice" or quiz_kind == "true_false" or quiz_kind == "free" or quiz_kind == "connecting" or quiz_kind == "ordering": # Logic for quiz types
                    full_task_list = list(mycol.find({"exercice_type":quiz_kind}))
                    for i in range(1,len(full_task_list)+1):
                        task_list.append(self.get_random_type_document(mycol))
                        actual_tasks = len(task_list)
                if quiz_kind == "grammar" or quiz_kind == "syntax" or quiz_kind == "vocabulary":# Logic for quiz tags
                    full_task_list = list(mycol.find({"exercice_tags":quiz_kind}))
                    for i in range(1,len(full_task_list)+1):
                        task_list.append(self.get_random_type_document(mycol))
                        actual_tasks = len(task_list)
            once = 0
            current_index = 0
            right_answers = 0
            current_object = task_list[current_index]
        
        current_answer = ""
        self.clear_widgets()

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
            if current_answer != "":
                Next.disabled = False
                Submit.disabled = False
        
        #Free Response & Ordering Words & Connecting Words
        elif current_object["exercice_type"] == "free" or current_object["exercice_type"] == "connecting" or current_object["exercice_type"] == "ordering":
            global answer_field
            self.add_widget(Label(text = current_object["question_text"], color = '5D3B23', font_size = 20))
            Options = GridLayout(rows = current_object["options"], cols = 1, spacing=(10,10),padding=(10,10))
            self.add_widget(Options)
            answer_field = TextInput(text = "", hint_text = "Place response here...", hint_text_color = 'FFFFFF', multiline = False, font_size = 20, color = 'FFFFFF', foreground_color = 'FFFFFF', background_color = 'B27B3E')
            answer_field.bind(on_text_validate=self.get_answer)
            Options.add_widget(answer_field)
            Explanation = Label(text = "", color = '5D3B23', font_size = 20)
            exp_text = current_object["explanation"]
            self.add_widget(Explanation)
            Buttons = GridLayout(cols = 2, spacing=(10,10),padding=(10,10))
            self.add_widget(Buttons)
            Submit = Button(text="Submit",font_size = 20, border= (2,2,2,2), halign="center", background_color='B27B3E', background_normal ='', on_press = self.reveal_answer, disabled = False)
            Next = Button(text="Next",font_size = 20, border= (2,2,2,2), halign="center", background_color='B27B3E', background_normal ='', disabled = True, on_press = self.next_task)
            Buttons.add_widget(Submit)
            Buttons.add_widget(Next)
            if current_answer != "":
                Next.disabled = False
                Submit.disabled = False
    
    def similarity(self,first,second): #Check the similarity ratio between two strings (used in free response)
        return SequenceMatcher(None, first, second).ratio()
    
    def reveal_answer(self, instance): #Function for revealing answer after question has been submitted and determining whether user was correct
        global button_sound
        button_sound.play() 
        global Explanation
        global answer_field
        global exp_text
        global current_object
        global current_answer
        global Options
        global Submit
        global Next
        global right_answers
        if current_object["exercice_type"] == "connecting" or current_object["exercice_type"] == "ordering":
            current_answer = answer_field.text
        elif current_object["exercice_type"] == "free":
            current_answer = answer_field.text
            #make the slightly wrong current answer equal to the propper answer  
            for i in current_object["correct_answer"]:
                if self.similarity(current_answer,i) > 0.75:
                    current_answer = current_object["correct_answer"][0]
        Next.disabled = False
        for child in Options.children:
            child.disabled = True
        Submit.disabled = True
        if current_answer in current_object["correct_answer"]: #if correct answer after submit
            Explanation.text = "Good Job. "+"\n"+exp_text #show explanation
            right_answers += 1 #incriment right response
        else: #else
            Explanation.text = "Not Quite. "+"\n"+exp_text #show explanation without incrimenting
    def get_answer(self, instance): #Function to handle setting the current_answer variable by getting data from different UI
        global button_sound
        button_sound.play()
        global current_object
        global Next
        global Submit
        global Explanation
        global current_answer
        if current_object["exercice_type"] == "multiple_choice":
            if instance.state == "down":
                current_answer = instance.text
            else:
                current_answer = ""
            if current_answer != "":
                Submit.disabled = False
            else:
                Next.disabled = True
                Submit.disabled = True
        elif current_object["exercice_type"] == "true_false":
            if instance.state == "normal":
                current_answer = "False"
                instance.text = "False"
            else:
                current_answer = "True"
                instance.text = "True"
            if current_answer != "":
                Submit.disabled = False
            else:
                Next.disabled = True
        elif current_object["exercice_type"] == "free":
            Submit.disabled = False
            current_answer = instance.text
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
        current_index += 1
        if current_index == actual_tasks:
            score = math.ceil((right_answers/actual_tasks)*100)
            latinapp.screen_manager.current = "Results"
        else:
            current_object = task_list[current_index]
            self.build()


class MainApp(App): #Class for the Main Application, used for connecting all the pages together and handling restarts
    def build(self):
        self.title = "Astaxulator"
        self.screen_manager = ScreenManager()

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
    
    def restart(self):
        self.root.clear_widgets()
        self.stop()
        #self.build()
        Builder.unload_file("main.kv")
        #self.build()
        return (MainApp().run())
        

if __name__ == "__main__": #Run the application
    latinapp = MainApp()
    latinapp.run()

