class AgentException(Exception):
    """Base exception for agent errors."""

    def __init__(self, message: str = "An error occurred with the agent"):
        self.message = message
        super().__init__(self.message)


class SearchException(AgentException):
    """Exception raised when web search fails."""

    def __init__(self, message: str = "Web search failed"):
        super().__init__(message)


class PriceSearchException(AgentException):
    """Exception raised when price search fails."""

    def __init__(self, message: str = "Price search failed"):
        super().__init__(message)
