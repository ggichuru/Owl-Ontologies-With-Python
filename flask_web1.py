from flask import Flask, url_for
app = Flask(__name__)

@app.route('/path/<parameter>')
def generate_web_page(parameter):
    html = "<html><body>"
    html += "The value of the parameter is: %s" % parameter
    html += "</body></html>"
    return html