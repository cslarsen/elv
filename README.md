Elv
===

Elv is a small utility for parsing exported CSV files from the online Norwegian
bank Jæren Sparebank.

I use it for personal purposes, but decided to simply upload the code anyway,
in case anyone wants to do the same.

If you want to contribute other formats, please send pull requests on the
project's GitHub page at 

Use the "export data" feature in the online bank, and you should be able to
parse the file using Elv.

Features
--------

  * Parses CSV file from bank containing transactions
  * Money is stored in exact decimals (as you should do; never use floats for
    stuff like this)
  * Contains a simple Python query API for sorting through large collections of
    transactions.
  * Can optionally put transactions in an in-memory SQLite3 database for even
    better queries.

Norwegian short description
---------------------------

Elv er en Python modul for å lese banktransaksjoner eksportert fra banken din
som en CSV-fil. Foreløpig er det kun Jæren Sparebank som jeg _vet_ er støttet,
men du kan nok ganske enkelt legge til lesere for andre format.

The CSV File Format
-------------------

The CSV file should be a plain text file with the
[ISO-8859-1](https://en.wikipedia.org/wiki/ISO/IEC_8859-1) encoding (aka
Latin1).  It looks like this:

    "31-12-2014";"31-12-2014";"Test 1";"-497,78";"5.520,09"
    "30-12-2014";"31-12-2014";"Test 2";"-100,00";"6.017,87"
    "30-12-2014";"31-12-2014";"Test 3 --æøåÆØÅ--";"-145,47";"6.117,87"
    "30-12-2014";"30-12-2014";"Test 4";"-457,24";"6.263,34"
    "29-12-2014";"29-12-2014";"Test 5";"-108,30";"6.720,58"

The fields are as follows:

  * Date when the transaction was placed, in format `"DD-MM-YYYY"`.
  * Date when the transaction was posted ("bokført").
  * A message associated with the transaction, set by the one making the
    transaction.
  * The amount deposited or deducted from the account in [NOK (Norwegian
    kroner)](https://en.wikipedia.org/wiki/Norwegian_krone) in format
    `"-123,45"`, always two decimals and an optional sign.
  * The balance of your account after this transaction was completed.

The file itself contains no headers, and can contain many such transactions,
one per line.

License
=======

Copyright (C) 2015 Christian Stigen Larsen

Licensed under AGPL v3 or later; see http://www.gnu.org/licenses/agpl-3.0.html
