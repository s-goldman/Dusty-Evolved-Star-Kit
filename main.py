import pdb
import argparse
import desk

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("script", help="script", default="fit", choices=['fit', 'plot'])
    parser.add_argument("--t", "--target", help="file target name", dest="target")
    parser.add_argument("--d", "--distance", help="distance to source", type=int, dest="distance")
    parser.add_argument("--g", "--grid", help="model grid to use", dest="grid")
    args = parser.parse_args()
    # pdb.set_trace()
    print(args)
    if args.script == 'fit':
        desk.sed_fit.main(arg_input=[args.target], dist=args.distance, grid=args.grid)
    if args.script == 'plot':
        desk.plotting_seds.create_fig()

if __name__ == '__main__':
    main()































