import kivy
import pymongo
from kivy.core.audio import SoundLoader
from kivy.clock import Clock
import time
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
from data_base_testing import we_addin
from bson.objectid import ObjectId
from kivy.event import EventDispatcher
import math
Window.size = (720*0.65, 1280*0.65)
import random
kivy.require('1.11.1')
Window.clearcolor = (0.1, 0.1, 0.2, 1)
global score
global passcode 
global once 
global answer_field
global button_sound
button_sound = SoundLoader.load('Computer_Science_Internal_Assessment/bwuaaap.wav')
once = 1
passcode = "passcode"
score = 0
looper = True
global quiz_kind #mc, fr, cw, ow, rw, grammar, vocabulary, syntax, #random
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

class Home(GridLayout):
    def login(self):
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
    def home(self):
        global button_sound
        button_sound.play()
        latinapp.screen_manager.current = "Home"
    def change_stats(self):
        global score
        self.clear_widgets()
        self.rows = 4
        self.padding = (10,10)
        self.spacing = (10,10)
        text_score_label = Label(
            text="Congratulations",
            font_size=40,
            color=(1, 1, 1, 1)
        )
        num_score_label = Label(
            text= str(score)+"%",
            font_size=80,
            color=(1,1,1,1)
        )
        progress_bar = ProgressBar(
            # color= (0.459, 0.722, 0.31, 1) ,
            # back_color= (0.459, 0.722, 0.31, 1) ,
            max=100,
            value= score
        )
        home = Button(
            text="Home",
            font_size=40,
            border=(2, 2, 2, 2),
            background_color=(0.459, 0.722, 0.31, 1),
            background_normal='',
        )
        self.add_widget(text_score_label)
        self.add_widget(num_score_label)
        self.add_widget(progress_bar)
        self.add_widget(home)
        home.on_press = self.home
        
class TeacherDashboard(GridLayout):
    def add(self):
        global button_sound
        button_sound.play()
        latinapp.screen_manager.current = "AddDrill"
    def drills(self):
        global button_sound
        button_sound.play()
        latinapp.screen_manager.current = "DrillList"
    def home(self):
        global button_sound
        button_sound.play()
        latinapp.screen_manager.current = "Home"

class DrillList(GridLayout):
    def build(self, instance):
        global button_sound
        button_sound.play()
        self.ids.carousel.clear_widgets()
        myclient = pymongo.MongoClient("mongodb://localhost:27017/")
        mydb = myclient["IA"]
        mycol = mydb["Exercices"]
        mylist = list(mycol.find())
        for i in mylist:
            self.ids.carousel.add_widget(Button(text = i["question_text"]+"\n"+str(i["_id"]), font_size = 20, background_color = (0.459, 0.722, 0.31, 1), background_normal='', on_press = self.update))
    def home(self):
        global button_sound
        button_sound.play()
        latinapp.screen_manager.current = "Home"
    def add(self):
        global button_sound
        button_sound.play()
        latinapp.screen_manager.current = "AddDrill"
    def update(self, instance):
        global button_sound
        button_sound.play()
        global current_drill_id
        current_drill_id = instance.text[instance.text.find('\n')+1:]
        global myupdate
        myupdate = True 
        latinapp.screen_manager.current = "ModifyDrill"
        ModifyDrill.update(ModifyDrill())

class ModifyDrill(GridLayout):
    global myupdate
    def update(self):
        Builder.load_file("Main.kv")
        global current_drill_id
        global current_drill
        global myupdate
        global tags
        if myupdate:
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
    def add_to_db(self):
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
        we_addin(mytype,tags,questiondb, optiondb, all_optionsdb, correctdb, exp_db)
        global current_drill
        mycol.delete_one(current_drill[0])
    def addremove_tag(self, value, active):
        global button_sound
        button_sound.play()
        global tags
        if active:
            tags.append(value)
        else:
            tags.remove(value)
    def delete_from_alloptions(self):
        global button_sound
        button_sound.play()
        global all_optionsdb
        if all_optionsdb:
            all_optionsdb.pop()
        self.ids.all_options.text = str(all_optionsdb)
        pass
    def add_to_alloptions(self):
        global button_sound
        button_sound.play()
        global all_optionsdb
        all_optionsdb.append(self.ids.one_option.text)
        self.ids.all_options.text = str(all_optionsdb)
    def delete_from_allanswers(self):
        global button_sound
        button_sound.play()
        global correctdb
        if correctdb:
            correctdb.pop()
        self.ids.all_answers.text = str(correctdb)
        pass
    def add_to_allanswers(self):
        global button_sound
        button_sound.play()
        global correctdb
        correctdb.append(self.ids.one_answer.text)
        self.ids.all_answers.text = str(correctdb)
    def home(self):
        global button_sound
        button_sound.play()
        latinapp.screen_manager.current = "Home"
    def change_type(self, value):
        global button_sound
        button_sound.play()
        global mytype
        mytype = value
        mytype = str(mytype)
        if mytype == "true_false" or mytype == "free":
            self.ids.option_slider.value = 1
            self.ids.option_slider.disabled = True
        else:
            self.ids.option_slider.disabled = False
    def slider(self,value):
        global optiondb
        optiondb = value
        self.ids.options.text = "Options " + str(value)
    # ev = MyEventDispatcher()
    # ev.bind(on_test=update)
    # ev.do_something('pwease')

class AddDrill(GridLayout):
    def add_to_db(self):
        global button_sound
        button_sound.play()
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
        we_addin(mytype,tags,questiondb, optiondb, all_optionsdb, correctdb, exp_db)
        pass
    def addremove_tag(self, value, active):
        global button_sound
        button_sound.play()
        global tags
        if active:
            tags.append(value)
        else:
            tags.remove(value)
    def delete_from_alloptions(self):
        global button_sound
        button_sound.play()
        global all_optionsdb
        if all_optionsdb:
            all_optionsdb.pop()
        self.ids.all_options.text = str(all_optionsdb)
        pass
    def add_to_alloptions(self):
        global button_sound
        button_sound.play()
        global all_optionsdb
        all_optionsdb.append(self.ids.one_option.text)
        self.ids.all_options.text = str(all_optionsdb)
    def delete_from_allanswers(self):
        global button_sound
        button_sound.play()
        global correctdb
        if correctdb:
            correctdb.pop()
        self.ids.all_answers.text = str(correctdb)
        pass
    def add_to_allanswers(self):
        global button_sound
        button_sound.play()
        global correctdb
        correctdb.append(self.ids.one_answer.text)
        self.ids.all_answers.text = str(correctdb)
    def home(self):
        global button_sound
        button_sound.play()
        latinapp.screen_manager.current = "Home"
    def change_type(self, value):
        global button_sound
        button_sound.play()
        global mytype
        mytype = value
        mytype = str(mytype)
        if mytype == "true_false" or mytype == "free":
            self.ids.option_slider.value = 1
            self.ids.option_slider.disabled = True
        else:
            self.ids.option_slider.disabled = False
    def slider(self,value):
        global optiondb
        optiondb = value
        self.ids.options.text = "Options " + str(value)

class TeacherLogin(GridLayout):
    def home(self):
        global button_sound
        button_sound.play()
        latinapp.screen_manager.current = "Home"
    def dashboard(self):
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
    def get_random_type_document(self,collection):
        global full_task_list
        global random_index
        global quiz_kind
        random_index = random.randint(0, len(full_task_list)-1)
        random_document = full_task_list.pop(random_index)
        return random_document
    def get_random_document(self,collection):
        global full_task_list
        global random_index
        # count = collection.count_documents({})  # Get the total number of documents in the collection
        random_index = random.randint(0, len(full_task_list)-1)  # Generate a random index within the range of document count
        # random_document = collection.find().limit(1).skip(random_index)[0]
        random_document = full_task_list.pop(random_index)
        return random_document
    global current_object
    global current_index
    current_index = 0
    global right_answers
    right_answers = 0
    def build(self):
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
        full_task_list = list(mycol.find())
        task_amount = len(full_task_list)
        if once == 1:
            if task_amount < 10:
                if quiz_kind == "random":
                    for i in range(1,len(full_task_list)+1):
                        task_list.append(self.get_random_document(mycol))
                        actual_tasks = len(task_list)
                if quiz_kind == "multiple_choice" or quiz_kind == "true_false" or quiz_kind == "free" or quiz_kind == "connecting" or quiz_kind == "ordering":
                    full_task_list = list(mycol.find({"exercice_type":quiz_kind}))
                    for i in range(1,len(full_task_list)+1):
                        task_list.append(self.get_random_type_document(mycol))
                        actual_tasks = len(task_list)
                if quiz_kind == "grammar" or quiz_kind == "syntax" or quiz_kind == "vocabulary":
                    full_task_list = list(mycol.find({"exercice_tags":quiz_kind}))
                    for i in range(1,len(full_task_list)+1):
                        task_list.append(self.get_random_type_document(mycol))
                        actual_tasks = len(task_list)
            else:
                if quiz_kind == "random":
                    for i in range(1,11):
                        task_list.append(self.get_random_document(mycol))
                        actual_tasks = 10
                if quiz_kind == "multiple_choice" or quiz_kind == "true_false" or quiz_kind == "free" or quiz_kind == "connecting" or quiz_kind == "ordering":
                    full_task_list = list(mycol.find({"exercice_type":quiz_kind}))
                    for i in range(1,len(full_task_list)+1):
                        task_list.append(self.get_random_type_document(mycol))
                        actual_tasks = len(task_list)
                if quiz_kind == "grammar" or quiz_kind == "syntax" or quiz_kind == "vocabulary":
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
            self.add_widget(Label(text = current_object["question_text"], color = (1,1,1,1), font_size = 20))
            Options = GridLayout(rows = current_object["options"], cols = 1, spacing=(10,10),padding=(10,10))
            self.add_widget(Options)
            for i in current_object["all_options"]:
                # Options.add_widget(Label(text=str(i), color = (1,1,1,1), font_size = 20))
                # Options.add_widget(CheckBox(group="v", active = False, x = str(i), on_press = self.get_answer))
                Options.add_widget(ToggleButton(group="v", state = "normal", text = str(i), background_color=(0.459, 0.722, 0.31, 1),background_normal ='', on_press = self.get_answer, font_size = 20))
            Explanation = Label(text = "", color = (1,1,1,1), font_size = 20)
            exp_text = current_object["explanation"]
            self.add_widget(Explanation)
            Buttons = GridLayout(cols = 2, spacing=(10,10),padding=(10,10))
            self.add_widget(Buttons)
            Submit = Button(text="Submit",font_size = 20, border= (2,2,2,2), halign="center", background_color=(0.459, 0.722, 0.31, 1), background_normal ='', on_press = self.reveal_answer, disabled = True)
            Next = Button(text="Next",font_size = 20, border= (2,2,2,2), halign="center", background_color=(0.459, 0.722, 0.31, 1), background_normal ='', disabled = True, on_press = self.next_task)
            Buttons.add_widget(Submit)
            Buttons.add_widget(Next)
            if current_answer != "":
                Next.disabled = False
                Submit.disabled = False
        
        #True_False
        elif current_object["exercice_type"] == "true_false":
            self.add_widget(Label(text = current_object["question_text"], color = (1,1,1,1), font_size = 20))
            Options = GridLayout(rows = current_object["options"], cols = 1, spacing=(10,10),padding=(10,10))
            self.add_widget(Options)
            Options.add_widget(ToggleButton(group="v", state = "normal", text = "False", background_color=(0.459, 0.722, 0.31, 1),background_normal ='', on_press = self.get_answer, font_size = 20))
            Explanation = Label(text = "", color = (1,1,1,1), font_size = 20)
            exp_text = current_object["explanation"]
            self.add_widget(Explanation)
            Buttons = GridLayout(cols = 2, spacing=(10,10),padding=(10,10))
            self.add_widget(Buttons)
            Submit = Button(text="Submit",font_size = 20, border= (2,2,2,2), halign="center", background_color=(0.459, 0.722, 0.31, 1), background_normal ='', on_press = self.reveal_answer, disabled = False)
            Next = Button(text="Next",font_size = 20, border= (2,2,2,2), halign="center", background_color=(0.459, 0.722, 0.31, 1), background_normal ='', disabled = True, on_press = self.next_task)
            Buttons.add_widget(Submit)
            Buttons.add_widget(Next)
            if current_answer != "":
                Next.disabled = False
                Submit.disabled = False
        
        #Free Response
        elif current_object["exercice_type"] == "free":
            global answer_field
            self.add_widget(Label(text = current_object["question_text"], color = (1,1,1,1), font_size = 20))
            Options = GridLayout(rows = current_object["options"], cols = 1, spacing=(10,10),padding=(10,10))
            self.add_widget(Options)
            answer_field = TextInput(text = "", hint_text = "Place response here...", hint_text_color = (1,1,1,1), multiline = False, font_size = 20, color = (1,1,1,1), foreground_color = (1,1,1,1), background_color = (0.482, 0.82, 0.38, 1))
            answer_field.bind(on_text_validate=self.get_answer)
            Options.add_widget(answer_field)
            Explanation = Label(text = "", color = (1,1,1,1), font_size = 20)
            exp_text = current_object["explanation"]
            self.add_widget(Explanation)
            Buttons = GridLayout(cols = 2, spacing=(10,10),padding=(10,10))
            self.add_widget(Buttons)
            Submit = Button(text="Submit",font_size = 20, border= (2,2,2,2), halign="center", background_color=(0.459, 0.722, 0.31, 1), background_normal ='', on_press = self.reveal_answer, disabled = False)
            Next = Button(text="Next",font_size = 20, border= (2,2,2,2), halign="center", background_color=(0.459, 0.722, 0.31, 1), background_normal ='', disabled = True, on_press = self.next_task)
            Buttons.add_widget(Submit)
            Buttons.add_widget(Next)
            if current_answer != "":
                Next.disabled = False
                Submit.disabled = False

    def reveal_answer(self, instance):
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
        if current_object["exercice_type"] == "free":
            current_answer = answer_field.text
        Next.disabled = False
        for child in Options.children:
            child.disabled = True
        Submit.disabled = True
        if current_answer in current_object["correct_answer"]:
            Explanation.text = "Good Job. "+"\n"+exp_text
            right_answers += 1
        else:
            Explanation.text = "Not Quite. "+"\n"+exp_text
    def get_answer(self, instance):
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
    def next_task(self, instance):
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


class MainApp(App):
    def build(self):
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

if __name__ == "__main__":
    latinapp = MainApp()
    latinapp.run()

