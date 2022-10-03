

def filter_dict_by_set(dictionary: dict, valid_keys: set):
    """ create new dict with key value pairs of dictionary, where key is in valid_keys """
    new_dictionary = {}

    for key, value in dictionary.items():
        if key in valid_keys:
            new_dictionary[key] = value

    return new_dictionary


def pop_from_dict_by_set(dictionary: dict, valid_keys: set):
    """ remove and create new dict with key value pairs of dictionary, where key is in valid_keys """
    new_dictionary = {}

    for key in list(dictionary.keys()):
        if key in valid_keys:
            new_dictionary[key] = dictionary.pop(key)

    return new_dictionary
