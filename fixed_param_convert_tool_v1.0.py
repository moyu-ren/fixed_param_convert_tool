# -*- coding: utf-8 -*-
"""
Created on Fri Jan 13 19:37:26 2023

@author: huamou_chen
"""

import os
import sys
import re
import numpy as np

# from PyQt5.QtWidgets import QMainWindow, QPushButton, QApplication
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtPrintSupport import *



'''删除C语言注释'''
def C_note_delete(str_in):
    # re_c_note = re.compile(r'/*(.*)*/')
    # str_match = re_c_note.findall(str_out)
    # str_match = re.findall(r'/*(.*)*/', str_in)
    # str_match = re.findall(r'\/+\*(.*)\*\/+', str_in, re.S)
    # str_match = re.findall(r'(//\s*.*)|(?sm)(/\*(\s*(.*?)\s*)\*/)', str_in, re.S)
    # str_match = re.findall(r'(/\*(\s*(.*?)\s*)\*/)', str_in, re.S)
    # str_match = re.findall(r'(/\*(.*?)\*/)', str_in, re.S)
    # str_match = re.search(r'[/+]\*([^/]*)\*[/+]', str_in, re.S)
    
    str_out = re.sub(r'(/\*(\s*(.*?)\s*)\*/)', "", str_in, re.S)
    if str_out==None:
        return str_in;
    str_out2 = re.sub(r'(//(.*))', "", str_out)
    if str_out2==None:
        return str_out;
    # print(str_out)
    return str_out2

'''删除C语言注释'''
def C_macro_delete(str_in):
    # str_out = re.findall(r'(\#(.*))', str_in)
    str_out = re.sub(r'(\#(.*))', "", str_in)
    if str_out==None:
        return str_in;
    # print(str_out)
    # return str_in
    return str_out
    

def FIXED_QUANTIFY(data, Q_val):
    # print("FIXED_QUANTIFY: ", data, ", Q_val: ", Q_val)
    if (Q_val == 0):
        return int(data + 0.5)
    else:
        return int((data*(2**Q_val-1)) + 0.5)

def FIXED_ANGLE(data):
    return FIXED_QUANTIFY(data/360.0, 31)

def FIXED_QUANTIFY_INV(data, Q_val):
    # print("FIXED_QUANTIFY: ", data, ", Q_val: ", Q_val)
    if (Q_val == 0):
        return float(data)
    else:
        return (float(data)/(2**Q_val-1))

def FIXED_ANGLE_INV(data):
    return FIXED_QUANTIFY_INV(data, 31)*360.0


'''查找变量字符串'''
def first_value_str_find(str_in, str_match):
    print("first_value_str_find:")
    # posi = re.search(str_match, str_in).span()
    try:
        posi = re.search(str_match, str_in).span()
    except AttributeError:
        print("找不到变量: ", str_match)
        return ""
    # print(posi)
    # print(str_in[posi[0]:posi[0]+100])
    str_match2 = str_in[posi[0]:-1]
    try:
        posi2 = re.search(r'([\+\-]*[0-9\.]+)', str_match2, re.S).span()
    except AttributeError:
        print("找不到数值！")
        return ""
    # print('posi2:', posi2)
    value = str_match2[posi2[0]:posi2[1]]
    # print('value:', value)
    return value

'''查找数组字符串'''
def array_str_find(str_in, str_match):
    print("array_str_find:")
    # posi = re.search(str_match, str_in).span()
    try:
        posi = re.search(str_match, str_in).span()
    except AttributeError:
        print("找不到数组: ", str_match)
        return ""
    # print(posi)
    # print(str_in[posi[0]:posi[0]+100])
    str_match2 = str_in[posi[0]:-1]
    # posi2 = re.search(r'\{([0-9f\s\.+-,]*)\}', str_match2, re.S).span()
    try:
        posi2 = re.search(r'\{([0-9f\s\.\+\-,]*)\}', str_match2, re.S).span()
    except AttributeError:
        print("找不到数值！")
        return ""
    # print(posi2)
    value = str_match2[posi2[0]:posi2[1]]
    # print(value)
    return value

'''数组字符串转数组'''
def str_to_array(str_in, array_num):
    print("str_to_array:")
    str_out = list(re.findall(r'\d+\.?\d*', str_in))
    print('str_in: ', str_out)
    array_out = np.zeros(int(array_num))
    cnt = 0
    while(cnt < len(str_out)):
        array_out[cnt] = float(str_out[cnt])
        cnt = cnt + 1
    # print(array_out)
    return array_out

'''浮点转定点'''
def array_float2int(array_in, Q_val):
    print("array_float2int:")
    array_out = np.zeros(len(array_in), dtype='int32')
    print(array_in)
    i = 0
    while(i < len(array_in)):
        # print("Q_val: ", Q_val)
        if (len(Q_val) == 1):
            if (Q_val[0].find("raw") == 1):
                array_out[i] = array_in[i]
            elif (Q_val[0].find("angle") == 1):
                array_out[i] = FIXED_ANGLE(array_in[i])
            else:
                array_out[i] = FIXED_QUANTIFY(array_in[i], int(Q_val[0]))
        else:
            if (Q_val[i].find("raw") == 1):
                # print("raw: ", Q_val[i], ", i: ", i)
                array_out[i] = array_in[i]
            elif (Q_val[i].find("angle") == 1):
                array_out[i] = FIXED_ANGLE(array_in[i])
            else:
                array_out[i] = FIXED_QUANTIFY(array_in[i], int(Q_val[i]))
        i = i+1
    print(array_out)
    return array_out

'''定点转浮点'''
def array_int2float(array_in, Q_val):
    print("array_int2float:")
    array_out = np.zeros(len(array_in), dtype='float32')
    print(array_in)
    i = 0
    while(i < len(array_in)):
        # print("Q_val: ", Q_val)
        if (len(Q_val) == 1):
            if (Q_val[0].find("raw") == 1):
                array_out[i] = array_in[i]
            elif (Q_val[0].find("angle") == 1):
                array_out[i] = FIXED_ANGLE_INV(array_in[i])
            else:
                array_out[i] = FIXED_QUANTIFY_INV(array_in[i], int(Q_val[0]))
        else:
            if (Q_val[i].find("raw") == 1):
                # print("raw: ", Q_val[i], ", i: ", i)
                array_out[i] = array_in[i]
            elif (Q_val[i].find("angle") == 1):
                array_out[i] = FIXED_ANGLE_INV(array_in[i])
            else:
                array_out[i] = FIXED_QUANTIFY_INV(array_in[i], int(Q_val[i]))
        i = i+1
    print(array_out)
    return array_out

'''数组转字符串'''
def array_to_str(str_pre, array_in, str_last):
    # print("\n array_to_str:")
    # print('array_in:', array_in)
    str_array = str(list(array_in))
    # print('str_array:', str_array)
    str_out = str_pre + str_array[1:-1] + str_last
    # print('str_out:', str_out)
    return str_out


class TextEdit(QTextEdit):
    def canInsertFromMimeData(self, source):
        if source.hasImage():
            return True
        else:
            return super(TextEdit, self).canInsertFromMimeData(source)

    def insertFromMimeData(self, source):
        cursor = self.textCursor()
        document = self.document()
 
        if source.hasUrls():
            for u in source.urls():
                file_ext = splitext(str(u.toLocalFile()))
                if u.isLocalFile() and file_ext in IMAGE_EXTENSIONS:
                    image = QImage(u.toLocalFile())
                    document.addResource(QTextDocument.ImageResource, u, image)
                    cursor.insertImage(u.toLocalFile())
                else:
                    break
            else:
                return
 
        elif source.hasImage():
            image = source.imageData()
            uuid = hexuuid()
            document.addResource(QTextDocument.ImageResource, uuid, image)
            cursor.insertImage(uuid)
            return
 
        super(TextEdit, self).insertFromMimeData(source)


class QDoublePushButton(QPushButton):
    doubleClicked = pyqtSignal()
    clicked = pyqtSignal()

    def __init__(self, *args, **kwargs):
        QPushButton.__init__(self, *args, **kwargs)
        self.timer = QTimer()
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.clicked.emit)
        super().clicked.connect(self.checkDoubleClick)

    @pyqtSlot()
    def checkDoubleClick(self):
        if self.timer.isActive():
            self.doubleClicked.emit()
            self.timer.stop()
        else:
            self.timer.start(250)

class Fixed_param_convert_tool(QMainWindow):

    def __init__(self):
        super().__init__()

        # self.editor = TextEdit()
        self.editor = QTextEdit()
        self.editor.setAutoFormatting(QTextEdit.AutoAll)
        # self.editor.selectionChanged.connect(self.update_format)
        # 添加阴影
        effect_shadow = QGraphicsDropShadowEffect(self)
        effect_shadow.setOffset(1, 1) # 偏移
        effect_shadow.setBlurRadius(5) # 阴影半径
        effect_shadow.setColor(Qt.black) # 阴影颜色
        self.editor.setGraphicsEffect(effect_shadow) # 将设置套用到widget窗口中
        
        self.text_output = QTextEdit()
        self.text_output.setAutoFormatting(QTextEdit.AutoAll)
        # self.text_output.selectionChanged.connect(self.update_format)
        
        self.message_text = QTextEdit()
        self.message_text.setAutoFormatting(QTextEdit.AutoAll)
        # self.message_text.selectionChanged.connect(self.update_format)
        # 设置字体颜色
        message_text_pl = QPalette()
        message_text_pl.setColor(QPalette.Text, Qt.red)
        self.message_text.setPalette(message_text_pl)
        # 设置最大高度
        self.message_text.setMaximumHeight(180)
        
        self.cfg_file_path = ''
        
        self.cfg_file_text = QTextEdit()
        self.cfg_file_text.setAutoFormatting(QTextEdit.AutoAll)
        # self.cfg_file_text.selectionChanged.connect(self.update_format)
        # 设置最大高度
        self.cfg_file_text.setMaximumHeight(22)

        self.UI_init()


    def UI_init(self):
        cfg_file_layout = QHBoxLayout()
        
        cfg_file_button = QDoublePushButton("配置文件选择", self)
        cfg_file_button.clicked.connect(self.open_cfg_file)
        cfg_file_button.doubleClicked.connect(self.button_double_int2float)
        cfg_file_layout.addWidget(cfg_file_button)
        cfg_file_layout.addWidget(self.cfg_file_text)

        button_layout = QHBoxLayout()
        # btn1 = QPushButton("浮点转定点", self)
        btn1 = QDoublePushButton("浮点转定点", self)
        # btn1.move(50, 250)
        btn1.clicked.connect(self.btn1_float2int)
        btn1.doubleClicked.connect(self.button_double_int2float)
        button_layout.addWidget(btn1)

        # btn2 = QPushButton("定点转浮点", self)
        btn2 = QDoublePushButton("定点转浮点", self)
        # btn2.move(250, 250)
        btn2.clicked.connect(self.btn2_int2float)
        btn2.doubleClicked.connect(self.button_double_int2float)
        button_layout.addWidget(btn2)
        
        edit_layout = QVBoxLayout()
        edit_layout.addWidget(self.editor)
        edit_layout.addLayout(button_layout)
        
        # font = QFont('Times', 12)
        # self.editor.setFont(font)
        # self.editor.setFontPointSize(12)
        # self.path = None
        text_layout = QHBoxLayout()
        text_layout.addLayout(edit_layout)
        text_show_layout = QVBoxLayout()
        text_show_layout.addWidget(self.text_output)
        text_show_layout.addWidget(self.message_text)
        text_layout.addLayout(text_show_layout)
    
        central_layout = QVBoxLayout()
        central_layout.addLayout(cfg_file_layout)
        central_layout.addLayout(text_layout)
        # central_layout.addLayout(button_layout)
        container = QWidget()
        container.setLayout(central_layout)
        self.setCentralWidget(container)

        self.statusBar()

        # self.setGeometry(300, 300, 290, 150)
        self.setGeometry(300, 300, 400, 300)
        self.setWindowTitle('定点参数转换工具v1.0')
        self.show()

    # def update_format(self):
        # self.block_signals(self._format_actions, True)
        # self.fonts.setCurrentFont(self.editor.currentFont())
        # self.fontsize.setCurrentText(str(int(self.editor.fontPointSize())))
        # self.italic_action.setChecked(self.editor.fontItalic())
        # self.underline_action.setChecked(self.editor.fontUnderline())
        # self.bold_action.setChecked(self.editor.fontWeight() == QFont.Bold)
        # self.alignl_action.setChecked(self.editor.alignment() == Qt.AlignLeft)
        # self.alignc_action.setChecked(self.editor.alignment() == Qt.AlignCenter)
        # self.alignr_action.setChecked(self.editor.alignment() == Qt.AlignRight)
        # self.alignj_action.setChecked(self.editor.alignment() == Qt.AlignJustify)
        # self.block_signals(self._format_actions, False)
        
    def open_cfg_file(self):
        filename = QFileDialog.getOpenFileNames(self, '选择图像', os.getcwd(), "All Files(*);;Text Files(*.txt)")
        self.cfg_file_path = filename[0][0]
        # 输出文件，查看文件路径
        print(filename)
        print(self.cfg_file_path)
        print("len(self.cfg_file_path): ", len(self.cfg_file_path))
        # 根据输出结果选取对应的文件名
        # self.message_text.insertPlainText("filename:"+filename+"\n")
        self.cfg_file_text.setText(self.cfg_file_path)
        
    def btn1_float2int(self):
        # sender = self.sender()
        # self.editor.setText("yes")
        # 获取文本
        text_str = self.editor.toPlainText()
        self.fixed_param_float2int(text_str)
        # self.text_output.setText(text_str)
        self.statusBar().showMessage('float to int start!')


    def btn2_int2float(self):
        text_str = self.editor.toPlainText()
        self.fixed_param_int2float(text_str)
        self.statusBar().showMessage('int to float start!')

    def button_double_int2float(self):
        self.text_output.setText("(Hey man, Why do you double-click? what the fuck with you!)")
        self.statusBar().showMessage('int to float start!')


    def fixed_param_float2int(self, str_in):
        # self.message_text.insertPlainText("test")
        self.text_output.setText("")
        str_out = C_note_delete(str_in)
        str_out2 = C_macro_delete(str_out)
        str_out = C_note_delete(str_out2)
        str_out2 = C_macro_delete(str_out)
        param_int_str = str_out2
        # self.text_output.insertPlainText(param_int_str)
        
        # with open('fixed_test_float2int.cfg', 'r', encoding='utf-8') as infile:
        if len(self.cfg_file_path) == 0:
            self.message_text.insertPlainText("还没选配置文件啊！吊毛！\n")
            return
        else:
            self.message_text.insertPlainText("当前配置文件：\n" + self.cfg_file_path + "\n\n")
            
        with open(self.cfg_file_path, 'r', encoding='utf-8') as infile:
            for line in infile:
                # data_line = line.strip("\n").split()  # 去除首尾换行符，并按空格划分
                # print("data_line: ", data_line)
                if (len(line) < 2) | (line[0] == '#'):
                    print("skip: ", line)
                    continue
                data_line = re.sub(r'[\<\>\'\"\t]*', "", line)
                print('data_line:', data_line)
                data_line = data_line.split(',')
                if len(data_line) < 5:
                    continue
                # print(data_line)
                
                array_match = data_line[0]
                str_pre = data_line[1]
                str_last = data_line[2]
                array_num = int(data_line[3])
                # Q_val = np.zeros(len(data_line)-4, dtype='int32')
                Q_val = {}
                i = 0
                while(i < (len(data_line)-4)):
                    Q_val[i] = data_line[4 + i]
                    i = i+1
                print('\narray_match: ', array_match)
                print('str_pre: ', str_pre)
                print('str_last: ', str_last)
                print('array_num: ', array_num)
                print('Q_val: ', Q_val)
                
                if array_num == 1:
                    str_value = first_value_str_find(str_out2, array_match)
                else:
                    str_value = array_str_find(str_out2, array_match)
                if len(str_value) == 0:
                    self.message_text.insertPlainText("error 1: 找不到数组 " + array_match + '\n')
                    continue
                
                array_float = str_to_array(str_value, array_num)
                if (len(array_float) == 0):
                    self.message_text.insertPlainText("error 2: 数组转换失败 " + array_match + "\n")
                    continue
                
                array_int = array_float2int(array_float, Q_val)
                
                array_str_out = array_to_str(str_pre, array_int, str_last)
                
                self.text_output.insertPlainText(array_str_out + "\n\n")


    def fixed_param_int2float(self, str_in):
        self.text_output.setText("")
        str_out = C_note_delete(str_in)
        str_out2 = C_macro_delete(str_out)
        str_out = C_note_delete(str_out2)
        str_out2 = C_macro_delete(str_out)
        param_int_str = str_out2
        
        # with open('fixed_test_float2int.cfg', 'r', encoding='utf-8') as infile:
        # if len(self.cfg_file_path) == 0:
        #     self.message_text.insertPlainText("还没选配置文件啊！吊毛！\n")
        #     return
        # else:
        #     self.message_text.insertPlainText("当前配置文件：\n" + self.cfg_file_path + "\n\n")
            
        with open(self.cfg_file_path, 'r', encoding='utf-8') as infile:
            for line in infile:
                # data_line = line.strip("\n").split()  # 去除首尾换行符，并按空格划分
                # print("data_line: ", data_line)
                if (len(line) < 2) | (line[0] == '#'):
                    print("skip: ", line)
                    continue
                data_line = re.sub(r'[\<\>\'\"\t]*', "", line)
                print('data_line:', data_line)
                data_line = data_line.split(',')
                if len(data_line) < 5:
                    continue
                # print(data_line)
                
                array_match = data_line[0]
                str_pre = data_line[1]
                str_last = data_line[2]
                print('data_line[3]: ', data_line[3])
                print('data_line[4]: ', data_line[4])
                array_num = int(data_line[3])
                # Q_val = np.zeros(len(data_line)-4, dtype='int32')
                Q_val = {}
                i = 0
                while(i < (len(data_line)-4)):
                    Q_val[i] = data_line[4 + i]
                    i = i+1
                print('array_match: ', array_match)
                print('str_pre: ', str_pre)
                print('str_last: ', str_last)
                print('array_num: ', array_num)
                print('Q_val: ', Q_val)
                
                if array_num == 1:
                    str_value = first_value_str_find(str_out2, array_match)
                else:
                    str_value = array_str_find(str_out2, array_match)
                if len(str_value) == 0:
                    self.message_text.insertPlainText("error 1: 找不到数组 " + array_match + '\n')
                    continue
                
                array_int = str_to_array(str_value, array_num)
                if (len(array_int) == 0):
                    self.message_text.insertPlainText("error 2: 数组转换失败 " + array_match + "\n")
                    continue
                
                array_float = array_int2float(array_int, Q_val)
                
                array_str_out = array_to_str(str_pre, array_float, str_last)
                
                self.text_output.insertPlainText(array_str_out + "\n\n")
        # self.text_output.setText("")
        # self.message_text.insertPlainText("现在还不支持定点转浮点！吊毛！\n")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Fixed_param_convert_tool()
    window.resize(800,600)
    
    # 打包改回这条命令，不然会闪退
    sys.exit(app.exec_())
    
    # 调试用这条命令，避免控制台卡死
    # sys.exit(app.exec_)
    