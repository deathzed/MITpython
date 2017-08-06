#coding=utf-8
# This python file defines 3 picture getting python functions
from cassandra.cluster import Cluster
                                     #Econnect cassandra
cluster = Cluster(["127.0.0.1"])
session = cluster.connect("k1")


def pic_airplane():
	import json
	import requests
	payload = {'date':'2016-05-17','key':'d39de78b6bbe7aa8fcc3b2b3a2171b4a95171e85'}
	r = requests.get("https://gateway-a.watsonplatform.net/visual-recognition/api/v3/classify?api_key=d39de78b6bbe7aa8fcc3b2b3a2171b4a95171e85&url=https://static.independent.co.uk/s3fs-public/styles/article_small/public/thumbnails/image/2017/05/08/08/comacc919.png&version=2016-05-17'.", params=payload)
	a=r.json()
	watson_result = json.dumps(a,sort_keys=True,ensure_ascii=False,indent=4)
	return watson_result

def pic_ball():
	import json
	import requests
	payload = {'date':'2016-05-17','key':'d39de78b6bbe7aa8fcc3b2b3a2171b4a95171e85'}
	r = requests.get("https://gateway-a.watsonplatform.net/visual-recognition/api/v3/classify?api_key=d39de78b6bbe7aa8fcc3b2b3a2171b4a95171e85&url=https://thumbs.dreamstime.com/b/golden-football-ball-23600413.jpg&version=2016-05-17'.", params=payload)
	a=r.json()
	watson_result = json.dumps(a,sort_keys=True,ensure_ascii=False,indent=4)
 	return watson_result

def pic_book():
	import json
	import requests
	payload = {'date':'2016-05-17','key':'d39de78b6bbe7aa8fcc3b2b3a2171b4a95171e85'}
	r = requests.get("https://gateway-a.watsonplatform.net/visual-recognition/api/v3/classify?api_key=d39de78b6bbe7aa8fcc3b2b3a2171b4a95171e85&url=http://admin.emanuelnyc.org/sps/var/images/image_lg_1380.jpg&version=2016-05-17'.", params=payload)
	a=r.json()
	watson_result = json.dumps(a,sort_keys=True,ensure_ascii=False,indent=4)
	return watson_result


def get_sound_text(name):
    '''
        This function accepts one string name and returns the string that the audio file refers to.
        name can be any 8 values below:
        name_list = ['airplane','ball','book','helicopter','laptop','ocean','strawberry','train']
    '''
    import json
    from os.path import join, dirname
    from watson_developer_cloud import SpeechToTextV1
    
    name_list = ['airplane','ball','book','helicopter','laptop','ocean','strawberry','train']
    if name not in name_list:
        return 'You gave "name" a wrong value, it is not in our list' 
    
    speech_to_text = SpeechToTextV1(
            username='de53e458-2f1e-4cd3-8c7a-6502446bbff9',
            password='WWr0X6RJZXnd',
            x_watson_learning_opt_out=False
	)
    with open(join(dirname(__file__), '/home/steve/Documents/Presentation/request_sound/'+name+'.mp3'),
          'rb') as audio_file:
    		watson_result = json.dumps(speech_to_text.recognize(
        	audio_file, content_type='audio/mp3', timestamps=False,
        	word_confidence=True),
	indent=2)
        
    print('Watson\'s sound guessing result is: ')
    print(watson_result)            # Here we get watson's result and we print watson's result 
    
    resultstr = str(watson_result)      # Below we slice the result and keep the string that the sound refers to
    resultlist = resultstr.splitlines()
    for i in resultlist:
		if "transcript" in i:
			termstr = i # termstr contains "transcript": "correct_word"(it's our word)
    start_index = termstr.find(': "')
    rm_start_str = termstr[start_index+3:]
    end_index = rm_start_str.find('"') 
    return rm_start_str[:end_index-1]       # The return value is exactly the string that the sound refers to


pic_choice = raw_input( 'Please choose a picture, you can enter a number 1,2, or 3: ')
if pic_choice == '1':
    resultstr = str(pic_airplane())
if pic_choice == '2':
    resultstr = str(pic_ball())
if pic_choice == '3':
    resultstr = str(pic_book())
if (pic_choice!='1')and(pic_choice!='2')and(pic_choice!='3'):
    print 'You have entered a picture number that is not in our list'


audio_result = raw_input('''Please enter a choice, 
the choices are: 
name_list = ['airplane','ball','book','helicopter','laptop','ocean','strawberry','train'] 
            ''')
            # now we have completed the user input, next: get watson results
            
resultlist = resultstr.splitlines()
a = '                            "'
for item in resultlist:
    if (': ' not in item):
        resultlist.remove(item)
for item in resultlist:
    if (('{' in item)or('}' in item)):
        resultlist.remove(item)
for item in resultlist:
    if item[:len(a)]!=a:
        resultlist.remove(item)
for item in resultlist:
    if (('images' in item)or('classes' in item)or('classifier_id' in item)or('source_url' in item)or('images_processed' in item)or('type_hierarchy' in item)or('],' in item)):
        resultlist.remove(item)
					#Now we have removed the lines that we do not want
class1 = []
score0 = []
for item in resultlist:
    if "class" in item:
        begin_index = item.find(': ')+3
        end_index = item.find('",')
        class1.append(item[begin_index:end_index])
for item in resultlist:
    if "score" in item:
        begin_index = item.find(': ')+2
        end_index = begin_index+5
        score0.append(item[begin_index:end_index])
for item in score0:
    if ',' in item:
        end = item.find(',')
        score0[score0.index(item)] = item[:end]
for item in class1:
    if item =='':
        class1.remove(item)
        
score1=[]
for i in score0:
    tem = float(i) 
    score1.append(tem)
            # now we have got the picture result, we are going to write results in cassandra
'''    
dict = {}    
for i in range(len(class1)):
    dict[class1[i]] = float(score1[i])
'''

print 'Watson\'s picture guessing result is: '
for i in range(len(class1)):
    a=class1[i]
    b=score1[i]
    query1 = "INSERT into mit_2 (value,key) values(?,?)"
    prepare1 = session.prepare(query1)
    print 'class:',a,'score:',b
    session.execute(prepare1,[b,a])

query2 = "SELECT * from mit_2 where key = ? allow filtering"
prepare2 = session.prepare(query2)
return_value = []


audio_str = get_sound_text(audio_result)
            # now we get watson sound result
temp=session.execute(prepare2,[audio_str])
return_value.append(temp)
            

print "_______________________________________"
print ' '
print "The results are here:"
print "your audio guess is " +audio_str


judge = False

for i in return_value:
    for j in i:
        if (j.value>0.5):
            print 'Yeah! you guess it! the picture is ', str(j.key)
            judge = True
       
if judge ==False:
    print "Your guess is not correct, the picture is not "+audio_str





















