# -*- encoding: utf-8 -*-

import datetime
import decimal
import elv
import io
import os
import sys
import unittest

PY3 = sys.version > "3"

class TestElv(unittest.TestCase):
    def setUp(self):
        _csv = u'''"31-12-2014";"31-12-2014";"Test 1";"-497,78";"5.520,09"
"30-12-2014";"31-12-2014";"Test 2";"-100,00";"6.017,87"
"30-12-2014";"31-12-2014";"Test 3 --æøåÆØÅ--";"-145,47";"6.117,87"
"30-12-2014";"30-12-2014";"Test 4";"-457,24";"6.263,34"
"29-12-2014";"29-12-2014";"Test 5";"-108,30";"6.720,58"'''

        if not PY3:
            _csv = _csv.encode("latin1")
            from StringIO import StringIO
            stream = StringIO(_csv)
        else:
            stream = io.StringIO(_csv)

        self.trans = elv.parse_stream(stream)

    def test_parse_stream(self):
        self.assertTrue(self.trans is not None)

    def test_first_last(self):
        self.assertEqual(self.trans.first.xfer, datetime.date(2014,12,29))
        self.assertEqual(self.trans.last.xfer, datetime.date(2014,12,31))

    def test_len(self):
        self.assertEqual(len(self.trans), 5)

    def test_add(self):
        t1 = elv.Transaction(1, datetime.date(2015,4,15),
                datetime.date(2015,4,15), "trans 1", decimal.Decimal("100"),
                decimal.Decimal("100"))

        t2 = elv.Transaction(1, datetime.date(2015,4,14),
                datetime.date(2015,4,14), "trans 1", decimal.Decimal("100"),
                decimal.Decimal("-43"))

        ts = elv.Transactions([t1,t2])
        ts1 = elv.Transactions([t1])
        ts2 = elv.Transactions([t2])
        self.assertEqual(ts, ts1 + ts2)
        self.assertEqual(ts.first_index, t1)
        self.assertEqual(ts.last_index, t2)

    def test_encoding(self):
        self.assertEqual(self.trans[2].message, u"Test 3 --æøåÆØÅ--")

    def test_sqlite3(self):
        with self.trans.to_sqlite3() as con:
            self.assertTrue(con is not None)

            cur = con.cursor()
            res = cur.execute("""
                select min(xfer) as 'first [date]',
                       max(xfer) as 'last [date]'
                from transactions""")

            first, last = res.fetchone()
            self.assertEqual(first, datetime.date(2014,12,29))
            self.assertEqual(last, datetime.date(2014,12,31))


class TestElvOnFile(unittest.TestCase):
    def test_iso8859_1_file(self):
        filename = os.path.join(os.path.dirname(__file__),
                "iso-8859-1-dos-crlf.csv")
        self.assertTrue(os.path.exists(filename))

        trans = elv.parse(filename, encoding="latin1")
        self.assertTrue(trans is not None)
        self.assertEqual(len(trans), 2)


if __name__ == "__main__":
    unittest.main()
