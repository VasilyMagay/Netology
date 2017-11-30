import chardet


def get_dict_from_news_file(filename, min_word_len=6):
    
    my_dict = {}

    with open(filename, 'rb') as f:
        data = f.read()
        result = chardet.detect(data)
        text_data = data.decode(result['encoding'])
        
    if text_data:
        line = text_data.strip()
        line_list = line.split(' ')
        for word in line_list:
            if len(word) >= min_word_len:
                word = word.lower()
                my_dict[word] = my_dict.get(word, 0) + 1
     
    return my_dict


def print_top(my_dict, top_num=10):
    sorted_list = sorted(my_dict.items(), key=lambda x: x[1], reverse=True)
    for i in range(top_num):
        print(sorted_list[i])


def process_file(filename):
    print('News file: {}'.format(filename))
    my_dict = get_dict_from_news_file(filename)
    print_top(my_dict)


files = ['newsafr.txt', 'newscy.txt', 'newsfr.txt', 'newsit.txt']

for fname in files:
    process_file(fname)

