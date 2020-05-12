import time
import pandas
from pyecharts import options as opts
from pyecharts.charts import Pie
from pyecharts.charts import Bar
from pyecharts.charts import Line


def district_analysis(name, number):
    a = (
        Pie()
            .add(
            "",
            [list(z) for z in zip(name, number)],
            center=["35%", "50%"],
        )
            .set_global_opts(
            title_opts=opts.TitleOpts(title="区域招聘比例"),
            legend_opts=opts.LegendOpts(pos_left="15%"),
        )
            .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))
    )
    a.render('1.html')


def educational_analysis(name, number):
    b = (
        Bar()
            .add_xaxis(name)
            .add_yaxis('', number)
            .set_global_opts(title_opts=opts.TitleOpts(title="各学历招聘数量"))
    )
    b.render('2.html')


def month_analysis(name, number):
    c = (
        Line()
            .add_xaxis(name)
            .add_yaxis(None, number)
            .set_global_opts(
            title_opts=opts.TitleOpts(title="招聘需求走势")
        )
    )
    c.render('3.html')


def educational_mode_mean(name, mean, mode):
    d = (
        Bar()
            .add_xaxis(name)
            .add_yaxis("平均薪资", mean)
            .add_yaxis("普遍薪资", mode)
            .set_global_opts(
            title_opts=opts.TitleOpts(title="各学历的平均工资和普遍薪资"),
            yaxis_opts=opts.AxisOpts(
                axislabel_opts=opts.LabelOpts(formatter="每月/{value}k")
            ),
        )
    )
    d.render('4.html')


def educational_mean_Mode(educational, data):
    mode_list = list(map(lambda x: int(data[data['要求学历'] == x]['真实薪资'].mode()[0]), educational))
    mean_list = list(map(lambda x: int(data[data['要求学历'] == x]['真实薪资'].mean()), educational))
    return mode_list, mean_list


def main():
    file_name = 'BOSS直聘深圳招聘信息{}.xlsx'.format(time.strftime('%Y-%m-%d', time.localtime(time.time())))
    data = pandas.read_excel(file_name, sheet_name='Sheet1')
    # district = ['福田', '罗湖', '盐田', '坪山', '龙岗', '龙华', '光明', '宝安', '南山']
    # district_number = list(map(lambda x: list(data['区域']).count(x), district))
    # district_analysis(district, district_number)
    # educational = ['学历不限', '初中及以下', '高中', '中专/中技', '大专', '本科', '硕士', '博士']
    # educational_number = list(map(lambda x: list(data['要求学历']).count(x), educational))
    # educational_analysis(educational, educational_number)
    month = ['2019年4月', '2019年5月', '2019年6月', '2019年7月', '2019年8月', '2019年9月', '2019年10月', '2019年11月', '2019年12月',
             '2020年1月', '2020年2月', '2020年3月']
    month_nnumber = list(map(lambda x: list(data['具体时间']).count(x), month))
    month_analysis(month, month_nnumber)
    # result = educational_mean_Mode(educational, data)
    # educational_mode_mean(educational, result[1], result[0])


if __name__ == '__main__':
    main()
