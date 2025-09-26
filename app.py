from flask import Flask, render_template, request, redirect, url_for
import json
import urllib.parse
import qrcode
from io import BytesIO
import base64

app = Flask(__name__)

# Load courses
with open('courses.json', 'r') as f:
    courses = json.load(f)

# Your WhatsApp number
WHATSAPP_NUMBER = "917890650560"

# Your UPI ID
UPI_ID = "9831677534@ybl"

@app.route("/", methods=["GET", "POST"])
def index():
    course_found = None
    amount = None
    error = None
    qr_base64 = None

    if request.method == "POST":
        if "search_course" in request.form:
            search_course = request.form.get("course_name")
            if search_course in courses:
                course_found = search_course
                amount = courses[search_course]

                # Generate UPI QR code without name
                upi_url = f"upi://pay?pa={UPI_ID}&am={amount}&cu=INR"
                qr = qrcode.QRCode(version=1, box_size=10, border=4)
                qr.add_data(upi_url)
                qr.make(fit=True)
                img = qr.make_image(fill="black", back_color="white")

                # Convert QR to base64
                buffer = BytesIO()
                img.save(buffer, format="PNG")
                qr_base64 = base64.b64encode(buffer.getvalue()).decode("utf-8")
            else:
                error = "Course not found!"

        elif "transaction_id" in request.form:
            # Redirect to WhatsApp
            full_name = request.form.get("full_name")
            father_name = request.form.get("father_name")
            course_name = request.form.get("course_name")
            amount = request.form.get("amount")
            transaction_id = request.form.get("transaction_id")

            message = f"Student Name: {full_name}\nFather's Name: {father_name}\nCourse: {course_name}\nAmount: ₹{amount}\nTransaction ID: {transaction_id}"
            url = f"https://wa.me/{WHATSAPP_NUMBER}?text={urllib.parse.quote(message)}"
            return redirect(url)

    return render_template("index.html", courses=courses.keys(),
                           course=course_found, amount=amount,
                           error=error, qr_base64=qr_base64)
                           
if __name__ == "__main__":
    app.run(debug=True)
