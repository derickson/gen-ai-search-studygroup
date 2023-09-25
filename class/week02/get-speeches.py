
import requests 
from datetime import datetime
from bs4 import BeautifulSoup
from tqdm import tqdm
import pickle


PICKLE_FILE = "./STATE_OF_THE_UNION.pickle"


## Converts dates like this "February 7, 2023" to "2023-02-07"
def convert_to_iso(date_str):
    # Parse the string to a datetime object
    date_obj = datetime.strptime(date_str, '%B %d, %Y')    
    # Convert the datetime object to an ISO format string
    return date_obj.date().isoformat()



## State of the Union Addresses can be found here: https://www.govinfo.gov/features/state-of-the-union
speech_links = [
  {
    "date": "February 7, 2023",
    "administration": "Biden",
    "url": "https://www.govinfo.gov/content/pkg/CREC-2023-02-07/html/CREC-2023-02-07-pt1-PgS257-2.htm"
  },
  {
    "date": "March 1, 2022",
    "administration": "Biden",
    "url": "https://www.govinfo.gov/content/pkg/DCPD-202200127/html/DCPD-202200127.htm"
  },
  {
    "date": "April 28, 2021",
    "administration": "Biden",
    "url": "https://www.govinfo.gov/content/pkg/DCPD-202100347/html/DCPD-202100347.htm"
  },
  {
    "date": "February 4, 2020",
    "administration": "Trump",
    "url": "https://www.govinfo.gov/content/pkg/DCPD-202000058/html/DCPD-202000058.htm"
  },
  {
    "date": "February 5, 2019",
    "administration": "Trump",
    "url": "https://www.govinfo.gov/content/pkg/DCPD-201900063/html/DCPD-201900063.htm"
  },
  {
    "date": "January 30, 2018",
    "administration": "Trump",
    "url": "https://www.govinfo.gov/content/pkg/DCPD-201800064/html/DCPD-201800064.htm"
  },
  {
    "date": "February 28, 2017",
    "administration": "Trump",
    "url": "https://www.govinfo.gov/content/pkg/DCPD-201700150/html/DCPD-201700150.htm"
  },
  {
    "date": "January 12, 2016",
    "administration": "Obama",
    "url": "https://www.govinfo.gov/content/pkg/DCPD-201600012/html/DCPD-201600012.htm"
  },
  {
    "date": "January 20, 2015",
    "administration": "Obama",
    "url": "https://www.govinfo.gov/content/pkg/DCPD-201500036/html/DCPD-201500036.htm"
  },
  {
    "date": "January 28, 2014",
    "administration": "Obama",
    "url": "https://www.govinfo.gov/content/pkg/DCPD-201400050/html/DCPD-201400050.htm"
  },
  {
    "date": "February 12, 2013",
    "administration": "Obama",
    "url": "https://www.govinfo.gov/content/pkg/DCPD-201300090/html/DCPD-201300090.htm"
  },
  {
    "date": "January 24, 2012",
    "administration": "Obama",
    "url": "https://www.govinfo.gov/content/pkg/DCPD-201200048/html/DCPD-201200048.htm"
  },
  {
    "date": "January 25, 2011",
    "administration": "Obama",
    "url": "https://www.govinfo.gov/content/pkg/DCPD-201100047/html/DCPD-201100047.htm"
  },
  {
    "date": "January 27, 2010",
    "administration": "Obama",
    "url": "https://www.govinfo.gov/content/pkg/DCPD-201000055/html/DCPD-201000055.htm"
  },
  {
    "date": "February 24, 2009",
    "administration": "Obama",
    "url": "https://www.govinfo.gov/content/pkg/DCPD-200900105/html/DCPD-200900105.htm"
  },
  {
    "date": "February 4, 2008",
    "administration": "Bush43",
    "url": "https://www.govinfo.gov/content/pkg/WCPD-2008-02-04/html/WCPD-2008-02-04-Pg117.htm"
  },
  {
    "date": "January 29, 2007",
    "administration": "Bush43",
    "url": "https://www.govinfo.gov/content/pkg/WCPD-2007-01-29/html/WCPD-2007-01-29-Pg57.htm"
  },
  {
    "date": "February 6, 2006",
    "administration": "Bush43",
    "url": "https://www.govinfo.gov/content/pkg/WCPD-2006-02-06/html/WCPD-2006-02-06-Pg145-3.htm"
  },
  {
    "date": "February 7, 2005",
    "administration": "Bush43",
    "url": "https://www.govinfo.gov/content/pkg/WCPD-2005-02-07/html/WCPD-2005-02-07-Pg126.htm"
  },
  {
    "date": "January 26, 2004",
    "administration": "Bush43",
    "url": "https://www.govinfo.gov/content/pkg/WCPD-2004-01-26/html/WCPD-2004-01-26-Pg94-2.htm"
  },
  {
    "date": "February 3, 2003",
    "administration": "Bush43",
    "url": "https://www.govinfo.gov/content/pkg/WCPD-2003-02-03/html/WCPD-2003-02-03-Pg109.htm"
  },
  {
    "date": "February 4, 2002",
    "administration": "Bush43",
    "url": "https://www.govinfo.gov/content/pkg/WCPD-2002-02-04/html/WCPD-2002-02-04-Pg133-3.htm"
  },
  {
    "date": "March 5, 2001",
    "administration": "Bush43",
    "url": "https://www.govinfo.gov/content/pkg/WCPD-2001-03-05/html/WCPD-2001-03-05-Pg351-2.htm"
  },
  {
    "date": "January 31, 2000",
    "administration": "Clinton",
    "url": "https://www.govinfo.gov/content/pkg/WCPD-2000-01-31/html/WCPD-2000-01-31-Pg160-2.htm"
  },
  {
    "date": "January 25, 1999",
    "administration": "Clinton",
    "url": "https://www.govinfo.gov/content/pkg/WCPD-1999-01-25/html/WCPD-1999-01-25-Pg78-2.htm"
  },
  {
    "date": "February 2, 1998",
    "administration": "Clinton",
    "url": "https://www.govinfo.gov/content/pkg/WCPD-1998-02-02/html/WCPD-1998-02-02-Pg129-2.htm"
  },
  {
    "date": "February 10, 1997",
    "administration": "Clinton",
    "url": "https://www.govinfo.gov/content/pkg/WCPD-1997-02-10/html/WCPD-1997-02-10-Pg136.htm"
  },
  {
    "date": "January 29, 1996",
    "administration": "Clinton",
    "url": "https://www.govinfo.gov/content/pkg/WCPD-1996-01-29/html/WCPD-1996-01-29-Pg90.htm"
  },
  {
    "date": "January 30, 1995",
    "administration": "Clinton",
    "url": "https://www.govinfo.gov/content/pkg/WCPD-1995-01-30/html/WCPD-1995-01-30-Pg96.htm"
  },
  {
    "date": "January 31, 1994",
    "administration": "Clinton",
    "url": "https://www.govinfo.gov/content/pkg/WCPD-1994-01-31/html/WCPD-1994-01-31-Pg148.htm"
  },
  {
    "date": "February 22, 1993",
    "administration": "Clinton",
    "url": "https://www.govinfo.gov/content/pkg/WCPD-1993-02-22/html/WCPD-1993-02-22-Pg215-2.htm"
  }
]


## scrape the Content from the web
for speech in tqdm(speech_links, desc="Scraping speeches"):
    
    url = speech["url"]
    result = requests.get(url)
    content = result.content
    soup = BeautifulSoup(content, "html.parser")
    speech["text"] = soup.get_text()

    speech["date_iso"] = convert_to_iso(speech["date"])


## print one of the speeches
print(speech_links[0])


## save the scraped data to a .picle file so we don't have to do this again
with open(PICKLE_FILE, "wb") as f:
    pickle.dump(speech_links, f, protocol=pickle.HIGHEST_PROTOCOL)


