from typing import Any, Callable


class ToolRegistry:
    """Store and retrieve tools available to the AI agent."""

    def __init__(self) -> None:
        self._tools: dict[str, Callable[..., Any]] = {}

    def register(
        self,
        name: str,
        function: Callable[..., Any],
    ) -> None:
        """Register a tool."""

        if name in self._tools:
            raise ValueError(
                f"Tool already registered: {name}"
            )

        self._tools[name] = function

    def get(self, name: str) -> Callable[..., Any]:
        """Get a registered tool by name."""

        if name not in self._tools:
            raise KeyError(
                f"Tool not found: {name}"
            )

        return self._tools[name]

    def list_tools(self) -> list[str]:
        """Return the names of all registered tools."""

        return list(self._tools.keys())