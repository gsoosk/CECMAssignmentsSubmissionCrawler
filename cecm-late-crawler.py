
# coding: utf-8

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


# In[17]:


print("Get Late Submissions from CECM")
assignment_id = int(input("AssignmentID: "))
session = getpass("Session[MoodleSession]: ")
id_csv_path = input("CSV Containing IDs Path: ")
file_name = input("Output CSV File Name: ")


# In[95]:


def print_progressbar(title, i, l):
    percentage = i / l * 100
    print( title + "\t" + "%s\t%.2f%% (%d of %d)\t\r" % (int(percentage / 10) * "|" + (10 - int(percentage / 10)) * ".", percentage, i, l), end='\r')


# In[96]:


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


# In[97]:


lates = get_late_submissions(session, assignment_id)


# In[98]:


lates_csv = pd.read_csv(id_csv_path, index_col='id')


# In[99]:


lates_csv['late'] = 'Not Submitted'
lates_csv['name'] = 'Not Submitted'


# In[100]:


for idx, late in enumerate(lates) :
    lates_csv.at[int(late['id']), 'name'] = late['name']
    lates_csv.at[int(late['id']), 'late'] = late['status']


# In[101]:


def cint(x):
    return int(x) if x else 0


# In[102]:


def AP_grade_system_mapper(s): 
    if s == 'Not Submitted':
        return -1
    elif s == 'Submitted for grading':
        return 0
    else :
        times = re.search('((?P<days>[0-9]+) days )?((?P<day>[0-9]+) day )?((?P<hours>[0-9]+) hours )?((?P<hour>[0-9]+) hour )?((?P<mins>[0-9]+) mins )?((?P<min>[0-9]+) min )?((?P<secs>[0-9]+) secs )?', s).groupdict()
        days, hours, mins, secs = cint(times['days'])+cint(times['day']), cint(times['hours'])+cint(times['hour']), cint(times['mins'])+cint(times['min']), cint(times['secs'])
        total_time_in_mins = days*24*60 + hours*60 + mins

        if total_time_in_mins <= 30: return  0
        elif total_time_in_mins <= 60 * 24: return  1
        elif total_time_in_mins <= 60 * 24 * 2 : return 2
        elif total_time_in_mins <= 60 * 24 * 3 : return 3
        else : return  -1

        # return int(total_time_in_mins/60)

# In[103]:


lates_csv['late'] = lates_csv['late'].apply(AP_grade_system_mapper)


# In[104]:


lates_csv.to_csv(f'{file_name}.csv')

