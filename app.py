import random
import string
import json
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy


with open('config.json', 'r') as json_file:
    parse = json.load(json_file)
    
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = parse['database_uri']
db = SQLAlchemy(app)

class Url(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    urlCode = db.Column(db.String(100), nullable=False)
    longUrl = db.Column(db.String(100), nullable=False)

    def __repr__(self) -> str:
        return f'{self.sno} - {self.urlCode}'
    

@app.route("/", methods=['GET','POST'])
def hello_world():
    if request.method == "POST":
        dlt = Url.query.all()
        for i in dlt:
            db.session.delete(i)
            db.session.commit()

    block = f"display: {'none'};"
    return render_template('index.html',block=block)

@app.route("/shorten", methods=['POST'])
def shorten_url():
    longUrl = request.form['url']
    urlCode = generate_short_url()
    sentTodb = Url(urlCode=urlCode, longUrl=longUrl)
    db.session.add(sentTodb)
    db.session.commit()
    shortUrl = f'{parse["domain"]}{urlCode}'
    block = f"display: {'block'};"
    return render_template('index.html',shortUrl=shortUrl,block=block, longUrl=longUrl)

def generate_short_url():
    characters = string.ascii_letters + string.digits
    short_url = ''.join(random.choice(characters) for _ in range(6))
    return short_url

@app.route(f"/<urlCode>", methods=['GET'])
def redirect_to(urlCode):
    codes = Url.query.all()
    for code in codes:
        if(urlCode == (code.urlCode)):
            LongUrl = code.longUrl
            return redirect(LongUrl)
    return redirect('/')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=3000)
