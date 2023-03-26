# from bs4 import BeautifulSoup
# import requests
# import spacy

# from flask import Flask, jsonify, request
# from sexual_words import sexual_keywords

# app = Flask(__name__)

# nlp = spacy.load('en_core_web_sm')

# @app.route("/health")
# def health():
#     return "app running on port:8080"

# @app.route("/blogs-articles")
# def scrap_articles():
#     args = request.args
#     sentence = args.get("s")
#     doc = nlp(sentence)

#     keywords = [token.text for token in doc if token.pos_ in ['NOUN', 'PROPN'] and token.text in sexual_keywords]

#     blogURLs = []

#     for keyword in keywords:
#         url = f"https://www.bbc.co.uk/search?q={keyword}"
#         r = requests.get(url)

#         if r.status_code != 200:
#             print("Error fetching content for url " + url + " skipping.....")
#             continue

#         soup = BeautifulSoup(r.content, "html.parser")
#         links = soup.find_all("a", {"class": "css-1dv5jt5-StyledA e1f5wbog12"})
#         for link in links:
#             blogURLs.append({"title": link.text.strip(), "url": link['href']})

#     print("sending response:")
#     print(blogURLs)

#     return blogURLs, 200


# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=8080)


from bs4 import BeautifulSoup
import requests
import spacy

from flask import Flask, jsonify, request

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

    keywords = [token.text for token in doc if token.pos_ in ['NOUN', 'PROPN']]

    blogURLs = []

    for keyword in keywords:
        url = f"https://www.bbc.co.uk/search?q={keyword}"
        r = requests.get(url)

        if r.status_code != 200:
            print("Error fetching content for url " + url + " skipping.....")
            continue

        soup = BeautifulSoup(r.content, "html.parser")
        links = soup.find_all("a", {"class": "css-1dv5jt5-StyledA e1f5wbog12"})
        for link in links:
            blogURLs.append({"title": link.text.strip(), "url": link['href']})

    print("sending response:")
    print(blogURLs)

    return jsonify(blogURLs), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
