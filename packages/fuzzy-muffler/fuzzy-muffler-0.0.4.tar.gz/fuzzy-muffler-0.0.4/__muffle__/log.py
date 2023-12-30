import logging

# logging globals
LEVEL = logging.INFO
LOG_TO = ''
FMT = '%(asctime)-15s|%(levelname)-15s|%(message)s'

if LOG_TO:
    logging.basicConfig(
        filename=LOG_TO,
        level=LEVEL, 
        format=FMT
    )
else:
    logging.basicConfig(
        level=LEVEL, 
        format=FMT
    )

# logging decorator
def log(func):
    def wrapper(*args, **kwargs):
        logging.info(f'{func.__name__}: {args}, {kwargs}')
        resp = func(*args, **kwargs)
        logging.info(f'{func.__name__} returned')

        return resp
    
    return wrapper