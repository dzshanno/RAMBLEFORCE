# Flask backend to handle registrations, tickets, and comments
from flask import Flask, request, jsonify, render_template
import stripe
import boto3
import os

app = Flask(__name__)

# Stripe configuration
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

# AWS S3 configuration
s3 = boto3.client("s3")
S3_BUCKET = os.getenv("S3_BUCKET")


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/register", methods=["POST"])
def register():
    data = request.json
    # Store registration details (e.g., in a database)
    # For now, just return the received data
    return jsonify({"message": "Registration successful", "data": data})


@app.route("/create-checkout-session", methods=["POST"])
def create_checkout_session():
    try:
        # Create a Stripe checkout session for ticket purchase
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[
                {
                    "price_data": {
                        "currency": "usd",
                        "product_data": {
                            "name": "Rambleforce Ticket",
                        },
                        "unit_amount": 50,
                    },
                    "quantity": 1,
                },
            ],
            mode="payment",
            success_url="https://yourdomain.com/success",
            cancel_url="https://yourdomain.com/cancel",
        )
        return jsonify({"id": session.id})
    except Exception as e:
        return jsonify(error=str(e)), 500


@app.route("/upload-photo", methods=["POST"])
def upload_photo():
    file = request.files["file"]
    s3.upload_fileobj(file, S3_BUCKET, file.filename)
    return jsonify({"message": "Photo uploaded successfully"})


if __name__ == "__main__":
    app.run(debug=True)
