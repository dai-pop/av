import pysrt
import sys
from bs4 import BeautifulSoup

for f in sys.argv[1:]:
    s = pysrt.open(f)
    for i,x in enumerate(s):
        soup = BeautifulSoup(x.text, features="html.parser")
        s[i].text = soup.get_text()
    s.save()
