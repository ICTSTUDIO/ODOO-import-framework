# -*- coding: utf-8 -*-
# ©2016 ICTSTUDIO <http://www.ictstudio.eu>
# License: AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

import csv, codecs

class UTF8Recoder:
    """
    Iterator that reads an encoded stream and reencodes the input to UTF-8
    """
    def __init__(self, f, encoding):
        self.reader = codecs.getreader(encoding)(f)

    def __iter__(self):
        return self

    def next(self):
        return self.reader.next().encode("utf-8")

class UnicodeReader:
    """
    A CSV reader which will iterate over lines in the CSV file "f",
    which is encoded in the given encoding.
    """

    def __init__(self, f, dialect=csv.excel, encoding="utf-8", **kwds):
        f = UTF8Recoder(f, encoding)
        self.reader = csv.reader(f, dialect=dialect, **kwds)

    def next(self):
        row = self.reader.next()
        return [unicode(s, "utf-8") for s in row]

    def __iter__(self):
        return self

class CSVImport(object):

    def __init__(self, file, encoding='utf-8', *args, **kwargs):
        self._csv_file = open(file)
        self.reader = UnicodeReader(self._csv_file, encoding=encoding, delimiter=',')
        self.headers = [h.lower().replace(' ', '') for h in self.reader.next()]
        self.dict_lines = self._to_dict()

    def _to_dict(self):
        dict_lines = []
        for line in self.reader:
            #print line
            # Should this be done?
            if not line:
                continue
            line_dict = {}
            for i in range(len(line)):
                line_dict[self.headers[i]] = line[i].strip() or ''
            dict_lines.append(line_dict)
        return dict_lines
