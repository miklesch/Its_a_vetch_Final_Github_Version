"""Getting the Data by scraping a website: 
https://www.mikroveda.info/en/2021/02/06/good-neighbors-bad-neighbors/
"""
from bs4 import BeautifulSoup
import requests
import json
import re

page = requests.get("https://www.mikroveda.info/en/2021/02/06/good-neighbors-bad-neighbors/")
soup = BeautifulSoup(page.content, 'html.parser')
datas = soup.find_all("li")

page_list = []
for e in datas:
  page_list.append(e.text)
    
# #Extracting the data

x_beginning = page_list.index("Potatoes: broad beans, spinach, kohlrabi")
x_end = page_list.index("Beet: cucumbers, bush beans, savory, dill, garlic, onions, cabbage, lettuce")
y_beginning = page_list.index("Cucumbers: tomatoes, radishes, radishes, potatoes.")
y_end = page_list.index("Fennel: tomato, kohlrabi, beans.")

# Checking for beginning and end of the lists:

# print(x_beginning, x_end)
# print(y_beginning, y_end)
# print(page_list[8: 29])
# print(page_list[30: 48])


# #Getting lists of good and bad neighbours


good_neighbours_lst = []
bad_neighbours_lst = []

for i in page_list[8:30]:
  good_neighbours_lst.append(i)
for i in page_list[30: 49]:
  bad_neighbours_lst.append(i)

# Modifing the lists (replace and remove disruptive characters)

veg_list1 = []
veg_list2 = []

for e in good_neighbours_lst:
  f = re.split(": ",e)
  if len(f) == 2:
    veg_list1.append(f)
  else:
    print(f"Skipping item in good_neighbours_lst due to unexpected format: {e}")

veg_list1 = [[item.replace(".", "") for item in lst] for lst in veg_list1]

for p in bad_neighbours_lst:
  q = re.split(": ", p)
  if len(q) == 2:
    veg_list2.append(q)
  else:
    print(f"Skipping item in bad_neighbours_lst due to unexpected format: {p}")

veg_list2 = [[item.replace(".", "") for item in lst] for lst in veg_list2]

# Splitting the lists into two lists with keys and values of the dictionary

good_neighbours_lst_values = []
good_neighbours_lst_keys = []
for i in veg_list1:
  j = re.split(", ", i[1])
  good_neighbours_lst_values.append(j)
for k in veg_list1:
  good_neighbours_lst_keys.append(k[0])


bad_neighbours_lst_values = []
bad_neighbours_lst_keys = []
for i in veg_list2:
  j = re.split(", ", i[1])
  bad_neighbours_lst_values.append(j)
for k in veg_list2:
  bad_neighbours_lst_keys.append(k[0])

#Putting the items of the good and bad_neighbours_lst_keys as keys in a dictionary

good_neighbours_dictionary_keys = dict.fromkeys(good_neighbours_lst_keys, "None")
bad_neighbours_dictionary_keys = dict.fromkeys(bad_neighbours_lst_keys, "None")

#Putting the items of the good and bad_neigbours_lst_values as values to the keys in the dictionary

good_neighbours_dictionary = dict(zip(good_neighbours_dictionary_keys, good_neighbours_lst_values))
bad_neighbours_dictionary = dict(zip(bad_neighbours_dictionary_keys, bad_neighbours_lst_values))

# Capitalize the words in the dictionary

good_neighbours_dictionary = {k:[x.capitalize() for x in v] for k, v in good_neighbours_dictionary.items()}
bad_neighbours_dictionary = {k:[x.capitalize() for x in v] for k, v in bad_neighbours_dictionary.items()}

# print(good_neighbours_dictionary)
# print("sssssssssssss")
# print(bad_neighbours_dictionary)

# Exporting the dictionarys into a json file

import json

json.dump(good_neighbours_dictionary, open("good_neighbours.json", "w"))
json.dump(bad_neighbours_dictionary, open("bad_neighbours.json", "w"))

