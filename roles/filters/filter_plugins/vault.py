try:
    from shlex import quote as cmd_quote
except ImportError:
    from pipes import quote as cmd_quote

from six import string_types


def shell_quote(input):
    """Quote string for Shell"""
    return cmd_quote(input)


def quote_string(input):
    """Shell quote if string. Otherwise, do nothing. This is for Vault write"""
    if isinstance(input, string_types):
        quoted = shell_quote(input)
        if quoted[0] == '"' or quoted[0] == "'":
            return quoted
        else:
            return "'{}'".format(quoted)
    else:
        return input


def map_key_value(dictionary):
    """Turn a dictionary into the format required for Vault CLI"""
    return " ".join(["{}={}".format(key, quote_string(value))
                     for key, value in dictionary.items()])


def map_key_file(dictionary):
    """Turn a dictionary of file paths and prefix the paths with `@` as
    required by Vault CLI"""
    return " ".join(["{}={}".format(key, quote_string("@{}".format(value)))
                     for key, value in dictionary.items()])


class FilterModule(object):
    """
    Custom module for Vault specific operations
    """

    def filters(self):
        return {
            "map_key_value": map_key_value,
            "map_key_file": map_key_file,
            "shell_quote": shell_quote
        }
