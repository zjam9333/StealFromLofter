#coding=utf-8
import requests
import json
import os
from multiprocessing import Pool

myFilePath = "savedPhotos"

def downloadfile(savepath, url):
    if os.path.exists(savepath):
        # print 'exist:' +savepath
        return True
    print 'downloading:' + savepath + ", from:" + url
    res = requests.get(url, stream = True)
    with open(savepath, 'wb') as savefile:
        for chunk in res.iter_content(chunk_size = 128):
            savefile.write(chunk)
    print 'finish:' + savepath
    return True


if __name__ == "__main__":
    url = 'http://api.lofter.com/v1.1/batchdata.api?product=lofter-iphone-6.1.1'
    headers = {
        'Host':'api.lofter.com',
        'secruityinfo':'''{"id_ver":"IOS_1.0.8","rk":"QyGdIhaThmxuNEDqqi4dQU\/Q2N575kI7A1aA7h+kM0dESSRm9Fh+LBYpYWkHPudP5litpbXcsdKHUKQn0kNJTE+iXGOXdfRt4fkrcPxW6rJ8oTCv3Zh4M8HIVzt8X0U8UsnsJ5JixdW3XhszhZSQ3nLR\/yDLeXFXDs9BXYwNRas=","rdata":"vuOM7gqyqIntSPAtitbBNcV3+HnHkFT7b6m9jR3LiQGnKOH\/z3fCyAjK64xJ1x6wvyp89FPM1vH0UaqbaqqYJ69nyIS8lRF\/t+2PE+vlbNCfFu81p5HLVofiLtUeYCU6kK8tGnfv7B2SYKx+7vU9p72Jvf4mtaQLU5ovSp2buyJhKYj8qFYd\/Ky++bgLExSb","datatype":"aimt_datas"}''',
        'Accept':'*/*',
        'Authorization':'ThirdParty TZFQwlEgO-L-s6d9E8Dhx1nDf3jcpg2zXOLl_54hxmGEsRr1kOeLy93XC1aDwdwSmEeZTqpAK1Vu%0Aif1fWN52D7mOsslD2zJ2',
        'Accept-Encoding':'gzip, deflate',
        'Content-Type':'application/x-www-form-urlencoded;charset=utf-8',
        'Accept-Language':'zh-Hans-CN;q=1',
        'deviceid':'765647CF-BE8D-46A3-BC6A-ED1048FD241E',
        'dadeviceid':'f849feadf85a8ad13a3cd828f35b8c8bbff51ae1',
        'User-Agent':'LOFTER/6.0.8 (iPhone; iOS 9.3.3; Scale/2.00)',
        'Cookie':'NTESwebSI=70A55C791961E21A414E2FEE8C7089C8.hzayq-lofter56.server.163.org-8010',
        'Connection':'keep-alive',
    }
    data = {
        'limit':1000,
        'method':'favorites',
        'offset':0,
        'postdigestnew':1,
        'supportposttypes':'1,2,3,4,5,6',
        'targetblogid':'507382434',
        'targetblognickname':'Jam.',
    }
    response = requests.post(url, headers=headers, data=data)
    response = json.loads(response.content)
    response = response['response']
    items = response['items']
    if not os.path.exists(myFilePath):
        os.mkdir(myFilePath)
    pool = Pool(50)
    for oneitem in items:
        if oneitem == None:
            continue
        postobj = oneitem.get('post')
        
        tag = postobj['tag']
        noticeLinkTitle = postobj.get('noticeLinkTitle')
        basefilename = tag
        if noticeLinkTitle:
            basefilename = noticeLinkTitle + '-' + basefilename
        photolinks = postobj['photoLinks']
        # print photolinks
        photolinks = json.loads(photolinks)
        count = len(photolinks)
        for x in range(count):
            photoobj = photolinks[x]
            # print str(photoobj) + "\n\n"
            photoid = photoobj.get('id')
            orignSp = photoobj['orign'].split('?')
            rawurl = orignSp[0]

            filename = basefilename + '-' + str(x) + '-' + str(photoid) + '.jpg'
            filename = filename.replace("/","")
            filepath = myFilePath+'/'+filename
            
            # downloadfile(filepath, rawurl)
            pool.apply_async(func=downloadfile, args=(filepath, rawurl,))
    pool.close()
    pool.join()  
    print "ojbk"





    