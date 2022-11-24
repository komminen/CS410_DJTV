# importing modules
from flask import Flask, render_template, request
from application.searchEngine.dummyTest import queryMovies
  
# declaring app name
app = Flask(__name__)

# defining home page
@app.route('/')
def index():
# returning index.html and list
# and length of list to html page
    return render_template("index.html")


@app.route('/search/', methods=['POST'])
def searchMovies():
    query = request.form.get("query")
    movie_result = queryMovies(query)

    return render_template("index.html", movieResults=movie_result)


if __name__ == '__main__':
    # running app
    app.run(host='0.0.0.0', port=5000, use_reloader=True, debug=True)