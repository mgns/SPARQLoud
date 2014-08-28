import sys, io
from urllib2 import HTTPError, URLError

def store(query, uri, num, id):

    url=None
    file_name = "data.ttl"

    registry = "wiss:feed" + str(id) +  " a wiss:Feed ; \n wiss:query " + query + " ; " + "\n" + "wiss:endpoint " + uri + " ; " + "\n" + "wiss:number " + num + ". \n";
    # saves the results to a file
    try:
        local_file = open(file_name, "a+")
        local_file.write(registry)
        local_file.close()
        #with open(file_name, "a+") as local_file:
        #file_name.write(registry)

        print "saved to file" + file_name
    #handle errors
    except HTTPError, e:
        print "HTTP Error:", e.code, url
    except URLError, e:
        print 'URL Error:', e.reason, url


query = "test1"
uri = "test2"
num = "test3"
id = 4
store (query, uri, num,id)