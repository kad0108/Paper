#coding=utf-8
import word2vec
import numpy    
import codecs
from sklearn.cluster import KMeans

import os

'''
 dataId: dataset index, current 5, 7, 9
 usingExist: whether use exist  bin file, default True
'''

def solve(dataId, usingExist = True):

    dataId = str(dataId)
    dataPath = './data/'+ dataId +'.txt'
    binPath = './out/' + dataId + '.bin'
    outputPath = "out/ans"+ dataId +".txt"
    
    if not os.path.exists(binPath) or not usingExist:
        word2vec.word2vec(dataPath, binPath, size=100, verbose=True)

    # 使用word2vec载入binPath
    model = word2vec.load(binPath)

    # 打开输出文件
    output = codecs.open(outputPath, "w", "utf-8")

    ClustersNumber = 10
    WordNumber = len(model.vectors)


    # 使用Kmeans算法
    kmeans = KMeans(n_clusters=ClustersNumber, random_state=0).fit(model.vectors)

    # 得到每个word ID 所属于的cluster 编号，编号范围[0, WordNumber)
    label = kmeans.labels_
    # 获取每个word 的得分，即是每个word和cluster中心的距离的相反数
    scores = []
    for i in xrange(WordNumber):
        scores.append(kmeans.score([model.vectors[i]]) )


    # 把处于相同cluster的word ID 放入相同的list
    allCluster = []
    for i in xrange(ClustersNumber):
        allCluster.append([])
    for i in xrange(len(label)):
        allCluster[label[i]].append(i)


    

    # 定义两个word ID的大小关系，使用scores数组比较其大小关系
    def comparator(a, b):

        vala = scores[a]
        valb = scores[b]

        if vala > valb: return 1
        elif vala == valb : return 0
        else : return -1

    #对于每个cluster分别处理
    for clusterId in xrange(len(allCluster)):
        output.write("-----------------------------------cluster " + str(clusterId) + ":\n")        
        
        #排序，按照score从高到低排序
        allCluster[clusterId].sort(cmp = comparator, reverse = True)

        #获取前30个
        for x in allCluster[clusterId][:30]:
            #输出score的相反数，即输出距离
            output.write(model.vocab[x] + "  " + str(-scores[x])  + "\n")
    print '\n'


# solve(5, False)
# solve(7, False)
# solve(9, False)

solve(5)
solve(7)
solve(9)









# word2vec.word2clusters('text8/text8', 'text8/text8-clusters.txt', 100, verbose=True)


# model = word2vec.load('out/5.bin')


# model = word2vec.load('text8/text8.bin')
# print (model.vectors)

# print model.vectors.shape

# clusters = word2vec.load_clusters('out/5-clusters.txt')
# clusters = word2vec.load_clusters('text8/text8-clusters.txt')


# clusters[u'互联网']




# for x in model.vocab:
#     print x