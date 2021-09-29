from search import app

@app.route('/cardTemplates/')
def getCardTemplates():
    return 'Hello World!'
