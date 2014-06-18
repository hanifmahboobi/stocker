from flask import Flask, render_template, request
from flask.ext.script import Manager
from flask.ext.bootstrap import Bootstrap
import stocks
from pymongo import MongoClient

app = Flask(__name__)

manager = Manager(app)
bootstrap = Bootstrap(app)

mongo = MongoClient()
db = mongo.stock
stock = db.stock
user = db.user

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/stock/<ticker>')
def stock(ticker):
    return render_template('stock.html', ticker=ticker, quote=stocks.get_quote(ticker))

@app.route('/add/<ticker>')
def add(ticker):
    try:
      user.insert({'stock':ticker})
      return render_template('add.html', ticker=ticker)
    except:
      return render_template('uhoh.html')

@app.route('/add/',methods=['GET'])
def badd():
    return render_template('badd.html')

@app.route('/add/',methods=['POST'])
def padd():
    ticker = request.form['stock']
    add(ticker)
    return render_template('add.html', ticker=ticker)

@app.route('/remove/<ticker>')
def remove(ticker):
    try:
      user.remove({'stock':ticker}) 
      return render_template('remove.html', ticker=ticker)
    except:
      return render_template('uhoh.html')

@app.route('/remove/')
def bremove():
    return render_template('bremove.html')

@app.route('/remove/',methods=['POST'])
def premove():
    ticker = request.form['stock']
    remove(ticker)
    return render_template('remove.html', ticker=ticker)

@app.route('/view/',methods=['POST'])
def search():
    ticker = request.form['search']
    price = stocks.get_quote(ticker)
    return render_template('view.html', ticker=ticker,price=price) 

@app.route('/profile/')
def profile():
    stocklist = user.find()    
    return render_template('profile.html', stocklist=stocklist, stocks=stocks)

if __name__ == '__main__':
#    manager.run()
    app.run(debug=True)