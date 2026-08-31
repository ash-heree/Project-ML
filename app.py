from flask import Flask, render_template, request, redirect, session, flash
import pandas as pd
import joblib
import mysql.connector
from datetime import datetime

# ==========================================
# Flask App
# ==========================================

app = Flask(__name__)
app.secret_key = "transaction_risk_analysis"

# ==========================================
# MySQL Connection
# ==========================================

try:
    db = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="Lenoir003))",
        database="transaction_risk_analysis"
    )
    cursor = db.cursor()
    print("Database connection established successfully")
except mysql.connector.Error as err:
    print(f"Database connection error: {err}")
    raise

# ==========================================
# Load Machine Learning Files
# ==========================================

try:
    model = joblib.load("models/risk_model.pkl")
    label_encoders = joblib.load("models/label_encoders.pkl")
    feature_columns = joblib.load("models/feature_columns.pkl")

    print("=" * 60)
    print("Machine Learning Model Loaded Successfully")
    print("=" * 60)
except FileNotFoundError as err:
    print(f"Error loading model files: {err}")
    raise
# ==========================================
# Home
# ==========================================

@app.route("/")
def home():
    return redirect("/login")


# ==========================================
# Login
# ==========================================

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        if username == "admin" and password == "admin":

            session["username"] = username

            return redirect("/dashboard")

        return render_template(
            "login.html",
            error="Invalid Username or Password"
        )

    return render_template("login.html")
# ==========================================
# Dashboard
# ==========================================

@app.route("/dashboard")
def dashboard():

    if "username" not in session:
        return redirect("/login")

    # Dashboard Statistics
    cursor.execute("SELECT COUNT(*) FROM transactions")
    total = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM transactions WHERE predicted_risk='High'")
    high = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM transactions WHERE predicted_risk='Medium'")
    medium = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM transactions WHERE predicted_risk='Low'")
    low = cursor.fetchone()[0]

    # Recent Transactions
    cursor.execute("""
        SELECT
            id,
            transaction_amount,
            location,
            predicted_risk,
            prediction_time
        FROM transactions
        ORDER BY id DESC
        LIMIT 5
    """)

    recent_transactions = cursor.fetchall()

    return render_template(
        "dashboard.html",
        username=session["username"],
        total=total,
        high=high,
        medium=medium,
        low=low,
        recent_transactions=recent_transactions
    )
# ==========================================
# New Transaction
# ==========================================

@app.route("/new_transaction")
def new_transaction():

    if "username" not in session:
        return redirect("/login")

    return render_template("new_transaction.html")
# ==========================================
# Predict Transaction
# ==========================================

@app.route("/predict", methods=["POST"])
def predict():

    if "username" not in session:
        return redirect("/login")

    # Get Form Values
    customer_age = int(request.form["customer_age"])
    customer_gender = request.form["customer_gender"]
    account_balance = float(request.form["account_balance"])
    account_age_months = int(request.form["account_age_months"])

    transaction_amount = float(request.form["transaction_amount"])
    average_transaction_amount = float(request.form["average_transaction_amount"])

    time_period = request.form["time_period"]
    location = request.form["location"]
    payment_method = request.form["payment_method"]
    device_type = request.form["device_type"]
    merchant_category = request.form["merchant_category"]

    daily_transaction_count = int(request.form["daily_transaction_count"])
    weekly_transaction_count = int(request.form["weekly_transaction_count"])

    distance_from_home_km = float(request.form["distance_from_home"])

    login_attempts = int(request.form["login_attempts"])
    failed_transactions_last_24h = int(request.form["failed_transactions"])

    new_device = request.form["new_device"]
    international_transaction = request.form["international_transaction"]
    card_present = request.form["card_present"]

    ip_risk_score = int(request.form["ip_risk_score"])

    now = datetime.now()

    transaction_day = now.day
    transaction_month = now.month
    transaction_hour = now.hour

    input_data = {
        "Customer_Age": customer_age,
        "Customer_Gender": customer_gender,
        "Account_Balance": account_balance,
        "Account_Age_Months": account_age_months,
        "Transaction_Amount": transaction_amount,
        "Average_Transaction_Amount": average_transaction_amount,
        "Time_Period": time_period,
        "Location": location,
        "Payment_Method": payment_method,
        "Device_Type": device_type,
        "Merchant_Category": merchant_category,
        "Daily_Transaction_Count": daily_transaction_count,
        "Weekly_Transaction_Count": weekly_transaction_count,
        "Distance_From_Home_KM": distance_from_home_km,
        "Login_Attempts": login_attempts,
        "Failed_Transactions_Last_24H": failed_transactions_last_24h,
        "New_Device": new_device,
        "International_Transaction": international_transaction,
        "Card_Present": card_present,
        "IP_Risk_Score": ip_risk_score,
        "Transaction_Day": transaction_day,
        "Transaction_Month": transaction_month,
        "Transaction_Hour": transaction_hour
    }

    df = pd.DataFrame([input_data])
    # ==========================================
    # Encode Categorical Columns
    # ==========================================

    for column in df.columns:

        if column in label_encoders:

            try:
                df[column] = label_encoders[column].transform(df[column])

            except Exception as e:
                print(f"Warning: Could not encode {column}: {e}")
                df[column] = 0

    # Arrange Columns
    df = df[feature_columns]

    # ==========================================
    # Predict Risk
    # ==========================================

    prediction = model.predict(df)[0]

    if prediction == 0:
        predicted_risk = "Low"

    elif prediction == 1:
        predicted_risk = "Medium"

    else:
        predicted_risk = "High"

    prediction_date = now.strftime("%Y-%m-%d")
    prediction_time = now.strftime("%H:%M:%S")

    # ==========================================
    # Save Prediction into MySQL
    # ==========================================

    sql = """
    INSERT INTO transactions
    (
        customer_age,
        customer_gender,
        account_balance,
        account_age_months,
        transaction_amount,
        average_transaction_amount,
        location,
        payment_method,
        device_type,
        merchant_category,
        daily_transaction_count,
        weekly_transaction_count,
        distance_from_home_km,
        login_attempts,
        failed_transactions_last_24h,
        new_device,
        international_transaction,
        card_present,
        ip_risk_score,
        predicted_risk,
        prediction_date,
        prediction_time
    )
    VALUES
    (
        %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,
        %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s
    )
    """

    values = (
        customer_age,
        customer_gender,
        account_balance,
        account_age_months,
        transaction_amount,
        average_transaction_amount,
        location,
        payment_method,
        device_type,
        merchant_category,
        daily_transaction_count,
        weekly_transaction_count,
        distance_from_home_km,
        login_attempts,
        failed_transactions_last_24h,
        new_device,
        international_transaction,
        card_present,
        ip_risk_score,
        predicted_risk,
        prediction_date,
        prediction_time
    )

    cursor.execute(sql, values)
    db.commit()

    return render_template(
        "result.html",
        risk_level=predicted_risk
    )
# ==========================================
# Prediction History
# ==========================================

@app.route("/history")
def history():

    if "username" not in session:
        return redirect("/login")

    cursor.execute("""
        SELECT
            id,
            customer_age,
            customer_gender,
            transaction_amount,
            payment_method,
            location,
            predicted_risk,
            prediction_date,
            prediction_time
        FROM transactions
        ORDER BY id DESC
    """)

    records = cursor.fetchall()

    return render_template(
        "history.html",
        username=session["username"],
        records=records
    )


# ==========================================
# Reports
# ==========================================

@app.route("/reports")
def reports():

    if "username" not in session:
        return redirect("/login")

    return render_template("reports.html")


# ==========================================
# Logout
# ==========================================

@app.route("/logout")
def logout():

    session.clear()
    flash("Logged out successfully", "success")

    return redirect("/login")


# ==========================================
# Run Flask
# ==========================================

if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True,
        use_reloader=False
    )