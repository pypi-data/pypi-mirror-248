from .app  import ania
from ania.ui import error, bye

def run():
    try:
        ania()

    except KeyboardInterrupt:
        bye()
#    except Exception as e:
#        error(e)
