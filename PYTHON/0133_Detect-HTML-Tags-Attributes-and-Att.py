#09/09/2026
#Easy
#Detect HTML Tags, Attributes and Attribute Values
# HackerRank: Use the HTMLParser standard library to extract tags and attributes.

from html.parser import HTMLParser

class CustomHTMLParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        print(tag)
        for attr, value in attrs:
            print(f"-> {attr} > {value}")
            
    def handle_startendtag(self, tag, attrs):
        print(tag)
        for attr, value in attrs:
            print(f"-> {attr} > {value}")

n = int(input())
html_content = ""
for _ in range(n):
    html_content += input() + "\n"

parser = CustomHTMLParser()
parser.feed(html_content)