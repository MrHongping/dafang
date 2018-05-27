s='''<root>
<T>MYSQL</T>
<H>localhost</H>
<U>root</U>
<P>password</P>
<L>utf8</L>
</root>'''

from xml.etree import ElementTree

def print_node(node):
    print "node.tag:%s" % node.tag
    print "node.text:%s" % node.text

root=ElementTree.fromstring(s)
node_find = root.find('T')
print_node(node_find)