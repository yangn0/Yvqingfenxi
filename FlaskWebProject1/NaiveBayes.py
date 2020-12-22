import jieba
import re
import random
from numpy import *


def text_parse(filename):
    """对评论集进行预处理"""
    contents = []
    with open(filename, 'r', encoding='utf-8') as f:
        for line in f:  # 读行,对每行进行处理
            line = line.strip()  # 去掉末尾的换行符
            line = re.sub("\d.", "", line)  # 将所有的数字去掉
            text = re.sub('\W*', '', line)  # 将所有的特殊符号去掉，即非字母，非数字
            seg_list = jieba.cut(text, cut_all=False)  # 精确模式分割
            contents.append(list(seg_list))

    return contents


def createVocabList(dataset):
    """创建一个词汇表（即数据源中的所有的词语）"""

    vocbset = set([])  # 创建一个集合 使词汇表中词语不重复
    for document in dataset:  # 读取每一个文档（实质上是每一篇文档就是一个集合）
        vocbset = vocbset | set(document)  # 求两个集合的并集

    return list(vocbset)  # 转换为列表


def setOfWords2Vec(vocablist, inputset):
    '''
    词集模型
    function:形成一个文档向量
    :param vocabSet: 词汇表
    :param inputSet: 一个文档
    :return:文档向量
    '''

    returnVec = [0] * len(vocablist)  # 创建一个其中所含元素都为0的向量
    # 向量的每一元素为1或0 代表是否出现
    for word in inputset:
        if word in vocablist:
            returnVec[vocablist.index(word)] = 1
        else:
            print("{}未在词汇表中".format(word))
    return returnVec


def trainNBO(trainMatrix, trainCategory):
    '''
    训练模型
    :param trainMatmix: 训练集矩阵
    :param trainCategory: 训练集类别
    :return:先验概率，条件概率
    '''
    # 类别概率
    denominator = len(trainMatrix)  # 分母
    numerator = sum(trainCategory)  # 分子
    Pgood = numerator / denominator  # 好评的类别概率
    # 因为是二元分类所以只需要知道一个概率就好

    # 条件概率   使用拉普拉斯平滑进行处理
    number = len(trainMatrix[1])
    # 分子
    p1 = ones(number)
    p2 = ones(number)
    # 分母
    p1denom = 2
    p2denom = 2

    for i in range(len(trainCategory)):
        if trainCategory[i] == 1:  # 如果是好评
            p1 = p1 + trainMatrix[i]
            p1denom = p1denom + sum(trainMatrix[i])
        else:
            p2 = p2 + trainMatrix[i]
            p2denom = p2denom + sum(trainMatrix[i])
    p1vect = log(p1 / p1denom)
    p2vect = log(p2 / p2denom)

    return p1vect, p2vect, Pgood


def ClassifyNB(vec2Classify, p1Vect, p2Vect, pAClass):
    '''

    :param vec2Classify: 文档向量
    :param p1Vect: 条件概率good
    :param p0Vect: 条件概率bad
    :param pAClass: 类别概率
    :return:

    '''
    p1 = sum(vec2Classify * p1Vect) + log(pAClass)
    p0 = sum(vec2Classify * p2Vect) + log(1 - pAClass)
    if p1 > p0:
        return 1
    else:
        return 0


def test():
    doclist = []  # 文档集合
    classlist = []  # 文档集合中每篇文档的类别 ，1代表good 0代表bad
    wordlist = text_parse("positive.txt")  # 读取内容，good
    for item in wordlist:
        doclist.append(item)
        classlist.append(1)
    wordlist = text_parse("negative.txt")  # bad
    for item in wordlist:
        doclist.append(item)
        classlist.append(0)
    vocablist = createVocabList(doclist)  # 调用函数生成一个词汇表

    # 进行交叉验证
    trainSet = list(range(len(doclist)))  # 训练集
    testSet = []  # 测试集
    for i in range(150):  # 选出100个测试集
        randomIndex = int(random.uniform(0, len(trainSet)))  # 随机选择出一个索引
        testSet.append(trainSet[randomIndex])  # 添加入测试集
        del (trainSet[randomIndex])  # 在训练集集中删除
    # print(trainSet)
    # print(len(doclist))
    trainMat = []  # 训练集矩阵
    trainClass = []  # 训练集类别矩阵
    for docIndex in trainSet:  # 遍历训练集
        trainMat.append(setOfWords2Vec(vocablist, doclist[docIndex]))  # 将生成的词集模型添加到训练矩阵中
        trainClass.append(classlist[docIndex])

    p1V, p2V, pT = trainNBO(trainMat, trainClass)  # 训练朴素贝叶斯模型
    # 进行测试
    print(vocablist)  # 词汇表
    print("goodVect:")
    print(list(p1V))
    print("badVect:")
    print(list(p2V))
    print("Prior probability:")
    print(pT)
    print("\n")
    errorcount = 0  # 错误分类计数
    for docIndex in testSet:  # 遍历测试集
        wordVector = setOfWords2Vec(vocablist, doclist[docIndex])  # 测试集的词集模型
        if ClassifyNB(wordVector, p1V, p2V, pT) != classlist[docIndex]:
            errorcount = errorcount + 1
    return errorcount / len(testSet)


if __name__ == '__main__':
    for i in range(20):  # 进行20次测试，计算平均错误率
        print(test())
