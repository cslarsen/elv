Elv
===

.. image:: https://pypip.in/wheel/elv/badge.svg
    :target: https://pypi.python.org/pypi/elv/
    :alt: Wheel Status

Elv is a small module for parsing bank transactions from CSV files and
performing queries on the data.

Supported formats
-----------------

It currently supports the banks who use the Eike Alliance solution.
These include, but are not limited to

- Jæren Sparebank
- Sandnes Sparebank

but I'll add support for other banks whenever I get an example dump of their
format.  Send pull requests if you have them at
https://github.com/cslarsen/elv/.

Sandnes Sparebank used to have another format, and I've kept it here, although
I'm not sure anyone uses that anymore.

Norwegian short description
---------------------------

Elv er en Python modul for å lese banktransaksjoner eksportert fra
banken din som en CSV-fil.

Foreløpig er det kun støtte for å lese filer fra Jæren Sparebank og Sandnes
Sparebank. For å eksportere transaksjoner for en konto, velg et datointervall
og deretter i øverste høyre ikon velger du "eksporter til fil".

Jeg har sett at andre nettbanker har tilsvarende funksjonalitet, så send meg
gjerne eksempler på andre format så skal jeg legge dem til.

Features
--------

- Parses CSV file from bank containing transactions

- Money is stored in exact decimals

- Contains a simple Python query API for sorting through large collections of
  transactions.

- Can optionally put transactions in an in-memory SQLite3 database for even
  better queries.


Elevator pitch
--------------

Here's how easy it is to use elv::

  >>> from datetime import date
  >>> import elv
  >>> trans = elv.parse("data.csv")
  >>> trans
  <Transactions:453 items from 2009-01-27 to 2015-03-20>
  >>> trans[0].amount
  Decimal('300.00')
  >>> trans.range(date(2015,1,1), date(2015,3,1))
  <Transactions:15 items from 2015-01-02 to 2015-02-20>
  >>> trans.range(date(2015,1,1), date(2015,3,1)).total()
  Decimal('4500.00')

Installation
------------

You can install from ``setup.py``::

  $ python setup.py install # you may have to run as sudo

or from PyPI::

  $ pip install elv

Example usage
-------------

If you have the bank account transactions in a file called ``data.csv``, you
can simply do::

  $ python
  >>> import elv
  >>> transactions = elv.parse("data.csv")
  >>> transactions
  <Transactions:400 items from 2009-01-27 to 2014-09-29>
  >>> transactions[0]
  <Transaction:2014-09-29 2014-09-29 -2677.00  29519.13 'Vacation'>
  >>> transactions[0].xfer
  datetime.date(2014, 9, 29)
  >>> transactions[0].posted
  datetime.date(2014, 9, 29)
  >>> transactions[0].amount
  Decimal('-2677.00')

You can also get an in-memory SQLite3 database by doing::

  >>> db = transactions.to_sqlite3()
  >>> db
  <sqlite3.Connection object at 0x10f31e200>
  >>> db.execute("SELECT * FROM Transactions").next()
  (0, datetime.date(2014, 9, 29), datetime.date(2014, 9, 29),
   u'Vacation', Decimal('-2677'), Decimal('29519.13'))

How to parse other formats
--------------------------

To parse the default format, Jæren Sparebank::

  >>> ts = elv.parse("file.csv", format="Jæren Sparebank")

To parse Sandnes Sparebank::

  >>> ts = elv.parse("file.txt", format="Sandnes Sparebank")

To see a list of formats, see the dictionary ``elv.formats``.

The CSV File Format: Jæren Sparebank
------------------------------------

The CSV file should be a plain text file with the
`ISO-8859-1 <https://en.wikipedia.org/wiki/ISO/IEC_8859-1>`__ encoding
(aka Latin1). It looks like this:

::

  "31-12-2014";"31-12-2014";"Test 1";"-497,78";"5.520,09"
  "30-12-2014";"31-12-2014";"Test 2";"-100,00";"6.017,87"
  "30-12-2014";"31-12-2014";"Test 3 --æøåÆØÅ--";"-145,47";"6.117,87"
  "30-12-2014";"30-12-2014";"Test 4";"-457,24";"6.263,34"
  "29-12-2014";"29-12-2014";"Test 5";"-108,30";"6.720,58"

The fields are as follows:

-  Date when the transaction was placed, in format ``"DD-MM-YYYY"``.

-  Date when the transaction was posted ("bokført").

-  A message associated with the transaction, set by the one making the
   transaction.

-  The amount deposited or deducted from the account in `NOK (Norwegian
   kroner) <https://en.wikipedia.org/wiki/Norwegian_krone>`__ in format
   ``"-123,45"``, always two decimals and an optional sign.

-  The balance of your account after this transaction was completed.

The file itself contains no headers, and can contain many such
transactions, one per line.

License
=======

Copyright 2015, 2016 Christian Stigen Larsen

Licensed under Affero GPL v3 or later; see
http://www.gnu.org/licenses/agpl-3.0.html
