#encoding=utf-8

def replaceTextByDict(text, strDict):
    """根据strDict提供的字符串字典替换text文本，
    strDict={ "text_old1":"text_new1", "text_old2":"text_new2"}"""
    result = ""
    if (text != None) and (strDict != None):
        for key in strDict:
            result = text.replace(key, strDict[key])
            text = result
    return result
