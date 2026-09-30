from src.agent.tools import create_tool_registry


def main() -> None:
    registry = create_tool_registry()

    print("\nREGISTERED TOOLS")
    print("-------------------------")

    for tool in registry.list_tools():
        print(f"- {tool}")


if __name__ == "__main__":
    main()