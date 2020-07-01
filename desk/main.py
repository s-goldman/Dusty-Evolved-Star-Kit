import argparse
import inspect
import pdb

from desk import console_commands


def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="subparser_name", help="sub-command help")

    # create the subparsers and populate them with the correct arguments
    funcs_to_subcommand = inspect.getmembers(console_commands, inspect.isfunction)
    for name, func in funcs_to_subcommand:
        subparser = subparsers.add_parser(name, help=func.__doc__)
        for parname, arg in inspect.signature(func).parameters.items():
            if arg.default == inspect.Signature.empty:
                subparser.add_argument(parname)
            else:
                subparser.add_argument("--" + parname, default=arg.default)

    # now actually parse the arguments
    args = parser.parse_args()

    # and call the function
    for name, func in funcs_to_subcommand:
        if args.subparser_name == name:
            # make a dictionary containing the correct inputs to the function,
            # extracted from the parsed arguments
            funcargs = {}
            for parname in inspect.signature(func).parameters:
                funcargs[parname] = getattr(args, parname)
            func(**funcargs)
            break  # drop out immediately, which skips the "else" below
    else:
        assert False, "Invalid subparser! This should be impossible..."


if __name__ == "__main__":
    main()
