def omit_empty(dictionary):
    """Omit key in dictionary if value is not truthy"""
    return {key: value for key, value in dictionary.items() if value}


def omit_if_false(value):
    """Returns None if value is falsey"""
    if value:
        return value
    else:
        return None


class FilterModule(object):
    """
    Custom module for omit operations
    """

    def filters(self):
        return {
            "omit_empty": omit_empty,
            "omit_if_false": omit_if_false
        }
