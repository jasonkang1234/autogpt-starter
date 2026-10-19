import argparse
import logging
from agent import AutoAgent

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="AutoGPT-style Autonomous Agent")
    parser.add_argument("--goal", type=str, required=True, help="The goal for the agent to achieve")
    parser.add_argument("--name", type=str, default="Agent-1", help="Agent name")
    parser.add_argument("--max-iter", type=int, default=10, help="Max iterations")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    agent = AutoAgent(name=args.name, goal=args.goal, max_iterations=args.max_iter)
    status = agent.run()
    print(f"Agent finished with status: {status}")


if __name__ == "__main__":
    main()
