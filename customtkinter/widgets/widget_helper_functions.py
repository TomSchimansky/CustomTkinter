

def filter_dict_by_set(dictionary: dict, valid_keys: set):
    """ remove all key value pairs, where key is not in valid_keys set """
    new_dictionary = {}

    for key, value in dictionary.items():
        if key in valid_keys:
            new_dictionary[key] = value

    return new_dictionary
