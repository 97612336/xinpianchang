def num_to_int(some_string):
    if isinstance(some_string,int):
        return some_string
    elif isinstance(some_string,str):
        return int(some_string.replace(',',''))