from flask import Flask, request, redirect, render_template
from urllib.parse import urlparse
import string
import random

app = Flask(__name__)

# This is the hashmap to store the URL
urlDictionary = {}


# Random Short code generater
def generate_short_code(length=4):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))


# Route for the home page
@app.route('/', methods=['GET', 'POST'])
def index():
    numUrl = 0
    if request.method == 'POST':
        long_url = request.form['long_url']
        # Check if it is a valid url
        if is_valid_url(long_url):
            short_code = generate_short_code()
            short_url = request.host_url + short_code
            # Checks there are no duplicates for short_url
            while (urlDictionary.get(short_url) != None):
                short_code = generate_short_code()
                short_url = request.host_url + short_code
            urlDictionary[short_url] = long_url
        else:
            print("invalid url")

    # include number of shortened urls
        if urlDictionary:
            numUrl = len(urlDictionary)
    return render_template('index.html', urlDictionary=urlDictionary, numUrl=numUrl)


# Route to redirect short URLs to the original URL
@app.route('/<short_code>')
def redirect_to_long_url(short_code):
    shortUrl = request.host_url+short_code
    result = request.host_url
    if shortUrl in urlDictionary:
        result = urlDictionary[request.host_url+short_code]
    else:
        print("No shortUrl in dictionary")

    return redirect(result)


# function to check invalid url
def is_valid_url(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False


if __name__ == '__main__':
    app.run(debug=True)

# Is this how to check invalid url
