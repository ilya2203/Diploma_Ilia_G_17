from getDataFromDb import get_seasons_db, get_players_db # Functions to get data
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=('GET', 'POST'))

def index():
    seasonsIDsApp = get_seasons_db()
    playersApp = get_players_db()
    
    return render_template('index.html', seasonsIDs=seasonsIDsApp, players=playersApp)

if __name__ == '__main__':
    app.run(debug=True)



    
