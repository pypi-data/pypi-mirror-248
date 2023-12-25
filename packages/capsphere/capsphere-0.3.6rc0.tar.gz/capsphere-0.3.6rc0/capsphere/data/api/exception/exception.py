class AWSConnectionError(Exception):
    """Exception raised when the AWS connection fails."""
    pass


class AWSExecutionError(Exception):
    """Exception raised for errors during query execution."""
    pass
