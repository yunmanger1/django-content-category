try:
    from common import logwrapper
except ImportError:
    logwrapper = None
    import logging

def getLogger(file):
    if logwrapper:
        return logwrapper.defaultLogger(file)
    return logging.getLogger(file)
