from tkinter import *

#搭建界面


#创建窗口
root = Tk()
#窗口标题
root.title("百度图片爬虫脚本")
#窗口大小及位置
root.geometry("550x400+550+230")
#标签控件
label = Label(root,text = "请输入你需要搜索图片的关键字:",font = ('宋体', 10))
#定位     grid：网格式布局   pack：包    place：位置
label.grid()

#输入框
entry = Entry(root, font=('微软雅黑', 20))
entry.grid(row=0,column=1)

#列表框
text = Listbox(root, font=("微软雅黑",15),width=45,height=10)
#columnspan 组件所跨越的列数
text.grid(row=1,columnspan=2)

#点击按钮
button = Button(root,text = "开始爬取",font=("宋体",10))
# sticky：对齐方式  N S W E
button.grid(row=2,column=0, sticky=W)

button1 = Button(root,text= "退出",font=("宋体",10))
button1.grid(row=2,column=1, sticky=E)
#显示窗口
root.mainloop()