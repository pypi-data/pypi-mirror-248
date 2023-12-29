import pkg_resources

def version():
    msg = "Hello from piops " + pkg_resources.get_distribution("piops").version
    #print(msg)
    return msg