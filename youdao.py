#! /usr/bin/python
import re;
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
def print_translations(xml, with_color):

	root = ET.fromstring(xml);
	original_query = root.find("original-query");
	queryword = original_query.text;

	custom_translations = root.findall("custom-translation");
	print BOLD + UNDERLINE + queryword + NORMAL;
	
	for cus in custom_translations:
		source = cus.find("source/name");
		print RED + "Translations from " + source.text + DEFAULT;
		contents = [];
		for content in cus.iterfind(".//content"):
			contents.append(content.text);

		if with_color:
			for content in contents[0:5]:
				print GREEN + content + DEFAULT;
		else:
			for content in contents[0:5]:
				print content;

	yodao_translations = root.findall("yodao-web-dict");
	printed = False;
	for trans in yodao_translations:
		webtrans = trans.findall("web-translation");
		for web in webtrans[0:5]:
			if not printed:
				print RED + "Translations from yodao:" + DEFAULT;
				printed = True;
			key = web.find("key");
			values = web.findall("trans/value");

			key = key.text.strip();
			value = values[0].text.strip();
			if with_color:
				print BOLD +  key + ":\t" + DEFAULT + GREEN + value + NORMAL;
			else:
				print value;
	
def usage():
	print "usage: dict.py word_to_translate";

def main(argv):
	if len(argv) <= 0:
		usage();
		sys.exit(1);
	xml = crawl_xml(" ".join(argv));
	print_translations(xml, True);

if __name__ == "__main__":
	main(sys.argv[1:]);
