import logging
from dataclasses import dataclass, field
from typing import List, Optional
from memory import Memory
from tools import ToolRegistry, ToolResult

logger = logging.getLogger(__name__)


@dataclass
class Task:
    goal: str
    steps: List[str] = field(default_factory=list)
    completed: bool = False


class AutoAgent:
    """Autonomous agent that decomposes goals into steps and executes them using tools."""

    def __init__(self, name: str, goal: str, max_iterations: int = 10) -> None:
        self.name = name
        self.goal = goal
        self.max_iterations = max_iterations
        self.memory = Memory()
        self.tools = ToolRegistry()
        self.task = Task(goal=goal)
        self._iteration = 0

    def think(self) -> Optional[str]:
        """Determine the next action based on goal and memory."""
        context = self.memory.recall(limit=5)
        logger.info("[%s] Thinking... context: %s", self.name, context)
        if not self.task.steps:
            return f"decompose:{self.goal}"
        for step in self.task.steps:
            if step not in self.memory.completed_steps:
                return f"execute:{step}"
        return None

    def act(self, action: str) -> ToolResult:
        """Execute an action using the tool registry."""
        if action.startswith("decompose:"):
            goal = action.split(":", 1)[1]
            self.task.steps = self.tools.run("decompose", goal=goal).output
            return ToolResult(tool="decompose", output=self.task.steps, success=True)
        elif action.startswith("execute:"):
            step = action.split(":", 1)[1]
            result = self.tools.run("execute", step=step)
            if result.success:
                self.memory.mark_completed(step)
            return result
        return ToolResult(tool="unknown", output="Unknown action", success=False)

    def run(self) -> str:
        """Main agent loop."""
        logger.info("[%s] Starting. Goal: %s", self.name, self.goal)
        while self._iteration < self.max_iterations:
            self._iteration += 1
            action = self.think()
            if action is None:
                self.task.completed = True
                logger.info("[%s] Goal completed in %d iterations.", self.name, self._iteration)
                break
            logger.info("[%s] Iteration %d — action: %s", self.name, self._iteration, action)
            result = self.act(action)
            self.memory.store(action, result)
        return "completed" if self.task.completed else "max_iterations_reached"
