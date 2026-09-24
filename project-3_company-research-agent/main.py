from workflow import app

result = app.invoke({"company": "Adidas", "research_data": "", "report": ""})
print(result["report"])
