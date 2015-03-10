# -*- encoding: utf-8 -*-

import io
import datetime
import elv
import unittest


class TestElv(unittest.TestCase):
    def setUp(self):
        _csv = io.StringIO(u'''"31-12-2014";"31-12-2014";"Test 1";"-497,78";"5.520,09"
"30-12-2014";"31-12-2014";"Test 2";"-100,00";"6.017,87"
"30-12-2014";"31-12-2014";"Test 3 --æøåÆØÅ--";"-145,47";"6.117,87"
"30-12-2014";"30-12-2014";"Test 4";"-457,24";"6.263,34"
"29-12-2014";"29-12-2014";"Test 5";"-108,30";"6.720,58"'''.encode("latin1"))

        self.trans = elv.parse_stream(_csv)

    def test_parse_stream(self):
        self.assertTrue(self.trans is not None)

    def test_first_last(self):
        self.assertEqual(self.trans.first.xfer, datetime.date(2014,12,29))
        self.assertEqual(self.trans.last.xfer, datetime.date(2014,12,31))

    def test_len(self):
        self.assertEqual(len(self.trans), 5)

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


if __name__ == "__main__":
    unittest.main()
