import os
import sys

class WallethubException(Exception):
    def __init__(self, error_message:Exception, error_details:sys):
        super().__init__(error_message) # passing the error to the parent class
        self.error_message = WallethubException.get_detailed_error_message(error_message = error_message, error_detail = error_details)


    def get_detailed_error_message(error_message:Exception, error_detail:sys):
        
        """
        error_msg: Exception object
        error_detail: object of sys module
        """
        _,_,e_detail = error_detail.exc_info() # from the error details, get the traceback of the error. 
                                                # It returns tuples of (filename, line number, function name, text)
        
        script_file_name = e_detail.tb_frame.f_code.co_filename # get the file name from the traceback
        function_name = e_detail.tb_frame.f_code.co_name        # get the function name from the traceback
        try_block_line_no = e_detail.tb_lineno                  # get the line number of the error in the try block
        exception_block_line_no = e_detail.tb_frame.f_lineno    # get the line number of the exception block error

        error_msg = f"""
        Error occurred in script: [{script_file_name}] 
        at try block line number: [{try_block_line_no}] and exception block line number: [{exception_block_line_no}] 
        in function : {function_name} 
        error message:\n{error_message}
        """
        return error_msg


    def __str__(self):
        return self.error_message

    def __repr__(self) -> str:
        return WallethubException.__name__.str()