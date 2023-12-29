import getpass

def hello():
    username = getpass.getuser()
    print("Hello ", username)


def sum(a, b):
    sm = a + b
    return sm