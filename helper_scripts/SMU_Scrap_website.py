from bs4 import BeautifulSoup
from bs4 import XMLParsedAsHTMLWarning
import warnings
import pandas as pd

warnings.filterwarnings("ignore", category=XMLParsedAsHTMLWarning)

with open("2120.html", encoding='utf-8') as file:
    content = file.read()

soup = BeautifulSoup(content, 'lxml')  # html.parser will NOT work
i = 0
data = "term;course_code;title;topic;section;meet;day;start_time;end_time;venue;instructor;num_instructors;start_date;end_date;class_number;\n"

elements_by_id = {tag.get("id"): tag for tag in soup.find_all("span") if tag.get("id")}
i = 0
data = "term;course_code;title;topic;section;meet;day;start_time;end_time;venue;instructor;num_instructors;start_date;end_date;class_number;\n"

while True:
    term_id = f"SIS_CLS_SCHDWRK_DESCR40${i}"
    if term_id not in elements_by_id:
        break

    fields = {
        "term": f"SIS_CLS_SCHDWRK_DESCR40${i}",
        "course_code": f"SIS_CLS_SCHD_VW_SIS_CRSE_CD${i}",
        "title": f"SIS_CLS_SCHD_VW_DESCR${i}",
        "topic": f"SIS_CLS_SCHD_VW_CRSE_TOPIC${i}",
        "section": f"SIS_CLS_SCHD_VW_CLASS_SECTION${i}",
        "meet": f"SIS_CLS_SCHD_VW_CLASS_MTG_NBR${i}",
        "day": f"SIS_CLS_SCHD_VW_CLASS_MTG_DAYS${i}",
        "start_time": f"SIS_CLS_SCHD_VW_MEETING_TIME_START${i}",
        "end_time": f"SIS_CLS_SCHD_VW_MEETING_TIME_END${i}",
        "venue": f"SIS_CLS_SCHD_VW_FACILITY_DESCR${i}",
        "instructor": f"SIS_CLS_SCHD_VW_SIS_NAME${i}",
        "num_instructors": f"SIS_CLS_SCHD_VW_INSTR_ASSIGN_SEQ${i}",
        "start_date": f"SIS_CLS_SCHD_VW_START_DT${i}",
        "end_date": f"SIS_CLS_SCHD_VW_END_DT${i}",
        "class_number": f"SIS_CLS_SCHD_VW_CLASS_NBR${i}"
    }

    for key, field_id in fields.items():
        span = elements_by_id.get(field_id)
        data += span.get_text(strip=True) + ";" if span else ";"
    data += "\n"
    i += 1

# while (True):
#     print(i)
#     term = soup.find("span", {"id": f"SIS_CLS_SCHDWRK_DESCR40${i}"})
#     if (term == None):
#         break
#     fields = {
#         "term": f"SIS_CLS_SCHDWRK_DESCR40${i}",
#         "course_code": f"SIS_CLS_SCHD_VW_SIS_CRSE_CD${i}",
#         "title": f"SIS_CLS_SCHD_VW_DESCR${i}",
#         "topic": f"SIS_CLS_SCHD_VW_CRSE_TOPIC${i}",
#         "section": f"SIS_CLS_SCHD_VW_CLASS_SECTION${i}",
#         "meet": f"SIS_CLS_SCHD_VW_CLASS_MTG_NBR${i}",
#         "day": f"SIS_CLS_SCHD_VW_CLASS_MTG_DAYS${i}",
#         "start_time": f"SIS_CLS_SCHD_VW_MEETING_TIME_START${i}",
#         "end_time": f"SIS_CLS_SCHD_VW_MEETING_TIME_END${i}",
#         "venue": f"SIS_CLS_SCHD_VW_FACILITY_DESCR${i}",
#         "instructor": f"SIS_CLS_SCHD_VW_SIS_NAME${i}",
#         "num_instructors": f"SIS_CLS_SCHD_VW_INSTR_ASSIGN_SEQ${i}",
#         "start_date": f"SIS_CLS_SCHD_VW_START_DT${i}",
#         "end_date": f"SIS_CLS_SCHD_VW_END_DT${i}",
#         "class_number": f"SIS_CLS_SCHD_VW_CLASS_NBR${i}"
#     }
#     for key, field_id in fields.items():
#         span = soup.find("span", {"id": field_id})
#         data += span.get_text(strip=True) + ";"
#     data += "\n"
#     i += 1


with open('output.csv', 'w') as f:
    f.write(data)

