def is_blank(some_string):
    if some_string and some_string.strip():
        # some_string is not None AND some_string is not empty or blank
        return False
    # some_string is None OR some_string is empty or blank
    return True
