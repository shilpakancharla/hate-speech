import sys
from flask import Flask, render_template
from flask_frozen import Freezer # Added
app = Flask(__name__, static_folder='templates/static')
freezer = Freezer(app) # Added

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "build":
        freezer.freeze()
    else:
        app.run(debug=True)