# n8n Node Reference Table

| Node | Parameters | Settings | What It Does | JSON Input | JSON Output | Key Transformations |
|------|------------|----------|--------------|------------|-------------|---------------------|
| Manual Trigger | None | None | Starts the workflow execution manually when user clicks Execute | None | `[{}]` | No transformation — just starts the flow |
| Edit Fields (Set) | Assignments (field name + value pairs) | Include Other Input Fields | Transforms and renames fields in the JSON data | `[{}]` | Modified JSON with new field names/values | Extracts `$json.output[0].content[0].text` and maps it to `Daily News` field |
| Schedule Trigger | Trigger At Hour (7am), Interval | None | Starts the workflow automatically at a set time every day | None | `[{}]` | No transformation — triggers at 7am daily |
| OpenAI (Message a model) | Model (gpt-5.4-mini), Messages (system + user), Built-in Tools (webSearch) | Options | Calls OpenAI API with a prompt and returns AI-generated text with web search | Prompt text | JSON with `output` array containing `content[0].text` | Text prompt → AI response with web search results |
| Send an Email | To, Subject, Body, Options | None | Sends an email with the workflow output data | JSON with email content fields | Email sent confirmation | JSON data → outbound email |
| Chat Trigger | Options | Webhook ID | Receives a chat message from the n8n chat interface and starts the workflow | User chat message | `{ action, sessionId, chatInput }` | Incoming chat message → n8n JSON format |
| AI Agent | Options | None | Orchestrates LLM reasoning with tools and memory to answer complex questions | `{ chatInput }` | `{ output }` with agent response | Routes between LLM, memory and tools to build a final answer |
| OpenAI Chat Model | Model (gpt-5.4-mini), Built-in Tools, Options | None | Provides the language model brain to the AI Agent node | Agent reasoning request | LLM text response | Powers the AI Agent's reasoning capability |
| Simple Memory | Context Window Length (10) | None | Stores the last 10 messages so the AI Agent remembers the conversation | Conversation history | Last N messages as context | Keeps conversation context within a sliding window of 10 messages |
| MCP Client | Endpoint URL, Include Tools (search_docs_by_lang_chain), Options | None | Connects to an MCP server to give the AI Agent access to external tools | Agent tool request | Tool result from MCP server | AI Agent request → external MCP tool → result back to agent |
| Notion (Create a page) | Page ID (URL mode), Options | Notion API credential | Creates a new page in Notion with the workflow output data | JSON with page content | Notion API response with created page data | n8n JSON data → new Notion page |