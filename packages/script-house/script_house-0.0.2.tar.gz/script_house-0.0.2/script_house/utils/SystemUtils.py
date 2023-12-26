import socket


def only_work_on(hostname: str):
    """
    a helper function for dev to run code on certain computers
    """
    cur_hostname = socket.gethostname()
    # exit or raise Exception ?
    if hostname != cur_hostname:
        raise Exception(f'expected host: {hostname}; real host: {cur_hostname}')
