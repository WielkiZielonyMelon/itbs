def update_dict_if_key_not_present(original, incoming):
    for key in incoming:
        if key not in original:
            original[key] = incoming[key]