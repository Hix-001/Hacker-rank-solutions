#22/08/2026
#Easy
#HTML Parser - Part 1
# HackerRank: Subclass HTMLParser to extract tags and attributes.

from html.parser import HTMLParser

class MyHTMLParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        print(f"Start : {tag}")
        for name, value in attrs:
            print(f"-> {name} > {value}")

    def handle_endtag(self, tag):
        print(f"End   : {tag}")

    def handle_startendtag(self, tag, attrs):
        print(f"Empty : {tag}")
        for name, value in attrs:
            print(f"-> {name} > {value}")

parser = MyHTMLParser()
n = int(input())

for _ in range(n):
    parser.feed(input())
