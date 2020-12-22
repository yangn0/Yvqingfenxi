from numpy import *
import json
import jieba
import re


def setOfWords2Vec(vocablist, inputset):
    '''
    词集模型
    function:形成一个文档向量
    :param vocabSet: 词汇表
    :param inputSet: 一个文档
    :return:文档向量
    '''

    returnVec = [0] * len(vocablist)
    for word in inputset:
        if word in vocablist:
            returnVec[vocablist.index(word)] = 1
    return returnVec


def ClassifyNB(vec2Classify, p1Vect, p2Vect, pAClass):
    '''

    :param vec2Classify: 文档向量
    :param p1Vect: 条件概率
    :param p0Vect: 条件概率
    :param pAClass: 类别概率
    :return:

    '''
    p1 = sum(vec2Classify * p1Vect) + log(pAClass)
    p0 = sum(vec2Classify * p2Vect) + log(1 - pAClass)
    # print(p1)
    # print(p0)
    if p1 > p0:
        return 1, p1, p0
    else:
        return 0, p1, p0


def main(text):
    # 读取条件概率p1
    with open('trainresult\p1', 'r', encoding='utf-8') as f:
        text1 = f.read()  # 读取文件内容
        p1 = json.loads(text1)  # 转换为JSON对象，最终类型为list
        p1 = array(p1)  # 转换为numpy数组

    # 读取条件概率p2
    with open('trainresult\p2', 'r', encoding='utf-8') as f:
        text2 = f.read()  # 读取文件内容
        p2 = json.loads(text2)  # 转换为JSON对象，最终类型为list
        p2 = array(p2)  # 转换为numpy数组

    # 类别概率
    pT = 0.5056734089787864

    # 读取词汇表
    with open('trainresult/vocablist', 'r', encoding='utf-8') as f:
        text3 = f.read()
        text3 = text3.replace("'", '"')  # JSONS数据需要用双引号来包围，不能使用单引号，所以这里使用替换
        vocablist = json.loads(text3)
    # 对读入的文本进行操作
    text = re.sub("\d.", "", text)  # 将所有的数字去掉
    text = re.sub('\W*', '', text)  # 将所有的特殊符号去掉，即非字母，非数字
    # print(text)
    test_test = jieba.cut(text, cut_all=False)  # 精确模式分割
    a = list(test_test)
    # print(a)
    wordVector = setOfWords2Vec(vocablist, a)
    # print(ClassifyNB(wordVector, p1, p2, pT))
    return ClassifyNB(wordVector, p1, p2, pT)


if __name__ == '__main__':
    number, p1, p0=main('我爱你中国，亲爱的母亲')
    if number==1:
        print("good")
    else:
        print("bad")
