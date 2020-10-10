from flask import Flask, render_template, url_for, redirect, request, session
# creating of an application with Flask instance
app = Flask(__name__)
app.secret_key = "test"

# this will open index page
@app.route("/")
def index():
    return render_template('index.html')

# this will get entered number prof previous form
@app.route("/enter", methods=["POST", "GET"])
def enter():
    output = request.form["number"]
    session["word_length"] = output
    html = '<h2>Vyhľadávanie slov so {} písmenami...s</h2><h3>Zadajte písmena, ktoré poznáte:</h3><form action="/positions" method="post">'.format(output)

    for x in range(int(output)):
        html += '<p class="poradie">{}. písmeno: <input type="text" name="{}" value="-"></p>'.format(x+1, x)

    html += '<input type="submit" value="Vyhľadať"></form>'
    return html

@app.route("/positions", methods=["POST", "GET"])
def search():
    dict_request = request.form
    form_output = dict_request.to_dict(flat=False)

    with open("csv_database.txt") as csv_file:
        word_length = int(session["word_length"])
        html_output = '<div id="word_output">'
        csv_string = csv_file.read()
        words = csv_string.split(",")
        word_search = {}
        for key, value in form_output.items():
            if value != ['-']:
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
                    if word_list[key2] != value2[0]:
                        word_success = 0
                        pass
            if word_success == 1:
                html_output += html_word
            else:
                continue
        html_output += '</div>'
    if html_output == '<div id="word_output"></div>':
        return 'Neboli nájdená žiadne slová'
    else:
        return html_output


if __name__ == "__main__":
    app.run(debug=True)
