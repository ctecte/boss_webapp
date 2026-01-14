# SMU BOSS bidding Historical bids combined with Timings, with enhanced filter options 

<img width="2524" height="1258" alt="image" src="https://github.com/user-attachments/assets/5e585394-389e-4205-af74-267815bb6483" />

No idea why school doesnt offer this, so ill do it myself for easier reference.

# If you just want to use it, visit here
https://orangepi.tail4dee5c.ts.net
The Docker compose yml is there for anyone who wants to run this locally, or update the boss_data.db when I am not a student anymore.
```
docker compose up -d
```
To run, download only the main folder, then run the above command in the directory with the docker yaml inside. By default it is on http://localhost:5000 .

This db contains data from 2021-22 T2 to 2025-26 T1, and may be updated by me manually when the smu sharepoint releases the excel sheet. 

# Explaning the data collection 
Boss data is collected from BOSS website naturally. There is a download link that leads to a shared file drive allowing active students to download an xlsx of the previous term bids. 

For data that maps section (G1) to the day (FRI 12:00), this is available here on SMU's own website
https://publiceservices.smu.edu.sg/psc/ps/EMPLOYEE/SA/c/SIS_CR.SIS_CS_SS_CLS_SCHD.GBL

You can download the results of current sem and future sems into an excel. If I am not mistaken, it is downloaded as a .xls. It should be converted with an online converted to .xlsx.

The page does not allow you to query past semesters, as it is not selectable in the dropdown. The curl command is how i got around the lack of dropdown option, by directly passing in parameters to query the backend database.

# Curl the SMU website
In case you require past data, refer to the curl smu website txt file
the last line
... &ICAppClsData=^&SIS_CLS_SCHDWRK_STRM=2432^" --output 2432.html 

Adjust this line accordingly "...STRM=2432" 
The 4 digit number represents the year and term. 
The first 2 digits represent the year. 

24XX is 2024-25

The next 2 represent the semester

2420 is 2024-25 T2

2410 is 2024-25 T1

Curl it into a html output, and parse it with beautifulsoup. Take note the html you parse will likely be broken, and you should use parser=lxml. Refer to the SMU scrape website py for more info
The script parses the website and then saves the data into a csv, which can be manipulated with pandas and exported to excel. You can then merge this csv-> excel with the available boss data excel.

# Merging the data with pandas 
Once you have the timing sheet, follow the naming convention for the file

20XX-20XX_T1_timing.xlsx

After that, replace the headers/column names of xx_timing.xlsx with the column names found in template.xlsx (in raw_data folder) before using the Merge_timing_and_bid_ipynb to merge the dfs. 

Please ensure that the boss bid xlsx and the timing.xlsx are in the same folder as the notebook
# Data storage: SQLite3 .db file
The db file can be rebuilt with the excel sheets using the helper script convert_to_sql.py






