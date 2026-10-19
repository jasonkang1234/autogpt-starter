# AutoGPT Starter

A minimal, dependency-free AutoGPT-style autonomous agent in pure Python.
Inspired by [AutoGPT](https://github.com/Significant-Gravitas/AutoGPT) open source.

## Architecture

```
AutoAgent
  ├── Memory     — stores action/result history, tracks completed steps
  ├── ToolRegistry — pluggable tools (decompose, execute, search, write_file)
  └── Agent loop — think() → act() → store() until goal completed
```

## Usage

```bash
pip install -r requirements.txt
python main.py --goal "Research and summarise quantum computing"
python main.py --goal "Write a Python sorting algorithm" --name MyAgent --max-iter 20
```

## Extend with Real LLM

Replace the stubs in `tools.py` with actual LLM API calls:

```python
# tools.py — _tool_decompose
import anthropic
client = anthropic.Anthropic()
response = client.messages.create(
    model="claude-sonnet-5",
    max_tokens=512,
    messages=[{"role": "user", "content": f"Break this goal into 4 steps: {goal}"}]
)
```

## Run Tests

```bash
pytest
```

## License

MIT — inspired by AutoGPT open source.
