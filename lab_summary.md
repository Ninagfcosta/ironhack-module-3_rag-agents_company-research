# Lab Summary

After analyzing the n8n workflows, the most useful nodes were the **AI Agent**, 
**OpenAI (Message a model)**, and **Schedule Trigger** nodes. The AI Agent node 
orchestrates reasoning between the LLM, memory, and external tools — making it 
the core of any intelligent automation. To pick the right node for a task, I ask: 
"Does this need to think (AI Agent), call an API (HTTP Request / OpenAI), 
transform data (Edit Fields), or trigger on time (Schedule Trigger)?" Each answer 
points to a different node. My top debugging tip is to click on any node after 
execution and carefully compare the **Input and Output panels** — most errors 
happen when a field name in the JSON does not match what the next node expects, 
for example `$json.output[0].content[0].text` must match exactly.