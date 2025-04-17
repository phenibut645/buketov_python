
class Logs:
    logs_list: list[str] = []
    logs_actions = {}
    
    def output() -> None:
        for log in Logs.logs_list:
            print(log)

    def debug(action):
        def decorator(func):
            def wrapper(*args, **kwargs):
                out = ""
                index = 0
                for arg in args:
                    index += 1
                    out += str(arg)
                    if(index != len(args)):
                        out += action
                Logs.logs_list.append(out)
                match action:
                    case "+":

                return func(*args, **kwargs)
            return wrapper
        return decorator

class Math:
    def calculate_validation(func):
        def wrapper(*args, **kwargs) -> int | None:
            for arg in args:
                if isinstance(arg, str):
                    print("vale")
                    return None
            try:
                return func(*args, **kwargs)
            except ZeroDivisionError:
                print("value")
                return None
        return wrapper    

    @calculate_validation
    @Logs.debug("+")
    def liitumine(*args, **kwargs) -> int | None:
        sum = 0
        for num in args:
            sum += num
        return sum

    @calculate_validation
    @Logs.debug("-")
    def lahutamine(x: int, y: int) -> int | None:
        return x - y

    @calculate_validation
    @Logs.debug("*")
    def korrutamine(*args, **kwargs) -> int | None:
        sum: int = None
        for arg in args:
            if sum is None:
                sum = arg
            sum *= arg
        return sum

    @calculate_validation
    @Logs.debug("/")
    def jagamine(x: int, y: int) -> float | None:
        return x / y


print(Math.korrutamine(5, 5, 5, 5))
Logs.output()
