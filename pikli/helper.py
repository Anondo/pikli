

int_flags = []


def get_int(flag_name):
    for flag in int_flags:
        if flag_name == flag.flag_name:
            return flag.default


def add_int_flag(flag):
    int_flags.append(flag)
