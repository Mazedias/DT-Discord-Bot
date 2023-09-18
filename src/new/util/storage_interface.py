import logging


def log_message(message: str, is_error: bool):
    """
    Method to log an output to the log file
    :param message: Message to log
    :param is_error: Whether the message is an error message
    :return: None
    """
    logging.basicConfig(filename='./storage/logs.log', encoding='utf-8', level=logging.INFO)

    if is_error:
        logging.error(message)
    else:
        logging.info(message)