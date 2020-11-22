#!/user/bin/env python

import sys

from models import Company

def fread(filename):
    with open(filename, 'r') as fp:
        return [line.rstrip() for line in fp.readlines()]


def read_companies(filename):
    company_lines = fread(filename)
    return [line.split(",") for line in company_lines]


company_file = sys.argv[1]

for ticker, name in read_companies(company_file):
    print("Saving {} ({})".format(name, ticker))
    try:
        Company.create(name = name, ticker = ticker)
    except:
        print("{} already exists".format(name))
