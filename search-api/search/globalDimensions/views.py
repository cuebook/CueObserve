from search import app

@app.route('/globalDimensions/')
def getGlobalDimensions():
    return 'Hello World!'
