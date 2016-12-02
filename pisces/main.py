#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import traceback
import uuid
import os
import urllib
import requests
from selenium import webdriver
import re
import codecs
import datetime
THIS_PATH = os.path.abspath(os.path.dirname(__file__))  # 本文件路径
ROOT_PATH = os.path.abspath(os.path.dirname(THIS_PATH))  # 项目根路径
CHROMEDRIVER = os.path.join(ROOT_PATH, 'tools/chromedriver')


def get_local_path(output_dir, m):
    filename = '%s_%s.jpg' % (m, uuid.uuid4().__str__().replace('-', ''))
    return os.path.join(output_dir, filename)

def download_image(img_url, filename):
    if img_url.startswith('data:'):  # google或者百度图片有这种形式的图片,data:image/jpeg;开头
        urllib.urlretrieve(img_url, filename)
        return
    headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36;'}
    r = requests.get(img_url, headers=headers, stream=True)
    with open(filename, 'wb') as f_write:
        f_write.write(r.raw.read())


def main(name, basetime, endtime, day_delta, last_end, close=True):
    '''
    @brief 根据某个搜索地址,下载搜索的图片链接
    @param 搜索关键词
    @param 搜索开始时间
    @param 搜索结束时间
    @param 搜索间隔
    @param 上次搜索开始位置
    @param 是否在运行结束后关闭浏览器
    @param 使用的浏览器类型,firefox/chrome/ie/opera/safari
    @return 下载的图片数量
    '''

    xpath = '//div[@id="ires"]/div/div[@id="isr_mc"]/div/div/div/div/a/img'
    picsUrlPattern = re.compile(r'\"ou\":\"(.+?)\"')
    

    for i in range(1, last_end):
        basetime = basetime + datetime.timedelta(days=day_delta)

    # 启动浏览器    
    # chromedriver to see http://chromedriver.storage.googleapis.com/index.html
    # If it cannot run, please check the version of chromedriver; I use version=2.9
    os.environ["webdriver.chrome.driver"] = CHROMEDRIVER
    driver = webdriver.Chrome(CHROMEDRIVER)
    
    # 最大化窗口，因为每一次爬取只能看到视窗内的图片
    driver.maximize_window()
    # 浏览器打开爬取页面

    all_img = 0
    # 存储下载链接
    fw = codecs.open('fordownload_%s.txt' % name, 'w', 'utf-8')
    # 存储下载日志
    fw_log = codecs.open('log_%s.txt' % name, 'w', 'utf-8')
    time_count = 1
    while basetime < endtime :
        m = 1  # 图片编号
        time_count = time_count + 1
        if basetime < datetime.datetime(2014, 1, 1):
            image_count = 50
        elif basetime < datetime.datetime(2015, 1, 1):
            image_count = 100
        else:
            image_count = 300
        tmp_time = basetime + datetime.timedelta(days=day_delta)
        url = 'https://www.google.com.hk/search?q=%s&safe=strict&tbs=itp%%3Aface%%2Ccdr%%3A1%%2Ccd_min%%3A%s%%2F%s%%2F%s%%2Ccd_max%%3A%s%%2F%s%%2F%s&tbm=isch' % \
              (name, basetime.year, basetime.month, basetime.day, tmp_time.year, tmp_time.month, tmp_time.day)
        driver.get(url)
        img_url_dic = {}  # 记录下载过的图片地址，避免重复下载
        picsNum = 1

        scrolltime = 0
        while m <= image_count:
            if scrolltime > 30:
                break
            scrolltime += 1
            # 向下滑动
            driver.execute_script("window.scrollBy(0,2500)", "")
            driver.implicitly_wait(100)  # wait 1 second
            new_image_add = 0
            picsUrlList = picsUrlPattern.findall(str(driver.page_source.encode('utf-8')))
            for pics in picsUrlList:
                # 保存图片到指定路径
                img_url = pics
                if img_url and img_url not in img_url_dic:
                    img_url_dic[img_url] = ''
                    new_image_add += 1
                    filename = get_local_path(output_dir, m)
                    print('%s save %s to %s' % (basetime.strftime('%Y-%m-%d'),img_url, filename))
                    newPath = os.path.join('%s_%s_%s_%s' % (name, basetime.year, basetime.month, basetime.day), '%s_google.jpg' % picsNum)
                    fw.write(pics + '\t' + newPath + '\n')
                    picsNum += 1
                    all_img += 1
                    m += 1
                    if m > image_count:
                        break
            fw_log.write('%s %s %s\n' % (time_count, basetime.strftime('%Y-%m-%d'),m))
        basetime = basetime + datetime.timedelta(days=day_delta+1)
    # 关闭浏览器该标签页
    if close:
        driver.close()
    return all_img
