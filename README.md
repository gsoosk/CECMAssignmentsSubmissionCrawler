# CECM Assignment's Submission Crawler
This is a simple script to crawl assignment's submissions of [CECM](cecm.ut.ac.ir). For running this script you should have student ids. It can be crawled by [hadi's script](https://github.com/hadisfr/cecm-sid-crawler) which you can use it instead.

## How to run?
```
pip install -r requirements.txt
python3 cecm-late-crawler.py 
```
## What returns?
It returns your input ids with their late status. This status mapped to [UT AP](https://github.com/UTAP) late grading system (you can customized it if you want). 
UT AP grading system outputs : 
```
0 -> Submitted on time
0.3 -> less than 3 hours
[0.3, 3.3] ->  3 hours to 3 days and 3 hours
-1 -> Not submitted/More than 3 days and 3 hours
```
