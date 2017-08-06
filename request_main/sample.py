from cassandra.cluster import Cluster

//....

                                      //connect cassandra

cluster = Cluster(["10.178.209.161"])
session = cluster.connect()
keyspacename = "demo_space"

                                      //create  table

session.execute(CREATE TABLE users (
  user_id text PRIMARY KEY,
  first_name text,
  last_name text,
  
);

 
                                       // use keyspace; create a sample table
session.set_keyspace(keyspacename)

s = session


file_object = open('pic.txt')           //  read piecture final answer ,save 
pic_text = readline("pic.txt")
file_object.close( )



 s.execute("CREATE TABLE list_test (a ascii PRIMARY KEY, b list<blob>)")


audio=file_object.read(’ardio.text‘)      //  read audio final answer , save 
pic_text = file_object.readline ("pic.txt")
file_object.close( )


s.execute("INSERT INTO list (a, b) VALUES (%s, %s)", pic_text,pic_text)


bool ans = cmp(sStr1,sStr2)
if ans ==1
		print('正确')
 	else
 		print（'错误'）










