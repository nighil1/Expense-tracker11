from flask import Flask, render_template, request, redirect
import statistics

app = Flask(__name__)

income = 0
expenses = []
descriptions = []

@app.route("/", methods=["GET","POST"])
def dashboard():
    global expenses, descriptions, income

    if request.method == "POST":
        amount = int(request.form["amount"])
        desc = request.form["description"]

        expenses.append(amount)
        descriptions.append(desc)

    total_expense = sum(expenses)

    # AI Prediction
    if len(expenses) > 0:
        prediction = round(statistics.mean(expenses),2)
    else:
        prediction = 0

    # AI Feedback
    if total_expense > income*0.8 and income != 0:
        feedback = "Warning: Your expenses are very close to your income."
    else:
        feedback = "Your spending is currently under control."

    # Dummy chart data
    income_data = [income, income, income, income, income, income]
    expense_data = [sum(expenses)//6]*6 if expenses else [0,0,0,0,0,0]

    categories = descriptions
    amounts = expenses

    return render_template("dashboard.html",
                           income=income,
                           expense=total_expense,
                           feedback=feedback,
                           prediction=prediction,
                           income_data=income_data,
                           expense_data=expense_data,
                           categories=categories,
                           amounts=amounts)

@app.route("/add_income", methods=["POST"])
def add_income():
    global income
    income += int(request.form["income"])
    return redirect("/")

app.run(debug=True)
