import datetime
import json
from typing import Any, List

from langchain import PromptTemplate, LLMChain
from langchain.llms import OpenAI
from langchain.schema import Document
from langchain.tools import BaseTool
from langchain.retrievers import ContextualCompressionRetriever, RouterRetriever
from langchain.vectorstores import PGVector

from app.database import SessionLocal
from app.models.database_models import Task as TaskModel, ChatHistory as ChatHistoryModel, ChatStyle as ChatStyleModel, User as UserModel
from sqlalchemy.orm import Session

def get_task_retriever(vectorstore: PGVector) -> ContextualCompressionRetriever:
    base = vectorstore.as_retriever(search_kwargs={"filter": {"status": "lagging"}, "k": 5})
    return ContextualCompressionRetriever(base_retriever=base, compressor=None)

def get_chat_retriever(vectorstore: PGVector) -> ContextualCompressionRetriever:
    base = vectorstore.as_retriever(search_kwargs={"k": 10})
    return ContextualCompressionRetriever(base_retriever=base, compressor=None)

def get_router_retriever(vectorstore: PGVector) -> RouterRetriever:
    task_ret = get_task_retriever(vectorstore)
    chat_ret = get_chat_retriever(vectorstore)
    return RouterRetriever(retrievers={"task": task_ret, "chat": chat_ret}, metadata_key="type")

class UpdateTaskTool(BaseTool):
    name = "update_task"
    description = (
        "Update a task field in the database. "
        "Args (JSON): {task_id: int, field: str, value: Any}. "
        "Returns: JSON of updated task."
    )

    def _run(self, args_json: str) -> str:
        params = json.loads(args_json)
        task_id = params["task_id"]
        field = params["field"]
        value = params["value"]

        db: Session = SessionLocal()
        task = db.query(TaskModel).filter(TaskModel.id == task_id).first()
        setattr(task, field, value)
        db.commit()
        db.refresh(task)
        db.close()

        return json.dumps({
            "id": task.id,
            "user_id": task.user_id,
            "goal_id": task.goal_id,
            "name": task.name,
            "description": task.description,
            "priority": task.priority,
            "is_completed": task.is_completed
        })

    async def _arun(self, args_json: str) -> str:
        raise NotImplementedError("UpdateTaskTool does not support async")

# ---------------------- ACTIVE LISTENING ROLE PROMPT FRAMEWORK ----------------------

SYSTEM_TEMPLATE = """
You are EmotiTask, an intelligent AI emotional supporter that helps the user to manage their tasks while adapting to their personalities and caring for their emotional well-being.
Always use these tone keywords: {chat_style.keywords}
User's MBTI profile: {user_id}: {}
User's name: {user_name}
Current time: {now}

--- 
**Active Listening Techniques:**  
1. Paraphrasing: Rephrase what the user said to show understanding.  
2. Verbalizing Emotions: Directly express and acknowledge the user's emotions.  
3. Summarizing: Write a short and concise summary of the conversation so far.  
4. Encouraging: Praise the user when they share personal issues, especially difficult ones.

**Chain of Thought (CoT) Guidance:**  
When the user mentions an issue they're struggling with, guide them step-by-step:
- First, ask which aspect causes the most stress (e.g. fear of unpreparedness, performance pressure, etc.).  
- Then, once the source is identified, brainstorm concrete strategies to address it.

**Heuristic for Emotion Words:**  
When you detect words like “sad,” “frustrated,” “anxious,” “depressed,” or “disappointed,” always do all of the following:
1. Paraphrase their sentence to confirm you’ve understood.  
2. Verbalize your own empathetic response (“I can see this must feel…”).  
3. Summarize the main point to show clarity.  
4. Encourage them to open up, praise their bravery, or offer comfort.

--- 
"""

CONTEXT_TEMPLATE = """
### OPEN TASKS
{tasks_block}

### RECENT CHAT
{chat_block}
"""

INSTRUCTION_TEMPLATE = """
When a task is overdue or within 15 minutes, start with a friendly check-in using active listening.
Then suggest exactly one adjustment using the update_task tool.
Format tool call as JSON string.

Example:
{{"task_id":123,"field":"start_time","value":"2025-06-21T15:00:00"}}

Always finish with an empathic, encouraging closer that matches the active listening style.
"""

def build_rag_chain(llm_api_key: str, pgvector_url: str) -> LLMChain:
    llm = OpenAI(temperature=0.7, openai_api_key=llm_api_key)
    vectorstore = PGVector.from_connection_string(conn_str=pgvector_url, index_name="rag_index")
    retriever = get_router_retriever(vectorstore)
    update_tool = UpdateTaskTool()
    combined = SYSTEM_TEMPLATE + CONTEXT_TEMPLATE + INSTRUCTION_TEMPLATE
    prompt = PromptTemplate(
        template=combined,
        input_variables=["chat_style", "user_name", "now", "tasks_block", "chat_block"]
    )
    chain = LLMChain(
        llm=llm,
        prompt=prompt,
        verbose=True,
        callbacks=[],
        tools=[update_tool],
        retriever=retriever
    )
    return chain

def docs_to_block(docs: List[Document], header: str) -> str:
    lines = []
    for d in docs:
        if d.metadata.get("type") == "task":
            lines.append(f"- {d.page_content.splitlines()[0]} (id: {d.metadata.get('task_id')})")
        else:
            lines.append(d.page_content)
    return header + "\n" + "\n".join(lines)

# Usage example:
# chain = build_rag_chain(
#     llm_api_key="YOUR_OPENAI_API_KEY",
#     pgvector_url="postgresql://user:pass@host:port/dbname"
# )
# docs = chain.retriever.get_relevant_documents("") 
# tasks_block = docs_to_block([d for d in docs if d.metadata["type"]=="task"], "### OPEN TASKS")
# chat_block  = docs_to_block([d for d in docs if d.metadata["type"]=="chat"], "### RECENT CHAT")
# output = chain.run({
#     "chat_style": chat_style_obj,
#     "user_name": user.name,
#     "now": datetime.datetime.utcnow().isoformat(),
#     "tasks_block": tasks_block,
#     "chat_block": chat_block
# })
