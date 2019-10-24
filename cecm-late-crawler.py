
# coding: utf-8

# <h1>Table of Contents<span class="tocSkip"></span></h1>
# <div class="toc"><ul class="toc-item"></ul></div>

# # CECM Late Crawler
# 
# This code crawle status of submissions. 
# 
# * You should have a csv containing student ids.
# * You can use [hadi's repository](https://github.com/hadisfr/cecm-sid-crawler) to crawle student ids.

# In[1]:


import requests
import re
from getpass import getpass
import pandas as pd


# In[2]:


print("Get Late Submissions from CECM")
assignment_id = int(input("AssignmentID: "))
session = getpass("Session[MoodleSession]: ")
id_csv_path = input("CSV Containing IDs Path: ")
file_name = input("Output CSV File Name: ")


# In[3]:


def print_progressbar(title, i, l):
    percentage = i / l * 100
    print( title + "\t" + "%s\t%.2f%% (%d of %d)\t\r" % (int(percentage / 10) * "|" + (10 - int(percentage / 10)) * ".", percentage, i, l), end='\r')


# In[4]:


def get_late_submissions(session, assignment_id):

    print_progressbar('Fetching Page' ,0, 100)
    request_response = requests.post(
        f"https://cecm.ut.ac.ir/mod/assign/view.php?id={assignment_id}&action=grading", 
        cookies={'MoodleSession': session},
        data={
            'unified-filters[]': "4:5",  # role: student
            'unified-filter-submitted': 1,
        }
    ).text.replace("\n", "")
    print_progressbar('Fetching Page' ,100, 100)
    late_pattern = (
        r'<tr[^>]*class="user(?P<id>[0-9]+)[^>]*>.*?'
        r'<td class="cell c2"[^>]*>.*?<a[^>]*>(?P<name>[^<]+)</a></td>.*?'
        r'<td class="cell c4"[^>]*>.*?<div[^>]*>(?P<status>[^<]+)</div></td>.*?'
        r'</tr>'
    )
    founded = list(re.finditer(late_pattern, request_response))
    groupdicts = []
    for idx, entry in enumerate(founded):
        groupdicts.append(entry.groupdict())
        print_progressbar('Crawling Submissions' ,idx+1, len(founded))
    return groupdicts


# In[5]:


lates = get_late_submissions(session, assignment_id)


# In[6]:


lates_csv = pd.read_csv(id_csv_path, index_col='id')


# In[7]:


lates_csv['late'] = 'Not Submitted'
lates_csv['name'] = 'Not Submitted'


# In[8]:


for idx, late in enumerate(lates) :
    lates_csv.at[int(late['id']), 'name'] = late['name']
    lates_csv.at[int(late['id']), 'late'] = late['status']


# In[9]:


def cint(x):
    return int(x) if x else 0


# In[10]:


def AP_grade_system_mapper(s): 
    if s == 'Not Submitted':
        return -1
    elif s == 'Submitted for grading':
        return 0
    else :
        times = re.search('((?P<days>[0-9]+) days )?((?P<hours>[0-9]+) hours )?((?P<mins>[0-9]+) mins )?((?P<secs>[0-9]+) secs )?', s).groupdict()
        days, hours, mins, secs = cint(times['days']), cint(times['hours']), cint(times['mins']), cint(times['secs'])
        total_time_in_mins = days*24*60 + hours*60 + mins
        if total_time_in_mins <= 4: return  0
        elif total_time_in_mins <= 3*60: return  0.33
        elif total_time_in_mins >= 75*60: return  -1
        else: return int((total_time_in_mins - 3*60) / (24*60)) + 1.33


# In[11]:


lates_csv['late'] = lates_csv['late'].apply(AP_grade_system_mapper)


# In[12]:


lates_csv.to_csv(f'{file_name}.csv')

