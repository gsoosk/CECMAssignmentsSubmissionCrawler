
# coding: utf-8

# # CECM Late Crawler
# 
# This code crawle status of submissions. 
# 
# * You should have a csv containing student ids.
# * You can use [hadi's repository](https://github.com/hadisfr/cecm-sid-crawler) to crawle student ids.

# In[22]:


import requests
import re
from getpass import getpass
import pandas as pd


# In[23]:


print("Get Late Submissions from CECM")
assignment_id = int(input("AssignmentID: "))
session = getpass("Session[MoodleSession]: ")
id_csv_path = input("CSV Containing IDs Path: ")
file_name = input("Output CSV File Name: ")


# In[33]:


def get_late_submissions(session, assignment_id):
    request_response = requests.post(
        f"https://cecm.ut.ac.ir/mod/assign/view.php?id={assignment_id}&action=grading", 
        cookies={'MoodleSession': session},
        data={
            'unified-filters[]': "4:5",  # role: student
            'unified-filter-submitted': 1,
        }
    ).text.replace("\n", "")
    late_pattern = (
        r'<tr[^>]*class="user(?P<id>[0-9]+)[^>]*>.*?'
        r'<td class="cell c2"[^>]*>.*?<a[^>]*>(?P<name>[^<]+)</a></td>.*?'
        r'<td class="cell c4"[^>]*>.*?<div[^>]*>(?P<status>[^<]+)</div></td>.*?'
        r'</tr>'
    )
    return [entry.groupdict() for entry in re.finditer(late_pattern, request_response)]


# In[42]:


lates = get_late_submissions(session, assignment_id)


# In[43]:


lates_csv = pd.read_csv(id_csv_path, index_col='id')


# In[44]:


lates_csv['late'] = 'Not Submitted'
lates_csv['name'] = 'Not Submitted'


# In[45]:


for late in lates :
    lates_csv.at[int(late['id']), 'name'] = late['name']
    lates_csv.at[int(late['id']), 'late'] = late['status']


# In[46]:


def cint(x):
    return int(x) if x else 0


# In[47]:


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
        elif total_time_in_mins <= 3*60: return  0.3
        elif total_time_in_mins >= 75*60: return  -1
        else: return int((total_time_in_mins - 3*60) / (24*60)) + 1.3


# In[48]:


lates_csv['late'] = lates_csv['late'].apply(AP_grade_system_mapper)


# In[49]:


lates_csv.to_csv(f'{file_name}.csv')

