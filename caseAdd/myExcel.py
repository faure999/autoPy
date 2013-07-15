import win32com.client
class myExcel:
    def __init__(self,filename = None):
        self.xlApp = win32com.client.Dispatch('Excel.Application')
        if filename:
            self.filename = filename
            self.xlBook = self.xlApp.Workbooks.Open(filename)
        else:
            self.xlBook = self.xlApp.Workbooks.Add()
            self.filename = filename
    def save(self,newfilename = None):
        if newfilename:
            self.filename = newfilename
            self.xlBook.SaveAs(newfilename)
        else:
            self.xlBook.Save()
    def close(self):
        self.xlBook.Close(SaveChanges=0)
        del self.xlApp
        
    def get_cell(self,sheet,row,col):
        '''get value of one cell'''
        return self.xlBook.Worksheets(sheet).Cells(row,col).Value 
    def set_cell(self,sheet,row,col,value):
        '''set value of one cell'''
        self.xlBook.Worksheets(sheet).Cells(row,col).Value = value
    def get_rowCount(self,sheet):
        '''get the used rows count of specified sheet'''
        return self.xlBook.Worksheets(sheet).UsedRange.Rows.Count
    def get_colCount(self,sheet):
        '''get the used columns count of specified sheet'''
        return self.xlBook.Worksheets(sheet).UsedRange.Columns.Count
    def get_sheetCount(self):
        '''get the sheet count of current workbook'''
        return self.xlBook.Worksheets.Count
    def active_sheet(self):
        '''get the name of current active sheet'''
        return self.xlBook.ActiveSheet.Name
    
    def copy_sheet(self,sheet):
        '''copy sheet
        '''
        orgin = self.xlBook.Worksheets(sheet)
        orgin.Copy(None,orgin)
        
    def select(self,sheet,replace):
        '''
        @type replace: boolean
        @param replace : if clear selected contect. true means clear.
        '''
        self.xlBook.Worksheets(sheet).Select(replace)
        
    def copy(self,sheet,region=''):
        '''
        copy the current content to ClipBoard
        '''
        if region:
            self.xlBook.Worksheets(sheet).Range(region).Copy()
        else:
            self.xlBook.Worksheets(sheet).UsedRange.Copy()
    def pasteBack(self,sheet,destinat =''):
        ''' 
        paste the clipBoard content on the background
        '''
        slSheet = self.xlBook.Worksheets(sheet)
        if destinat:
            slSheet.Range(destinat).Select
            slSheet.Paste(slSheet.Range(destinat))
        else:
            slSheet.Paste()
        
    def pasteFore(self,sheet,destinat =''):
        ''' 
        paste the clipBoard content on the foreground
        '''
        slSheet = self.xlBook.Worksheets(sheet)
        slSheet.Activate()
        if destinat:
            slSheet.Range(destinat).Select
            slSheet.Paste(slSheet.Range(destinat))
        else:
            slSheet.Paste()
        #slSheet.PasteSpecial()
        
    def get_string_in_row(self,sheet,row,s):
        '''
        Search the given string s in the giver row
        Return value is the col number
        '''
        i=1
        while True:
            if self.get_cell(sheet,row,i)==s:
                break
            i+=1
            if i > self.get_colCount(sheet):
                print"[Error:] didn't find the %s!" % s
                return None
        print 'col number: %d' % i
        return i
    def get_string_in_col(self,sheet,col,s):
        '''
        search the given string s in the given col
        return value is the row number
        '''
        i = 1
        while True:
            if self.get_cell(sheet, i, col) ==s:
                break
            i+=1
            if i>self.get_rowCount(sheet):
                print"[Error:] didn't find the %s!" % s
                return None
        print 'row number: %d' % i
        return i
    def get_location(self,sheet,s):
        '''get the location of specify string in specify sheet
        @type s: string
        @return: a list contains the row and column of cells which value equal s
        '''
        l=[]
        for i in range(1,self.get_rowCount(sheet)+1):
            for j in range(1,self.get_colCount(sheet)+1):
                if self.get_cell(sheet, i, j)==s:
                    l.append([i,j])
                    print 'row: %d col: %d' % (i,j)
        return l
    def get_location_by_diagonal(self,sheet,cell_diagonal,s):
        l=[]
        for line in range(1,cell_diagonal+1):
            for i in range(1,line+1):
                if self.get_cell(sheet, line, i)==s :
                    l.append([line,i])
                if i!=line and self.get_cell(sheet, i, line)==s:
                    l.append([i,line])
        return l
    def write_value(self,sheet,string_in_row,string_in_col,s):
        '''
        '''
        row_num= self.get_string_in_col(sheet, 1, string_in_col)
        col_num= self.get_string_in_row(sheet, 1, string_in_row)
        
        self.set_cell(sheet, row_num, col_num, s)
        print "Write value \'%s\' to [%d,%d]" % (s,row_num,col_num)
        
    def get_value(self,sheet,string_in_row,string_in_col):
        row_num= self.get_string_in_col(sheet, 1, string_in_col)
        col_num= self.get_string_in_row(sheet, 1, string_in_row)
        
        return self.get_cell(sheet, row_num, col_num)

if __name__ =='__main__':

    xls = myExcel(r'D:\Work\Temp\test.xls')

    
    xls.save()
    xls.close()