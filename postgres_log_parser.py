#!/usr/bin/env python

import csv
import re

#for cleaning the statements
CLEAN=re.compile('^[^:]*: *')

def extract_sql(args):
    if args[7] in ['SELECT'] or (args[13].startswith('statement:') and 'DEALLOCATE' not in args[13]):
        return '/* #%s */ %s' % (args[0],CLEAN.sub('', args[13]))

def filter_users(users, args):
    if args[1] in users:
        return args


def main():
    import argparse
    parser = argparse.ArgumentParser(description='Process postgres csv logs.')
    parser.add_argument('--users', type=str, nargs='*', help='Only output logs for this user.')
    parser.add_argument('--sql_only', action='store_true', help='Output SQL only.')
    parser.add_argument('log', help='The pg csv log file')
    args = parser.parse_args()
    
    with open(args.log, 'rb') as fh:
        for entry in csv.reader(fh, 'excel'):
            if args.users:
                entry = filter_users(args.users, entry)
            if entry is not None:
                if args.sql_only:
                    result = extract_sql(entry)
                else:
                    result = entry
                if result is not None:
                    print result
    
if __name__ == '__main__':
    main()





