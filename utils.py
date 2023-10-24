from datetime import datetime


def print_msg(msg: str):
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"{current_time}: {msg}")
