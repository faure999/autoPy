# -*- coding: utf-8 -*-

#Author: Jason Hou
#Date: 2013/06/16
import os,sys
try:
    for p in os.environ['PYTHONPATH'].split(';'):
       if not p in sys.path:
          sys.path.append(p)
except:
    pass

from com.android.monkeyrunner import MonkeyRunner,MonkeyDevice,MonkeyImage
from com.dtmilano.android.viewclient import ViewClient
from log import trace

logPath = r'.\test'
logName = 'case_log.txt'
logFile = logPath + '\\' + logName

trace = trace(logFile).trace

package = 'com.android.contacts'
activity = '.activities.PeopleActivity'
componentName = package + '/' + activity
	
def sleep(duration = 1):
	MonkeyRunner.sleep(duration)

class contacts:
    def __init__(self, device, devID='emulator-5554',sample = False):
        '''if sample is True, take snapshot as expected result.'''
        self.device=device
        self.sample=sample
        self.vc=ViewClient(device, devID)
        #use below code to remove the status bar from the snapshot
        width = int(device.getProperty('display.width'))
        height = int(device.getProperty('display.height'))
        density = device.getProperty('display.density')
        if density == .75:
            statusBarHeight = 19
        elif density == 1.5:
            statusBarHeight = 38
        elif density == 2.0:
            statusBarHeight = 50
        else:
            statusBarHeight = 25
        self.snap_rect = 0, statusBarHeight, width, height - statusBarHeight
	
    def start(self):
        self.device.startActivity(component=componentName)
	
    def getView(self,str,contentDescription=False):
        self.vc.dump()
        if not contentDescription:
            return self.vc.findViewWithText(str)
        else:
            return self.vc.findViewWithContentDescription(str)
			
    def isReady(self):
        while True:
            view=self.getView('Contact list is being updated to reflect the change of language.')
            if not view: 
                break
                sleep(2)
            return True
	
    def isEmpty(self):
        view=self.getView('Create a new contact')
        if view:
            view.touch()
            view=self.getView('Keep local')
            if view:
                view.touch()
                return True
            else:
                return True
        else:
            view=self.getView('Add Contact',True)
            view.touch()
            return True
    def snapshot(self,title):
        snapName = title + '.png' 
        snapFile = logPath + '\\' + snapName
        result = self.device.takeSnapshot().getSubImage(self.snap_rect)
        result.writeToFile(snapFile,'png')
	
    def addContact(self):
        trace('start...')
        self.start()
        sleep(3)
        trace('take snapshot')
        self.snapshot('contact_snap')
		
    def editDetails(self):
        pass
	
    def search(self):
        pass
	
    def sort(self):
        pass
		
    def favorite(self):
        pass
		
    def delete(self,kwd = ''):
        
    	'''delete one contact
    	@kwd : keyword which contact to be delete, if none,delete first contact
    	'''
        NOCONTACT = 'No contacts.'
        self.start()
        trace('launch on contact application')
        sleep(3)
        self.vc.dump()
        if self.getView(NOCONTACT) == None:
            total_contacts=self.vc.findViewById('id/no_id/21')
            trace('launch on success')
            total_contacts_text = total_contacts.getText()
            
            total_amount = int(total_contacts_text.split()[0])
            trace('current contact count:' + total_contacts_text)
            if kwd == '':
                # keyword is empty,delete first contact
                self.vc.dump()
                trace('keyword is none, first contact with be delete')
                find = self.vc.findViewById('id/no_id/27')
                #if find != None:
                
            else :
                # keyword is not none
                # search specifying contact by keyword
                self.vc.dump()
                search = self.vc.findViewWithContentDescription('Search') 
                search.touch()
                self.device.type(kwd)
                trace('searching contact with the keyword : '+ kwd )
                self.vc.dump()
                find = self.vc.findViewById('id/no_id/28')
                trace('')
                # if find != None:
            if find != None:
                # delete operate 
                find.touch()
                sleep(3)
                trace('show contact detail information')
                sleep(1)
                self.device.press('KEYCODE_MENU')
                sleep(4)
                self.vc.dump()
                delete_menu = self.vc.findViewWithText('Delete')
                trace('choose delete contact')
                delete_menu.touch()
                    
                # confirm delete operate
                self.vc.dump()
                ok_menu = self.vc.findViewWithText('OK')
                ok_menu.touch()
                sleep(3)
                # if current activity is not Main Activity back to Main Activity
                self.vc.dump()
                while self.vc.findViewWithContentDescription('All contacts') == None:
                    self.device.press('KEYCODE_BACK')
                    sleep(3)
                    self.vc.dump()
            
            else:
                raise 'Could not find the contact : ' + kwd
                
            #verification the operate 
            self.vc.dump()
            current_contacts=self.vc.findViewById('id/no_id/21')
            if current_contacts != None:
                current_contacts_text = current_contacts.getText()
                trace('operation success.current contact count:' + current_contacts_text)
                no_contacts = self.getView(NOCONTACT)
                if (no_contacts != None) and (total_amount == 1):
                    trace('data verification success. all contacts has been deleted, no record!')
                else:
                    current_amount = int(current_contacts_text.split()[0])
                    if total_amount - current_amount == 1:
                        trace('data verification success')
                    else:
                        trace('data verification failed')
                        raise 'data verification failed, current contacts amount: '+current_contacts_text
            else:
                trace('get contact amount failed')
                
        else:
            trace('no contact exists')
            raise 'Could not find any contact data,no record!'
        
if __name__ == '__main__':
	device=MonkeyRunner.waitForConnection()
	print 'test'
	c=contacts(device)
	c.delete()
