from flask import Flask, render_template, request, redirect
from bokeh.plotting import figure
from bokeh.embed import components 
import numpy as np
import pandas as pd
import requests

app = Flask(__name__)

app.vars={}

def datetime(x):
    return np.array(x, dtype=np.datetime64)
    
@app.route('/')
def main():
  return redirect('/index')

@app.route('/index',methods=['GET','POST'])
def index():
    if request.method == 'POST':
        app.vars['stock'] = request.form['ticker']
        return redirect ('/stockq')
    else:
        return render_template('index.html')


@app.route('/stockq')
def stockq():
    api_url = 'https://www.quandl.com/api/v1/datasets/WIKI/%s.json?api_key=pFAQ3QcDfiaEzfUoi6xq' %app.vars['stock']
    session = requests.Session()
    session.mount('http://', requests.adapters.HTTPAdapter(max_retries=3))
    sdata=requests.get(api_url)  
    datastock = sdata.json()
    dstock=pd.DataFrame(datastock['data'],columns=datastock['column_names'])
    p1 = figure(x_axis_type = "datetime")
    p1.title = "Stock Closing Prices"
    p1.grid.grid_line_alpha=0.3
    p1.xaxis.axis_label = 'Date'
    p1.yaxis.axis_label = 'Price'
    p1.line(datetime(dstock['Date']), dstock['Close'], color='#A6CEE3', legend='%s' %app.vars['stock'])
    script, div =components(p1)        
    return render_template('stockq.html', script=script, div=div)
    #p1.line(datetime(dstock['Date']), dstock['Close'], color='#A6CEE3', legend='%s'% stock) 
    #output_file("stockq.html", title="stocks.py example")
    #return render_template('stockq.html', script=script, div=div)
    
     
if __name__ == '__main__':
    app.run()
