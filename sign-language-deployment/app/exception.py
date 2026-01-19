import sys


class SignException(Exception):
    def __init__(self, error_message, error_detail: sys):
        self.error_message = error_message
        _, _, exc_tb = error_detail.exc_info()

        file_name = exc_tb.tb_frame.f_code.co_filename if exc_tb else "Unknown"
        line_no = exc_tb.tb_lineno if exc_tb else "Unknown"

        super().__init__(
            f"Error occurred in script [{file_name}] "
            f"at line [{line_no}] error message [{error_message}]"
        )
