import requests
#
# def downloadFile(path):
#     chunk_size=1024
#     payload = {'sqzr': 'F', 'z1': path, 'z0': 'UTF-8'}
#     response = requests.post('http://192.168.127.136:8080/examples/jsp/one.jsp', data=payload,stream=True)
#     print type(response.status_code)
#     print response.raw.data
#     # print response.headers
#     for data in response.iter_content(chunk_size=chunk_size):
#         # print data
#         yield data
#
# for i in downloadFile('/root/Downloads/apache-tomcat-7.0.85/webapps/examples/WEB-INF/lib/taglibs-standard-impl-1.2.5.ar'):
#     print len(i)

data='/1234/5678/9/123'
dl=data.split('/')
print dl[len(dl)-1]

for x in range(1,5):
    print x