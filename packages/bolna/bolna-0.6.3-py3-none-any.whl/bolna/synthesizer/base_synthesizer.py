from bolna.helpers.logger_config import CustomLogger

custom_logger = CustomLogger(__name__)


class BaseSynthesizer:
    def __init__(self, stream=True, buffer_size=40, log_dir_name=None):
        self.stream = stream
        self.buffer_size = buffer_size
        self.logger = custom_logger.update_logger(log_dir_name=log_dir_name)
