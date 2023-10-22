import pymongo
#multiple_choice
#true_false
#free
#connecting
#ordering
#grammar
#vocabulary
#syntax
def adding(type,tags,question,option,all_options,correct,explanation_text):
    #Connect to the local MongoDB client
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["IA"]
    mycol = mydb["Exercices"]
    #create_wanted_entry
    mydict = {"exercice_type": type, "exercice_tags":tags, "question_text": question, "options": option,
     "correct_answer": correct, "all_options": all_options, "explanation": explanation_text}
    x = mycol.insert_one(mydict) #add_entry_to_database
