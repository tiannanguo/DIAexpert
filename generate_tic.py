#!/usr/bin/python

"""
This script reads in multiple .mzXML.gz files, and outputs a single .tsv file, each line of which
is the sum of TIC for each input file.
"""
import xml
from xml.sax.handler import ContentHandler
import os
import sys
import gzip
import argparse

class MzXmlTicParser(ContentHandler):
    """
    parser class for handling mzXML file TIC
    """
    def __init__(self):
        self.sumMsLevel1 = 0
        self.sumMsLevel2 = 0

    # callback by sax parser
    def startElement(self, name, attrs):
        if (name == "scan"):
            msLevel = attrs.get("msLevel")
            totIonCurrent = int(attrs.get("totIonCurrent"))
            if msLevel == "1":
                self.sumMsLevel1 += totIonCurrent
            elif msLevel == "2":
                self.sumMsLevel2 += totIonCurrent
            else:
                pass
        else:
            ContentHandler.startElement(self, name, attrs)

    def parse(self, filepath):
        xml.sax.parse(filepath, self)
        return self.sumMsLevel1, self.sumMsLevel2

def generate_tic(fp):
    return MzXmlTicParser().parse(fp)

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="generate TIC file")

    parser.add_argument("--map_file", required=True,
        help="samples mapping file.")

    parser.add_argument("--file_dir", required=True,
        help="all mzXML.gz files under the directory will be processed.")

    parser.add_argument("--out", required=True,
        help="output file path. the format is tsv")

    args = parser.parse_args()

    sample_names = []
    with open(args.map_file) as map_file:
        for line in map_file:
            sample_names.append(line.strip().split()[1])

    mzXML_dir = args.file_dir

    with open(args.out, 'w') as fout:
        fout.write('sample\tms1_tic\tms2_tic\n')

        for name in sample_names:
            fname = os.path.join(mzXML_dir, "%s.mzXML.gz" % name)
            if os.path.exists(fname):
                with gzip.open(fname, 'rb') as fp:
                    sums = generate_tic(fp)
                    fout.write('%s\t%s\t%s\n' % (name, sums[0], sums[1]))
