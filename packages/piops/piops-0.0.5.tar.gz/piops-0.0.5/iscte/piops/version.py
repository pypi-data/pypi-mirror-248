from importlib.metadata import version as md

def version():
    #print("Hello from piops 0.0.3 !")
    #print("I'm running it using virtual environment:", sys.prefix )
    return "Hello from piops " + md.version('piops')
