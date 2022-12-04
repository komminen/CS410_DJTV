# importing modules
from flask import Flask, render_template, request
from application.searchEngine.search import movieSearchEngine
  
# declaring app name
app = Flask(__name__)

movie_search_engine = movieSearchEngine(
    cfg="config.toml", 
    movie_review_path="application/searchEngine/movie_reviews_dataset.json",
    ranker="bm25"
)

# defining home page
@app.route('/')
def index():
# returning index.html and list
# and length of list to html page
    return render_template("index.html")


@app.route('/search/', methods=['POST'])
def searchMovies():
    query = request.form.get("query")
    # movie_result = run("config_whole.toml", "bm25", query)
    movie_result = movie_search_engine.run(query)
    movie_result = {
        "results": movie_result
    }
    print(movie_result)

    return render_template("index.html", movieResults=movie_result)


if __name__ == '__main__':
    # running app
    app.run(host='0.0.0.0', port=5000, threaded=False)