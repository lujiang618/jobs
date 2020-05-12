import time
import pandas
import re
import requests


def txt_Transformation_xlsx(file_name):
    result = []
    with open('BOSS_result{}.txt'.format(time.strftime('%Y-%m-%d', time.localtime(time.time()))), 'r',
              encoding='utf-8')as R:
        for i in R.readlines():
            if not eval(i)['公司名称'] or not eval(i)['薪资待遇'] or not eval(i)['公司地址']:
                continue
            result.append(eval(i))
    boss_result = pandas.DataFrame(result, columns=['公司名称', '职位名称', '详情链接', '公司地址', '薪资待遇', '要求学历', '发布时间'])
    boss_result.to_excel(file_name, index=0)


def analysis_price(data):
    analysis_result = []
    for i in data['薪资待遇']:
        if '天' in i:
            result = int(int(re.findall('\d+', i)[0]) * 30 / 1000)
            analysis_result.append(result)
            # print(result)
        else:
            result = re.findall('\d+', i)[0]
            analysis_result.append(result)
            # print(result)
    data['真实薪资'] = analysis_result


def analysis_adress(data):
    analysis_result = []
    sz_fq = ['福田', '罗湖', '盐田', '坪山', '龙岗', '龙华', '光明', '宝安', '南山']
    for i in data['公司地址']:
        for j in sz_fq:
            if j in i:
                result = j
                analysis_result.append(result)
                # print(i, result)
                break
            if j == '南山':
                try:
                    headers = {
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36',
                        'Referer': 'https://map.baidu.com/@12697919.69,2560977.31,12z',
                        'Cookie': 'BAIDUID=A1AB38E2ADD5D325CD902A5FA58964BA:FG=1; BIDUPSID=A1AB38E2ADD5D325CD902A5FA58964BA; PSTM=1570874236; BDUSS=UtzQkpqazRWTHlwfm1TYVpnYnJyT2ctYjJUVTRRcnBXQXlua1pNZlplUDNtY3RkSVFBQUFBJCQAAAAAAAAAAAEAAAAq3nExwOu~qrGvyctMAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAPcMpF33DKRdV; routeiconclicked=1; routetype=bus; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; H_PS_PSSID=30975_1437_31117_21127_30901_31051_30823_31085_26350; delPer=0; PSINO=7; __yjsv5_shitong=1.0_7_120b89e88a1a5c577656f245ec9d04e9462a_300_1584754654230_116.25.99.78_6d9a1cd1; yjs_js_security_passport=7570d70c349e424572647f797b06928e0d2d6167_1584754655_js; MCITY=-%3A; session_id=1584755736124; session_name=www.baidu.com; M_LG_UID=829546026; M_LG_SALT=cacf07c60714d50236257d47798a4f3f; validate=22826'
                    }
                    url = 'https://map.baidu.com/su?'
                    params = {
                        'wd': i,
                        'cid': 340,
                        'type': 0,
                        'newmap': 1,
                        'b': '(12685734.394103905,2559898.9028746583;12686187.058999216,2560368.3101702076)',
                        't': int(time.time() * 1000),
                        'pc_ver': 2
                    }
                    response = requests.get(url, params=params, headers=headers)
                    # print(response.content.decode('utf-8'))
                    result = re.findall('深圳市\$(.*?)\$\$', response.content.decode('utf-8'))[0].replace('区', '')
                    analysis_result.append(result)
                    # print(i, result)
                except:
                    analysis_result.append('其他')
                    # print(i, '其他')
    data['区域'] = analysis_result


def analysis_time(data):
    analysis_result = []
    for i in data['发布时间']:
        try:
            create_time = re.findall('\d+月', i)[0]
            if create_time[0] == "0":
                create_time = create_time[1:]
        except:
            create_time = '3月'
        if int(re.findall('\d+', create_time)[0]) > 3:
            create_time = '2019年' + create_time
        else:
            create_time = '2020年' + create_time
        # print(create_time)
        analysis_result.append(create_time)
    data['具体时间'] = analysis_result


def main():
    file_name = 'BOSS直聘深圳招聘信息{}.xlsx'.format(time.strftime('%Y-%m-%d', time.localtime(time.time())))
    txt_Transformation_xlsx(file_name)
    print('清洗空值并保存成xlsx'.center(40, '='))
    data = pandas.read_excel(file_name, sheet_name='Sheet1')
    print('对薪资待遇进行分类'.center(40, '='))
    analysis_price(data)
    print('对发布时间进行分类'.center(40, '='))
    analysis_time(data)
    print('对公司地址进行分类'.center(40, '='))
    analysis_adress(data)
    data.to_excel(file_name, index=False)


if __name__ == '__main__':
    main()
