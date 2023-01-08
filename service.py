import time

import pymysql


def create():
    db = pymysql.connect(host='localhost', user='root', password='123456', port=3306, db='todolist')
    cursor = db.cursor()
    sql = 'CREATE TABLE IF NOT EXISTS task (ID INT PRIMARY KEY AUTO_INCREMENT,title VARCHAR(255) NOT NULL ,' \
          'content TEXT NOT NULL,status VARCHAR(255) NOT NULL , add_time INT NOT NULL,end_time INT NOT NULL)'
    cursor.execute(sql)
    db.close()


def create_task(title, content, status, end_time):
    code = 200
    db = pymysql.connect(host='localhost', user='root', password='123456', port=3306, db='todolist')
    cursor = db.cursor()
    data = {
        'title': title,
        'content': content,
        'status': status,
        'add_time': time.time(),
        'end_time': end_time,
    }
    table = 'task'
    keys = ', '.join(data.keys())
    values = ', '.join(['%s'] * len(data))
    sql = 'INSERT INTO {table}({keys}) VALUES ({values})'.format(table=table, keys=keys, values=values)
    try:
        if cursor.execute(sql, tuple(data.values())):
            print('Successful')
            db.commit()
    except Exception as e:
        code = 404
        print('Failed\n')
        print(e)
        db.rollback()
    db.close()
    return code


def show_task(tid):
    code = 200
    db = pymysql.connect(host='localhost', user='root', password='123456', port=3306, db='todolist')
    cursor = db.cursor()
    sql = 'SELECT * FROM task WHERE ID = %s'
    try:
        cursor.execute(sql, tid)
        res = cursor.fetchall()
        fields = cursor.description
        db.commit()
        cursor.close()
        db.close()
    except Exception as e:
        code = 404
        print(e)
        db.rollback()
        cursor.close()
        db.close()
        return {
            'data': "",
            'code': code,
        }
    column_list = []
    for i in fields:
        # 提取字段名，追加到列表中
        column_list.append(i[0])
    for row in res:
        data = {}
        for i in range(len(column_list)):
            data[column_list[i]] = str(row[i])
            # data[column_list[0]] = row[0]
            # # Python字段格式 和json字段格式转换
            # data[column_list[1]] = str(row[1])
            # data[column_list[2]] = str(row[2])
            # data[column_list[3]] = str(row[3])
            # Python的dict --转换成----> json的object
        return {
            'data': data,
            'code': code,
        }


def list_task(page, status):
    code = 200
    db = pymysql.connect(host='localhost', user='root', password='123456', port=3306, db='todolist')
    cursor = db.cursor()
    if status != '' and str(status) != 'None':
        sql = 'SELECT * FROM task where status = {status} ORDER BY id ASC LIMIT {limit} offset {offset}'.format(
            status=status, limit=5, offset=(5 * int(page) - 5))
    else:
        sql = 'SELECT * FROM task  ORDER BY id ASC LIMIT {limit} offset {offset}'.format(limit=5,
                                                                                         offset=(5 * int(page) - 5))
    try:
        cursor.execute(sql)
        res = cursor.fetchall()
        fields = cursor.description
        db.commit()
        cursor.close()
        db.close()
    except Exception as e:
        code = 404
        print(e)
        db.rollback()
        cursor.close()
        db.close()
        return {
            'data': "",
            'code': code,
        }
    column_list = []
    for i in fields:
        # 提取字段名，追加到列表中
        column_list.append(i[0])
    data = {}
    number = 0
    for row in res:
        number += 1
        task = {}
        for i in range(len(column_list)):
            task[column_list[i]] = str(row[i])
            # data[column_list[0]] = row[0]
            # # Python字段格式 和json字段格式转换
            # data[column_list[1]] = str(row[1])
            # data[column_list[2]] = str(row[2])
            # data[column_list[3]] = str(row[3])
            # Python的dict --转换成----> json的object
        data[number] = task
    return {
        'data': data,
        'total': number,
        'code': code,
    }


def update_task(tid, status):
    code = 200
    db = pymysql.connect(host='localhost', user='root', password='123456', port=3306, db='todolist')
    cursor = db.cursor()
    sql = "UPDATE task SET status=%s WHERE id = %s"
    try:
        # 执行SQL语句
        cursor.execute(sql, (status, tid))
        # 提交到数据库执行
        db.commit()
    except Exception as e:
        print(e)
        code = 404
        # 发生错误时回滚
        db.rollback()
    db.close()
    return code


def update_tasks(status):
    code = 200
    db = pymysql.connect(host='localhost', user='root', password='123456', port=3306, db='todolist')
    cursor = db.cursor()
    sql = "UPDATE task SET status=%s "
    try:
        # 执行SQL语句
        cursor.execute(sql, status)
        # 提交到数据库执行
        db.commit()
    except Exception as e:
        print(e)
        code = 404
        # 发生错误时回滚
        db.rollback()
    db.close()
    return code


def find_task(page, keyword):
    code = 200
    db = pymysql.connect(host='localhost', user='root', password='123456', port=3306, db='todolist')
    cursor = db.cursor()
    sql = "SELECT * FROM task  WHERE (title like'%{keyword}%' or content like '%{keyword}%') ORDER BY id ASC LIMIT {limit} offset {offset}".format(
        limit=5,
        offset=(5 * int(page) - 5), keyword=keyword)
    # 执行SQL语句
    cursor.execute(sql)
    res = cursor.fetchall()
    fields = cursor.description
    # 提交到数据库执行
    db.commit()
    cursor.close()
    db.close()
    column_list = []
    for i in fields:
        # 提取字段名，追加到列表中
        column_list.append(i[0])
    data = {}
    number = 0
    for row in res:
        number += 1
        task = {}
        for i in range(len(column_list)):
            task[column_list[i]] = str(row[i])
        data[number] = task
    return {
        'data': data,
        'total': number,
        'code': code,
    }


def delete_task(tid):
    code = 200
    db = pymysql.connect(host='localhost', user='root', password='123456', port=3306, db='todolist')
    cursor = db.cursor()
    sql = "DELETE FROM task  WHERE id = %s"
    try:
        # 执行SQL语句
        cursor.execute(sql, tid)
        # 提交到数据库执行
        db.commit()
    except Exception as e:
        print(e)
        code = 404
        # 发生错误时回滚
        db.rollback()
    db.close()
    return code


def delete_tasks(status):
    code = 200
    db = pymysql.connect(host='localhost', user='root', password='123456', port=3306, db='todolist')
    cursor = db.cursor()
    if status != '' and str(status) != 'None':
        sql = "DELETE FROM task where status = '{status}'".format(status=status)
    else:
        sql = "DELETE FROM task"
    try:
        # 执行SQL语句
        cursor.execute(sql)
        # 提交到数据库执行
        db.commit()
    except Exception as e:
        print(e)
        code = 404
        # 发生错误时回滚
        db.rollback()
    db.close()
    return code
