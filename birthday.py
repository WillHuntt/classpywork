import datetime
from flask import Flask, render_template

app = Flask(__name__)

birthdays = {
    "Alice": datetime.date(1990, 6, 4),
    "Bob": datetime.date(1985, 8, 22),
    "Charlie": datetime.date(1992, 12, 3)
}

def check_birthdays():
    today = datetime.date.today()
    upcoming_birthdays = []

    for name, birthday in birthdays.items():
        if (birthday.month, birthday.day) == (today.month, today.day):
            upcoming_birthdays.append(name)

    return upcoming_birthdays

@app.route('/')
def upcoming_birthdays():
    upcoming = check_birthdays()
    if upcoming:
        message = f"It's {', '.join(upcoming)}'s birthday today!"
    else:
        message = "No birthdays today."

    return render_template('birthday.html', message=message)

if __name__ == '__main__':
    app.run(debug=True)
