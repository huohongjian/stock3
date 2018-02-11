import xlrd
import xlwt
from xlutils.copy import copy


class Excel:
    """
    Excel表格封装
    1. 读取Excel的数据
    2. 数据写入到Excel中
    """
    def __init__(self):
        self.path = "E:\z_shishi\data\param.xlsx"

    def get_data(self,rowx, colx):
        """获取Excel中的值"""
        sheet = xlrd.open_workbook(self.path)
        index = sheet.sheet_by_index(0)
        value = index.cell_value(rowx, colx)
        return value

    def write_data(self,P_F,style):
        """写入Excel"""
        rb =xlrd.open_workbook("E:\z_shishi\data\param.xlsx")
        wb = copy(rb)
        s = wb.get_sheet(0)
        #设置样式
        s.write(2, 5,P_F,style)
        wb.save("change06.xls")
        return wb

    def set_style(self,color):
        """写入数据库的样式"""
        font = xlwt.Font()
        font.name = "Times New Roman"
        font.colour_index = color
        style = xlwt.XFStyle()
        style.font = font
        return  style

    def result_write(self,res,color):
        """对结果进行判断,如果结果为0(成功),写入Excel 红色PASS
                          如果结果为1(失败),写入Excel 蓝色Fail  11为银绿色  12为蓝色
        """
        try:
            if res==0:
                self.write_data("PASS",self.set_style(color) )
            elif res==1:
                self.write_data("PASS", self.set_style(12))
            print ("finished")
        except Exception as e :
            print ("写入Excel时不能打开Excel文档")


        # if res==0:    #不写类,直接使用函数调用
        #
        #     write_data("PASS",set_style(color))
        # elif res==1:
        #     write_data("FAIL",set_style(12))
        # print ("finished")

if __name__=="__main__":
    excel = Excel()
    excel.result_write(0,2)
