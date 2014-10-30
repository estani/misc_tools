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

def process_log(input_h, output_h, args):
    for entry in csv.reader(input_h, 'excel'):
        if args.users:
            entry = filter_users(args.users, entry)
        if entry is not None:
            if len(entry) < 14:
                #this is broken, probably the stream has already started
                continue
            if args.sql_only:
                result = extract_sql(entry)
            else:
                result = entry
            if result is not None:
                output_h.write(result)
                output_h.write('\n')
                output_h.flush()

def read_stdin():
    import sys, os
    sep=os.linesep
    while sep == os.linesep:
        data = sys.stdin.readline()
        sep = data[-len(os.linesep):]
        yield data.strip()

def main():
    import argparse
    import sys
    parser = argparse.ArgumentParser(description='Process postgres csv logs.')
    parser.add_argument('--users', type=str, nargs='*', help='Only output logs for this user.')
    parser.add_argument('--sql_only', action='store_true', help='Output SQL only.')
    parser.add_argument('log', help='The pg csv log file or "-" to read from stdin')
    args = parser.parse_args()

    if args.log == '-':
        process_log(read_stdin(), sys.stdout, args)
    else:
        with open(args.log, 'rb') as fh:
            process_log(fh, sys.stdout, args)
    
if __name__ == '__main__':
    main()





