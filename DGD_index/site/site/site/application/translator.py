from urllib import request, parse
import json


def translator(text):
    req_url = 'http://fanyi.youdao.com/translate?smartresult=dict&smartresult=rule'  # 创建连接接口

    Form_Date = {}
    Form_Date['i'] = text
    Form_Date['doctype'] = 'json'
    Form_Date['form'] = 'AUTO'
    Form_Date['to'] = 'AUTO'
    Form_Date['smartresult'] = 'dict'
    Form_Date['client'] = 'fanyideskweb'
    Form_Date['salt'] = '1526995097962'
    Form_Date['sign'] = '8e4c4765b52229e1f3ad2e633af89c76'
    Form_Date['version'] = '2.1'
    Form_Date['keyform'] = 'fanyi.web'
    Form_Date['action'] = 'FY_BY_REALTIME'
    Form_Date['typoResult'] = 'false'
    data = parse.urlencode(Form_Date).encode('utf-8')
    response = request.urlopen(req_url, data)
    html = response.read().decode('utf-8')
    translate_results = json.loads(html)
    translate_results = translate_results['translateResult'][0][0]['tgt']
    return translate_results


if __name__ == '__main__':
    text = 'person'
    print(translator(text))
