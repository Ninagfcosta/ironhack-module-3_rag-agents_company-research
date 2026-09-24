from flask import Flask, request, jsonify
from workflow import app as agent_app

app = Flask(__name__)

@app.route("/research", methods=["GET"])
def research():
    company = request.args.get("company", "Tesla")
    result = agent_app.invoke({"company": company, "research_data": "", "report": ""})
    return jsonify({"report": result["report"]})

if __name__ == "__main__":
    app.run(port=5000)