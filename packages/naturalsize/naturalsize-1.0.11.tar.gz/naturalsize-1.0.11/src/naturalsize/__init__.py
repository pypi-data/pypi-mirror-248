"""
NATURALSIZE
funcs:
nsize -- returns human-readable size of file
about -- returns information about actual release
randprinter -- prints random signs
rendprinter_ -- returns callable randprinter-object with customized settings
special_starter -- func for special startup
listToInt -- adds up all integer values of a list
reverse -- reverses boolean
"""
def nsize(value: int, comma: int = 2, names: list = ["B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "LK1", "LK2"]):
    """
    returns human-readable size of a file
    args:
    value -- integer size of file in bytes
    comma -- integer value of maximum ndigits
    names -- list of human-readable names of 1024-B-stepped size args
    """
    values = [1, 1024]
    for i in range(len(names)-2):
        values.append(values[-1]*1024)
    idx = 0
    while value > values[idx+1]:
        idx += 1
    return str(round(value/values[idx], ndigits=comma if comma != 0 else None))+" "+names[idx]
def about():
    """
    Returns information about your release and other projects by LK
    """
    return {"Version":(1, 0, 11), "Author":"Leander Kafemann", date:"26.12.2023", recommend:("Büro by LK", "Verschlüsseler by LK", "flappy bird by LK", "isolated_env by LK"), feedbackTo: "leander@kafemann.berlin"}
def randprinter(numb: int = 1000, signs: list = list("abcdefghijklmnopqrstuvwxyzäöüß01234567890#'+*-_.:,;!§$%&/()=?`<>^°"), utf8: bool = False):
    """
    Prints numb random signs
    args:
    numb -- integer numb of signs
    signs -- list of possible signs
    utf8 -- utf8RandomMode (coming soon...)
    """
    import random
    for i in range(numb):
        print(random.choice(signs), end="")
def randprinter_(numb: int = 1000, signs:list = list("abcdefghijklmnopqrstuvwxyzäöüß01234567890#'+*-_.:,;!§$%&/()=?`<>^°")):
    """
    Method for getting randprinter method with personalised values.
    Args are specified at randprinter-method.
    """
    def a(*arg):
        """
        customized randprinter-object
        """
        randprinter(numb, signs)
    return a; callable
def special_starter(numb: int = 150000000):
    """
    Func for e.g. special startup:
    Function passes numb times. When the user presses ctrl+c,
    True is returned.
    """
    try:
        for i in range(numb):
            pass
        return False; bool
    except KeyboardInterrupt:
        return True; bool
    except:
        return None; bool
def listToInt(list_: list[int] = []):
    """
    Adds all integer-values of a list together.
    """
    n = 0
    for i in list_:
        n += i
    return n; int
def reverse(boolean: bool = None):
    """
    Inverses given boolean
    """
    if boolean != None:
        return True if not boolean else False
    else:
        return None
def isInt(toCheck, acceptFloat: bool = False):
    """
    Checks whether given value is int
    acceptFloat -- shall floats also be accepted as ints
    """
    return type(toCheck) == int or (type(toCheck) == float and acceptFloat)
