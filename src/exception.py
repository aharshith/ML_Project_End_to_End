import sys
from src.logger import logging


def error_message_detail(error, error_detail: sys):
    _, _, exc_tb = error_detail.exc_info()
    file_name = exc_tb.tb_frame.f_code.co_filename
    error_message = 'Error occurred in python script name [{0}] line number [{1}] error message [{2}]'.format(
        file_name, exc_tb.tb_lineno, str(error)
    )
    return error_message

class CustomException(Exception):
    def __init__(self, error_message, error_detail: sys):
        super().__init__(error_message)
        self.error_message = error_message_detail(error_message, error_detail=error_detail)

    def __str__(self):
        return self.error_message
import sys

# Function to extract detailed error information
def error_message_detail(error, error_detail: sys):
    # Get the traceback object from the error_detail
    _, _, exc_tb = error_detail.exc_info()
    
    # Extract the file name where the error occurred
    file_name = exc_tb.tb_frame.f_code.co_filename
    
    # Create a formatted error message with file name, line number, and error message
    error_message = 'Error occurred in python script name [{0}] line number [{1}] error message [{2}]'.format(
        file_name, exc_tb.tb_lineno, str(error)
    )
    
    return error_message

# Custom exception class that extends the base Exception class
class CustomException(Exception):
    def __init__(self, error_message, error_detail: sys):
        # Call the base class constructor with the original error message
        super().__init__(error_message)
        
        # Create a detailed error message using the custom function
        self.error_message = error_message_detail(error_message, error_detail=error_detail)

    # Override the string representation to return the detailed error message
    def __str__(self):
        return self.error_message


