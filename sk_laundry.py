#!/usr/bin/env python3
"""Stamkartstraat laundry API"""

SK_LAUNDRY_URL = "http://80.114.145.155/eng/Status.asp"

import re
from sys import argv
from urllib.request import urlopen
from bs4 import BeautifulSoup
from datetime import datetime

def scrub(s):
    return re.sub('\s', ' ', s.strip())

def ignore_before_number(s):
    pieces = re.split("(\d)", s, maxsplit=1)

    # if there were no digits, return an empty string
    if len(pieces) != 3:
        return ''

    _, first_digit, rest = tuple(pieces)
    return first_digit + rest

class Machine:
    def __init__(self, soup_row):
        cells = soup_row("td")

        self.name = scrub(cells[0].string)
        self.price = scrub(cells[1].string)
        self.status = scrub(cells[2].string)
        self.remaining = ignore_before_number(scrub(cells[3].string))
        self.started = ignore_before_number(scrub(cells[4].string))

    def __str__(self):
        if self.status == "Ready":
            return self.name + ": available"

        s = self.name + ": " + self.status

        if self.started:
            s += " since " + self.started

        if self.remaining:
            s += ", " + self.remaining + " remaining"

        return s

    @classmethod
    def scrape_all(cls) -> "list of Machines":
        with urlopen(SK_LAUNDRY_URL) as w:
            soup = BeautifulSoup(w, "html.parser")

        # skip the first table, it's just a header
        table = soup("table")[1]

        # ignore the first row, it's just a header
        rows = table("tr")[1:]

        # make machines from the information
        return [ cls(row) for row in rows ]

def basic_cli(*args):
    if '-vv' in args:
        print('\n'.join([ str(m) for m in Machine.scrape_all() ]))
        return

    sparse_machines = '\n'.join([ str(m) for m in Machine.scrape_all() if m.status != "Ready" ])
    if '-v' in args:
        print(sparse_machines or "All machines available.")
    else:
        print(sparse_machines)

if __name__ == "__main__":
    basic_cli(argv[1:])
