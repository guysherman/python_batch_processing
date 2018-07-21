# pylint: disable=C0103
"""
An object which handles recursively searching the file system,
based on some search predicate supplied by the user
"""
import os

class RecursiveSearch:
    """
    An object which handles recursively searching the file system,
    based on some search predicate supplied by the user
    """
    def __init__(self, predicate):
        """
        Constructs a new RecursiveSearch object which uses the given predicate

        predicate:- a boolean lambda or function which determines whether a
                    file name matches a pattern
        """
        self.predicate = predicate

    def search(self, start_location):
        """
        Performs a recursive search from **start_location**, calling predicate for
        each filename to determine if it matches the search pattern

        start_location:- the top path to start searching from
        returns:- a list of paths relative to the top path that satisfy the search predicate
        """
        dirs = []
        files = []
        matches = []
        contents = os.listdir(start_location)
        for sub in contents:
            sub_path = os.path.join(start_location, sub)
            if os.path.isdir(sub_path):
                dirs.append(sub_path)
            elif os.path.isfile(sub_path):
                files.append(sub_path)
        for subdir in dirs:
            dir_matches = self.search(subdir)
            matches = matches + dir_matches
        for subfile in files:
            match = self.predicate(subfile)
            if match:
                matches.append(subfile)
        return matches

    def search_many(self, start_locations):
        """
        Perform a recursive search on each of several locations. Convenient
        when using a multi-valued argument from the command line

        start_locations:- an array of paths to search
        returns:- a list of matches
        """
        result = []
        for path in start_locations:
            matches = self.search(path)
            result = result + matches
        return result
