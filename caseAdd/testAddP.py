from com.android.monkeyrunner import MonkeyRunner,MonkeyDevice,MonkeyImage
from datetime import datetime
import os,sys


def currentTime():
    #timeC = time.ctime()
    timeC = datetime.now().__str__()
    return timeC

def Log(str):
    now=currentTime()
    try:
        logs = open('./test/logs.txt','a')
        logs.write('*'*50+'\n')
        logs.write("["+now+"]"+'\t'+str+'\n')
        #print "["+now+"] "+str+'\n',
        sys.stdout.write("["+now+"] "+str+'\n')
        logs.close()
    except IOError:
        print "log read/write error, "
        
def ConnectDevice():
    try:
        Log('wait for connect device')
        device = MonkeyRunner.waitForConnection()
        Log('device connect success')
    except:
        Log('device connect faild')
    device.wake()
    device.press('KEYCODE_HOME')
    MonkeyRunner.sleep(5)
    return device

def AddContacts(device):
   
    device.startActivity(component = 'com.android.contacts/.activities.PeopleActivity')
    MonkeyRunner.sleep(3)
    Log('contacts application launch success')
    
    screen = device.takeSnapshot()
    Log('next step: add a new contact')
    subScreen = screen.getSubImage((94,285,291,264))
    MonkeyRunner.sleep(3)
    firstScreen = MonkeyRunner.loadImageFromFile('./test/firstScreen.png')
    Log('is there any contact record on the device?')
    isFirstAddContact = subScreen.sameAs(firstScreen,0.9)
    if isFirstAddContact:
        Log('No,it is first time add contact ')
        firstAddContact(device)
        
    else:
        Log('Yes,already have record on the device')
        unFirstAddContact(device)
            
    AddContactDetail(device)
    
def AddContactDetail(device):

    Log('now adding contact detail')
    device.touch(150,220,'DOWN_AND_UP')
    device.type('Test'+ str(1))
    Log('add contact name')
    MonkeyRunner.sleep(2)
    device.touch(150,410,'DOWN_AND_UP')
    device.type(str(1)+"123456789")
    Log('add contact number')
    MonkeyRunner.sleep(2)
    device.touch(150,610,'DOWN_AND_UP')
    device.type('user'+str(1)+'@yyy.com')
    Log('add contact email address')
    MonkeyRunner.sleep(2)
    device.touch(60,60,'DOWN_AND_UP')
    MonkeyRunner.sleep(5)

    screenShot = device.takeSnapshot()
    Log('show contact detail information')
    MonkeyRunner.sleep(5)
    detailInfoScreenShot = screenShot.getSubImage((0,365,465,300))
    MonkeyRunner.sleep(1)
    detailInfo = MonkeyRunner.loadImageFromFile('./test/DetailInfo.png')
    MonkeyRunner.sleep(1)
    compareDetailInfo = detailInfoScreenShot.sameAs(detailInfo)
    if compareDetailInfo:
        Log('detail information add fail')
    else:
        Log('detail information add success!')
    

def CheckData(device):
    device.touch(30,60,'DOWN_AND_UP')
    MonkeyRunner.sleep(3)
    Log('turn to People main activity')
    screenShot = device.takeSnapshot()
    MonkeyRunner.sleep(3)
    contactsCount = screenShot.getSubImage((345,120,90,30))
    Log('next step: compare contact count  ')
    MonkeyRunner.sleep(1)
    if os.path.exists('./test/contactsCount.png'):
        Log('now compare contact count 2')
        lastContactCount = MonkeyRunner.loadImageFromFile('./test/contactsCount.png')
        MonkeyRunner.sleep(1)
        #compare last contact count graphic with new contact count graphic
        #differect means add operation success.
        compareCount= contactsCount.sameAs(lastContactCount)
        if compareCount:
            Log('many record exists, data check failed ')
        else:
            Log('many record exists, data check success ')
    else:
        Log('now compare contact count 1')
        oneContact=MonkeyRunner.loadImageFromFile('./test/oneContact.png')
        MonkeyRunner.sleep(1)
        compareCount= contactsCount.sameAs(oneContact)
        if compareCount:
            Log('only one record,Data check success')
        else:
            Log('only one record,Data check failed')
        

def EndOfAddOperate(device):
    #device = MonkeyRunner.waitForConnection()
    device.shell('am force-stop com.android.contacts')
    MonkeyRunner.sleep(3)
    Log('destroy current contacts application')
    resultHome = device.takeSnapshot()
    MonkeyRunner.sleep(3)
    homeScreen = MonkeyRunner.loadImageFromFile('./test/home.png')
    
    if resultHome.sameAs(homeScreen,0.98):
        Log('back to Home screen')
        Log('case executed success')
    
    else:
        Log('case executed failed')
        
    
def firstAddContact(device):
    Log('choose create new contact')
    device.touch(200,310,'DOWN_AND_UP')
    MonkeyRunner.sleep(3)
    Log('contacts information will keep local')
    device.touch(140,480,'DOWN_AND_UP')
    MonkeyRunner.sleep(3)
    
    
def unFirstAddContact(device):
    #device = MonkeyRunner.waitForConnection()
    screenShot = device.takeSnapshot()
    MonkeyRunner.sleep(3)
    contactsCount = screenShot.getSubImage((345,120,90,30))
    contactsCount.writeToFile('./test/contactsCount.png','png')
    Log('ready to insert contact info')
    device.touch(420,760,'DOWN_AND_UP')
    Log('login in contact information edit page')
    MonkeyRunner.sleep(3)
    

    
def main():
    try:
        d = ConnectDevice()
        AddContacts(d)
        CheckData(d)
        EndOfAddOperate(d)
    except:
        Log('case executed failed')
        
if __name__ == '__main__':
    main()
#    caseFile = open('./test/case.txt','r')
#    for case in caseFile:

