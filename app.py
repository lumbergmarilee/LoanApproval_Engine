import os
from flask import Flask, request, jsonify, render_template
from Loan_Approval_Engine import loan_approval_algorithm

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__, template_folder=BASE_DIR, static_folder=BASE_DIR, static_url_path="")


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/loan-decision", methods=["POST"])
def loan_decision():
    data = request.get_json()

    if not data:
        return jsonify({"error": "Request body is required"}), 400

    personal_code = data.get("personalCode")
    loan_amount = data.get("loanAmount")
    loan_period = data.get("loanPeriod")

    if personal_code is None or loan_amount is None or loan_period is None:
        return jsonify({"error": "personalCode, loanAmount, and loanPeriod are required"}), 400

    try:
        personal_code = int(personal_code)
        loan_amount = float(loan_amount)
        loan_period = int(loan_period)
    except (ValueError, TypeError):
        return jsonify({"error": "Invalid parameter types"}), 400

    if loan_amount < 2000 or loan_amount > 10000:
        return jsonify({"error": "Loan amount must be between €2,000 and €10,000"}), 400

    result = loan_approval_algorithm(personal_code, loan_amount, loan_period)
    decision = result[0]
    response = {"decision": decision}

    if decision == "positive" and len(result) >= 3:
        response["approvedAmount"] = result[1]
        response["approvedPeriod"] = result[2]
        if result[2] != loan_period:
            response["note"] = f"Original period of {loan_period} months was not possible. Adjusted to {result[2]} months."
        if result[1] != loan_amount:
            note = response.get("note", "")
            response["note"] = (note + f" Maximum approved amount is €{result[1]:,.0f} for this period.").strip()
    elif decision == "negative":
        if len(result) >= 2 and isinstance(result[1], str):
            response["reason"] = result[1]
        else:
            response["reason"] = "No suitable loan offer could be found for this applicant."

    return jsonify(response)


if __name__ == "__main__":
    app.run(debug=True, port=5000)