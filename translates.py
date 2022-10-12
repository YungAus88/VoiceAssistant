import re #正則運算函式 (Regular Expression)

def trans(word): # 重複搜尋
    text = word
    dic = {
        "做得很好，你呢？":"我很好，你呢？",
        "主席先生":"先生"
    }
    for key in dic.keys(): # 讀取字典內的字
        text = re.sub(key, dic[key], text)
    return text # 傳回修改後的

def trans_e(word): # 重複搜尋
    text = word
    dic = {
        'Mathematics':'math',

    }
    for key in dic.keys(): # 讀取字典內的字
        text = re.sub(key, dic[key], text)
    return text # 傳回修改後的

def  googletrans(word):
    text = word
    dic = {
        "Chinese ":"zh-TW",
        "Japanese":"ja",
        "Korean":"ko",
        "English ":"en",
    }
    for key in dic.keys(): # 讀取字典內的字
        text = re.sub(key, dic[key], text)
    return text # 傳回修改後的

def  translate(word):
    text = word
    dic = {
        "chinese":"chinese (traditional)",
    }
    for key in dic.keys(): # 讀取字典內的字
        text = re.sub(key, dic[key], text)
    return text # 傳回修改後的

