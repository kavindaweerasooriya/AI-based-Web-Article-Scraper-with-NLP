
from bs4 import BeautifulSoup
import requests
import spacy

from flask import Flask, jsonify, request
from sexual_words import sexual_keywords

app = Flask(__name__)


nlp = spacy.load('en_core_web_sm')

@app.route("/health")
def health():
    return "app running on port:8080"


@app.route("/blogs-articles")
def scrap_articles():
    args = request.args
    sentence = args.get("s")
    doc = nlp(sentence)

    keywords = [token.text for token in doc if token.pos_ in ['NOUN', 'PROPN'] and token.text in sexual_keywords]


    blogURLS = []

    for keyword in keywords:
        url = "https://www.bbc.co.uk/search?q="+keyword+"&d=HOMEPAGE_GNL"
        r=requests.get(url)
        
        if r.status_code !=200:
            print("Error fetching content for url " + url +" skipping.....")
            continue

        soup=BeautifulSoup(r.content,"html.parser")
        url=soup.find("a",{"class":"ssrcss-rl2iw9-PromoLink e1f5wbog1"}).get("href")
        blogURLS.append({"url":url})
        

    print("sending response:")
    print(blogURLS)


    return blogURLS, 200


if __name__ == '__main__':
      app.run(host='0.0.0.0', port=8080)




# from bs4 import BeautifulSoup
# import requests
# import spacy

# from flask import Flask, jsonify, request
# from sexual_words import sexual_keywords

# app = Flask(__name__)

# # Load the Spacy model for English language processing
# nlp = spacy.load('en_core_web_sm')

# @app.route("/health")
# def health():
#     return "app running on port:8080"

# @app.route("/keywords")
# def get_keywords():
#     # Return a list of all the sexual keywords that are being used to filter the search
#     return jsonify(sexual_keywords)

# @app.route("/blogs-articles")
# def scrap_articles():
#     args = request.args
#     sentence = args.get("s")

#     if not sentence:
#         return jsonify({"error": "No sentence provided"}), 400

#     doc = nlp(sentence)

#     # Extract keywords from the input sentence
#     keywords = [token.text for token in doc if token.pos_ in ['NOUN', 'PROPN'] and token.text in sexual_keywords]

#     blogURLS = []

#     # Loop through each keyword and perform a search on the BBC website
#     for keyword in keywords:
#         url = f"https://www.bbc.co.uk/search?q={keyword}&d=HOMEPAGE_GNL"
#         r = requests.get(url)

#         if r.status_code != 200:
#             app.logger.error(f"Error fetching content for url {url}")
#             continue

#         soup = BeautifulSoup(r.content, "html.parser")

#         # Find the URL of the first article that matches the keyword
#         link = soup.find("a", {"class": "ssrcss-rl2iw9-PromoLink e1f5wbog1"})

#         if link is not None:
#             blogURLS.append({"keyword": keyword, "url": link.get("href")})
#         else:
#             app.logger.warning(f"No search results for keyword {keyword}")

#     # Return a list of dictionaries containing the URLs of articles related to the extracted keywords
#     if len(blogURLS) > 0:
#         return jsonify(blogURLS), 200
#     else:
#         return jsonify({"error": "No articles found"}), 404

# if __name__ == '__main__':
#     # Add basic authentication to the app
#     app.config['BASIC_AUTH_USERNAME'] = 'user'
#     app.config['BASIC_AUTH_PASSWORD'] = 'password'
#     basic_auth = BasicAuth(app)

#     # Add logging to the app
#     handler = RotatingFileHandler('app.log', maxBytes=10000, backupCount=1)
#     handler.setLevel(logging.INFO)
#     app.logger.addHandler(handler)

#     app.run(host='0.0.0.0', port=8080)
