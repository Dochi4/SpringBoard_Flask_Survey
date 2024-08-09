from flask import Flask, request, render_template, redirect, flash
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "surveytime"
debug = DebugToolbarExtension(app)

responses = []

app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

@app.context_processor
def inject_survey():
    return dict(survey=survey)

@app.route('/')
def home_page():
    return render_template("start.html",  survey=survey )



@app.route('/questions/<int:question_id>', methods=["GET", "POST"])
def show_question(question_id):
    if question_id < 0 or question_id >= len(survey.questions):
        flash("Invalid question ID.")
        return redirect('/thank_you')

    if question_id < len(responses):
        flash("You’ve already answered this question.")
        return redirect('/thank_you')

    if request.method == "POST":
        choice = request.form['answer']
        responses.append(choice)
        if len(responses) == len(survey.questions):
            return redirect("/thank_you")
        else:
            return redirect(f"/questions/{len(responses)}")

    question = survey.questions[question_id]
    return render_template('questions.html', question=question, question_id=question_id)
    
@app.route("/thank_you")
def thank_you():
    return render_template("thank_you.html")