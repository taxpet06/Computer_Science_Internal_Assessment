import pymongo
#multiple_choice
#true_false
#free
#connecting
#ordering
def we_addin():
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["IA"]
    mycol = mydb["Exercices"]
    type = "true_false"
    question = "Eisai Mparmpouniaris"
    option = 1
    all_options = ["3", "5", "8"]
    correct = ["True"]
    explanation_text = "Fysika kai eisai barbouniaris"
    mydict = {"exercice_type": type, "question_text": question, "options": option, "correct_answer": correct, "all_options": all_options, "explanation": explanation_text}
    x= mycol.insert_one(mydict)
we_addin()
