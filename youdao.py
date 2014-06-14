#! /usr/bin/python
import re;
import urllib;
import urllib2;
import sys;
import xml.etree.ElementTree as ET;
def debug():
	xml = open("word.xml").read();
	print get_text(xml);
	print get_elements_by_path(xml, "custom-translation/content");
	#print_translations(xml, False, False);
def get_elements_by_path(xml, elem):
	if type(xml) == type(''):
		xml = [xml];
	if type(elem) == type(''):
		elem = elem.split('/');
	if (len(xml) == 0):
		return [];
	elif (len(elem) == 0):
		return xml;
	elif (len(elem) == 1):
		result = [];
		for item in xml:
			result += get_elements(item, elem[0]);
		return result;
	else:
		subitems = [];
		for item in xml:
			subitems += get_elements(item, elem[0]);
		return get_elements_by_path(subitems, elem[1:]);
# <![CDATA[ patent ]]>
textre = re.compile("\!\[CDATA\[(.*?)\]\]", re.DOTALL);
def get_text(xml):
	match = re.search(textre, xml);
	if not match:
		return xml;
	return match.group(1);
def get_elements(xml, elem):
	p = re.compile("<" + elem + ">" + "(.*?)</" + elem + ">", re.DOTALL);
	it = p.finditer(xml);
	result = [];
	for m in it:
		result.append(m.group(1));
	return result;
GREEN = "\033[1;32m";
DEFAULT = "\033[0;49m";
BOLD = "\033[1m";
UNDERLINE = "\033[4m";
NORMAL = "\033[m";
RED = "\033[1;31m"
def crawl_xml(queryword):
	return urllib2.urlopen("http://dict.yodao.com/search?q="
        + urllib.quote_plus(queryword) + "&doctype=xml").read();
def print_translations(xml, with_color, detailed):

	root = ET.fromstring(xml);
	original_query = root.find("original-query");
	queryword = original_query.text;

	custom_translations = root.findall("custom-translation");
	print BOLD + UNDERLINE + queryword + NORMAL;
	translated = False;
	
	for cus in custom_translations:
		source = cus.find("source/name");
		print RED + "Translations from " + source.text + DEFAULT;
		contents = cus.findall("translation/content");
		if with_color:
			for content in contents[0:5]:
				print GREEN + content.text + DEFAULT;
		else:
			for content in contents[0:5]:
				print content.text;
		translated = True;

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
		#debug();
		sys.exit(1);
	xml = crawl_xml(" ".join(argv));
	print_translations(xml, True, False);

if __name__ == "__main__":
	main(sys.argv[1:]);
