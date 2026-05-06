from flask import Flask, render_template, request, redirect, url_for, session
from google import genai

app = Flask(__name__)
app.secret_key = "secret123"

# 🔑 Gemini client
client = genai.Client(api_key="AIzaSyBv2TeRv7gUFW5dsNv_9nxDvkFMzEQWltw")


# -----------------------------
# SAFE GEMINI CALL
# -----------------------------
def ask_ai(prompt):
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash-lite",
            contents=prompt
        )

        if response and response.text:
            return response.text.strip()

    except Exception as e:
        print("Gemini Error:", e)

    return "AI not available (check API / quota / model access)."


# -----------------------------
# HOME
# -----------------------------
@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        session["level"] = request.form.get("level")
        session["role"] = request.form.get("role")
        session["q_no"] = 0
        session["questions"] = []
        session["answers"] = []
        return redirect(url_for("interview"))

    return render_template("index.html")


# -----------------------------
# INTERVIEW FLOW
# -----------------------------
@app.route("/interview", methods=["GET", "POST"])
def interview():

    if "q_no" not in session:
        return redirect(url_for("home"))

    # Save answer
    if request.method == "POST":
        answer = request.form.get("answer")
        if answer:
            session["answers"].append(answer)
            session["q_no"] += 1

    # Stop after 5 questions
    if session["q_no"] >= 5:
        return redirect(url_for("result"))

    # Generate question
    if len(session["questions"]) <= session["q_no"]:
        prompt = f"""
        You are a strict technical interviewer.

        Generate ONE interview question.

        Level: {session['level']}
        Role: {session['role']}

        Only return the question.
        """

        question = ask_ai(prompt)
        session["questions"].append(question)
    else:
        question = session["questions"][session["q_no"]]

    return render_template(
        "interview.html",
        question=question,
        q_no=session["q_no"] + 1
    )


# -----------------------------
# RESULT ANALYSIS
# -----------------------------
@app.route("/result")
def result():

    questions = session.get("questions", [])
    answers = session.get("answers", [])

    qa = ""
    min_len = min(len(questions), len(answers))

    for i in range(min_len):
        qa += f"Q{i+1}: {questions[i]}\nA{i+1}: {answers[i]}\n"

    prompt = f"""
    Evaluate this interview:

    {qa}

    Return:
    Score out of 10
    Strengths
    Weaknesses
    Improvement Plan
    Final Verdict
    """

    feedback = ask_ai(prompt)

    return render_template("result.html", feedback=feedback)


if __name__ == "__main__":
    app.run(debug=True)