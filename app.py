from flask import Flask, render_template, request, jsonify, session
from groq import Groq
from dotenv import load_dotenv
import os
import json

load_dotenv()

app = Flask(__name__)
app.secret_key = "mock_interviewer_secret"

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

@app.route("/")
def home():
    session.clear()
    return render_template("index.html")

@app.route("/get_question", methods=["POST"])
def get_question():
    data = request.json
    tech_stack = data.get("tech_stack")
    difficulty = data.get("difficulty")
    
    prompt = f"""You are a technical interviewer. Generate 1 interview question for someone who knows: {tech_stack}.
    Difficulty: {difficulty}.
    Return ONLY a JSON object like this:
    {{"question": "your question here", "topic": "topic name"}}"""
    
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )
    text = response.choices[0].message.content.strip().replace("```json","").replace("```","")
    return jsonify(json.loads(text))

@app.route("/evaluate", methods=["POST"])
def evaluate():
    data = request.json
    question = data.get("question")
    answer = data.get("answer")
    
    prompt = f"""You are a technical interviewer. Evaluate this answer:
    Question: {question}
    Student's Answer: {answer}
    
    Return ONLY a JSON object like this:
    {{"score": 7, "out_of": 10, "good": "what was good", "missing": "what was missing", "ideal_answer": "brief ideal answer"}}"""
    
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )
    text = response.choices[0].message.content.strip().replace("```json","").replace("```","")
    return jsonify(json.loads(text))

if __name__ == "__main__":
    app.run(debug=True)