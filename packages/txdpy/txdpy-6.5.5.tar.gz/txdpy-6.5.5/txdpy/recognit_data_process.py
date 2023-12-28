# -*- coding: utf-8 -*-
# @File  : data_processing.py
# @Time  : 2023/9/4 13:21
# @Author: 唐旭东

import re
from txdpy import optstr

class Recognit_Data_Process:
    def __init__(self,datas,isjcpc=True,isjckl=True,isjcpckl=True):
        self.isjcpc, self.isjckl, self.isjcpckl= isjcpc, isjckl, isjcpckl
        self.datas=datas
        self.pbk={"页码":None,"批次":None,"科类":None}
        self.page_re_str=['-第(\d+)页-','^[^\d](\d)[^\d]$']#page
        self.ignore_list=['计划及专业','第三篇']#忽略列表
        self.batch_ls= {}#批次
        self.kelei_ls= {}#科类
        self.batch_kelei_ls= {
            '【物理】本科提前批A段':('本科提前批A','物理'),
            '【物理】本科提前批B段':('本科提前批B','物理'),
            '【物理】本科批':('本科批','物理'),
            '【物理】高职专科提前批':('高职专科提前批','物理'),
            '【物理】高职专科批':('高职专科批','物理'),
            '【体育类】体育本科批':('体育本科批','体育类'),
            '【体育类】体育高职专科批':('体育高职专科批','体育类'),
            '【艺术类】艺术本科提前批':('艺术本科提前批','艺术类'),
            '【艺术类】艺术本科批A段':('艺术本科批A段','艺术类'),
            '【艺术类】艺术本科批B段':('艺术本科批B段','艺术类'),
            '【艺术类】艺术高职专科批':('艺术高职专科批','艺术类'),
                                }#批次和科类
        self.pi = []#需要删除的数据索引
        self.basic_process()

    #识别文字格式化
    def word_format(self):
        for data in self.datas:
            data['words']['word']=optstr(data['words']['word'])

    # 忽略部分识别数据
    def ignore_part_data(self):
        for i, data in enumerate(self.datas):
            if data['words']['word'] in self.ignore_list:
                self.pi.append(i)

    # 检查页码
    def re_page(self):
        for i,data in enumerate(self.datas):
            for re_str in self.page_re_str:
                page_re=re.search(re_str,data['words']['word'])
                if  page_re:
                    self.pbk["页码"]=page_re.group(1)
                    # self.pi.append(i)
                    self.datas=self.datas[:i]
                    break

    # 检查批次
    def inspect_batch(self):
        for i,data in enumerate(self.datas):
            if data['words']['word'] in self.batch_ls:
                self.pbk["批次"]=self.batch_ls[data['words']['word']]
                self.pi.append(i)

    # 检查科类
    def inspect_kelei(self):
        for i, data in enumerate(self.datas):
            if data['words']['word'] in self.kelei_ls:
                self.pbk["科类"] = self.kelei_ls[data['words']['word']]
                self.pi.append(i)

    #检查批次科类
    def inspect_batch_kelei(self,wrod=None):
        if wrod:
            if wrod in self.batch_kelei_ls:
                return self.batch_kelei_ls[wrod]
        for i, data in enumerate(self.datas):
            if data['words']['word'] in self.batch_kelei_ls:
                self.pbk["批次"] = self.batch_kelei_ls[data['words']['word']][0]
                self.pbk["科类"] = self.batch_kelei_ls[data['words']['word']][1]
                self.pi.append(i)

    #数据基本处理
    def basic_process(self):
        self.word_format()
        self.ignore_part_data()
        self.re_page()
        if self.isjcpc:
            self.inspect_batch()
        if self.isjckl:
            self.inspect_kelei()
        if self.isjcpckl:
            self.inspect_batch_kelei()
        [self.datas.pop(i) for i in sorted(self.pi,reverse=True)]