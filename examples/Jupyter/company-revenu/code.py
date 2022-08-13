import pandas as pd
import io
#import seaborn as sns
import matplotlib.pyplot as plt
import requests 

#sns.set(style="darkgrid")

#resp = requests.get(url).text
#with open('data.csv', 'w') as f: f.write(resp)
url='https://gist.githubusercontent.com/bobbae/b4eec5b5cb0263e7e3e63a6806d045f2/raw/279b794a834a62dc108fc843a72c94c49361b501/data.csv'
s=requests.get(url).content
df= pd.read_csv(io.StringIO(s.decode('utf-8')))
#df= pd.read_csv('data.csv')

print(len(df))

#>> 25500

df.columns = ['year', 'rank', 'company', 'revenue', 'profit']

df.dtypes

#>>year         int64
#>>rank         int64
#>>company     object
#>>revenue    float64
#>>profit      object
#>>dtype: object

non_numeric_profits = df.profit.str.contains('[^0-9.-]')
print(non_numeric_profits.head())
#>>0    False
#>>1    False
#>>2    False
#>>3    False
#>>4    False
print(df.loc[non_numeric_profits].head())
#>>Name: profit, dtype: bool
#>>     year  rank                company  revenue profit
#>>228  1955   229                 Norton    135.0   N.A.
#>>290  1955   291        Schlitz Brewing    100.0   N.A.
#>>294  1955   295  Pacific Vegetable Oil     97.9   N.A.
#>>296  1955   297     Liebmann Breweries     96.0   N.A.
#>>352  1955   353     Minneapolis-Moline     77.4   N.A.
print(len(df.loc[non_numeric_profits]))
#>>369

set(df.profit[non_numeric_profits])

#>>{'N.A.'}

df = df.loc[~non_numeric_profits]
print(len(df))
#>>25131
df.profit = df.profit.apply(pd.to_numeric)
df.dtypes

#>>year         int64
#>>rank         int64
#>>company     object
#>>revenue    float64
#>>profit     float64
#>>dtype: object

with pd.option_context('display.max_rows', None, 'display.max_columns',None):
    print(df.sort_values(by='profit', ascending=False)[:20])
#>>       year  rank                 company   revenue   profit
#>>25001  2005     2             Exxon Mobil  270772.0  25330.0
#>>22001  1999     2              Ford Motor  144416.0  22071.0
#>>24501  2004     2             Exxon Mobil  213199.0  21510.0
#>>24507  2004     8               Citigroup   94713.0  17853.0
#>>23000  2001     1             Exxon Mobil  210392.0  17720.0
#>>25007  2005     8               Citigroup  108276.0  17046.0
#>>25004  2005     5        General Electric  152363.0  16593.0
#>>23501  2002     2             Exxon Mobil  191581.0  15320.0
#>>24005  2003     6               Citigroup  100789.0  15276.0
#>>24504  2004     5        General Electric  134187.0  15002.0
#>>25017  2005    18   Bank of America Corp.   63324.0  14143.0
#>>23506  2002     7               Citigroup  112022.0  14126.0
#>>24004  2003     5        General Electric  131698.0  14118.0
#>>23505  2002     6        General Electric  125913.0  13684.0
#>>23005  2001     6               Citigroup  111826.0  13519.0
#>>25005  2005     6           ChevronTexaco  147967.0  13328.0
#>>23004  2001     5        General Electric  129853.0  12735.0
#>>23009  2001    10  Verizon Communications   64707.0  11797.0
#>>24002  2003     3             Exxon Mobil  182466.0  11460.0
#>>25023  2005    24                  Pfizer   52921.0  11361.0

counts = {}

for d in df.to_dict('records'):
    company = d['company']
    if company not in counts:
        counts[company] = 0
    counts[company] += 1
print('unique companies ',len(counts))
#>>unique companies  1860

from collections import OrderedDict
cc = OrderedDict(sorted(counts.items(), key=lambda x: -x[1]))
ccc = list(cc.items())
print('most repeated ',ccc[:10])

#>>most repeated  [('CBS', 57), ('OfficeMax', 55), ('General Motors', 51), ('Exxon Mobil', 51), ('General Electric', 51), ('DuPont', 51), ('ChevronTexaco', 51), ('Goodyear Tire & Rubber', 51), ('Boeing', 51), ('Navistar International', 51)]

uu = OrderedDict(sorted(counts.items(), key=lambda x: x[1]))
uuu = filter(lambda x: x[1]==1, list(uu.items()))
print('unique and unrepeated ',len(list(uuu)))

#>>unique and unrepeated  182

jdf = df.to_json(orient='records')
with open('dataoutput.json','w') as jsonfp:
    jsonfp.write(jdf)

ddf = df.to_dict('records')
import json
with open('dataoutput2.json','w') as jf2:
     print(json.dump(ddf, jf2, indent=4))
#>>None

group_by_year = df.loc[:, ['year', 'revenue', 'profit']].groupby('year')
avgs = group_by_year.mean()
x = avgs.index
y1 = avgs.profit

def plot(x, y, ax, title, y_label):
    ax.set_title(title)
    ax.set_ylabel(y_label)
    ax.plot(x, y)
    ax.margins(x=0, y=0)

fig, ax = plt.subplots()
plot(x, y1, ax, 'Increase in mean Fortune 500 company profits from 1955 to 2005', 'Profit (millions)')

