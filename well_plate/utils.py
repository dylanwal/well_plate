
def flatten_list(list_in: list) -> list:
    """
    Turns nested lists into a single level list.
    List[List[List[...]]]  -> List[]
    """
    if not isinstance(list_in, list):
        return list_in

    list_out = []
    for _obj in list_in:
        if isinstance(_obj, list):
            list_out += flatten_list(_obj)
        else:
            list_out.append(_obj)

    return list_out
