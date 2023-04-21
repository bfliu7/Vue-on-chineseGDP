# -*- coding:utf-8 -*-
import ast
import random
import readbases
import json
import time
import threading
from flask_cors import CORS
from flask_failsafe import failsafe
from flask import Flask, render_template, request, make_response, jsonify
from redis import Redis

lock = threading.Lock()
lock_right_center = threading.Lock()

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
app.config['REDIS_HOST'] = '127.0.0.1'
app.config['REDIS_PORT'] = 6379
CORS(app, supports_credentials=True)  # 跨域问题

redis = Redis(host=app.config['REDIS_HOST'], port=app.config['REDIS_PORT'])

# 基础数据
year_kuadu = 9
year = 1952
res = [('1952', '安徽省', '22.88', '17.18', '2.27', '3.43', '75.0874', '9.9213', '14.9913', '78'),
       ('1952', '北京市', '7.88', '1.75', '3.05', '3.08', '22.2081', '38.7056', '39.0863', '170'),
       ('1952', '福建省', '12.73', '8.39', '2.42', '1.92', '65.9073', '19.0102', '15.0825', '102'),
       ('1952', '甘肃省', '13.32', '8.66', '1.73', '2.93', '65.015', '12.988', '21.997', '125'),
       ('1952', '广东省', '29.52', '14.39', '6.7', '8.43', '48.7466', '22.6965', '28.5569', '101.41'),
       ('1952', '广西壮族自治区', '12.81', '8.34', '2.95', '1.52', '65.1054', '23.0289', '11.8657', '66.57'),
       ('1952', '贵州省', '8.55', '5.85', '1.59', '1.11', '68.4211', '18.5965', '12.9825', '58'),
       ('1952', '河北省', '40.49', '25.23', '7.61', '7.65', '62.3117', '18.7948', '18.8936', '125'),
       ('1952', '河南省', '36.09', '22.46', '8.23', '5.4', '62.2333', '22.8041', '14.9626', '82.8'),
       ('1952', '黑龙江省', '26', '11.92', '7.84', '6.24', '45.8462', '30.1538', '24', '238'),
       ('1952', '湖北省', '24.51', '13.9', '3.83', '6.78', '56.7115', '15.6263', '27.6622', '90'),
       ('1952', '湖南省', '27.81', '18.72', '3.43', '5.66', '67.3139', '12.3337', '20.3524', '86'),
       ('1952', '吉林省', '16.55', '9.19', '4.54', '2.82', '55.5287', '27.432', '17.0393', '153'),
       ('1952', '江苏省', '48.41', '25.49', '8.53', '14.39', '52.6544', '17.6203', '29.7253', '131'),
       ('1952', '江西省', '18.86', '12.38', '2.47', '4.01', '65.6416', '13.0965', '21.2619', '114'),
       ('1952', '辽宁省', '41.38', '12', '20', '9.38', '28.9995', '48.3325', '22.668', '218'),
       ('1952', '内蒙古自治区', '12.16', '8.64', '1.37', '2.15', '71.0526', '11.2664', '17.6809', '173'),
       ('1952', '宁夏回族自治区', '1.73', '1.43', '0.08', '0.22', '82.659', '4.6243', '12.7168', '126'),
       ('1952', '青海省', '1.63', '1.2', '0.12', '0.31', '73.6196', '7.362', '19.0184', '101'),
       ('1952', '山东省', '43.41', '28.55', '7.87', '6.99', '65.7683', '18.1295', '16.1023', '91'),
       ('1952', '山西省', '16', '9.4', '2.7', '3.9', '58.75', '16.875', '24.375', '116'),
       ('1952', '陕西省', '12.85', '8.4', '1.92', '2.53', '65.3696', '14.9416', '19.6887', '85'),
       ('1952', '上海市', '36.66', '2.17', '19.22', '15.27', '5.9193', '52.4277', '41.653', ''),
       ('1952', '四川省', '31.69', '21.18', '4.55', '5.96', '66.835', '14.3578', '18.8072', '69'),
       ('1952', '天津市', '12.8', '1.85', '6.31', '4.64', '14.4531', '49.2969', '36.25', '299'),
       ('1952', '新疆维吾尔自治区', '7.91', '5.12', '1.74', '1.05', '64.7282', '21.9975', '13.2743', '166'),
       ('1952', '云南省', '11.78', '7.27', '1.82', '2.69', '61.7148', '15.4499', '22.8353', '70'),
       ('1952', '浙江省', '24.53', '16.28', '2.78', '5.47', '66.3677', '11.3331', '22.2992', '12'),
       ('1952', '中国', '679.1', '342.9', '141.1', '195.1', '50.5', '20.8', '28.7', '119')]

right_top_color = ['#fafafa', '#f9f6f6', '#f8f2f2', '#f7eeee', '#f6e9e9', '#f5e5e5', '#f4e1e1', '#f3dddd', '#f3d5d5',
                   '#f3cccc', '#f3c4c4', '#f3bbbb', '#f3b3b3', '#f3aaaa', '#f4a2a2', '#f49999', '#f49191', '#f48888',
                   '#f48080', '#f47777', '#f46f6f', '#f46666', '#f45e5e', '#f45555', '#f44d4d', '#f44444', '#f43c3c',
                   '#f53333', '#f52b2b', '#f52222', '#f51a1a', '#f51111', '#f50909', '#f50000']

# 各节点
left_top__=0
left_center__=0
left_bottom__=0
center_map__=0
right_top__=0
right_top_big__=0
right_center__=0
right_center_big__=0
right_bottom__=0


# 查询用于左中，左下，中间地图
def read():
    try:
        global year
        if year > 2020:
            year = 2020
        global res
        lock.acquire()
        res = readbases.readbase(
            f"SELECT 年份,省级,`地区生产总值/亿元`,`地区生产总值-第一产业/亿元`,`地区生产总值-第二产业/亿元`,`地区生产总值-第三产业/亿元`,`地区生产总值指数(上年=100)` FROM sheet1 WHERE 年份={str(year)}")
        lock.release()
    except:
        print('error happened in read()')


# 年份,省级,`地区生产总值/亿元`,`地区生产总值-第一产业/亿元`,`地区生产总值-第二产业/亿元`,`地区生产总值-第三产业/亿元`,,`第一产业占GDP的比重(%)`,`第二产业占GDP的比重(%)`,`第三产业占GDP的比重(%)`,
# 10 `人均地区生产总值/元`,`地区生产总值指数(上年=100)`,`地区生产总值指数-第一产业(上年=100)`,`地区生产总值指数-第二产业(上年=100)`,`地区生产总值指数-第三产业(上年=100)`


# # 修改为前端负责年份轮询,后端不需要多线程
# # # #轻量级多线程
# sched = BackgroundScheduler(daemon=True, timezone='Asia/Shanghai')  # 指定时区
# job=sched.add_job(func=read, trigger="interval", seconds=2,id='my_job')  #  间隔5s后启动
# # sched.add_job(func=update_date_time, trigger="cron", day="*", hour="11", minute="00")  # 定时启动
# sched.start()
# # sched.pause_job(job.id)
# # sched.resume_job(job.id)


# 左上
# 此处处理前端返回的year
@app.route('/left_top_search', methods=['POST'])
def left_top_search_():
    if request.method == 'POST':
        global year
        global left_top__
        if int(request.json.get('chaxun')):
            ress = request.json.get('want')
            year = int(ress)
            read()
            # sched.pause_job('my_job')
            left_top__=1
            return {'success': True}
        else:
            ress = request.json.get('want')
            year = int(ress)
            read()
            time.sleep(0.5)
            # sched.resume_job('my_job')
            left_top__=1
            return {'success': True}


# 左中
@app.route('/left_center', methods=['GET'])
def left_center_():
    data = {}
    global left_center__
    global res
    for line in res:
        if line[1] == '中国':
            data = {'lockNum': "{:.2f}".format(float(line[3])), 'onlineNum': "{:.2f}".format(float(line[4])),
                    'offlineNum': "{:.2f}".format(float(line[5])), 'totalNum': "{:.2f}".format(float(line[2]))}
    left_center__=1
    return data


# 左下
@app.route('/left_bottom', methods=['GET'])
def left_bottom_():
    data = []
    global left_bottom__
    for line in res:
        if line[1] == '中国':
            continue
        data.append({'name': line[1], 'value': float(line[2]), 'first': line[3], 'second': line[4], 'third': line[5]})
    data.sort(key=lambda x: x['value'])
    data.reverse()
    need = [[], [], [], []]
    i = 7
    while i > -1:
        need[0].append(data[i]['name'])
        need[1].append(data[i]['first'])
        need[2].append(data[i]['second'])
        need[3].append(data[i]['third'])
        i -= 1
    left_bottom__=1
    return {'list':need}


# 中间地图
def center_map(res):
    data = []
    for line in res:
        if line[1] == '中国':
            continue
        data.append({'name': line[1], 'value': line[2]})
    return data


@app.route('/center_map', methods=['GET'])
def center_map_():
    global center_map__
    global res
    data = center_map(res)
    center_map__=1
    return {'list':data}


# 右上
@app.route('/right_top', methods=['GET'])
def right_top_():
    global right_top_color
    global right_top__
    global res
    data = []
    for line in res:
        if line[1] == '中国':
            continue
        if line[6] == None:
            continue
        data.append({'name': line[1], 'value': float(line[6])})
    data_raw = []
    for i in data:
        data_raw.append(i)
    data.sort(key=lambda x: x['value'])
    for i, x in enumerate(data):
        x['color'] = right_top_color[i]
    # print(data_raw)
    # print(data)
    data_final = []
    for i in data_raw:
        color = ''
        for j in data:
            if i['name'] == j['name']:
                color = j['color']
        data_final.append({
            'value': [i['name'], round(float(i['value']) - 100, 2)],
            'itemStyle': {
                'color': color
            }
        })
    right_top__=1
    return {'list':data_final}


# 右上弹框3D
@app.route('/right_top_big', methods=['POST', 'GET'])
def right_top_big():
    global year
    global year_kuadu
    global right_top_big__
    if year_kuadu<20:
        year_kuadu1 = 20
    else:
        year_kuadu1=year_kuadu

    num = year_kuadu1 / 2
    left = year - num if year - num > 1951 else 1952
    right = left + year_kuadu1
    if right >= 2020:
        right = 2020
        left = right - year_kuadu1
    lock.acquire()
    ress = readbases.readbase(
        f"SELECT 省级,年份,`地区生产总值/亿元`,`地区生产总值-第一产业/亿元`,`地区生产总值-第二产业/亿元`,`地区生产总值-第三产业/亿元`,`人均地区生产总值/元`,`地区生产总值指数(上年=100)` FROM sheet1 WHERE 年份>={str(left)} and 年份<={str(right)} and 省级!='中国'")
    lock.release()
    data_final_ = []
    data_final_.append(["Province","Year","GDP","GDP_one","GDP_two","GDP_three","Average","Rate"])
    for i in ress:
        if i[7]==None:
            num = 0
        else:
            num=round(float(i[7])-100,2)



        data_final_.append([
            i[0],int(i[1]),float(i[2]),float(i[3]),float(i[4]),float(i[5]),float(i[6]),float(num)
        ])
    right_top_big__=1
    return {'list':data_final_}


# 右中，加上缓存
def right_center(year_kuadu):
    global year
    dataList = []
    numList = []
    numList2 = []
    numList3 = []
    numList4 = []
    flag = False  # 预测缓存里边没有
    my_id = str(year) + str(year_kuadu)  # 195257
    list_key = f"cart:{my_id}"
    lock_right_center.acquire()
    # 检索缓存
    if redis.lrange(list_key, 0, -1) != []:
        dataList = ast.literal_eval(redis.lrange(list_key, 0, -1)[0].decode())
        numList = ast.literal_eval(redis.lrange(list_key, 0, -1)[1].decode())
        numList2 = ast.literal_eval(redis.lrange(list_key, 0, -1)[2].decode())
        numList3 = ast.literal_eval(redis.lrange(list_key, 0, -1)[3].decode())
        numList4 = ast.literal_eval(redis.lrange(list_key, 0, -1)[4].decode())
        flag = True
    lock_right_center.release()
    # 没有，检索数据库
    if flag == False:
        num = year_kuadu / 2
        left = year - num if year - num > 1951 else 1952
        right = left + year_kuadu
        if right >= 2020:
            right = 2020
            left = right - year_kuadu

        lock.acquire()
        ress = readbases.readbase(
            f"SELECT 年份,`地区生产总值指数(上年=100)`,`地区生产总值指数-第一产业(上年=100)`,`地区生产总值指数-第二产业(上年=100)`,`地区生产总值指数-第三产业(上年=100)` FROM sheet1 WHERE 年份>={str(left)} and 年份<={str(right)} and 省级='中国'")
        lock.release()

        if ress:
            for i in ress:
                dataList.append(i[0])
                numList.append(round(float(i[2]) - 100, 2))
                numList2.append(round(float(i[3]) - 100, 2))
                numList3.append(round(float(i[4]) - 100, 2))
                numList4.append(round(float(i[1]) - 100, 2))

        # 数据缓存
        redis.rpush(list_key, str(dataList))
        redis.rpush(list_key, str(numList))
        redis.rpush(list_key, str(numList2))
        redis.rpush(list_key, str(numList3))
        redis.rpush(list_key, str(numList4))

        redis.expire(list_key, 120)  # 存活120秒，随后删除
    return {
        'dateList': dataList,
        'numList': numList,
        'numList2': numList2,
        'numList3': numList3,
        'numList4': numList4,
    }


@app.route('/right_center', methods=['GET'])
def right_center_():
    global right_center__
    data = right_center(9)
    right_center__=1
    return data


# 右中弹框
@app.route('/right_center_big_post', methods=['POST'])
def right_center_big_post_():
    global year_kuadu
    if request.method == 'POST':
        ress = request.json.get('want')
        year_kuadu = int(ress)
        # sched.pause_job('my_job')
        return {'success': True}
    return {'success': True}


@app.route('/right_center_big', methods=['GET'])
def right_center_big_():
    global year_kuadu
    global right_center_big__
    data = right_center(year_kuadu)
    right_center_big__=1
    return data

@app.route('/right_bottom',methods=['GET'])
def right_bottom_():
    global left_top__
    global left_center__
    global left_bottom__
    global center_map__
    global right_top__
    global right_top_big__
    global right_center__
    global right_center_big__
    global right_bottom__

    right_bottom__=1
    data={
        'name':'各节点状态',
        'children':[
            {
                'name':'左上',
                'value':left_top__
            },
            {
                'name': '左中',
                'value': left_center__
            },
            {
                'name': '左下',
                'value': left_bottom__
            },
            {
                'name': '中图',
                'value': center_map__
            },
            {
                'name': '右上',
                'children':[
                    {'name':'右上图','value':right_top__},
                    {'name':'右上大图','value':right_top_big__}
                ]
            },
            {
                'name': '右中',
                'children': [
                    {'name': '右中图', 'value': right_center__},
                    {'name': '右中大图', 'value': right_center_big__}
                ]
            },
            {
                'name': '右下',
                'value':right_bottom__
            },

        ]
    }
    return data


def clear():
    while (True):
        time.sleep(60)
        redis.flushall()

@failsafe
def create_app():
    return app

if __name__ == '__main__':
    read()
    clear_redis = threading.Thread(target=clear, args=("ProducerA",))
    create_app().run(host='0.0.0.0',port=2500)
