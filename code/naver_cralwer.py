import requests
from urllib.request import urlopen
from urllib.parse import urlparse
import pandas as pd
from pandas import json_normalize
import urllib.request
import json
import time


keyword = '조미김'
# 최대 55개 가능
display = 55
start = 1
url = 'https://openapi.naver.com/v1/search/image?query=' + keyword + '&display='+ str(display) +'&start=' + str(start)
result = requests.get(urlparse(url).geturl(),
                      headers={'X-Naver-Client-Id':'HRQsrgKYjVzz97H0KCmQ',
                             'X-Naver-Client-Secret':'oeabA9y57B'
                             }
                      )



json_obj = result.json()
temp_data = json.dumps(json_obj, indent = 4)
json_data = json.loads(temp_data)
links = json_normalize(json_data['items'])
df_link = pd.DataFrame(links['link'], index=links.index)

print('===========crawling start===========')
#download_time checking
total_time = time.time()
n = 1
for i in df_link.index:
       header = {'User-Agent': 'Mozilla/5.0'}
       imgUrl =  df_link['link'][i]
       req = urllib.request.Request(imgUrl, headers=header)
       start = time.time()
       with urlopen(req) as f:
              with open('./testimg/' + keyword + str(n)+'.jpg', 'wb') as l:
                     print(time.time()-start)
                     img = f.read()
                     l.write(img)
       n += 1
       # time.sleep(1)
       print(str(i+1)+"번째\n", "img_url-> " + imgUrl)       
print("총크롤링 시간-> " + str(time.time()-total_time))
print('===========crawling done===========')