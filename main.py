# importing modules
from flask import Flask, render_template, request
from application.searchEngine.search import movieSearchEngine
import json
  
# declaring app name
app = Flask(__name__)

# Init
movie_search_engine = movieSearchEngine(
    cfg="config.toml", 
    movie_review_path="application/searchEngine/movie_reviews_dataset.json",
    ranker="bm25"
)
movies_metadata = json.load(open("data/movies_metadata.json"))
movies_sentiment = json.load(open("data/review_sentiment_counts.json"))


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
    output = []
    for movie_id in movie_result:
        output.append(
            {
                "movie_id": movie_id,
                # Change required content here
                "cover_url": movies_metadata[movie_id]["cover_url"],
                "localized_title": movies_metadata[movie_id]["localized_title"],
                "year": movies_metadata[movie_id]["year"],
                "sentiment": movies_sentiment[movie_id]["sentiment"]
            }
        )
    
    print(output)

    return render_template("index.html", movieResults=output)

@app.route('/detail/<movie_id>/', methods=['GET'])
def movieDetail(movie_id):
    output = {'movie_id': movie_id}
    return render_template("detail.html", movie_detail=output)


if __name__ == '__main__':
    # running app
    app.run(host='0.0.0.0', port=5000, threaded=False)