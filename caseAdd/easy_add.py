from com.android.monkeyrunner import MonkeyRunner, MonkeyDevice
from com.android.monkeyrunner.easy import EasyMonkeyDevice
from com.android.monkeyrunner.easy import By
import os,sys
# import user lib
try:
    for p in os.environ['PYTHONPATH'].split(';'):
       if not p in sys.path:
          sys.path.append(p)
except:
    pass
# import trace module to save and print logs 
from log import trace

# 
logFile = './test/logs.txt'
#

trace=trace(logFile).trace

# Connect to the current device.
device = MonkeyRunner.waitForConnection()

# Use the EasyMonkey API, all methods on device are available in easy_device.
easy_device = EasyMonkeyDevice(device)
def addContact(name,phoneNumber):
    
    device.startActivity(component = 'com.android.contacts/.activities.PeopleActivity')
    MonkeyRunner.sleep(3)
    if  easy_device.visible(By.id('id/create_contact_button')):
        trace('add contact first time')
        addFirstContact()
    
    elif  easy_device.visible(By.id('id/menu_add_contact')):
        
        trace("Location of add contact menu:" + str(easy_device.locate(By.id('id/menu_add_contact'))))
    
        easy_device.touch(By.id('id/menu_add_contact'), MonkeyDevice.DOWN_AND_UP)
        MonkeyRunner.sleep(7)
    else:
        raise Error('Could not find the "menu_add_contact" button')
    addContactDetail(name,phoneNumber)
    
def addContactDetail(name,phoneNumber):  
    easy_device.type(By.id('id/0x3'),name)
    MonkeyRunner.sleep(3)
    easy_device.type(By.id('id/0x17'),phoneNumber)
    easy_device.touch(By.id('id/save_menu_item'),MonkeyDevice.DOWN_AND_UP)
    MonkeyRunner.sleep(7)
    s= easy_device.getText(By.id('id/data'))
    trace('contact add success,phone number:' + s)
    phoneInfo= s.replace('-','').replace(' ','').replace('(','').replace(')','')
    if phoneInfo == phoneNumber:
        trace('contact information check success')
    else:
        trace('contact information add wrong')
        
    device.shell('am force-stop com.android.contacts')
    trace('destroy current contacts application')
def addFirstContact():
    
    easy_device.touch(By.id('id/create_contact_button'),MonkeyDevice.DOWN_AND_UP)
    MonkeyRunner.sleep(6)
    if easy_device.visible(By.id('id/content')):
        easy_device.touch(By.id('id/left_button'),MonkeyDevice.DOWN_AND_UP)
        trace( 'select contact information keep local')
    else:
        MonkeyRunner.sleep(6)


addContact('test1','214234157')


#hierarchy_viewer=device.getHierarchyViewer()
#view_node=hierarchy_viewer.findViewById('id/data')
#print view_node
#text=str(view_node.namedProperties.get('mText'))
#print text
#easy_device.touch(view_node,MonkeyDevice.DOWN_AND_UP)
