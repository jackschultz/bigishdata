import json
import linecache
import random

NUM_TRAIN_SAMPLES = 800# * 16
NUM_TEST_SAMPLES = 200# * 16
NUM_TOTAL_SAMPLES = NUM_TRAIN_SAMPLES + NUM_TEST_SAMPLES

baby_count = 160792
baby_filename = "reviews_Baby_5.json"
tool_count = 134476
tool_filename = "reviews_Tools_and_Home_Improvement_5.json"
food_count = 151254
food_filename = "reviews_Grocery_and_Gourmet_Food_5.json"
pet_count = 157836
pet_filename = "reviews_Pet_Supplies_5.json"
home_count = 551682
home_filename = "data/reviews_Home_and_Kitchen_5.json"

infos = []
#infos.append({"keyword": "baby", "count": baby_count, "filename": baby_filename})
#infos.append({"keyword": "tool", "count": tool_count, "filename": tool_filename})
#infos.append({"keyword": "food", "count": food_count, "filename": food_filename})
#infos.append({"keyword": "pet", "count": pet_count, "filename": pet_filename})
infos.append({"keyword": "home", "count": home_count, "filename": home_filename})

for info in infos:
  filename = info["filename"]
  count = info["count"]
  keyword = info["keyword"]
  train_filename = "train_%s.json" % keyword
  test_filename = "test_%s.json" % keyword

  all_lines = random.sample(range(1,count), NUM_TOTAL_SAMPLES)
  train_lines = all_lines[0:NUM_TRAIN_SAMPLES]
  test_lines = all_lines[NUM_TRAIN_SAMPLES:]

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

