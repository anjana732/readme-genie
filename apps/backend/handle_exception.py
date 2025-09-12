import os
import traceback
from logger_file import logger


def handle_exception(func_name, exc_obj, e, id=None, feature=None):
    logger.info("Inside handle_exception function")

    exc_type, exc_value, exc_tb = exc_obj  # unpack sys.exc_info()

    # Print traceback for debugging (console output)
    traceback.print_exception(exc_type, exc_value, exc_tb)

    # Extract file and line info
    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    exception_string = f"{exc_type.__name__} & {fname} & Line {exc_tb.tb_lineno}"

    # Prepare structured log message
    logging_string = (
        f"Exception in {func_name} function. "
        f"Exception: {exception_string}. "
        f"Error Message: {str(e)}"
    )

    # Log as error
    logger.error(logging_string, extra={"function_name": func_name, "feature": feature, "id": id})
