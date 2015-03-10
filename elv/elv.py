# -*- encoding: utf-8 -*-

"""
Elv is a module for parsing bank account transactions from a CSV file.

Usage example::

    with open("data.csv", "rt") as f:
        trans = Parse.csv_to_transactions(f)
"""

from datetime import datetime
from decimal import Decimal
import csv
import sys

try:
    import sqlite3
except ImportError:
    pass

PY3 = sys.version > "3"

class Parse:
    """Parses a bank CSV file."""

    @staticmethod
    def date(date_string, date_format="%d-%m-%Y"):
        """Returns a Datetime object from date in string.

        Args:
            date_format: The datetime.datetime.strptime format of the date.

        Returns:
            A ``datetime.Date`` object.
        """
        return datetime.strptime(date_string, date_format).date()

    @staticmethod
    def money(s, thousand_sep=".", decimal_sep=","):
        """Converts money amount in string to a Decimal object.

        With the default arguments, the format is expected to be
        ``-38.500,00``, where dots separate thousands and comma the decimals.

        Args:
            thousand_sep: Separator for thousands.
            decimal_sep: Separator for decimals.

        Returns:
            A ``Decimal`` object of the string encoded money amount.
        """
        s = s.replace(thousand_sep, "")
        s = s.replace(decimal_sep, ".")
        return Decimal(s)

    @staticmethod
    def to_utf8(s, source_encoding="latin1"):
        if not PY3:
            return s.decode(source_encoding)
        else:
            return s

    @staticmethod
    def csv_row_to_transaction(index, row, source_encoding="latin1",
            date_format="%d-%m-%Y", thousand_sep=".", decimal_sep=","):
        """
        Parses a row of strings to a ``Transaction`` object.

        Args:
            index: The index of this row in the original CSV file. Used for
            sorting ``Transaction``s by their order of appearance.

            row: The row containing strings for [transfer_date, posted_date,
            message, money_amount, money_total].

            source_encoding: The encoding that will be used to decode strings
            to UTF-8.

            date_format: The format of dates in this row.

            thousand_sep: The thousand separator in money amounts.

            decimal_sep: The decimal separator in money amounts.

        Returns:
            A ``Transaction`` object.

        """
        xfer, posted, message, amount, total = row
        xfer = Parse.date(xfer)
        posted = Parse.date(posted)
        message = Parse.to_utf8(message, source_encoding)
        amount = Parse.money(amount)
        total = Parse.money(total)
        return Transaction(index, xfer, posted, message, amount, total)

    @staticmethod
    def csv_to_transactions(handle, source_encoding="latin1",
            date_format="%d-%m-%Y", thousand_sep=".", decimal_sep=","):
        """
        Parses CSV data from stream and returns ``Transactions``.

        Args:
            index: The index of this row in the original CSV file. Used for
            sorting ``Transaction``s by their order of appearance.

            row: The row containing strings for [transfer_date, posted_date,
            message, money_amount, money_total].

            source_encoding: The encoding that will be used to decode strings
            to UTF-8.

            date_format: The format of dates in this row.

            thousand_sep: The thousand separator in money amounts.

            decimal_sep: The decimal separator in money amounts.

        Returns:
            A ``Transactions`` object.
        """
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
        """Returns earliest ``Transaction`` by transfer date ``xfer``."""
        return min(self.trans, key=lambda x: x.xfer)

    @property
    def last(self):
        """Returns latest ``Transaction`` by transfer date ``xfer``."""
        return max(self.trans, key=lambda x: x.xfer)

    def start(self):
        """Returns the earliest transfer (``xfer``) date."""
        return self.first.xfer

    def stop(self):
        """Returns the latest transfer (``xfer``) date."""
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
        """Adds a ``Transaction``."""
        self.trans.append(value)

    def group_by(self, key, field=lambda x: x.xfer):
        """Returns all transactions whose given ``field`` matches ``key``.

        Returns:
            A ``Transactions`` object.
        """
        return Transactions([t for t in self.trans if field(t) == key])

    def total(self):
        """Returns the sum of all ``Transaction.amount``s."""
        return sum(t.amount for t in self.trans)

    def balance(self):
        """Returns a tuple of (total amount deposited, total amount
        withdrawn)."""
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
        """Return latest row, based on transfer date (``xfer``)."""
        return max(self.trans, key=lambda x: x.xfer)

    def range(self, start_date=None, stop_date=None, field=lambda x: x.xfer):
        """Return a ``Transactions`` object in an inclusive date range.

        Args:
            start_date: A ``datetime.Date`` object that marks the inclusive
            start date for the range.

            stop_date: A ``datetime.Date`` object that marks the inclusive end
            date for the range.

            field: The field to compare start and end dates to. Default is the
            ``xfer`` field.

        Returns:
            A ``Transactions`` object.
        """
        assert start_date <= stop_date, \
            "Start date must be earlier than end date."

        out = Transactions()

        for t in self.trans:
            date = field(t)
            if (start_date is not None) and not (date >= start_date):
                continue
            if (stop_date is not None) and not (date <= stop_date):
                continue
            out.append(t)

        return out

def parse(filename, Class=Parse):
    """Parses bank CSV file and returns Transactions instance.

    Returns:
        A ``Transactions`` object.
    """
    with open(filename, "rt") as f:
        return Class.csv_to_transactions(f)

def parse_stream(stream, Class=Parse):
    """Parses bank CSV stream (like a file handle or StringIO) and returns
    Transactions instance.

    Returns:
        A ``Transactions`` object.
    """
    return Class.csv_to_transactions(stream)
