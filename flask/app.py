import random
import traceback

import pymysql
from flask import Flask
from flask import request
from scipy.stats import pearsonr

app = Flask(__name__)

dbhost = "localhost"
dbuser = "lqy"
dbpassword = "671"
dbname = "moviedata"


@app.route('/api/register', methods=["post"])
def getRigistRequest():
    # 把用户名和密码注册到数据库中
    data = request.get_json(silent=True)
    username = data['username']
    password = data['password']
    # 连接数据库,此前在数据库中创建数据库TESTDB
    db = pymysql.connect(host=dbhost, user=dbuser, password=dbpassword, database=dbname)
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()
    # SQL 插入语句
    sql = "INSERT INTO user(iduser, password) VALUES ('" + username + "','" + password + "')"
    print(sql)
    try:
        # 执行sql语句
        cursor.execute(sql)
        initmatrix = '0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0'

        cursor2=db.cursor()
        sql2="update user set tag = '"+initmatrix+"' where iduser = '"+username+"'"
        print(sql2)
        cursor2.execute(sql2)
        # 提交到数据库执行
        db.commit()
        # 注册成功之后跳转到登录页面
        msg = '200'
    except:
        # 抛出错误信息
        traceback.print_exc()
        # 如果发生错误则回滚
        db.rollback()
        msg = '404'
    # 关闭数据库连接
    db.close()
    return {"code":msg}


@app.route('/api/inserthistory', methods=["get"])
def InsertHistoryRequest():
    # 查询用户名及密码是否匹配及存在
    # print(request.form)
    # username = request.form['username']
    # password = request.form['password']
    # print(username, ' ', password)
    data = request.get_json(silent=True)
    userid = request.args.get("userid")
    movieid = request.args.get("movieid")
    # userid movieid
    # 连接数据库,此前在数据库中创建数据库TESTDB
    # db = pymysql.connect("localhost", "root", "671jiayou", "moviedata")
    db = pymysql.connect(host=dbhost, user=dbuser, password=dbpassword, database=dbname)
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()
    cursor1 = db.cursor()
    sql = "select history from user where iduser = '" + userid + "'"
    # sql = "select * from user"
    historylist = []
    print(sql)
    try:
        # 执行sql语句
        cursor.execute(sql)
        result = cursor.fetchall()
        flag = 0
        for row in result:
            historylist = row[0].split(',')
            print(historylist)
            for item in historylist:
                print(item)
                if movieid == item:
                    flag = 1
            if flag == 0:
                historylist.append(movieid)
        insertstr = ','.join(str(x) for x in historylist)
        sql1 = "update user set history = %s where iduser = %s"
        val1 = [insertstr, userid]
        cursor1.execute(sql1, val1)
        db.commit()
        # 提交到数据库执行
    except:
        # 如果发生错误则回滚
        traceback.print_exc()
        db.rollback()
        msg = 'faild'
    # 关闭数据库连接
    db.close()
    return {'msg': msg, 'data': data}


@app.route('/api/gethistory', methods=["get"])
def GetHistoryRequest():
    # 查询用户名及密码是否匹配及存在
    # print(request.form)
    # username = request.form['username']
    # password = request.form['password']
    # print(username, ' ', password)
    data = request.get_json(silent=True)
    userid = request.args.get("userid")
    print(userid)
    # userid
    # 连接数据库,此前在数据库中创建数据库TESTDB
    # db = pymysql.connect("localhost", "root", "671jiayou", "moviedata")
    db = pymysql.connect(host=dbhost, user=dbuser, password=dbpassword, database=dbname)
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()
    sql = "select history from user where iduser = %s"
    val = [userid]
    # sql = "select * from user"
    print(sql)
    historylist = []
    try:
        # 执行sql语句
        cursor.execute(sql, val)
        result = cursor.fetchall()
        for row in result:
            historylist = row[0].split(',')
            print(historylist)
        # 提交到数据库执行
        msg = 'success'
    except:
        # 如果发生错误则回滚
        traceback.print_exc()
        db.rollback()
        msg = 'faild'
    # 关闭数据库连接
    db.close()
    return {'msg': msg, 'data': historylist}


@app.route('/api/login', methods=["post"])
def getLoginRequest():
    # 查询用户名及密码是否匹配及存在
    # postman 测试
    # print(request.form)
    # username = request.form['username']
    # password = request.form['password']
    # print(username, ' ', password)
    # 真正使用
    data = request.get_json(silent=True)
    username = data['username']
    password = data['password']
    # 连接数据库,此前在数据库中创建数据库TESTDB
    # db = pymysql.connect("localhost", "root", "671jiayou", "moviedata")
    db = pymysql.connect(host=dbhost, user=dbuser, password=dbpassword, database=dbname)
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()
    sql = "select * from user where iduser='" + username + "' and password='" + password + "'"
    # sql = "select * from user"
    print(sql)
    try:
        # 执行sql语句
        cursor.execute(sql)
        results = cursor.fetchall()
        print(results[0][2])
        if len(results) == 1:
            code = '200'
            data = results[0][2]

        else:
            code = '404'
            data = ''
        # 提交到数据库执行
        db.commit()
    except:
        # 如果发生错误则回滚
        traceback.print_exc()
        db.rollback()
        code = '404'
    # 关闭数据库连接
    db.close()
    return {'code': code, 'data': data}


# 点击按钮获取推荐
@app.route('/api/recommend', methods=["get"])
def getRecommend():
    tag = request.args.get("type")
    print(tag)
    if tag == 'plot':
        type = '剧情'
    elif tag == 'horror':
        type = '恐怖'
    elif tag == 'comedy':
        type = '喜剧'
    elif tag == 'suspense':
        type = '悬疑'
    elif tag == 'love':
        type = '爱情'
    else:
        type = '爱情'
        # type = '个性推荐'
        # res = personalRecommend()

    # 把用户名和密码注册到数据库中
    # 连接数据库,此前在数据库中创建数据库TESTDB
    db = pymysql.connect(host=dbhost, user=dbuser, password=dbpassword, database=dbname)
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()
    # SQL 插入语句
    sql = "select movie.id,movie.name,rating,img,person.name " + "from movie,relationships,person "
    sql += "where movie.id=relationships.movieid and relationships.personid = person.id "
    sql += "and genre = '" + type + "' "
    sql += "group by movie.id order by rating desc limit 32"
    print(sql)
    res = []
    try:
        # 执行sql语句
        cursor.execute(sql)
        results = cursor.fetchall()

        for item in results:
            id = item[0]
            movie = item[1].split(' ')[0]
            rating = item[2]
            img = item[3]
            director = item[4].split(' ')[0]
            temp = {"id": id, "movie": movie, "rating": rating, "img": img, "director": director, "url": ''}
            res.append(temp)
        print(res)
        # 提交到数据库执行
        db.commit()
        # 注册成功之后跳转到登录页面
        msg = 'success'
    except:
        # 抛出错误信息
        traceback.print_exc()
        # 如果发生错误则回滚
        db.rollback()
        msg = 'faild'
    # 关闭数据库连接
    db.close()
    return {'msg': msg, "data": res}


# 按id号查找电影
@app.route('/api/find', methods=["get"])
def Moviedetail():
    id = request.args.get("movieid")
    print(id)
    # 把用户名和密码注册到数据库中
    # 连接数据库,此前在数据库中创建数据库TESTDB
    db = pymysql.connect(host=dbhost, user=dbuser, password=dbpassword, database=dbname)
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()
    # SQL 插入语句
    sql = "select movie.id,movie.name,rating,img,person.name,summary,genre " + "from movie,relationships,person "
    sql += "where movie.id=relationships.movieid and relationships.personid = person.id "
    sql += "and movie.id = '" + id + "' "
    sql += "limit 1"
    print(sql)
    res = []
    try:
        # 执行sql语句
        cursor.execute(sql)
        results = cursor.fetchall()

        for item in results:
            id = item[0]
            movie = item[1].split(' ')[0]
            rating = item[2]
            img = item[3]
            director = item[4].split(' ')[0]
            summary = item[5]
            genre = item[6]
            temp = {"id": id, "movie": movie, "rating": rating, "img": img, "director": director, "summary": summary,
                    "url": '', "genre": genre}
            res.append(temp)
        print(res)
        # 提交到数据库执行
        db.commit()
        # 注册成功之后跳转到登录页面
        msg = 'success'
    except:
        # 抛出错误信息
        traceback.print_exc()
        # 如果发生错误则回滚
        db.rollback()
        msg = 'faild'
    # 关闭数据库连接
    db.close()
    return {'msg': msg, "data": res}


# 按名称查找电影
@app.route('/api/findmovie', methods=["get"])
def findMovie():
    name = request.args.get("name")
    print(name)
    # 把用户名和密码注册到数据库中
    # 连接数据库,此前在数据库中创建数据库TESTDB
    db = pymysql.connect(host=dbhost, user=dbuser, password=dbpassword, database=dbname)
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()
    # SQL 插入语句
    sql = "select movie.id,movie.name,rating,img,person.name,summary,genre " + "from movie,relationships,person "
    sql += "where movie.id=relationships.movieid and relationships.personid = person.id "
    sql += "and movie.name like '%" + name + "%' group by movie.name limit 32"
    print(sql)
    res = []
    try:
        # 执行sql语句
        cursor.execute(sql)
        results = cursor.fetchall()

        for item in results:
            id = item[0]
            movie = item[1].split(' ')[0]
            rating = item[2]
            img = item[3]
            director = item[4].split(' ')[0]
            summary = item[5]
            genre = item[6]
            temp = {"id": id, "movie": movie, "rating": rating, "img": img, "director": director, "summary": summary,
                    "url": '', "genre": genre}
            res.append(temp)
        print(res)
        # 提交到数据库执行
        db.commit()
        # 注册成功之后跳转到登录页面
        msg = 'success'
    except:
        # 抛出错误信息
        traceback.print_exc()
        # 如果发生错误则回滚
        db.rollback()
        msg = 'faild'
    # 关闭数据库连接
    db.close()
    return {'msg': msg, "data": res}


# 按id查找电影和评论
@app.route('/api/homemovie', methods=["get"])
def homeMovie():
    id = request.args.get("id")
    print(id)
    # 把用户名和密码注册到数据库中
    # 连接数据库,此前在数据库中创建数据库TESTDB
    db = pymysql.connect(host=dbhost, user=dbuser, password=dbpassword, database=dbname)
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()
    # SQL 插入语句
    sql = "select movie.id, movie.img, comments.name, comments.comment, movie.name "
    sql += "from movie, comments "
    sql += "where movie.id = comments.movieid and movie.id = '" + id + "' limit 4"
    print(sql)
    res = []
    try:
        # 执行sql语句
        cursor.execute(sql)
        results = cursor.fetchall()

        for item in results:
            id = item[0]
            img = item[1]
            name = item[2]
            comment = item[3]
            moviename = item[4].split(' ')[0]
            temp = {"id": id, "img": img, "name": name, "comment": comment, "moviename": moviename}
            res.append(temp)
        print(res)
        # 提交到数据库执行
        db.commit()
        # 注册成功之后跳转到登录页面
        msg = 'success'
    except:
        # 抛出错误信息
        traceback.print_exc()
        # 如果发生错误则回滚
        db.rollback()
        msg = 'faild'
    # 关闭数据库连接
    db.close()
    return {'msg': msg, "data": res}


# 电影排行榜
@app.route('/api/ranklist', methods=["get"])
def rankList():
    # 把用户名和密码注册到数据库中
    # 连接数据库,此前在数据库中创建数据库TESTDB
    db = pymysql.connect(host=dbhost, user=dbuser, password=dbpassword, database=dbname)
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()
    # SQL 插入语句
    sql = "select name,id from movie where length(substring_index(name,' ',1))<15 order by rating desc limit 10"
    print(sql)
    res = []
    count = 1
    try:
        # 执行sql语句
        cursor.execute(sql)
        results = cursor.fetchall()

        for item in results:
            name = item[0].split(' ')[0]
            movieid = item[1]
            temp = {"id": count, "name": name, "movieid": movieid}
            count += 1
            res.append(temp)
        print(res)
        # 提交到数据库执行
        db.commit()
        # 注册成功之后跳转到登录页面
        msg = 'success'
    except:
        # 抛出错误信息
        traceback.print_exc()
        # 如果发生错误则回滚
        db.rollback()
        msg = 'faild'
    # 关闭数据库连接
    db.close()
    return {'msg': msg, "data": res}


# 查找相似电影
@app.route('/api/similar', methods=["get"])
def similarmovie():
    db = pymysql.connect(host=dbhost, user=dbuser, password=dbpassword, database=dbname)
    id = request.args.get("id")
    cursor1 = db.cursor()
    sql1 = "select matrix from moviematrix where movieid='" + id + "'"
    # print("sql1 :",sql1)
    movieid = id
    # movietag= '1,1,1,2,0,0,1,2,1,5,1,1,0,2,0,1,4,1,5,1,2,6,1,5,1,4,1,4,1,8,1,6,0,0,0,0,0,0,0,0'

    try:
        cursor1.execute(sql1)
        result = cursor1.fetchall()
        result = str(result[0][0])
        movietag = result
        # print(result)
        # print(type(result))

        cursor2 = db.cursor()
        sql2 = "select movieid,matrix,rating from moviematrix"
        cursor2.execute(sql2)
        result = cursor2.fetchall()
        # print(result)
        movietag = movietag.split(',')
        movietag = list(map(int, movietag))
        list1 = []
        for row2 in result:
            movievector = row2[1].split(',')
            movievector = list(map(int, movievector))
            p = pearsonr(movietag, movievector)
            maptemp = dict()
            maptemp[row2[0]] = p[0]
            list1.append(maptemp)
        sorted(maptemp.values(), reverse=True)
        recommendlist = []
        i = 0
        while i < 40:
            for key in list1[i].keys():
                if key != movieid:
                    recommendlist.append(key)
            i += 1
        # recommendstr = ','.join(str(x) for x in recommendlist)
        random.shuffle(recommendlist)
        # print(recommendlist)
        cursor3 = db.cursor()
        sql3 = "select movie.id,movie.name,rating,img,person.name " + "from movie,relationships,person "
        sql3 += "where movie.id=relationships.movieid and relationships.personid = person.id "
        sql3 += "and movie.id in ('" + recommendlist[0] + "','" + recommendlist[1] + "','" + recommendlist[2] + "','" + \
                recommendlist[3] + "')"
        sql3 += " group by movie.name"
        # print(sql3)
        cursor3.execute(sql3)
        result = cursor3.fetchall()
        # print(result[0],result[1],result[2])
        res = []
        for item in result:
            id = item[0]
            name = item[1].split(' ')[0]
            rating = item[2]
            img = item[3]
            director = item[4].split(' ')[0]
            temp = {"id": id, "name": name, "rate": rating, "img": img, "director": director}
            res.append(temp)
        # print(res)
        return {"code": 200, "data": res}
    except:
        traceback.print_exc()
        # 如果发生错误则回滚
        db.rollback()
        return {"code": 404, "data": []}


# 个性推荐
@app.route('/api/personalrecommend', methods=["get"])
def personalrecommend():
    db = pymysql.connect(host=dbhost, user=dbuser, password=dbpassword, database=dbname)
    userid = request.args.get("userid")
    # userid = 'admin'
    try:
        cursor1 = db.cursor()
        sql1 = "select tag from user where iduser='" + userid + "'"
        cursor1.execute(sql1)
        result = cursor1.fetchall()
        print(result[0][0])
        usertag = result[0][0]

        cursor2 = db.cursor()
        sql2 = "select movieid,matrix,rating from moviematrix"
        cursor2.execute(sql2)
        result = cursor2.fetchall()
        uservector = usertag.split(',')
        uservector = list(map(int, uservector))
        list1 = []
        for row2 in result:
            movievector = row2[1].split(',')
            movievector = list(map(int, movievector))
            p = pearsonr(uservector, movievector)
            maptemp = dict()
            maptemp[row2[0]] = p[0]
            list1.append(maptemp)
        sorted(maptemp.values(), reverse=True)
        recommendlist = []
        i = 0
        while i < 40:
            for key in list1[i].keys():
                recommendlist.append(key)
            i += 1
        print(recommendlist)
        random.shuffle(recommendlist)

        searchrange = "('"
        for i in range(32):
            searchrange += str(recommendlist[i])
            searchrange += "','"
        searchrange = searchrange[:-2]
        searchrange += ')'
        # print(searchrange)
        # recommendstr = ','.join(str(x) for x in recommendlist)
        # res = recommendstr.split(',')
        # print(recommendstr)
        cursor3 = db.cursor()
        sql3 = "select movie.id,movie.name,rating,img,person.name " + "from movie,relationships,person "
        sql3 += "where movie.id=relationships.movieid and relationships.personid = person.id "
        sql3 += "and movie.id in " + searchrange
        sql3 += " group by movie.name"
        # print(sql3)
        cursor3.execute(sql3)
        result = cursor3.fetchall()
        print(result)
        res = []
        for item in result:
            id = item[0]
            name = item[1].split(' ')[0]
            rating = item[2]
            img = item[3]
            director = item[4].split(' ')[0]
            temp = {"id": id, "movie": name, "rating": rating, "img": img, "director": director}
            res.append(temp)

        return {"code": 200, "data": res}
    except:
        traceback.print_exc()
        # 如果发生错误则回滚
        db.rollback()
        return {"code": 404, "data": []}


# 个人兴趣选择
@app.route('/api/chooseinterests', methods=["post"])
def chooseinterests():
    data = request.get_json(silent=True)
    userid = data['userid']
    interests = data['interests']

    print("userid: ", userid)
    print("data: ", interests)
    try:
        db = pymysql.connect(host=dbhost, user=dbuser, password=dbpassword, database=dbname)
        cursor1 = db.cursor()
        sql1 = "select tag from user where iduser = '" + userid + "'"
        cursor1.execute(sql1)
        result = cursor1.fetchall()
        temp = result[0][0]
        result = result[0][0].split(',')
        result = [int(x) for x in result]
        print(result)
        for i in interests:
            if i == '喜剧':
                result[0] += 1
            elif i == '动作':
                result[1] += 1
            elif i == '犯罪':
                result[2] += 1
            elif i == '奇幻':
                result[3] += 1
            elif i == '剧情':
                result[4] += 1
            elif i == '冒险':
                result[5] += 1
            elif i == '家庭':
                result[6] += 1
            elif i == '爱情':
                result[7] += 1
            elif i == '同性':
                result[8] += 1
            elif i == '音乐':
                result[9] += 1
            elif i == '惊悚':
                result[10] += 1
            elif i == '情色':
                result[11] += 1
            elif i == '动画':
                result[12] += 1
            elif i == '歌舞':
                result[13] += 1
            elif i == '科幻':
                result[14] += 1
            elif i == '儿童':
                result[15] += 1
            elif i == '历史':
                result[16] += 1
            elif i == '战争':
                result[17] += 1
            elif i == '悬疑':
                result[18] += 1
            elif i == '传记':
                result[19] += 1
            elif i == '西部':
                result[20] += 1
            elif i == '恐怖':
                result[21] += 1
            elif i == '武侠':
                result[22] += 1
            elif i == '古装':
                result[23] += 1
            elif i == '灾难':
                result[24] += 1
            elif i == '黑色电影':
                result[25] += 1
            elif i == '运动':
                result[26] += 1
            elif i == '惊栗':
                result[27] += 1
            elif i == '悬念':
                result[28] += 1
            elif i == '荒诞':
                result[29] += 1
            elif i == '戏曲':
                result[30] += 1
            elif i == '鬼怪':
                result[31] += 1
            elif i == '达人秀':
                result[32] += 1
            elif i == '搞笑':
                result[33] += 1
            elif i == '成人':
                result[34] += 1
            elif i == '舞台艺术':
                result[35] += 1
            elif i == '真人秀':
                result[36] += 1
            elif i == '脱口秀':
                result[37] += 1
            elif i == '访谈':
                result[38] += 1
            elif i == '纪录片':
                result[39] += 1
        print(result)
        newres=""
        for i in result:
            newres+=str(i)
            newres+=","
        newres=newres[:-1]
        print("newres :",newres)
        print("temp: ",temp)
        cursor2 = db.cursor()
        sql2 = "update user set tag = '"+newres+"' where iduser = '"+userid+"'"
        cursor2.execute(sql2)
        db.commit()
        print("sql2 ",sql2)
        return {"code": 200}
    except:
        traceback.print_exc()
        # 如果发生错误则回滚
        db.rollback()
        return {"code": 404}


# 使用__name__ == '__main__'是 Python 的惯用法，确保直接执行此脚本时才
# 启动服务器，若其他程序调用该脚本可能父级程序会启动不同的服务器
if __name__ == '__main__':
    app.run(debug=True)
