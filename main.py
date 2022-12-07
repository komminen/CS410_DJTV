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
# For now, hard code to bert which had the best results


def fixSentimentText(sentiment):
    fixedSentiment = sentiment
    if sentiment == "pos":
        fixedSentiment = "Positive"
    elif sentiment == "neu":
        fixedSentiment = "Neutral"
    elif sentiment == "neg":
        fixedSentiment = "Negative"
    return fixedSentiment

# defining home page
@app.route('/')
def index():
# returning index.html and list
# and length of list to html page
    return render_template("index.html")


@app.route('/search/', methods=['POST'])
def searchMovies():
    query = request.form.get("query")
    ranker = request.form.get("ranker")
    corpus = request.form.get("corpus")
    print(ranker, corpus)
    # movie_result = run("config_whole.toml", "bm25", query)
    movie_result = movie_search_engine.run(query, ranker, corpus)
    output = []
    for movie_id in movie_result:
        output.append(
            {
                "movie_id": movie_id,
                # Change required content here
                "cover_url": movies_metadata[movie_id]["cover_url"],
                "localized_title": movies_metadata[movie_id]["localized_title"],
                "year": movies_metadata[movie_id]["year"],
                "sentiment": fixSentimentText(movies_sentiment[movie_id]["sentiment"])
            }
        )

    return render_template("index.html", movieResults=output)

@app.route('/detail/<movie_id>/', methods=['GET', 'POST'])
def movieDetail(movie_id):
    output = [] #{'movie_id': movie_id}
    similarMovies = []
    movies_similar = json.load(open("data/similarMovies_bert.json"))

    if request.method == 'POST':
        print('POST')
        algo = request.form.get("algorithm")
        filename = 'data/similarMovies_'+algo+'.json'
        print(algo, filename)
        movies_similar = json.load(open(filename))

    # Clean up the sentiment text for output in the rendered html
    sentiment = fixSentimentText(movies_sentiment[movie_id]["sentiment"])

    # Clean up the summary text for output in the rendered html
    summary = movies_metadata[movie_id]["summary"]
    plotindex = summary.find("Plot:")
    if plotindex != -1:
        plotindex += 5
        summary = summary[plotindex:]

    # Clean up the similar movie list for output in the rendered html
    for similarMovieId in movies_similar[movie_id]["similar_movie_ids"]:
        similarMovieSentiment = fixSentimentText(movies_sentiment[similarMovieId]["sentiment"])

        similarMovies.append(
            {
                "movie_id": similarMovieId,
                "cover_url": movies_metadata[similarMovieId]["cover_url"],
                "localized_title": movies_metadata[similarMovieId]["localized_title"],
                "year": movies_metadata[similarMovieId]["year"],
                "sentiment": similarMovieSentiment
            }
        )

    output.append(
        {
            "movie_id": movie_id,
            "cover_url": movies_metadata[movie_id]["cover_url"],
            "localized_title": movies_metadata[movie_id]["localized_title"],
            "year": movies_metadata[movie_id]["year"],
            "rating": movies_metadata[movie_id]["rating"],
            "director": movies_metadata[movie_id]["director"],
            "length": movies_metadata[movie_id]["runtimes"],
            "genres": movies_metadata[movie_id]["genres"],
            "cast": movies_metadata[movie_id]["cast"],
            "summary": summary,
            "sentiment": sentiment,
            "num_reviews": movies_sentiment[movie_id]["num_reviews"],
            "num_neg": movies_sentiment[movie_id]["num_neg"],
            "num_neu": movies_sentiment[movie_id]["num_neu"],
            "num_pos": movies_sentiment[movie_id]["num_pos"],
            "similar_movies": similarMovies
        }
    )
    return render_template("detail.html", movie_detail=output)


if __name__ == '__main__':
    # running app
    print("foo")
    app.run(host='0.0.0.0', port=5000, threaded=False)