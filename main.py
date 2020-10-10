from flask import Flask, render_template, url_for, redirect, request
from werkzeug.datastructures import ImmutableMultiDict

# creating of an application with Flask instance
app = Flask(__name__)

# this will open index page
@app.route("/")
def index():
    return render_template('index.html')

# this will get entered number prof previous form
@app.route("/enter", methods=["POST", "GET"])
def enter():
    output = request.form["number"]

    html = '<form action="/positions" method="post">'

    for x in range(int(output)):
        html += '<p class="poradie">{}. písmeno: <input type="text" name="{}" value="-"></p>'.format(x+1, x)

    html += '<input type="submit" value="Vyhľadať"></form>'

    return html

@app.route("/positions", methods=["POST", "GET"])
def search():
    dict_request = request.form
    form_output = dict_request.to_dict(flat=False)

    with open("csv_database.txt") as csv_file:
        word_length = 5
        html_output = '<div id="word_output">'
        csv_string = csv_file.read()
        words = csv_string.split(",")

        word_search = {}
        print(form_output)
        for key, value in form_output.items():
            if value != '-':
                word_search[int(key)] = value
        print(word_search)
        for word in words:
            word_success = 1
            if len(word) != word_length:
                word_success = 0
                pass
            else:
                html_word = '<p class="word">{}</p>'.format(word)
                word_list = list(word)
                for key2, value2 in word_search.items():
                    if word_list[key2] != value2:
                        word_success = 0
            if word_success == 1:
                print("success")
                html_output += html_word
            else:
                print("fail")
        html_output += '</div>'
    return html_output


if __name__ == "__main__":
    app.run(debug=True)
