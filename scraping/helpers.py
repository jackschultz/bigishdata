import os

def write_html(lib_name, page):
  if not os.path.exists("pages"):
    os.makedirs("pages")
  file_name = "pages/" + lib_name + "_page.html"
  with open(file_name, 'w') as f:
    f.write(page)

def write_data(lib, text_array):
  if not os.path.exists("texts"):
    os.makedirs("texts")
  lib_dir = "texts/" + lib
  if not os.path.exists(lib_dir):
    os.makedirs(lib_dir)
  for key, values in text_array.iteritems():
    filename = lib_dir + '/' + key + '.txt'
    with open(filename, 'w') as f:
      for value in values:
        if value is not None:
          f.write(value.encode('UTF-8') + '\n')
