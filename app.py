from flask import Flask, render_template, request, flash, redirect
from flask_mail import Mail, Message

from models import db, Form

from datetime import datetime

app = Flask(__name__)

app.config["SECRET_KEY"] = "mycabbooking123"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///cab_data.db"
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 465
app.config["MAIL_USE_SSL"] = True
app.config["MAIL_USERNAME"] = "vinovijayan@gmail.com"
app.config["MAIL_PASSWORD"] = "ekyvqmcykprdubjx"

db.init_app(app)

mail = Mail(app)


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/book_cab", methods=['GET', 'POST'])
def book_cab():
    entries = []

    if request.method == "POST":
        name = request.form["name"].title()
        mobile = request.form["mobile"]
        email = request.form["email"]
        pickup = request.form["from"].upper()
        drop = request.form["to"].upper()
        date = request.form["date"]
        date_obj = datetime.strptime(date, "%Y-%m-%d")
        formated_date = date_obj.strftime("%d-%B-%Y")
        time = request.form["time"]
        time_obj = datetime.strptime(time, "%H:%M").time()
        formated_time = time_obj.strftime("%I:%M %p")
        vehicle = request.form["vehicle"].title()

        form = Form(name=name, mobile=mobile, email=email,
                    pickup=pickup, drop=drop, date=date_obj, time=time_obj, vehicle=vehicle)

        entries.append(form)
        db.session.add(form)
        db.session.commit()

        message_body = f"Hi, {name}, your cab has been booked.\n\n" \
                       f"Here are your cab booking data:\n\n Name: {name}\n\n Mobile No. {mobile}\n\n From: {pickup}\n\n" \
                       f"To: {drop}\n\n Date: {date}\n\n Time: {time} hrs\n\n Type of cab: {vehicle}.\n\n" \
                       f"You will be receiving confirmation message from Garden City Cabs shortly.\n\n\n" \
                       f"Thank you.\n\n Vinod\n\n\n" \
                       f"This is automatically generated email please do not reply"

        message = Message(subject=f"Cab request {name}",
                          sender=app.config["MAIL_USERNAME"],
                          recipients=[email],
                          body=message_body)
        mail.send(message)

        flash(f"{name}, your cab booking request submitted successfully!", "success")

        with open("output/booking.txt", 'w') as file:
            lines = [
                "cab requirement: laminaar aviation infotech (india) private limited",
                "please provide cab as per the details below: ",
                "name: "+ name,
                "from: "+ pickup,
                "to: "+ drop,
                f"date: {formated_date}",
                f"time:  {time}  hrs, ({formated_time})",
                "vehicle: "+ vehicle,
                "contact: "+ mobile,
                "please confirm cab booking.",
                "thanks!"
            ]

            for line in lines:
                file.write(line.upper() + '\n')
                file.write('\n')

    return render_template("book_cab.html", entries=entries)


# set the number of records per page
BOOKINGS_PER_PAGE = 10


@app.route("/list")
def booking_list():
    # Get the page number from the query parameters, default to 1
    page = request.args.get('page', 1, type=int)

    # Retrieve the total number of records
    total_bookings = Form.query.count()

    # Calculate the total number of pages
    total_pages = (total_bookings // BOOKINGS_PER_PAGE) + (1 if total_bookings % BOOKINGS_PER_PAGE != 0 else 0)

    # Retrieve the subset of records for the current page
    bookings = Form.query.paginate(page=page, per_page=BOOKINGS_PER_PAGE)

    return render_template('list.html', bookings=bookings, total_pages=total_pages)


@app.route('/search', methods=['GET', 'POST'])
def search():
    bookings = Form.query.all()
    if request.method == 'POST':
        search_query = request.form['search_query']
        matching_records = Form.query.filter(Form.name.ilike(f"%{search_query}%")).all()
        return render_template('search.html', bookings=matching_records)
    return render_template('list.html', bookings=bookings)


@app.route("/booking/<int:booking_id>")
def booking_detail(booking_id):
    booking = Form.query.filter_by(id=booking_id).first()
    if booking:
        return render_template("booking_detail.html", booking=booking)
    return f"Cab booking details not available."

@app.route("/update/<int:booking_id>", methods=["GET", "POST"])
def booking_update(booking_id):
    booking = Form.query.filter_by(id=booking_id).first()
    if request.method == 'POST':
        if booking:
            db.session.delete(booking)
            db.session.commit()

            name = request.form["name"].title()
            mobile = request.form["mobile"]
            email = request.form["email"]
            pickup = request.form["from"].upper()
            drop = request.form["to"].upper()
            date = request.form["date"]
            date_obj = datetime.strptime(date, "%Y-%m-%d")
            time = request.form["time"]
            time_obj = datetime.strptime(time, "%H:%M").time()
            vehicle = request.form["vehicle"]

            booking = Form(name=name, mobile=mobile, email=email, pickup=pickup, drop=drop,
                           date=date_obj, time=time_obj, vehicle=vehicle)

            db.session.add(booking)
            db.session.commit()
            return redirect("/list")

        return f"Booking details doesn't exist."

    return render_template("update.html", booking=booking)


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        app.run(debug=True, port=5001)
