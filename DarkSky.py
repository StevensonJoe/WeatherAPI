print('---START---')
import time
start = time.time()
import urllib.request
import urllib.parse
import json
import os
import os.path
import sys
from datetime import datetime, timedelta
from time import sleep

# gust over 40 = closed port
sites = {'Southampton':'50.909507,-1.435869','Felixstowe':'51.946177,1.323400','London Gateway':'50.911605,-1.457433','Tilbury':'51.457349,0.35174'}
filelocation = ''
apikey = ''

def GetInfo(sitecoords,name):

    fail = False

    url = f'https://api.darksky.net/forecast/{apikey}/{sitecoords}s?units=uk2&exclude=[minutely,flags]' 
    url=url
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req) as response:
            json_string = response.read()
        parsedjson = json.loads(json_string)
                
    except urllib.error.HTTPError as e:
        print('HTTP Error, check logs')
        print(str(e))
        f = open(f'{filelocation}','a')
        f.write(str(datetime.now())[:19]+'\n'+str(e)+'\n\n')
        f.close()
        print(str(datetime.now())[:19]+'\n'+str(e)+'\n\n')
        fail = True
        return fail

    except urllib.error.URLError as e:
        print('URL Error, check logs')
        print(e)
        f = open(f'{filelocation}\\darksky\\errorlogs.txt','a')
        f.write(str(datetime.now())[:19]+'\n'+str(e)+'\n\n')
        f.close()
        print(str(datetime.now())[:19]+'\n'+str(e)+'\n\n')
        fail = True
        return fail
    
    except WindowsError as e:
        print('undefined windows error, check logs')
        print(e)
        f = open(f'{filelocation}\\darksky\\errorlogs.txt','a')
        f.write(str(datetime.now())[:19]+'\n'+str(e)+'\n\n')
        f.close()
        print(str(datetime.now())[:19]+'\n'+str(e)+'\n\n')
        fail = True
        return fail
    
    if 'parsedjson' in locals() or 'parsedjson' in globals():
        Alerts(parsedjson,name)
    else:
        print('unknown failure')
        fail = True
        return fail
    

def Alerts(parsedjson,name):   

    if name != 'Southampton':
        f = open(f'{filelocation}\\darksky\\Alerts.txt','a')
        f.write('\n')

    else:           
        f = open(f'{filelocation}\\darksky\\Alerts.txt','w')


    try:
        f.write((parsedjson['alerts'][0]['title'].replace('\n','')))
        f.write(':')
        f.write((parsedjson['alerts'][0]['description'].replace('\n','')))
        

    except KeyError:
        f.write('%s:No Alerts'%(name))

    print(f"{time.time() - start} - {name} - Alerts.txt Complete")
    Currently(parsedjson,name)
    

def Currently(parsedjson,name):
    if name != 'Southampton':
        f = open(f'{filelocation}\\darksky\\Currently.txt','a')
        f.write('\n')
    else:
        f = open(f'{filelocation}\\darksky\\Currently.txt','w')

    f.write(name)
    f.write('\n')
    f.write('Summary:%s'%(parsedjson['hourly']['summary']))
    f.write('\n')
    f.write('Weather:%s'%(parsedjson['currently']['summary']))
    f.write('\n')
    f.write('Visibility:%s'%(parsedjson['currently']['visibility']))
    f.write('\n')
    f.write('Gust:%s'%(parsedjson['currently']['windGust']))
    f.write('\n')    
        

    f.close()


    print(f"{time.time() - start} - {name} - Currently.txt Complete")
    ThisWeek(parsedjson,name)


def ThisWeek(parsedjson,name):    
    if name != 'Southampton':
        f = open(f'{filelocation}\\darksky\\ThisWeek.txt','a')
        f.write('\n\n')
        
    else:
        f = open(f'{filelocation}\\darksky\\ThisWeek.txt','w')


    f.write(name)
    f.write('\n%s\n'%(parsedjson['daily']['summary']))

    for i in parsedjson['hourly']['data']:
        unixtime = i['time']
        f.write(datetime.fromtimestamp(int(unixtime)).strftime('%Y-%m-%d %H:%M:%S'))
        f.write(';')

    f.write('\n')
    for i in parsedjson['hourly']['data']:
        f.write(i['summary'])
        f.write(';')

    f.write('\n')
    for i in parsedjson['hourly']['data']:
        f.write(str(i['visibility']))
        f.write(';')

    f.write('\n')
    for i in parsedjson['hourly']['data']:
        f.write(str(i['windGust']))
        f.write(';')


    print(f"{time.time() - start} - {name} - ThisWeek.txt Complete")
    Daily(parsedjson,name)
    

def Daily(parsedjson,name):
    if name != 'Southampton':
        f = open(f'{filelocation}darksky\\Daily.txt','a')
        f.write('\n\n')
        
    else:
        f = open(f'{filelocation}darksky\\Daily.txt','w')

    f.write(name)
    f.write('\n')

    for i in parsedjson['daily']['data']:
        unixtime = i['time']
        f.write(datetime.fromtimestamp(int(unixtime)).strftime('%Y-%m-%d %H:%M:%S'))
        f.write(';')

    f.write('\n')
    for i in parsedjson['daily']['data']:
        f.write(i['summary'])
        f.write(';')

    f.write('\n')
    for i in parsedjson['daily']['data']:
        f.write(str(i['windGust']))
        f.write(';')
    print(f"{time.time() - start} - {name} - Dailytemp.txt Complete")

def SuccessfulRestart():
        sleeptime = 3600
        futuredate = datetime.now() + timedelta(seconds=sleeptime)
        print('')
        print(datetime.now().strftime('Previous Run Completed: %H:%M:%S %d/%m/%y'))
        print(futuredate.strftime('Next Run Time: %H:%M:%S %d/%m/%y'))
        print('\nwaiting...\n\n')
        sleep(sleeptime)
        print('------------RESTART------------\n\n')    


class mainClass():
    def __init__(self):
        for name,sitecoords in sites.items():
            print(name)
            fail = GetInfo(sitecoords,name)
            if fail == True:
                print('Failed to get info, trying again')
                #ProxyTest()
                sys.exit('quit')
                return
        else:
            #fail = ReplaceFiles()
            if fail == True:
                sys.exit('quit')
                return
            else:
                SuccessfulRestart()

if __name__ == "__main__":
    while True:
        mainClass()
