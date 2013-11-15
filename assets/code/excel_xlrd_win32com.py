# -*- coding:utf-8 -*-
import xlrd
from win32com.client import Dispatch
import pythoncom
from win32com.client import constants as c

def readExcelByxlrd(filename,page):
	global at
	data = xlrd.open_workbook(filename)
	table = data.sheets()[page]
	for i in range(1, table.nrows):
		at.append(int(table.cell(i, 0).value))
		
def writeExcelBywin32com():
    try:
        xl = Dispatch("Excel.Application")
        wb = xl.Workbooks.Open("E:\project\zx\gitzx\output.xlsx")
        xl.Visible = 1;
        ws_data = wb.Worksheets(1);
        ws_data.Range('A1').FormulaR1C1 = '数据：'
        ws_data.Range('$B1:$K1').Value = at; #写的数据在excel中的位置
        #wb.Save();
        #('',10,150,400,300)中数字分别表示折线图的左边距、上边距和图形长宽
        ch = ws_data.Shapes.AddChart('',10,150,400,300).Select()
        xl.ActiveChart.ChartType = c.xlXYScatterLines #绘折线图
        xl.ActiveChart.SetSourceData(Source=ws_data.Range("A1:k2"))
    except pythoncom.com_error, (hr, msg, exc, arg):
        print "The Excel call failed with code %d: %s" % (hr, msg)
        if exc is None:
            print "There is no extended error information"
        else:
            wcode, source, text, helpFile, helpId, scode = exc
            print "The source of the error is", source
            print "The error message is", text
            print "More info can be found in %s (id=%d)" % (helpFile, helpId)
    
if __name__ == '__main__':
	filename ='input.xlsx'
	at = []
	readExcelByxlrd(filename,0) 
	writeExcelBywin32com()
	print at
	
	
