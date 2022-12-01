# goggle search
# first pip install googletrans==3.1.0a0 and flask

from flask_cors import CORS
from flask import Flask, request
from serpapi import GoogleSearch
from googletrans import Translator
translator = Translator()

app = Flask(__name__)
CORS(app)
cors=CORS(app,resources={r"/*":{"origins":"*"}})

# the function gets questions in Hebrew. translate and search in English and then return the answer in Hebrew


def getMyAns(he_q):
    # step 1 - translate the question from Hebrew to English
    en_q = translator.translate(he_q, src='he')
    print("en_q: "+en_q.text)

    # step 2 - search the qustion in english
    params = {
        "q": en_q.text,
        "hl": "en",
        "gl": "us",
        "api_key": "20a2b41d24b1640b84931cd0d544465b17eb357752b9ec1ff4b27dde51a715c7"
    }
    search = GoogleSearch(params)
    print("the search done")

    # step 3 - get the snippet answer in english
    results = search.get_dict()
    answer_box = results["answer_box"]
    en_a = answer_box["snippet"]
    try:
      for i in answer_box["list"]:
        en_a=en_a+" "+i+"\n"
    except:
        pass

    # step 4 - print the answer in hebrew
    he_a = translator.translate(en_a, src='en', dest='he')
    print("the answer is: "+he_a.text)
    return(he_a.text)

# the api function


@app.route("/result", methods=["POST", "GET"])
def result():
    output = request.get_json()
    the_q = str(output['the_q'])
    print("the question is: "+the_q)
    cal = {}
    try:
        cal['the_ans'] = getMyAns(the_q)
    except:
        cal['the_ans'] = "לא מצאנו תשובה נוספת לשאלתך מעבר למה שקיים בחיפוש הרגיל בגוגל. אבל הי! אל דאגה! הוספנו למטה את החיפוש שלך!"
    return (cal)


if 'app' == '__main__':
    app.run()
