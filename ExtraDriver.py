from functools import wraps
import win32com.client
import time

def dispatched_functions(function_decorator):
    def decorator(cls):
        for name, obj in vars(cls).items():
            if callable(obj):
                try:
                    obj = obj.__func__
                except AttributeError:
                    pass
                setattr(cls, name, function_decorator(obj))
        return cls
    return decorator

def on_call(func):
    @wraps(func)
    def wrapper(*args, **kw):
        #print('{} called'.format(func.__name__))
        try:
            res = func(*args, **{'funcName':func.__name__})
        finally:
            pass
            #print('{} finished'.format(func.__name__))
        return res
    return wrapper

@dispatched_functions(on_call)
class attachMate(object):
    def __init__(self,sessionPath='',timeOutValue=2000,*args, **kwargs):
        self.sessionPath=sessionPath
        self.system = win32com.client.Dispatch("EXTRA.System")
        self.system.TimeoutValue=500
        self.ActiveSession=None
        self.Screen=None

    def getActiveSession(self,**kwargs):
        '''
        Description:

            return the active session

        '''
        self.ActiveSession=self.system.ActiveSession
        return self.ActiveSession
        def Screen(self,**kwargs):
            '''
            Description:

            return the screen of the active session

            '''
        
            return self.ActiveSession.Screen

    def Open(self,sessionPath,**kwargs):

        '''
        Description:

            Open the session

        '''
        sess=getattr(self.system.Sessions,kwargs['funcName'])(session)
        sess.Visible=True

    def OpenExtraSession(self,sessionPath,timeout=12,**kwargs):
        '''
        Description:

            Open the session in the "sessionPath", has a timeout default 6 seconds to wait that the session is already open

        Ex:

            session=attachMate().OpenExtraSession('../as400-demostracion.edp')

        '''
        from os import system
        if '/' in sessionPath: sessionSplitedPath=sessionPath.split('/')
        elif '\\' in sessionPath: sessionSplitedPath=sessionSplitedPath.split('\\')
        sessionPathURL = sessionPath.replace(sessionSplitedPath[-1],'')
        from subprocess import Popen
        import time
        p = Popen(sessionSplitedPath[-1], shell=True,cwd=sessionPathURL)
        time.sleep(timeout)
        self.ActiveSession=self.system.ActiveSession
        return self.ActiveSession

    def Quit(self,**kwargs):
        '''
        Description:

            Closes all sessions and EXTRA! programs.
        '''
        getattr(self.system,kwargs['funcName'])()

    def Time(self,**kwargs):
        '''
        Description:

            Returns the current system time.
        '''
        return getattr(self.system ,kwargs['funcName'])()

    def ViewStatus(self,**kwargs):
        '''
        Description

            Starts the Status program.
        '''
        return getattr(self.system ,kwargs['funcName'])()

class TextNotFound(Exception):
    def __init__(self, m):
        self.message = m
    def __str__(self):
        return self.message

@dispatched_functions(on_call)
class extradriver(object):
    def __init__(self,attachMateSession, *args, **kwargs):
        self.sessionDriver=attachMateSession
        self.screenDriver=self.sessionDriver.Screen

    def Activate(self,**kwargs):
        '''
        Description:
            Makes the specified session the active window.
        
        Ex:
            attachMate().OpenExtraSession('YourSessionPath/as400-demostracion.edp')
            session=attachMate().getActiveSession()
            xdriver=extradriver(session)
            xdriver.Activate()
        '''
        getattr(self.sessionDriver,kwargs['funcName'])

    ##def add

    def Area(self,StartRow,StartCol,EndRow,EndCol,**kwargs):
        '''
        Description:
            Returns an Area object with the defined coordinates
        Ex:
            attachMate().OpenExtraSession('YourSessionPath/as400-demostracion.edp')
            session=attachMate().getActiveSession()
            xdriver=extradriver(session)
            area=xdriver.Area(2,47,3,60)
        '''
        return getattr(self.screenDriver,kwargs['funcName'])(StartRow,StartCol,EndRow,EndCol)

    def CaptureSetup(self,FileName='captured.log',Append=True,EnableCapture=True,StripEscSeq=True,**kwargs):
        '''
        Description:

            Determines how captured data will be written to a file.
        Ex:

            attachMate().OpenExtraSession('YourSessionPath/as400-demostracion.edp')
            session=attachMate().getActiveSession()
            xdriver=extradriver(session)
            xdriver.CaptureSetup()
            
        Optional params:

            Element         Description
            
            FileName        Sets the name of the file to which captured data will be written.
            Append          If the Boolean value appendBool is TRUE, appends data to the end of the file specified by FileName. If FALSE, overwrites any data previously stored in the file.
            EnableCapture   If the Boolean value enableBool is TRUE, allows data to be captured to file. If FALSE, disables data capture.
            StripEscSeq     If the Boolean value stripBool is TRUE, strips escape sequences from captured data before writing it to file.
        '''
        return getattr(self.sessionDriver,kwargs['funcName'])(FileName,Append,EnableCapture,StripEscSeq)

    ##Aply to waits
    ##def Clear(self,**kwarg):
    ##    pass

    def ClearComm(self,**kwargs):
        '''
        Description:

        Empties the communications buffers, and clears any outstanding conditions that could prevent transmitting or receiving data. It also cancels any escape sequence processing.

        Ex:

            attachMate().OpenExtraSession('YourSessionPath/as400-demostracion.edp')
            session=attachMate().getActiveSession()
            xdriver=extradriver(session)
            xdriver.ClearComm()
        '''
        getattr(self.sessionDriver,kwargs['funcName'])()

    def ClearHistory(self,**kwargs):
        '''
        Description:

        Removes all information from the History buffer.

        Ex:

            xdriver=extradriver(session)
            xdriver.ClearHistory()
        '''

        getattr(self.sessionDriver,kwargs['funcName'])()
    
    def ClearScreen(self,**kwargs):
        '''
        Description

            Clears display memory and sets all line attributes to normal.

        Ex:

            xdriver=extradriver(session)
            xdriver.ClearScreen()

        '''
        getattr(self.screenDriver,kwargs['funcName'])()

    def Close(self, **kwargs):
        '''
        Description:

            Closes the session.

        Ex:
        
            xdriver=extradriver(session)
            xdriver.Close()

        '''
        getattr(self.sessionDriver,kwargs['funcName'])()

    ## se aplica a sessions
    #def CloseAll(self, **kwargs):

    def CloseEx(self,options,**kwargs):
        '''
        Description:

            Closes the session.

        Example:

            attachMate().OpenExtraSession('YourSessionPath/as400-demostracion.edp')
            session=attachMate().getActiveSession()
            xdriver=extradriver(session)
            xdriver.CloseEx(1)

        Params:

            Use this value      To do this
            
            1                   Disconnect session without displaying a prompt
            4                   Save session while exiting
            8                   Exit session without saving
            16                  Prompt user to save session

        '''
        getattr(self.sessionDriver,kwargs['funcName'])(options)

    #Se aplica a sessions
    #def CloseAll(self,**kwargs):

    def ClosePrintJob(self,**kwargs):
        '''
        Description:

        Indicates the end of a print job, forces immediate printing of accumulated printer data from the print buffers, and sends a form feed to the print job, ejecting the current page.

        '''

        getattr(self.sessionDriver,kwargs['funcName'])()

    def Copy(self,StartRow,StartCol,EndRow,EndCol,**kwargs):
        '''
        Description:

            Copies the select text to the Clipboard but leaves the selected text unchanged in the display.

        Ex:

            attachMate().OpenExtraSession('YourSessionPath/as400-demostracion.edp')
            session=attachMate().getActiveSession()
            xdriver=extradriver(session)
            xdriver.Copy(3,47,4,60)

        '''
        self.Area(StartRow,StartCol,EndRow,EndCol).Select()
        getattr(self.screenDriver,kwargs['funcName'])()

    def CopyAppend(self,StartRow,StartCol,EndRow,EndCol,**kwargs):
        '''
        Description:

            Copies the selected text from a session to the existing contents of the Clipboard but leaves the selected text unchanged in the display.

        Ex:
        
            attachMate().OpenExtraSession('YourSessionPath/as400-demostracion.edp')
            session=attachMate().getActiveSession()
            xdriver=extradriver(session)
            xdriver.CopyAppend(3,47,4,60)

        '''
        self.Area(StartRow,StartCol,EndRow,EndCol).Select()
        getattr(self.screenDriver,kwargs['funcName'])()

    def Cut(self,StartRow,StartCol,EndRow,EndCol,**kwargs):
        '''
        Description:

            Removes selected text from the session and stores it in the Clipboard.


        Ex:
        
            attachMate().OpenExtraSession('YourSessionPath/as400-demostracion.edp')
            session=attachMate().getActiveSession()
            xdriver=extradriver(session)
            xdriver.Cut(6,53,6,57)

        '''
        self.Area(StartRow,StartCol,EndRow,EndCol).Select()
        getattr(self.screenDriver,kwargs['funcName'])()

    def CutAppend(self,StartRow,StartCol,EndRow,EndCol,**kwargs):
        '''
        Description:

            Removes selected text from a session and appends it to the existing contents of the Clipboard.

        Ex:
        
            attachMate().OpenExtraSession('YourSessionPath/as400-demostracion.edp')
            session=attachMate().getActiveSession()
            xdriver=extradriver(session)
            xdriver.CutAppend(6,53,6,57)

        '''
        self.Area(StartRow,StartCol,EndRow,EndCol).Select()
        getattr(self.screenDriver,kwargs['funcName'])()


    def Delete(self,StartRow,StartCol,EndRow,EndCol,**kwargs):
        '''
        Description:

            Deletes the current selection.

        Ex:
        
            attachMate().OpenExtraSession('YourSessionPath/as400-demostracion.edp')
            session=attachMate().getActiveSession()
            xdriver=extradriver(session)
            xdriver.Delete(6,53,6,57)

        '''
        self.Area(StartRow,StartCol,EndRow,EndCol).Select()
        getattr(self.screenDriver,kwargs['funcName'])()

    def EnlargeFont(self,**kwargs):
        '''
        Description:

            Increases the session font size by one increment.

        '''
        getattr(self.sessionDriver,kwargs['funcName'])()

    def FieldAttribute(self,row,column,**kwargs):
        '''
        Description:

            Returns the field attribute value for a given row/column position on the current screen. Returns zero if an invalid row or column is provided, or if the current screen does not contain field formatting. Valid only for 3270 or 5250 emulation types.

        '''
        #TODO: Preguntar que significan estos atributos
        return getattr(self.screenDriver,kwargs['funcName'])(row,column)

    ## applies to systemsession object
    # def GetDirectory ()

    def GetString(self,row,column,length,**kwargs):
        '''
        Description:

            Returns the text from the specified screen location.

        Ex:

            session=attachMate().getActiveSession()
            xdriver=extradriver(session)
            xdriver.GetString(6,53,25)
        
        '''
        initialRow=row
        initialColumn=column
        creatingCords=True
        column=column+length
        while creatingCords:
            if column>self.screenDriver.Cols:
                column=column-self.screenDriver.Cols
                row=row+1
            else: creatingCords=False
                        
        return self.Area(initialRow,initialColumn,row,column)

    #TODO: Se aplica sobre quickpads y toolbars
    # def HideAll(self,**kwargs):
    #    '''
    #     Description:

    #         Hides all visible QuickPad or Toolbar objects.




    #     '''

    def HostOptions(self,**kwargs):
        '''
        Description:
            Returns the HostOptions object associated with the session. Read-only.

        '''
        return getattr(self.screenDriver,kwargs['funcName'])

    def InvokeSettingsDialog(self,SettingsPage,SettingsTab,**kwargs):
        '''
        Description:

            Displays an EXTRA! Settings Dialog.

        Cons information: 
        
            http://docs.attachmate.com/extra/x-treme/apis/com/invokesettingsdialogmethod_con.htm

        
        '''
        return getattr(self.sessionDriver ,kwargs['funcName'])(SettingsPage,SettingsTab)

    ##Applye to multisessions and wwaits
    ##Def item method

    ##Applies to sessions
    ##def JumpNext()

    def MoveRelative(self,NumOfRows,NumOfcols,**kwargs):
        '''
        Description:
            Moves the cursor a specified number of rows and columns (or pages) from its current position.

        Ex:

            session=attachMate().getActiveSession()
            xdriver=extradriver(session)
            xdriver.MoveRelative(0,35)

        '''
        getattr(self.screenDriver ,kwargs['funcName'])(NumOfRows,NumOfcols)

    def MoveTo(self,Row, Col,**kwargs):
        '''
        Description:

            Moves the cursor to the specified location.
            Certain VT hosts do not allow arbitrary cursor positioning, in which case this method will have no effect.

        Ex:
            
            session=attachMate().getActiveSession()
            xdriver=extradriver(session)
            xdriver.MoveTo(10,53)

        '''
        
        getattr(self.screenDriver ,kwargs['funcName'])(Row,Col)

    ##TODO: Preguntar por el screenName
    def NavigateTo(self,screenName,**kwargs):
        '''
        Description:

            Navigates to a specified host screen, recorded from a session window.

        '''
        getattr(self.sessionDriver ,kwargs['funcName'])()

    def Paste(self,**kwargs):
        '''
        Description:

            For the Screen object, this method pastes Clipboard text at the current position or over the current selection.
        '''
        getattr(self.screenDriver ,kwargs['funcName'])()

    def PasteOn(self,Row,Col,**kwargs):
        '''
        Description:

            For the Screen object, this method pastes Clipboard text at the position.
        
        Ex:
    
            session=attachMate().getActiveSession()
            xdriver=extradriver(session)
            xdriver.PasteOn(10,53)

        '''
        self.MoveTo(Row,Col)
        self.Paste()

    def PasteContinue(self,**kwargs):
        '''
        Description

            Continues to insert more Clipboard data from the previous Paste operation.

        Ex:

            session=attachMate().getActiveSession()
            xdriver=extradriver(session)
            xdriver.PasteContinue()

        '''
        getattr(self.screenDriver ,kwargs['funcName'])()

    def PrintDisplay(self,**kwargs):
        '''
        Description:

            Prints or saves on PDF format the current display screen.

        Ex:

            session=attachMate().getActiveSession()
            xdriver=extradriver(session)
            xdriver.PrintDisplay()

        '''
        getattr(self.sessionDriver ,kwargs['funcName'])()

    def PutString(self,String,Row,Col,**kwargs):
        '''
        Description:

            Puts text in the specified location on the screen.

        Ex:
            
            session=attachMate().getActiveSession()
            xdriver=extradriver(session)
            xdriver.PutString('Juan',6,53)
        '''
        getattr(self.screenDriver ,kwargs['funcName'])(String,Row,Col)

    ##TODO: pendiente de utilidad
    ##def ReceiveFile

    def ReduceFont(self,**kwargs):
        '''
        Description:
            Reduces the session font size by one increment.

        '''
        getattr(self.sessionDriver ,kwargs['funcName'])()

    ##Applies to object Waits
    ##def Remove

    ##RemoveAll

    def Reset(self,**kwargs):
        '''
        Description:

            Used with the Session object, Reset returns the display to its power-up operating state. Session.Reset is only valid for VT terminal sessions.
        '''
        getattr(self.sessionDriver ,kwargs['funcName'])()

    ##def ResetAttributes
    ##def ResetColors
    ##def ResetTabs

    def Save(self,**kwargs):
        '''
        Description:

            Saves the current settings of the session.

        '''
        getattr(self.sessionDriver ,kwargs['funcName'])()
    
    def SaveAs(self,FileName,**kwargs):
        '''
        Description:

            Saves the current settings of the session.
            
        '''
        getattr(self.sessionDriver ,kwargs['funcName'])(FileName)

    
    def Search(self,Text,**kwargs):
        '''
        Description:

            Returns an Python dict object with the cords of specified object in the search.

        Ex:
            session=attachMate().getActiveSession()
            xdriver=extradriver(session)
            print(xdriver.Search('User  . . . . . . . . . . . . . .'))

        '''
        
        for i in range(30):
        
            ExtraObject=getattr(self.screenDriver ,kwargs['funcName'])(Text)
            ExtraObjectCords = {
                'Bottom': ExtraObject.Bottom,
                'Left': ExtraObject.Left,
                'Right': ExtraObject.Right,
                'Top': ExtraObject.Top
            }

            if ExtraObjectCords['Bottom'] != -1:
                # time.sleep(0.1)
                self.screenDriver.WaitHostQuiet()
                return ExtraObjectCords
            else:
                raise TextNotFound('Not found:' + Text)
            self.screenDriver.WaitHostQuiet()


        return ExtraObjectCords


    def Select(self,StartRowBottom,StartColLeft,EndRowTop,EndColRight,**kwargs):
        '''
        Description:

            Selects data in an Area based on cords.

        Ex:
            
            attachMate().OpenExtraSession('C:/Users/juan.restrepo/extraDriverProject/as400-demostracion.edp')
            session=attachMate().getActiveSession()
            xdriver=extradriver(session)
            xdriver.Select(6,17,6,49)

        '''
        self.Area(StartRowBottom,StartColLeft,EndRowTop,EndColRight).Select()

    def SelectExtraObject(self,ExtraObject,**kwargs):
        '''
        Description:

            Selects the ExtraObject(Dict)

        Ex:
            
            session=attachMate().getActiveSession()
            xdriver=extradriver(session)
            user=xdriver.Search('User')
            xdriver.SelectExtraObject(user)

        '''
        Left=ExtraObject['Left']
        Bottom=ExtraObject['Bottom']
        Right=ExtraObject['Right']
        Top=ExtraObject['Top']
        self.Select(Bottom,Left,Top,Right)

    def SelectAll(self,**kwargs):
        '''
        Description:

            Selects the entire screen and returns an Area object.
        '''
        getattr(self.screenDriver ,kwargs['funcName'])()


    ##TODO: hacer clase ExtraObject

    #TODO: preguntar para que sirve esto
    #def SendFile

    def SendInput(self,Text,**kwargs):
        '''
        Description

            Sends the specified text to the Screen object, simulating incoming data from the host.
        '''
        getattr(self.screenDriver ,kwargs['funcName'])(Text)
    
    def SendKeys(self,Text,**kwargs):
        '''
        Description

            Sends the specified text to the Screen object, simulating incoming data from the host.

        Ex:

            session=attachMate().getActiveSession()
            xdriver=extradriver(session)
            xdriver.SendKeys('qweqwe')

        '''
        getattr(self.screenDriver ,kwargs['funcName'])(Text)

    def TransferFile(self,**kwargs):
        '''
        Description:

            Displays the File Transfer dialog box.
        '''
        getattr(self.sessionDriver ,kwargs['funcName'])()

    #TODO: se aplica al host options
    def UDKClear(self,**kwargs):
        '''
        Description:

            Clear all the user-defined keys value.
        
        '''
        getattr(self.screenDriver.HostOptions ,kwargs['funcName'])()




    def UpdateStatusBar(self,String,**kwargs):
        '''
        Description

            Displays the specified string in the session's status bar.
        '''
        getattr(self.sessionDriver ,kwargs['funcName'])(String)

    def writeOn(self,ExtraObject,text,**kwargs):

        '''
        Description:

            Put the text on the next editable field at the right of the ExtraObject described

        Ex:

            xdriver.writeOn('User . . . ',Username)

        '''

        objectCords=self.Search(ExtraObject)
        self.SelectExtraObject(objectCords)
        col=objectCords['Right']
        row=objectCords['Top']

        editablerow,editablecolumn=self.searchNextEditableFields(row,col)
        self.PutString(text,editablerow,editablecolumn)
        self.CopyAll()

    def searchNextEditableFields(self,startrow,startcol,**kwargs):
        '''
        Description:

            Search and return the cords of the next editable fields at the right of the coord indicated (startrow,startcol)

        Ex:

            editablerow,editablecolumn=xdriver.searchNextEditableFields(row,col)

        '''
        for i in range(startcol,80):
            if self.FieldAttribute(startrow,i)==192 or self.FieldAttribute(startrow,i)==128:
                finalrow=startrow
                finalcolumn=i+1
                return finalrow,finalcolumn
        return 1,1

    def GoToNextScreen(self,**kwargs):
        '''
        Description:
        
            Sendkey <Enter> and waits for the next screen until is ready

        '''
    
        self.SendKeys('<Enter>')
        band=True
        while band:
            self.screenDriver.WaitHostQuiet()
            band=self.screenDriver.Updated
            print(band)

    
    def CopyAll(self,**kwargs):
        '''
        Description:

            Copy the session Screen to the clipboard

        '''
        self.CopyAppend(1,1,24,80)

    def CloseAll(self,**kwargs):
        '''
        Description:

            Close all sessions and the As/400 client

        '''
        import tkinter as tk
        root = tk.Tk()
        root.withdraw()
        c = root.clipboard_get()
        with open('report.txt', 'w') as f:
            f.write(c)
        self.CloseEx(1)

    def EraseInput(self,**kwargs):
        self.SendKeys(Key.ERASEINPUT)

class Key(object):

    ATTENTION='<Attn>'
    BACKSPACE='<BackSpace>'
    BACKTAB='<BackTab>'
    BEGINLINE='<BeginLine>'
    CLEAR='<Clear>'
    COMMAND1='<Pf1>'
    COMMAND2='<Pf2>'
    COMMAND3='<Pf3>'
    COMMAND4='<Pf4>'
    COMMAND5='<Pf5>'
    COMMAND6='<Pf6>'
    COMMAND7='<Pf7>'
    COMMAND8='<Pf8>'
    COMMAND9='<Pf9>'
    COMMAND10='<Pf10>'
    COMMAND11='<Pf11>'
    COMMAND12='<Pf12>'
    COMMAND13='<Pf13>'
    COMMAND14='<Pf14>'
    COMMAND15='<Pf15>'
    COMMAND16='<Pf16>'
    COMMAND17='<Pf17>'
    COMMAND18='<Pf18>'
    COMMAND19='<Pf19>'
    COMMAND20='<Pf20>'
    COMMAND21='<Pf21>'
    COMMAND22='<Pf22>'
    COMMAND23='<Pf23>'
    COMMAND24='<Pf24>'
    CURSORDOWN='<Down>'
    CURSORDOWN2ROWS='<Down2>'
    CURSORLEFT='<Left>'
    CURSORLEFT2COLUMNS='Left2'
    CURSORRIGHT='<Right>'
    CURSORRIGHT2COLUMNS='<Right2>'
    CURSORSELECT='<CursorSelect>'
    CURSORUP='<Up>'
    CURSORUP2ROWS='<Up2>'
    DELETECHAR='<Delete>'
    DUPLICATE='<Dup>'
    ENDOFLINE='<EndLine>'
    ENTER='<Enter>'
    ERASEEOF='<EraseEOF>'
    ERASEEOL='<EraseEOL>'
    ERASEINPUT='<EraseInput>'
    FIELDEXIT='<FieldExit>'
    FIELDMARK='<FieldMark>'
    FIELDMINUS='<FieldMinus>'
    FIELDPLUS='<FieldPlus>'
    HELP='<Help>'
    HOME='<Home>'
    INSERTMODE='<InsertMode>'
    INSERTTOGGLE='<Insert>'
    LEFTTAB='<BackTab>'
    NEWLINE='<NewLine>'
    PA1='<@x>'
    PA2='<@y>'
    PA3='<@z>'
    PRINT='<Print>'
    RESET='<Reset>'
    RIGHTTAB='<Tab>'
    ROLLDOWN='<RollDown>'
    ROLLUP='<RollUp>'
    SYSTEMREQUEST='<SysReq>'
    TAB='<Tab>'
    TESTREQUEST='<TestRequest>'
    


if __name__=='__mai2n__':

    screenLoggin = {
        'User':' User  . . . . . . ',
        'Password':'Password  . . . . . . . .',
        'Program':'Program/procedure . . . . ',
        'Menu':'Menu',
        'Current':'Current library'
    } 

    As400MainMenu = {
        'Command':'==>',
        }

    Emulator=attachMate()
    Emulator.OpenExtraSession('./as400-demostracion.edp')
    session=attachMate().getActiveSession()
    xdriver=extradriver(session)
    xdriver.writeOn(screenLoggin['User'],'CCJUAN')
    xdriver.writeOn(screenLoggin['Password'],'DEMO5250')
    xdriver.writeOn(screenLoggin['Program'],'Xprogram') 
    xdriver.writeOn(screenLoggin['Menu'],'inventado')
    xdriver.writeOn(screenLoggin['Current'],'actual')
    xdriver.GoToNextScreen()
    xdriver.writeOn(As400MainMenu['Command'],'comando')
    xdriver.CloseAll()
    
if __name__=='__main__':

    screenLoggin = {
        'User':' User  . . . . . . ',
        'Password':'Password  . . . . . . . .',
        'Program':'Program/procedure . . . . ',
        'Menu':'Menu',
        'Current':'Current library'
    } 

    As400MainMenu = {
        'Command':'==>',
        }

    Emulator=attachMate()
    Emulator.OpenExtraSession('./as400-demostracion.edp')
    session=attachMate().getActiveSession()
    xdriver=extradriver(session)
    xdriver.writeOn(screenLoggin['User'],'CCJUAN')
    xdriver.writeOn(screenLoggin['Password'],'DEMO5250')
    xdriver.writeOn(screenLoggin['Program'],'Xprogram') 
    xdriver.writeOn(screenLoggin['Menu'],'inventado')
    xdriver.writeOn(screenLoggin['Current'],'actual')
    
    xdriver.EraseInput()
    # xdriver.Erase(screenLoggin['Password'])
    # xdriver.Erase(screenLoggin['Program']) 
    # xdriver.Erase(screenLoggin['Menu'])
    # xdriver.Erase(screenLoggin['Current'])
