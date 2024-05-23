import logging
service_logger = logging.getLogger(__name__)
service_logger.setLevel(logging.INFO)
my_formatter = logging.Formatter("%(asctime)s — %(name)s — %(levelname)s — %(funcName)s:%(lineno)d — %(message)s")
my_handler = logging.FileHandler(f"{__name__}.log", mode='a', encoding='utf-8')

my_handler.setFormatter(my_formatter)
service_logger.addHandler(my_handler)