s='''<?xml version="1.0" encoding="utf-8"?>
<T>XDB</T>
<X>com.mysql.jdbc.Driverjdbc:mysql://localhost/test?user=rootpassword=123456</X>'''

import xml.dom.minidom as xmldom
print xmldom.parseString(s)