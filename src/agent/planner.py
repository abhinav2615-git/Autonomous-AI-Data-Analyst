from abc import ABC, abstractmethod

from src.models.agent import AnalysisPlan


class BasePlanner(ABC):
    """Base interface for all analysis planners."""

    @abstractmethod
    def create_plan(
        self,
        question: str,
    ) -> AnalysisPlan:
        """Create an analysis plan from a user question."""
        raise NotImplementedError