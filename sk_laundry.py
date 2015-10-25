#!/usr/bin/env python3
"""Stamkartstraat laundry API"""

SK_LAUNDRY_URL = "http://80.114.145.155/eng/Status.asp"

from pprint import pprint
from urllib.request import urlopen
from bs4 import BeautifulSoup
from datetime import datetime

class Machine:
    def __init__(self, soup_row):
        cells = soup_row("td")

        self.name = cells[0].string
        self.price = cells[1].string
        self.status = cells[2].string

        self.remaining = cells[3].string
        if self.remaining in ("  -        ", " "):
            self.remaining = False

        self.started = cells[4].string
        if self.started == "\xa0":
            self.started = False
        else:
            print(repr(self.started))
            self.started = (' ').split(self.started)[1]

    def __str__(self):
        if self.status == "Ready":
            return self.name + ": available"

        s = self.name + ": " + self.status

        if self.remaining:
            s += ", " + self.remaining + "remaining"

        if self.started:
            s += ", " + "started at" + self.remaining

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

if __name__ == "__main__":
    machines = Machine.scrape_all()
    lines = [ str(m) for m in Machine.scrape_all() ]
    print(*lines, sep='\n')
