from src.pam import save_progress





@save_progress()
def error_func():
    return "error"


if __name__ == "__main__":
    error_func()
