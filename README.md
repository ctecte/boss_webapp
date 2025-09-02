# SMU BOSS bidding Historical bids combined with Timings, and filter by prof functionality

No idea why school doesnt just do this, so ill do it myself for easier reference

# If you just want to use it, visit here
https://orangepi.tail4dee5c.ts.net

This is hosted on my personal orange pi zero 3 with tailscale funnel and gunicorn. 
The Docker compose yml is there for anyone who wants to run this.
```
docker compose up -d
```
Thats the only line of code you need to run this lol. Access through port 5000. http://localhost:5000

Note that this db only contains data from 2021-22 T2 to 2024-25 T2. Will update once the next round of bidding excel sheet is released

# Explaning the data collection 
Boss data is collected from BOSS website naturally. There is a download link that leads to a shared file drive allowing active students to download an xlsx of the previous term bids. 

For data that maps section (G1) to the day (FRI 12:00), this is available here on SMU's own website
https://publiceservices.smu.edu.sg/psc/ps/EMPLOYEE/SA/c/SIS_CR.SIS_CS_SS_CLS_SCHD.GBL

You can download the results of current sem and future sems into an excel.

However, the page does not allow you to query past semesters, as it is not selectable in the dropdown. The curl command is how i got around the lack of dropdown option, by directly passing in parameters to query the backend database.

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
Nothing to explain, just use Jupyter notebook to see what you're doing
Make sure you adjust the column names according to your data. 

Ensure you are merging only the same term, then left join on section = section and course_code = course_code
Could inner join too but just left join 

# Data storage: SQLite3 .db file
Its lightweight and works, aint spinning up a MySQL server docker container for this.
Pass the excel data into the SQLite database

# Functional website
First time using flask to build a website. First time building a website fullstop.
Followed this tutorial until part 3 https://www.youtube.com/watch?v=QnDWIZuWYW0&t=366s

# I have no idea if this breaks any SMU guidelines or data policies btw



