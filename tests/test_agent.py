from agent import AutoAgent
from memory import Memory
from tools import ToolRegistry, ToolResult


def test_memory_store_and_recall() -> None:
    mem = Memory()
    mem.store("action1", "result1")
    mem.store("action2", "result2")
    entries = mem.recall(limit=2)
    assert len(entries) == 2
    assert entries[-1].action == "action2"


def test_memory_completed_steps() -> None:
    mem = Memory()
    mem.mark_completed("step1")
    assert "step1" in mem.completed_steps
    mem.mark_completed("step1")  # no duplicate
    assert mem.completed_steps.count("step1") == 1


def test_tool_decompose() -> None:
    registry = ToolRegistry()
    result = registry.run("decompose", goal="Build a website")
    assert result.success
    assert isinstance(result.output, list)
    assert len(result.output) > 0


def test_tool_unknown() -> None:
    registry = ToolRegistry()
    result = registry.run("nonexistent_tool")
    assert not result.success


def test_agent_run_completes() -> None:
    agent = AutoAgent(name="TestAgent", goal="Test goal", max_iterations=20)
    status = agent.run()
    assert status == "completed"
