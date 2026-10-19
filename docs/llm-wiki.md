# LLM Wiki — AutoGPT Starter

## Table of Contents
1. [What is an LLM Agent?](#1-what-is-an-llm-agent)
2. [AutoGPT Architecture](#2-autogpt-architecture)
3. [Prompt Engineering](#3-prompt-engineering)
4. [Memory Systems](#4-memory-systems)
5. [Tool Use & Function Calling](#5-tool-use--function-calling)
6. [LLM Agent Frameworks](#6-llm-agent-frameworks)
7. [Popular LLMs for Agents](#7-popular-llms-for-agents)
8. [Safety & Limitations](#8-safety--limitations)
9. [Key Concepts Glossary](#9-key-concepts-glossary)
10. [Further Reading](#10-further-reading)

---

## 1. What is an LLM Agent?

An **LLM Agent** is an autonomous system that uses a Large Language Model as its reasoning engine to plan, decide, and act in order to complete a goal — without requiring a human to specify every step.

### Agent vs Plain LLM

| | Plain LLM | LLM Agent |
|---|---|---|
| Input | Single prompt | Goal + memory + tool results |
| Output | Single response | Actions in a loop |
| Iteration | One-shot | Multi-step (think → act → observe) |
| Memory | None (stateless) | Short-term + long-term |
| Tools | None | Web search, code execution, APIs |
| Autonomy | Zero | High |

---

## 2. AutoGPT Architecture

AutoGPT (released March 2023) was one of the first widely-used autonomous LLM agents. This repo implements the same core loop in pure Python.

```
┌─────────────────────────────────────────────────────┐
│                   Agent Loop                        │
│                                                     │
│  Goal ──► Think (LLM prompt) ──► Action             │
│              ▲                      │               │
│              │                      ▼               │
│           Memory ◄────────── Observation            │
│                                                     │
│  Repeat until: goal completed | max iterations      │
└─────────────────────────────────────────────────────┘
```

### The ReAct Pattern
Most LLM agents follow **ReAct** (Reason + Act):
1. **Reason** — LLM thinks step-by-step about what to do next
2. **Act** — LLM outputs a structured action (tool call)
3. **Observe** — Tool result is fed back into the LLM context
4. **Repeat** until done

```
Thought: I need to search for recent papers on ViT.
Action: search("vision transformer 2024 papers")
Observation: [search results...]
Thought: I found 3 relevant papers. I should summarise them.
Action: write_file("summary.md", ...)
Observation: File written successfully.
Thought: Task complete.
```

---

## 3. Prompt Engineering

The quality of an LLM agent depends heavily on how you prompt the LLM. Key techniques:

### System Prompt (Agent Identity)
```
You are an autonomous AI agent named {name}.
Your goal is: {goal}
You have access to the following tools: {tool_list}
Always respond in JSON: {"thought": "...", "action": "tool_name", "args": {...}}
```

### Chain-of-Thought (CoT)
Force the LLM to reason before acting:
```
Before taking any action, think step by step:
1. What is the current state?
2. What is the goal?
3. What is the best next action?
```

### Few-Shot Examples
Provide 2–3 examples of good reasoning in the prompt to guide the LLM's output format.

### Structured Output
Use JSON schema to enforce a parseable response:
```python
response_schema = {
    "thought": str,
    "action": str,   # tool name
    "args": dict,    # tool arguments
    "done": bool     # True if goal is complete
}
```

---

## 4. Memory Systems

| Memory Type | Storage | Use Case |
|---|---|---|
| **In-context** | LLM prompt window | Recent actions, current task |
| **Short-term** | Python list / dict | Current session history |
| **Long-term** | Vector database (Chroma, Pinecone) | Knowledge across sessions |
| **Episodic** | File / DB per session | Replay past task runs |

### Vector Memory (Semantic Search)
```python
from chromadb import Client

client = Client()
collection = client.create_collection("agent_memory")

# Store
collection.add(documents=["I searched for X and found Y"], ids=["mem_1"])

# Recall relevant memories
results = collection.query(query_texts=["What did I find about X?"], n_results=3)
```

---

## 5. Tool Use & Function Calling

Modern LLMs (Claude, GPT-4, Gemini) support **native function calling** — the LLM outputs a structured JSON tool call instead of plain text.

### Anthropic Claude Tool Use
```python
import anthropic

client = anthropic.Anthropic()
tools = [{
    "name": "search",
    "description": "Search the web",
    "input_schema": {
        "type": "object",
        "properties": {"query": {"type": "string"}},
        "required": ["query"]
    }
}]

response = client.messages.create(
    model="claude-sonnet-5",
    max_tokens=1024,
    tools=tools,
    messages=[{"role": "user", "content": "Find the latest AutoGPT release"}]
)
# response.content[0].type == "tool_use"
```

### OpenAI Function Calling
```python
from openai import OpenAI
client = OpenAI()

response = client.chat.completions.create(
    model="gpt-4o",
    tools=[{"type": "function", "function": {"name": "search", "parameters": {...}}}],
    messages=[{"role": "user", "content": "Search for AutoGPT"}]
)
```

---

## 6. LLM Agent Frameworks

| Framework | Language | Notes |
|---|---|---|
| **AutoGPT** | Python | Original autonomous agent, plugin system |
| **LangChain** | Python / JS | Chains, agents, memory, RAG |
| **LangGraph** | Python | Graph-based multi-agent workflows |
| **CrewAI** | Python | Role-based multi-agent teams |
| **AutoGen** | Python | Microsoft; conversational multi-agent |
| **Semantic Kernel** | Python / C# / Java | Microsoft; enterprise-focused |
| **Claude Agent SDK** | Python | Anthropic's native agent framework |

---

## 7. Popular LLMs for Agents

| Model | Provider | Strengths for Agents |
|---|---|---|
| **Claude Sonnet 5** | Anthropic | Long context (200K), strong reasoning, native tool use |
| **GPT-4o** | OpenAI | Fast, multimodal, function calling |
| **Gemini 1.5 Pro** | Google | 1M context window, multimodal |
| **Llama 3** | Meta | Open source, self-hostable |
| **Mistral Large** | Mistral AI | European, strong at code |

---

## 8. Safety & Limitations

| Risk | Mitigation |
|---|---|
| **Prompt injection** | Sanitise tool outputs before feeding back to LLM |
| **Infinite loops** | Always enforce `max_iterations` (done in this repo) |
| **Destructive actions** | Require human confirmation for irreversible tools |
| **Hallucinated tool calls** | Validate tool name and args against schema before executing |
| **Cost runaway** | Track token usage per iteration; set hard budget |

---

## 9. Key Concepts Glossary

| Term | Definition |
|---|---|
| **Agent** | An LLM system that autonomously takes actions to achieve a goal |
| **ReAct** | Reason + Act — the standard agent loop pattern |
| **Tool / Function** | An external capability the LLM can call (search, code exec, API) |
| **Orchestrator** | The controller that manages the agent loop and calls the LLM |
| **Context window** | Maximum tokens the LLM can see at once |
| **RAG** | Retrieval-Augmented Generation — grounding agent responses with retrieved docs |
| **Multi-agent** | Multiple LLM agents collaborating, each with a specialised role |
| **Guardrails** | Rules preventing the agent from taking harmful actions |

---

## 10. Further Reading

- [AutoGPT GitHub](https://github.com/Significant-Gravitas/AutoGPT)
- [ReAct: Synergizing Reasoning and Acting in Language Models](https://arxiv.org/abs/2210.03629)
- [Toolformer: Language Models Can Teach Themselves to Use Tools](https://arxiv.org/abs/2302.04761)
- [LangChain documentation](https://docs.langchain.com)
- [Anthropic Claude tool use guide](https://docs.anthropic.com/en/docs/tool-use)
- [AutoGen (Microsoft)](https://github.com/microsoft/autogen)
