import re
import datetime

def read_file(org_file):
    date_bins = {6: 0, 5: 0, 4: 0, 3: 0, 2: 0, 1: 0, 0: 0}
    now = datetime.date.today() 
    prev_line = ""
    with open(org_file) as fp:
        for line in fp:
            if "CLOSED" in line:
                m = re.search(r'(\d{4}-\d{2}-\d{2})', line).group(1)
                found_date = datetime.date.fromisoformat(m)
                difference = (now - found_date).days
                if difference < 7:
                    date_bins[difference] += 1
            else:
                prev_line = line
    return date_bins 

fp = "/Users/maryannewachter/dropbox/org/life.org"

vals = read_file(fp)
print(vals)

print("TEST")
if __name__ == " __main__":
    pass
