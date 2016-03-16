__author__ = 'jscarbor'

from fusionpy.fusion import Fusion
import sys
import json


def configure(args):
    """
    Configure collection(s) if not already there, fail if the collection(s) exist but differ from the given
    configuration.

    :param args: the name of a file with configuration information
    """
    with open(args[0]) as f:
        cfg = json.load(f)

    fusion = Fusion().ensure_config(write=False, **cfg)
    if fusion is None:
        # It's not there, so safe to write
        Fusion().ensure_config(**cfg)
    elif not fusion:
        # Cowardly not overwriting a differing configuration
        print "Fusion configuration differs from files.  Maybe clean to start over."
        sys.exit(5)

    print "Fusion collection matches file configuration."


def delete(args):
    """
    Delete a collection if it exists.  If the named collection does not exist, do nothing.

    :param args:  Optional, the name of a single collection to delete
    """
    if len(args) > 1:
        print "Too many arguments.  Name at most one collection."
        sys.exit(2)

    collection = None
    if len(args) == 1:
        collection = args[0]

    collection=Fusion().get_collection(collection)
    if collection.exists():
        collection.delete_collection(purge=True, solr=True)

def export(args):
    """
    Save out the current configuration from Fusion to file and folder(s) to permit re-import
    :param args:
    """
    pass


def print_help(args):
    print "Usage"
    print "  python -m fusionpy.tool <verb> [argument] [...]"


if __name__ == "__main__":
    if len(sys.argv) < 2 or sys.argv[1] not in dir(sys.modules[__name__]) or sys.argv[1] == "help":
        print_help([])
        sys.exit(1)
    # Call the requested function
    globals()[sys.argv[1]](sys.argv[2:])
