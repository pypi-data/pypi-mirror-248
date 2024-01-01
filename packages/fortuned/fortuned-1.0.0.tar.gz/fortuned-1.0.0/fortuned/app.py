"Gives you a random fortune"
import random
from flask import Flask, render_template

app = Flask(__name__)


def get_fortunes(file='fortunes.txt'):
    "Fortune parser"
    # opening the file in read mode
    with open(file, "r", encoding="utf-8") as file:
        # reading the file
        data = file.read()
        # replacing end splitting the text
        # when newline ('\n') is seen.
        fortunes = data.split("\n")
        file.close()
        return fortunes




@app.route('/')
def main():
    "main"
    numbers = [random.randint(1, 99) for i in range(0, 5)]
    return render_template("index.html", fortune=random.choice(get_fortunes()), numbers=numbers)


if __name__ == "__main__":
    app.run(debug=True)
