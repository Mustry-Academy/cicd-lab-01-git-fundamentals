"""Sample app for the Git fundamentals lab."""


def greet(name: str, shout: bool = False) -> str:
    message = f"Hello, {name}!"
    return message.upper() if shout else message


def farewell(name: str, shout: bool = False) -> str:
    message = f"Goodbye, {name}!"
    return message.upper() if shout else message


if __name__ == "__main__":
    import sys

    flags = {"--shout", "--bye"}
    args = [a for a in sys.argv[1:] if a not in flags]
    shout = "--shout" in sys.argv[1:]
    bye = "--bye" in sys.argv[1:]
    who = args[0] if args else "world"
    func = farewell if bye else greet
    print(func(who, shout=shout))
