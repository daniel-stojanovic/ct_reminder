from flask import Flask, render_template
import os
app = Flask(__name__)
app.debug=True

@app.route('/')
def index():
    reminder_rattlesnake = "python /Users/danny/PycharmProjects/test_webapp/app.py"
    os.system(reminder_rattlesnake)
    return "Running reminders now..."


if __name__ == '__main__':
    app.run()