from pam import err

def error_func(x):
    print(x)
    raise KeyboardInterrupt


error_func = err(number=1)(error_func)

error_func(4)