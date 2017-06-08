import json
import linecache
import random

NUM_TOTAL_SAMPLES = 10000
NUM_TRAIN_SAMPLES = 8000
NUM_TEST_SAMPLES = 2000

apps_count = 752937
apps_filename = "reviews_Apps_for_Android_5.json"

automotive_count = 20473
automotive_filename = "reviews_Automotive_5.json"

baby_count = 160792
baby_filename = "reviews_Baby_5.json"

books_count = 8898041
books_filename = "reviews_Books_5.json"

cell_phones_count = 194439
cell_phones_filename = "reviews_Cell_Phones_and_Accessories_5.json"

tool_count = 134476
tool_filename = "reviews_Tools_and_Home_Improvement_5.json"

food_count = 151254
food_filename = "reviews_Grocery_and_Gourmet_Food_5.json"

pet_count = 157836
pet_filename = "reviews_Pet_Supplies_5.json"

home_count = 551682
home_filename = "reviews_Home_and_Kitchen_5.json"

automotive_count = 20473
automotive = "reviews_Automotive_5.json"

instant_video_count = 37126
instant_video_filename = "reviews_Amazon_Instant_Video_5.json"

beauty_count = 198502
beauty_filename = "reviews_Beauty_5.json"

cds_vinyl_count = 1097592
cds_vinyl_filename = "reviews_CDs_and_Vinyl_5.json"

health_count = 346355
health_filename = "reviews_Health_and_Personal_Care_5.json"

clothes_count = 278677
clothes_filename = "reviews_Clothing_Shoes_and_Jewelry_5.json"

digital_music_count = 64706
digital_music_filename = "reviews_Digital_Music_5.json"

electronics_count = 1689188
electronics_filename = "reviews_Electronics_5.json"

kindle_count = 982619
kindle_filename = "reviews_Kindle_Store_5.json"

movies_tv_count = 1697533
movies_tv_filename = "reviews_Movies_and_TV_5.json"

instruments_count = 10261
instruments_filename = "reviews_Musical_Instruments_5.json"

office_count = 53258
office_filename = "reviews_Office_Products_5.json"

patio_count = 13272
patio_filename = "reviews_Patio_Lawn_and_Garden_5.json"

sports_count = 296337
sports_filename = "reviews_Sports_and_Outdoors_5.json"

toys_count = 167597
toys_filename = "reviews_Toys_and_Games_5.json"

video_games_count = 231780
video_games_filename = "reviews_Video_Games_5.json"

infos = []
infos.append({"class_name": "apps", "count": apps_count, "filename": apps_filename})
'''
infos.append({"class_name": "baby", "count": baby_count, "filename": baby_filename})
infos.append({"class_name": "tool", "count": tool_count, "filename": tool_filename})
infos.append({"class_name": "food", "count": food_count, "filename": food_filename})
infos.append({"class_name": "pet", "count": pet_count, "filename": pet_filename})
infos.append({"class_name": "home", "count": home_count, "filename": home_filename})
infos.append({"class_name": "automotive", "count": automotive_count, "filename": automotive_filename})
infos.append({"class_name": "instant_video", "count": instant_video_count, "filename": instant_video_filename})
infos.append({"class_name": "beauty", "count": beauty_count, "filename": beauty_filename})
infos.append({"class_name": "cds_vinyl", "count": cds_vinyl_count, "filename": cds_vinyl_filename})
infos.append({"class_name": "clothes", "count": clothes_count, "filename": clothes_filename})
infos.append({"class_name": "digital_music", "count": digital_music_count, "filename": digital_music_filename})
infos.append({"class_name": "cell_phones", "count": cell_phones_count, "filename": cell_phones_filename})
infos.append({"class_name": "electronics", "count": electronics_count, "filename": electronics_filename})
infos.append({"class_name": "kindle", "count": kindle_count, "filename": kindle_filename})
infos.append({"class_name": "movies_tv", "count": movies_tv_count, "filename": movies_tv_filename})
infos.append({"class_name": "instruments", "count": instruments_count, "filename": instruments_filename})
infos.append({"class_name": "office", "count": office_count, "filename": office_filename})
infos.append({"class_name": "patio", "count": patio_count, "filename": patio_filename})
infos.append({"class_name": "health", "count": health_count, "filename": health_filename})
infos.append({"class_name": "sports", "count": sports_count, "filename": sports_filename})
infos.append({"class_name": "toys", "count": toys_count, "filename": toys_filename})
infos.append({"class_name": "video_games", "count": video_games_count, "filename": video_games_filename})
infos.append({"class_name": "books", "count": books_count, "filename": books_filename})
'''

for info in infos:
  filename = "data/%s" % info["filename"]
  count = info["count"]
  class_name = info["class_name"]
  train_filename = "train_%s.json" % class_name
  test_filename = "test_%s.json" % class_name

  print class_name

  all_lines = random.sample(range(1,count), NUM_TOTAL_SAMPLES)
  train_lines = set(all_lines[0:NUM_TRAIN_SAMPLES])
  test_lines = set(all_lines[NUM_TRAIN_SAMPLES:])

  train_reviews = [eval(linecache.getline(filename, i)) for i in train_lines]
  test_reviews = [eval(linecache.getline(filename, i)) for i in test_lines]

  with open(train_filename, 'w') as f:
    for review in train_reviews:
      f.write(json.dumps(review))
      f.write('\n')

  with open(test_filename, 'w') as f:
    for review in test_reviews:
      f.write(json.dumps(review))
      f.write('\n')

