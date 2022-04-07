import argparse, sys
from pylogparser.parser import ParserTool

def main(args):
    pt = ParserTool(args.logfile)
    if args.request_by_day:
        pt.daily_request()
    if args.frequent_ua:
        pt.daily_frequent_ua()
    if args.method_by_os:
        pt.daily_method_ratio()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Parse log file and get report(s)'
    )
    parser.add_argument(
        '-f',
        dest='logfile',
        action='store',
        required=True,
        help='Path to the log file, eg: sample.log')
    parser.add_argument(
        '-r',
        dest='request_by_day',
        default=False,
        action='store_true',
        help='Report type: Number of requests served by day')
    parser.add_argument(
        '-u',
        dest='frequent_ua',
        default=False,
        action='store_true',
        help='Report type: Three most frequent user-agent by day')
    parser.add_argument(
        '-m',
        dest='method_by_os',
        default=False,
        action='store_true',
        help='Report type: Ratio of GETs to POSTs by OS by day')

    args = parser.parse_args()
    if not (args.request_by_day or args.frequent_ua or args.method_by_os):
        print('At least one parameter (-r, -u, -m) is required.')
        parser.print_help(sys.stderr)
        sys.exit(1)

    main(args)
