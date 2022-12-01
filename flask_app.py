# goggle search
# first pip install googletrans==3.1.0a0 and flask

from flask_cors import CORS
from flask import Flask, request, make_response
from serpapi import GoogleSearch
from googletrans import Translator
import os
import openai

OPENAI_API_KEY=os.getenv("OPENAI")
openai.api_key=OPENAI_API_KEY
translator = Translator()

app = Flask(__name__)
CORS(app)
cors = CORS(app, resources={r"/*": {"origins": "*"}})


# the function gets questions in Hebrew. translate and search in English and then return the answer in Hebrew


def getMyAns(he_q):
    # step 1 - translate the question from Hebrew to English
    en_q = translator.translate(he_q, src='he')
    print("en_q: " + en_q.text)

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
            en_a = en_a + " " + i + "\n"
    except:
        pass

    # step 4 - print the answer in hebrew
    he_a = translator.translate(en_a, src='en', dest='he')
    print("the answer is: " + he_a.text)
    return (he_a.text)


# the api function



@app.route("/image", methods=['POST'])
def get_img():
    '''
    :argument: txt , lang

    need to provide txt in hebrew / english and to choose which lang u need - he vs en

    200 is ok
    400 fail

    :return:
        image_url - generated image url
    '''
    input = request.get_json()
    if "txt" not in input and "lang" not in input:
        return make_response(
            {
                "status": False, "message": "please provide txt and lang"},
            400
        )
    text=input['txt']
    lang= input['lang']
    if lang == "he":
        en_q = translator.translate(text, src='he')
        en_q=en_q.text
        response = openai.Image.create(
            prompt=en_q,
            n=1,
            size="1024x1024"
        )
        image_url = response['data'][0]['url']
        return make_response({"status":True,"message":"image has been generated using DALL E 2 Technology", "image_url":image_url},200)

    elif lang == "en":
        response = openai.Image.create(
            prompt=text,
            n=1,
            size="1024x1024"
        )
        image_url = response['data'][0]['url']
        return make_response(
            {"status": True, "message": "image has been generated using DALL E 2 Technology", "image_url": image_url},
            200)
    else :
        return make_response(
            {
                "status": False, "message": "you can only use lang = he / en"},
            400
        )





@app.route("/result", methods=["POST", "GET"])
def result():
    output = request.get_json()
    the_q = str(output['the_q'])
    print("the question is: " + the_q)
    cal = {}
    try:
        cal['the_ans'] = getMyAns(the_q)
    except:
        cal[
            'the_ans'] = "לא מצאנו תשובה נוספת לשאלתך מעבר למה שקיים בחיפוש הרגיל בגוגל. אבל הי! אל דאגה! הוספנו למטה את החיפוש שלך!"
    return (cal)


if __name__ == '__main__':
    app.run()