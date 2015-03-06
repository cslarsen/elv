# -*- encoding: utf-8 -*-

"""
Contains some classes for parsing bank statements exported as CSV.

Usage:

    with open("data.csv", "rt") as f:
        trans = Parse.csv_to_transactions(f)
"""

from __future__ import with_statement
from datetime import datetime
from decimal import Decimal
import csv

try:
    import sqlite3
except ImportError:
    pass


class Parse:
    """Parses bank CSV file."""

    @staticmethod
    def date(date_string, date_format="%d-%m-%Y"):
        """Returns a Datetime object from date in string."""
        return datetime.strptime(date_string, date_format).date()

    @staticmethod
    def money(s):
        """Returns a Decimal object from money amount in string."""
        # Typical format can be "-38.500,00"

        # Remove dots
        s = s.replace(".", "")

        # Replace comma with dot
        s = s.replace(",", ".")

        return Decimal(s)

    @staticmethod
    def latin1(s):
        """Decodes Latin1 encoded string to UTF-8."""
        return s.decode("latin1")

    @staticmethod
    def csv_row_to_transaction(index, row):
        xfer, posted, message, amount, total = row
        xfer = Parse.date(xfer)
        posted = Parse.date(posted)
        message = Parse.latin1(message)
        amount = Parse.money(amount)
        total = Parse.money(total)
        return Transaction(index, xfer, posted, message, amount, total)

    @staticmethod
    def csv_to_transactions(handle):
        """Parses CSV data and returns Transactions."""
        trans = Transactions()
        rows = csv.reader(handle, delimiter=";", quotechar="\"")

        for index, row in enumerate(rows):
            trans.append(Parse.csv_row_to_transaction(index, row))

        return trans


class Transaction:
    """Represents one transaction in a bank statement."""

    def __init__(self, index, xfer, posted, message, amount, total):
        self.index = index
        self.xfer = xfer
        self.posted = posted
        self.message = message
        self.amount = amount
        self.total = total

    def __str__(self):
        s  = "%s " % self.xfer
        s += "%s " % self.posted
        s += "%9s " % self.amount
        s += "%9s " % self.total
        s += "'%s'" % self.message
        return s.encode("utf-8")

    def __repr__(self):
        return "<Transaction:%s>" % self.__str__()


class Transactions:
    """Contains several Transaction instances and provides querying."""

    def __init__(self, transactions = None):
        self.trans = []
        if transactions is not None:
            self.trans = transactions

    def __str__(self):
        s = "%d transactions\n" % len(self.trans)
        for t in sorted(self.trans, key=lambda x: x.xfer):
            s += str(t) + "\n"
        return s

    def __repr__(self):
        return "<Transactions:%d items from %s to %s>" % (
            len(self), self.start(), self.stop())

    def to_sqlite3(self, location=":memory:"):
        """Returns an SQLITE3 connection to a database containing the
        transactions."""

        def decimal_to_sqlite3(n):
            return int(100*n)

        def sqlite3_to_decimal(s):
            return Decimal(s)/100

        sqlite3.register_adapter(Decimal, decimal_to_sqlite3)
        sqlite3.register_converter("decimal", sqlite3_to_decimal)

        con = sqlite3.connect(location, detect_types=sqlite3.PARSE_COLNAMES |
                sqlite3.PARSE_DECLTYPES)
        cur = con.cursor()
        cur.execute("""create table transactions(
                           id primary key,
                           xfer date,
                           posted date,
                           message text,
                           amount decimal,
                           total decimal)""")
        for t in self:
            cur.execute("INSERT INTO transactions values(?,?,?,?,?,?)",
                (t.index, t.xfer, t.posted, t.message, t.amount, t.total))
        return con

    @property
    def first(self):
        """Returns earliest Transaction."""
        return min(self.trans, key=lambda x: x.xfer)

    @property
    def last(self):
        """Returns latest Transaction."""
        return max(self.trans, key=lambda x: x.xfer)

    def start(self):
        """Returns start date."""
        return self.first.xfer

    def stop(self):
        """Returns stop date."""
        return self.last.xfer

    def __len__(self):
        return len(self.trans)

    def __getitem__(self, key):
        return self.trans[key]

    def __setitem__(self, key, value):
        self.trans[key] = value

    def __reversed__(self):
        return reversed(self.trans)

    def __contains__(self, key):
        return key in self.trans

    def append(self, value):
        self.trans.append(value)

    def group_by(self, key, field=lambda x: x.xfer):
        return Transactions([t for t in self.trans if field(t) == key])

    def total(self):
        """Returns sum of amounts."""
        return sum(t.amount for t in self.trans)

    def balance(self):
        """Returns amount submitted, amount withdrawn."""
        sin = Decimal("0.00")
        sout = Decimal("0.00")

        for t in self.trans:
            if t.amount < Decimal("0.00"):
                sout += t.amount
            else:
                sin += t.amount

        return sin, sout

    @property
    def latest(self):
        """Return latest row."""
        return max(self.trans, key=lambda x: x.xfer)

    def range(self, start=None, stop=None, field=lambda x: x.xfer):
        """Return a Transactions object in an inclusive date range."""
        out = Transactions()

        for t in self.trans:
            date = field(t)
            if (start is not None) and not (date >= start):
                continue
            if (stop is not None) and not (date <= stop):
                continue
            out.append(t)

        return out

def parse(filename):
    """Parses bank CSV file and returns Transactions instance."""
    with open(filename, "rt") as f:
        return Parse.csv_to_transactions(f)

def parse_stream(stream):
    """Parses bank CSV stream (like a file handle or StringIO) and returns
    Transactions instance."""
    return Parse.csv_to_transactions(stream)
