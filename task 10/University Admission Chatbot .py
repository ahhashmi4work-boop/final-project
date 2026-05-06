from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

responses = {
    "admission requirements": "You need FSC/A-Levels with at least 60% marks, entry test, and required documents.",
    "deadline": "Admissions usually close on August 15.",
    "programs": "We offer BSCS, BBA, BSE, and MBA programs.",
    "fee": "The fee is approximately PKR 120,000 per semester.",
    "contact": "Email: admissions@university.edu"
}

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get", methods=["POST"])
def chatbot_response():
    data = request.get_json(silent=True) or {}
    user_input = data.get("message", "").lower()

    for key in responses:
        if key in user_input:
            return jsonify({"reply": responses[key]})

    return jsonify({"reply": "Sorry, I didn't understand. Ask about admissions, deadlines, or programs."})

if __name__ == "__main__":
    app.run(debug=True)