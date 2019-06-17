def Index_Data_FromCSV(self,csvfile):
    '''
    从CSV文件中读取数据，并存储到es中
    :param csvfile: csv文件，包括完整路径
    :return:
    '''
    # list = csv.ReadCSV(csvfile)
    list = csv.reader(csvfile)
    index = 0
    doc = {}
    for item in list:
        if index > 1:  # 第一行是标题
            doc['title'] = item[0]
            doc['contents'] = item[1]
            doc['date'] = item[2]
            doc['time'] = item[3]
            doc['source'] = item[4]
            doc['path'] = item[5]
            res = self.es.index(index=self.index_name,doc_type=self.index_type,body=doc)
            print(res['result'])
        index += 1
        print(index)


def IndexData(self):
    es = Elasticsearch()
    csvdir = 'newstxt'
    filenamelist = []
    for (dirpath,dirnames,filenames) in walk(csvdir):
        filenamelist.extend(filenames)
        break
    total = 0
    for file in filenamelist:
        csvfile = csvdir + '/' + file
        self.Index_Data_FromCSV(csvfile,es)
        total += 1
        print(total)
        time.sleep(10)