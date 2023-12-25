__author__ = 'amaharjan.de'

from flask import Flask, render_template
import requests

app = Flask(__name__)

@app.route('/')
def get_ip_info():
    '''
    Retrieves your public IP related information.
    '''
    url = 'http://ip-api.com/json'
    response = requests.get(url)
    return render_template('index.html', data=response.json())

if __name__ == '__main__':
    app.run()  
