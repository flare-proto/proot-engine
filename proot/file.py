from xml.dom.minidom import parseString
from xml.dom.minidom import Document

xml_string = "<root><item>Data 1</item><item>Data 2</item></root>"

def parse(text:str) -> Document:
    return parseString(xml_string)

def serialise(dom:Document) -> str:
    return dom.toxml()

dom_tree = parse(xml_string)
# Get the root element
root = dom_tree.documentElement
print(f"Root tag: {root.tagName}")

# Get all 'item' elements
items = dom_tree.getElementsByTagName("item")
for item in items:
    print(f"Item content: {item.firstChild.nodeValue}")

# Optional: Release resources
dom_tree.unlink()