#! /usr/bin/python
import urllib;
import urllib2;
import sys;
import xml.etree.ElementTree as ET;

GREEN = "\033[1;32m";
DEFAULT = "\033[0;49m";
BOLD = "\033[1m";
UNDERLINE = "\033[4m";
NORMAL = "\033[m";
RED = "\033[1;31m"

def crawl_xml(queryword):
	return urllib2.urlopen("http://dict.yodao.com/search?q="
        + urllib.quote_plus(queryword) + "&xmlDetail=true&doctype=xml").read();

def print_translations(xml):

	root = ET.fromstring(xml);

	original_query = root.find("original-query");
	queryword = original_query.text;
	print BOLD + UNDERLINE + queryword + NORMAL;
	
	cus = root.find("custom-translation");
	source = cus.find("source/name");
	print RED + "Translations from " + source.text + DEFAULT;

	for content in cus.iterfind(".//content"):
		print GREEN + content.text + DEFAULT;

def usage():
	print "usage: dict.py word_to_translate";

def main(argv):
	if len(argv) <= 0:
		usage();
		sys.exit(1);
	xml = crawl_xml(" ".join(argv));
	print_translations(xml);

if __name__ == "__main__":
	main(sys.argv[1:]);
