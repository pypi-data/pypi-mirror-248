import os


def file_path(filename: str) -> str:
    """Makes sure a string represents a valid, existing file, this can be used with argparse as a valid argument type.

    :param str filename: The filename to test

    :raises FileNotFoundError: When the file is not found.

    :return: The filename, unmodified.
    :rtype: str
    """
    if os.path.isfile(filename):
        return filename
    else:
        raise FileNotFoundError(filename)
