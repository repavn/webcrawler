def get_first_or_none(res_list: list):
    try:
        return next(iter(res_list), None)
    except:
        # TODO: log this
        return None
