#!/usr/bin/env python
# coding: utf-8

# **Copyright (c) 2022 Zhiyue Chen. All rights reserved.**

# # Raw Data Acquisition(not recommended to run)

# These cells will get web page information and save it locally. It may take a long time. If you have downloaded the dataset we offer, you **_needn't_** run these cells!<br/>***Network needed***
# ******
# In these cells, you may need to install **selenium** and **eventlet** to make sure they will work properly.
# If you havn't install yet, you need to open Anaconda Prompt, and run</br><code>pip install selenium</code><br/><code>pip install eventlet</code></br>in your environment.<br/>
# You also need to download **chromedriver**. You can download it at http://chromedriver.storage.googleapis.com/index.html and download the version which matches your Chrome version. You can check your chrome version [here](chrome://version)(chrome://version) with your chrome.

# ## for Parts

# ### Initialization

# In[1]:


from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from tqdm import tqdm
import time
import threading
import queue
import pandas as pd
import os
import eventlet
import re


# ### Main

# In[2]:


class Part:
    def __init__(self, part_num, part_name, part_id, part_url,
                 short_desc, part_type, team, year, sequence, contents,
                 assemble_std, linking_parts, parts_used, using_parts, len,
                 released, sample, twin, date, isfavorite, designer):
        self.part_num = part_num
        self.part_name = part_name
        self.part_id = part_id
        self.part_url = part_url
        self.short_desc = short_desc
        self.year = year
        self.sequence = sequence
        self.assemble_std = assemble_std
        self.contents = contents
        self.linking_parts = linking_parts
        self.parts_used = parts_used
        self.using_parts = using_parts
        self.len = len
        self.part_type = part_type
        self.team = team
        self.released = released
        self.sample = sample
        self.twin = twin
        self.date = date
        self.isfavorite = isfavorite
        self.designer = designer

    def print_parts(self):
        print(f"part_num = {self.part_num}")
        print(f"part_name = {self.part_name}")
        print(f"part_id = {self.part_id}")
        print(f"part_url = {self.part_url}")
        print(f"part_type = {self.part_type}")
        print(f"part_team = {self.team}")
        print(f"part_year = {self.year}")
        print(f"part_sequence = {self.sequence}")
        print(f"part_desc = {self.short_desc}")
        print(f"part_assemble_std = {self.assemble_std}")
        print(f"contents"f" = {self.contents}")
        print(f"parts_used = {self.parts_used}")
        print(f"using_parts = {self.using_parts}")
        print(f"len = {self.len}")
        print("------------------------------")


class myThread(threading.Thread):
    def __init__(self, threadID, name, q):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.q = q

    def run(self):
        print("Open threads:" + self.name)
        process_data(self.q)
        print("Quit threads:" + self.name)


def process_data(q):
    while not exitFlag:
        queueLock.acquire()
        if not workQueue.empty():
            data = q.get()
            queueLock.release()
            if curStep == 1:
                get_parts_urls_one(data)
            else:
                get_parts_details_one(data)
        else:
            queueLock.release()
        time.sleep(1)


def web_analysis_and_get_team_lists(year):
    global s
    global chrome_options
    print(f"---Start getting team lists in {year}---")
    front_url = "https://old.igem.org/Team_Parts?year="
    url = front_url + year
    driver = webdriver.Chrome(service=s, options=chrome_options)
    i = 0
    while 1:
        try:
            driver.get(url)
            WebDriverWait(driver, 30, 1).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="topBanner"]/a/img')), message='')
            break
        except:
            i = i + 1
            if i > 10:
                try:
                    driver.close()
                    print("network failed...please try again")
                except:
                    pass
                return
            print("refreshing")
            j = 0
            while 1:
                try:
                    driver.refresh()
                    break
                except:
                    j = j + 1
                    if j > 5:
                        try:
                            driver.close()
                            print("network failed...please try again")
                        except:
                            pass
                        return
                    pass
            pass
    time.sleep(1)
    all_team_with_urls = []
    one_team_with_url = []
    the_list = driver.find_elements(
        by=By.XPATH, value='/html/body/div/div[3]/div/div/div/div[4]/table/tbody/tr/td/div/a')
    for item in the_list:
        one_team_with_url = [year, str(item.text), str(
            item.get_attribute('href'))]
        all_team_with_urls.append(one_team_with_url)
    print(f"---Ending getting team lists in {year}---")
    while 1:
        try:
            driver.close()
            break
        except:
            pass
    return all_team_with_urls


def get_parts_urls_one(a_team):
    global all_process
    global process_count
    global s
    global whole_Parts
    global chrome_options
    year = a_team[0]
    team = a_team[1]
    url = a_team[2]
    i = 0
    while 1:
        try:
            driver = webdriver.Chrome(service=s, options=chrome_options)
            break
        except:
            i = i + 1
            if i > 100:
                print("webdriver failed...please try again")
                return
            pass
    while 1:
        i = 0
        while 1:
            try:
                driver.get(url)
                WebDriverWait(driver, 10, 1).until(
                    EC.presence_of_element_located((By.XPATH, '//*[@id="new_menubar"]/ul/li[1]/div[1]')), message='')
                break
            except:
                i = i + 1
                if i > 10:
                    try:
                        driver.close()
                        print("network failed...please try again")
                    except:
                        pass
                    return
                print("refreshing")
                j = 0
                while 1:
                    try:
                        driver.refresh()
                        break
                    except:
                        j = j + 1
                        if j > 5:
                            try:
                                driver.close()
                                print("network failed...please try again")
                            except:
                                pass
                            return
                        pass
                pass
        time.sleep(1)
        part_num_list = []
        part_numurl_list = []
        part_type_list = []
        part_desc = []
        part_designer = []
        part_len = []
        part_isfavorite_list = []
        try:
            items = driver.find_elements(
                by=By.XPATH, value='/html/body/div/div[4]/div/div/table[1]/tbody/tr/td[3]/a')
            for item in items:
                part_num_list.append(str(item.text))
                part_numurl_list.append(item.get_attribute('href'))
                part_isfavorite_list.append(True)
            items = driver.find_elements(
                by=By.XPATH, value='/html/body/div/div[4]/div/div/table[1]/tbody/tr/td[4]')
            for item in items:
                part_type_list.append(str(item.text))
            items = driver.find_elements(
                by=By.XPATH, value='/html/body/div/div[4]/div/div/table[1]/tbody/tr/td[5]')
            for item in items:
                part_desc.append(str(item.text))
            items = driver.find_elements(
                by=By.XPATH, value='/html/body/div/div[4]/div/div/table[1]/tbody/tr/td[6]')
            for item in items:
                part_designer.append(str(item.text))
            items = driver.find_elements(
                by=By.XPATH, value='/html/body/div/div[4]/div/div/table[1]/tbody/tr/td[7]')
            for item in items:
                part_len.append(str(item.text))
        except:
            part_num_list = []
            part_numurl_list = []
            part_type_list = []
            part_desc = []
            part_designer = []
            part_len = []
            part_isfavorite_list = []
        try:
            items = driver.find_elements(
                by=By.XPATH, value='/html/body/div/div[4]/div/div/table[2]/tbody/tr/td[3]/a')
            for item in items:
                part_num_list.append(str(item.text))
                part_numurl_list.append(item.get_attribute('href'))
                part_isfavorite_list.append(False)
            items = driver.find_elements(
                by=By.XPATH, value='/html/body/div/div[4]/div/div/table[2]/tbody/tr/td[4]')
            for item in items:
                part_type_list.append(str(item.text))
            items = driver.find_elements(
                by=By.XPATH, value='/html/body/div/div[4]/div/div/table[2]/tbody/tr/td[5]')
            for item in items:
                part_desc.append(str(item.text))
            items = driver.find_elements(
                by=By.XPATH, value='/html/body/div/div[4]/div/div/table[2]/tbody/tr/td[6]')
            for item in items:
                part_designer.append(str(item.text))
            items = driver.find_elements(
                by=By.XPATH, value='/html/body/div/div[4]/div/div/table[2]/tbody/tr/td[7]')
            for item in items:
                part_len.append(str(item.text))
        except:
            part_num_list = []
            part_numurl_list = []
            part_type_list = []
            part_desc = []
            part_designer = []
            part_len = []
            part_isfavorite_list = []
        try:
            for i in range(0, len(part_num_list)):
                new_part = Part(part_num_list[i], '', '', part_numurl_list[i], part_desc[i], part_type_list[i], team, year,
                                '', [], '', [], [], [], part_len[i], '', '', [], '', part_isfavorite_list[i], part_designer[i])
                whole_Parts.append(new_part)
                all_process = all_process + 1
        except:
            all_process = all_process + 1
        while 1:
            try:
                driver.close()
                break
            except:
                pass
        return


def get_parts_details_one(a_part):
    global all_process
    global process_count
    global s
    global chrome_options
    isurl = 1
    while 1:
        try:
            with eventlet.Timeout(180, True):
                try:
                    url = a_part.part_url
                except:
                    isurl = 0
                while isurl:
                    i = 0
                    while 1:
                        try:
                            driver = webdriver.Chrome(
                                service=s, options=chrome_options)
                            break
                        except:
                            i = i + 1
                            if i > 10:
                                return
                            pass
                    i = 0
                    gotten = False
                    while 1:
                        try:
                            driver.get(url)
                            WebDriverWait(driver, 10, 1).until(
                                EC.presence_of_element_located((By.XPATH, '//*[@id="new_menubar"]/ul/li[1]/div[1]')), message='')
                            gotten = True
                            break
                        except:
                            i = i + 1
                            if i > 10:
                                break
                            print("refreshing")
                            while 1:
                                try:
                                    driver.refresh()
                                    break
                                except:
                                    pass
                            pass
                    time.sleep(1)
                    if not gotten:
                        print('timeout')
                        print(f'{process_count}/{all_process} is done')
                        return
                    get_date(driver, a_part)
                    get_status(driver, a_part)
                    get_using_parts_and_other_info(driver, a_part)
                    get_assemble_std(driver, a_part)
                    get_used_parts(driver, a_part)
                    get_twin_parts(driver, a_part)
                    get_sequence(driver, a_part)
                    print(f'{process_count}/{all_process} is done')
                    process_count = process_count + 1
                    break
        except:
            print('timeout')
            print(f'{process_count}/{all_process} is done')
            process_count = process_count + 1
        return
    return


def get_sequence(driver, a_part):
    while 1:
        try:
            WebDriverWait(driver, 10, 1).until(
                EC.presence_of_element_located(
                    (By.XPATH, '//*[@id="new_menubar"]/ul/li[1]/div[1]')),
                message='')
            try:
                sequence_entrance = driver.find_elements(
                    by=By.XPATH, value='//*[@id="seq_features_div"]/div[1]/div[1]/span[5]')
                webdriver.ActionChains(driver).move_to_element(sequence_entrance[0]).click(
                    sequence_entrance[0]).perform()
                break
            except:
                print(
                    f"{a_part.part_num} No sequence or sequence acquisition failure...")
                driver.close()
                return
        except:
            i = 0
            while 1:
                try:
                    driver.refresh()
                    break
                except:
                    i = i + 1
                    if i > 10:
                        try:
                            driver.close()
                        except:
                            pass
                        return
                    pass
            pass
    time.sleep(2)
    handles = driver.window_handles
    index_handle = driver.current_window_handle
    for handle in handles:
        if handle != index_handle:
            driver.switch_to.window(handle)
    sequence = driver.find_elements(by=By.XPATH, value="/html/body/pre")
    if len(sequence) > 0:
        a_part.sequence = str(sequence[0].text)
    while 1:
        try:
            driver.close()
            break
        except:
            pass
    handle = driver.window_handles[0]
    driver.switch_to.window(handle)
    while 1:
        try:
            driver.close()
            break
        except:
            pass
    return


def get_status(driver, a_part):
    try:
        item = driver.find_elements(
            by=By.XPATH, value='//*[@id="part_status_wrapper"]/div[1]/a')
        a_part.released = str(item[0].text)
    except:
        a_part.released = ""
    try:
        item = driver.find_elements(
            by=By.XPATH, value='//*[@id="part_status_wrapper"]/div[2]/a')
        a_part.sample = str(item[0].text)
    except:
        a_part.sample = ""
    try:
        item = driver.find_elements(
            by=By.XPATH, value='//*[@id="part_status_wrapper"]/div[3]')
        a_part.stars.append = str(item[0].text)
    except:
        pass
    try:
        item = driver.find_elements(
            by=By.XPATH, value='//*[@id="mw-content-text"]/p')
        a_part.part_name = str(item[0].text)
        for eachitem in item:
            a_part.contents.append(str(eachitem.text))
    except:
        pass
    return


def get_using_parts_and_other_info(driver, a_part):
    if a_part.part_type != 'Composite':
        a_part.using_parts = ['self']
    else:
        using_parts_list = []
        for item in driver.find_elements(by=By.XPATH, value='//*[@id="seq_features_div"]/div[1]/div[4]/div/div[2]'):
            using_parts_list.append(str(item.text))
        for i in range(0, len(using_parts_list)):
            if 'BBa' in using_parts_list[i]:
                continue
            else:
                using_parts_list[i] = 'BBa_' + using_parts_list[i]
        a_part.using_parts = using_parts_list
    return


def get_assemble_std(driver, a_part):
    assemble_lists = []
    for item in driver.find_elements(by=By.XPATH, value='//*[@id="assembly_compatibility"]/div/ul/li'):
        if str(item.get_attribute("class")) == "boxctrl box_green":
            assemble_lists.append('1')
        else:
            assemble_lists.append('0')
    a_part.assemble_std = assemble_lists
    return


def get_used_parts(driver, a_part):
    try:
        item = driver.find_elements(
            by=By.XPATH, value='//*[@id="part_status_wrapper"]/div[4]/a')
        if len(item) == 0:
            a_part.part_used = 'None'
            return
        url = str(item[0].get_attribute('href'))
    except:
        a_part.part_used = 'None'
        return
    k = 0
    while 1:
        try:
            driver.get(url)
            WebDriverWait(driver, 10, 1).until(
                EC.presence_of_element_located((By.XPATH, '/html/body')),
                message='')
            break
        except:
            print("refreshing")
            while 1:
                try:
                    driver.refresh()
                    break
                except:
                    if k > 5:
                        print("network failed...please try again")
                        break
                    k = k + 1
                    pass
            pass
    time.sleep(1)
    used_parts = []
    list = driver.find_elements(by=By.CLASS_NAME, value='noul_link.part_link')
    for item in list:
        used_parts.append(str(item.text))
    if len(used_parts) == 0:
        used_parts.append('None')
    a_part.part_used = used_parts
    while 1:
        try:
            driver.back()
            break
        except:
            pass
    return


def get_twin_parts(driver, a_part):
    try:
        item = driver.find_elements(
            by=By.XPATH, value='//*[@id="part_status_wrapper"]/div[5]/a')
        url = str(item[0].get_attribute('href'))
    except:
        a_part.parts_twin = 'None'
        pass
    k = 0
    try:
        driver.get(url)
        WebDriverWait(driver, 10, 1).until(
            EC.presence_of_element_located((By.XPATH, '/html/body')),
            message='')
    except:
        print("refreshing")
        while 1:
            try:
                driver.refresh()
                break
            except:
                if k > 5:
                    print("network failed...please try again")
                    break
                k = k + 1
                pass
            pass
        pass
    time.sleep(1)
    twin_parts = []
    lst = driver.find_elements(by=By.CLASS_NAME, value='noul_link.part_link')
    for item in lst:
        twin_parts.append(str(item.text))
    if len(twin_parts) == 0:
        twin_parts.append('None')
    a_part.twin = twin_parts
    while 1:
        try:
            driver.back()
            break
        except:
            pass
    return


def get_date(driver, a_part):
    try:
        item = driver.find_element(
            by=By.XPATH, value='//*[@id="content"]/div[3]').text
        _date = re.findall(r'\((.*?)\)', item)[0]
    except:
        _date = 'None'
        pass
    a_part.date = _date
    return


def check_result():
    global whole_Parts
    print('Checking result Parts...')
    res = []
    for a_part in tqdm(whole_Parts):
        if not a_part.contents:
            res.append(a_part)
    return res


def store_parts():
    global whole_Parts
    df_parts = pd.DataFrame()
    print('Saving results...')
    for a_part in tqdm(whole_Parts):
        try:
            df_parts = pd.concat([df_parts, pd.DataFrame({'part_num': a_part.part_num, 'part_name': a_part.part_name, 'part_id': a_part.part_id, 'part_url': a_part.part_url,
                                                    'short_desc': a_part.short_desc, 'part_type': a_part.part_type, 'team': a_part.team, 'year': a_part.year, 'sequence': a_part.sequence, 'contents': ' '.join(a_part.contents), 'released': a_part.released, 'sample': a_part.sample,
                                                     'twins': ' '.join(a_part.twin), 'assemble_std': ' '.join(a_part.assemble_std), 'parts_used': ' '.join(a_part.part_used), 'using_parts': ' '.join(a_part.using_parts), 'len': a_part.len, 'date': a_part.date, 'isfavorite': a_part.isfavorite, 'designer': a_part.designer}, index=[0])])
        except:
            pass
    filename = str(year) + r'collection.csv'
    filepath = os.path.join(datapath, r'collections')
    isExists = os.path.exists(filepath)
    if not isExists:
        os.makedirs(filepath)
    parts_path = os.path.join(filepath, filename)
    try:
        df_parts.to_csv(parts_path, index=False, encoding='utf-8_sig')
        print(filename + 'saved successfully')
        pass
    except:
        print('saving failed...please try again')


def set_database():
    global process_count
    global all_process
    process_count = 1
    all_process = 0


# ### Script

# if you want to **save all_team_with_urls**
# please change this into the same place of the script:</br>
# <code>all_team_with_urls.extend(web_analysis_and_get_team_lists(
#         str(year), driver_path))
#     curStep = 1
#     threads = []
#     threadID = 1
# df1 = pd.DataFrame({'year': [a[0] for a in all_team_with_urls], 'team': [
#     a[1] for a in all_team_with_urls], 'url': [a[2] for a in all_team_with_urls]})
# all_team_path = os.path.join(datapath, r'all_team.csv')
# try:
#     df1.to_csv(all_team_path, index=False)
#     print('"all_team.csv" saved successfully')
#     pass
# except Exception:
#     print('saving failed...please try again')</code>

# In[3]:


# Set the number of threads according to the number of cores of your computer's cpu
threadList = []
for i in range(1,49):
    threadname = 'Thread' + str(i)
    threadList.append(threadname)
#threadList = ["Thread1", "Thread2", "Thread3", "Thread4"]
# Enter the year for which you want to acquire data
# years = range(2004, 2022)
years = [2009]
# Enter the path to your chromedriver
driver_path = r'chromedriver\chromedriver.exe'
chrome_options = Options()
chrome_options.add_argument('blink-settings=imagesEnabled=false')
chrome_options.add_argument('--disable-gpu')
s = Service(driver_path)
# Enter the path to save the data
datapath = r'dataset'
whole_Parts = []
all_process = 0
all_team_with_urls = []
queueLock = threading.Lock()
workQueue = queue.Queue(10000)
set_database()
for year in years:
    exitFlag = 0
    all_team_with_urls = (web_analysis_and_get_team_lists(str(year)))
    curStep = 1
    threads = []
    threadID = 1
    # Create threads
    for tName in threadList:
        thread = myThread(threadID, tName, workQueue)
        thread.start()
        threads.append(thread)
        threadID += 1
    # Fill the queue
    print('---Starting getting Parts---')
    for word in tqdm(all_team_with_urls):
        workQueue.put(word)
    while not workQueue.empty():
        pass
    exitFlag = 1
    for t in threads:
        t.join()
    print('---Ending getting Parts---')
    curStep = 2
    exitFlag = 0
    threads = []
    threadID = 1
    finished = 0
    # Create threads
    print('---Starting getting Part details---')
    for tName in threadList:
        thread = myThread(threadID, tName, workQueue)
        thread.start()
        threads.append(thread)
        threadID += 1
    # Fill the queue
    for word in tqdm(whole_Parts):
        workQueue.put(word)
    while not workQueue.empty():
        pass
    exitFlag = 1
    for t in threads:
        t.join()
    remaining_parts = check_result()
    curStep = 3
    exitFlag = 0
    threads = []
    threadID = 1
    all_process = len(remaining_parts)
    process_count = 1
    finished = 0
    # Create threads
    for tName in threadList:
        thread = myThread(threadID, tName, workQueue)
        thread.start()
        threads.append(thread)
        threadID += 1
    # Fill the queue
    for word in tqdm(remaining_parts):
        workQueue.put(word)
    while not workQueue.empty():
        pass
    exitFlag = 1
    for t in threads:
        t.join()
    print('---Ending getting Part details---')
    store_parts()


# In[ ]:




