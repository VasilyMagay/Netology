import chardet

def get_dict_from_news_file(filename, cp='', min_word_len = 6):
    
    dict = {}
    text = ""
    
    with open(filename, 'rb') as f:
        data = f.read()
        result = chardet.detect(data)
        text = data.decode(result['encoding'])
        
    if len(text) > 0:    
        line = text.strip()
        line_list = line.split(' ')
        for word in line_list:
            if len(word) >= min_word_len:
                word = word.lower()
                dict[word] = dict.get(word, 0) + 1
     
    return dict
    
def print_top(dict, top_num=10):
    sorted_list = sorted(dict.items(), key=lambda x: x[1], reverse=True)
    for i in range(top_num):
        print(sorted_list[i])
    
def process_file(filename):
    print('News file: {}'.format(filename))
    dict = get_dict_from_news_file(filename)    
    print_top(dict)    
    
files = ['newsafr.txt', 'newscy.txt', 'newsfr.txt', 'newsit.txt']

for fname in files:
    process_file(fname)

