#from importlib.metadata import version
import pkg_resources

def version2():
    #print("Hello from piops 0.0.3 !")
    #print("I'm running it using virtual environment:", sys.prefix )
    print("Hello from piops " + pkg_resources.get_distribution("piops").version)
    return "Hello from piops " + pkg_resources.get_distribution("piops").version # version('piops')

version2()
