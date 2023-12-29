from importlib.metadata import version

def version():
    #print("Hello from piops 0.0.3 !")
    #print("I'm running it using virtual environment:", sys.prefix )
    return "Hello from piops " + version('piops')
