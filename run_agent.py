import sys
from workflow import app

company = sys.argv[1]
result = app.invoke({"company": company, "research_data": "", "report": ""})
print(result["report"])