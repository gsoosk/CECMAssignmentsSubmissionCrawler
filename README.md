# CECM Assignment's Submission Crawler
This is a simple script to crawl assignment's submissions of [CECM](cecm.ut.ac.ir). For running this script you should have student ids. It can be crawled by [hadi's script](https://github.com/hadisfr/cecm-sid-crawler) which you can use it instead.

## How to run?
```
pip install -r requirements.txt
python3 cecm-late-crawler.py 
```
## What returns?
It returns your input ids with their late status. This status mapped to [UT AP](https://github.com/UTAP) late grading system (you can customize it if you want. For that goal, change `AP_grade_system_mapper`). 
UT AP grading system outputs : 
```
0 -> Submitted on time
1 -> [0:30, 24:00] hours late
2 -> [24:00, 48:00] hours late
3 -> [48:00, 72:00] hours late
-1 -> Not submitted/More than 72 hours
```
