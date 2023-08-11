class Error(Exception):
    """Base class for exceptions"""
    pass

class AwsErrorException(Error):
    """Generic exception for AWS errors"""
    pass
