from flask import Flask, jsonify, request, make_response
import sqlite3
from flask_cors import CORS




app = Flask(__name__)
cors = CORS(app, resources={r"*": {"origins": "https://ssg-courses.herokuapp.com"}})




@app.route('/users', methods=['GET'])
def getUsers():
    try:
        con = sqlite3.connect('data.db')
        cur = con.cursor()
        users = "select id, username, description,tags,coursesTakingId from users"
        cur.execute(users)
        allUsers=cur.fetchall()
        con.close()
        userList = []
        for u in allUsers:
            formattedUsers = {"id":u[0],"name":u[1],"description":u[2],"tags":eval(u[3]),"coursesTakingId":eval(u[4]) if u[4] != None else u[4]}
            userList.append(formattedUsers)
        return jsonify(userList),200
    except:
        return jsonify({"error":"the server falied"}),500


@app.route('/user/<string:usernameOrId>/<nameOrId>', methods=['GET'])
def getUser(usernameOrId,nameOrId):
    try:
        if nameOrId == '0':
            return jsonify({"name":"None"}),200
        else:
            con = sqlite3.connect('data.db')
            cur = con.cursor()
            user = f"select id, username,description,tags,coursesTakingId from users where {usernameOrId} ='{nameOrId}'"
            cur.execute(user)
            User=cur.fetchone()
            con.close()
            return jsonify({"userId":User[0],"name":User[1],"description":User[2],"tags":eval(User[3]),"coursesTakingId":eval(User[4]) if User[4] != None else User[4]}),200
    except:
        return jsonify({"messagge":"user not found"}),404






@app.route('/register', methods=['POST'])
def register():    
    try:
        data = request.get_json()
        name = data['name']
        password = data['password']
        description = data['description']
        tags = data['tags']
        con = sqlite3.connect('data.db')
        cur = con.cursor()
        cur.execute("insert into users(username,password,description,tags) values(?,?,?,?)",(str(name),str(password),str(description),str(tags)))
        con.commit()
        con.close()
        return jsonify({"message":"user created"})
    except:
        return jsonify({"error":"there was an error during the registry"})




@app.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        name = data['name']
        password = data['password']
        con = sqlite3.connect('data.db')
        cur = con.cursor()
        user = f"select password,id from users where username ='{name}'"
        cur.execute(user)
        DBdata = cur.fetchone()
        DBPassword = DBdata[0]
        _id = DBdata[1]
        con.close()
        if password == DBPassword:
            return jsonify({"userId":_id})
        else: 
            return jsonify({"message":"user or password is wrong"}),400
    except:
        return jsonify({"message":"the server failed"}),500


@app.route('/user/update/<int:_id>', methods=['PUT'])
def updateUser(_id):
    try:
        data = request.get_json()
        name = data['name']
        description = data['description']
        tags = data['tags']
        con = sqlite3.connect('data.db')
        cur = con.cursor()
        cur.execute(f"update users set username = '{name}',description = '{description}',tags = '{tags}'  where id ={_id}")
        con.commit()
        con.close()
        return jsonify({'message':'user updated'}),200
    except:
        return jsonify({"error":"the server failed"}),500

@app.route('/user/delete/<int:_id>', methods=['DELETE'])
def deleteUser(_id):
    try:
        con = sqlite3.connect('data.db')
        cur = con.cursor()
        cur.execute(f"DELETE FROM users WHERE id = {_id}")
        con.commit()
        cur.execute(f"update courses set adminId = '0'  where adminId ={_id}")
        con.commit()
        con.close()
        return jsonify({'message':'user deleted'}),200
    except:
        return jsonify({"error":"the server failed"}),500


@app.route('/course/create', methods=['POST'])
def createCourse():
    try:
        data = request.get_json()
        name = data['name']
        adminId = data['adminId']
        description = data['description']
        content = data['content']
        tags = data['tags']
        img = data['image']
        con = sqlite3.connect('data.db')
        cur = con.cursor()
        cur.execute("insert into courses(name,adminId,description,tags,content,image) values(?,?,?,?,?,?)",(str(name),str(adminId),str(description),str(tags),str(content),str(img)))
        con.commit()
        cur.execute(f"select id from courses where name ='{name}'")
        course = cur.fetchone()
        con.close()
        return jsonify({"id":course[0]}),201
    except:
        return jsonify({"error":"there was an error"}),500


@app.route('/courses', methods=['GET'])
def getcourses():
    try:
        con = sqlite3.connect('data.db')
        cur = con.cursor()
        courses = "select id,name,description,tags,adminId,content,image from courses"
        cur.execute(courses)
        allcourses=cur.fetchall()
        con.close()
        courseList = []
        for c in allcourses:
            formattedcourses = {"id":c[0],"name":c[1],"description":c[2],"tags":eval(c[3]),"adminId":c[4],"content":eval(c[5].replace("#",'"')),"image":c[6]}
            courseList.append(formattedcourses)
        return jsonify(courseList),200
    except:
        return jsonify({"error":"the server failed"}),500

@app.route('/courses/<search>', methods=['GET'])
def searchg(search):
        con = sqlite3.connect('data.db')
        cur = con.cursor()
        courses = f'select id,name,description,tags,adminId,content,image from courses where name LIKE ?'
        cur.execute(courses, ('%' + search + '%',))
        allcourses=cur.fetchall()
        con.close()
        courseList = []
        for c in allcourses:
            formattedcourses = {"id":c[0],"name":c[1],"description":c[2],"tags":eval(c[3]),"adminId":c[4],"content":eval(c[5].replace("#",'"')),"image":c[6]}
            courseList.append(formattedcourses)
        return jsonify(courseList),200


@app.route('/course/<string:typeOfSearch>/<nameOrId>', methods=['GET'])
def getcourse(typeOfSearch,nameOrId):
    try:
        con = sqlite3.connect('data.db')
        cur = con.cursor()
        course = f"select id, name,description,tags,adminId,content,image from courses where {typeOfSearch} ='{nameOrId}'"
        cur.execute(course)
        Course=cur.fetchone()
        con.close()
        return jsonify({"id":Course[0],"name":Course[1],"description":Course[2],"tags":eval(Course[3]),"adminId":Course[4],"content":eval(Course[5].replace("#",'"')),"image":Course[6]}),200
    except:
        return jsonify({"message":"user not found"}),404
@app.route('/course/add-content/<_id>', methods=['PUT'])
def addcontentcourse(_id):
    try:
        data = request.get_json()
        content = data['content']
        content = str(content)
        content.replace('"','#')
        content.replace("'",'#')
        con = sqlite3.connect('data.db')
        cur = con.cursor()
        cur.execute(f'update courses set content = "{content}" where id ={_id}')
        con.commit()
        con.close()
        return jsonify({'message':'course updated'}),200
    except:
        return jsonify({"error":"the server failed"}),500



@app.route('/user/<int:_id>/take/course/<int:courseId>', methods=['PUT'])
def takecourse(courseId,_id):
        con = sqlite3.connect('data.db')
        cur = con.cursor()
        cur.execute(f"select coursesTakingId from users where id ={_id}")
        DBdata = cur.fetchone()
        if DBdata[0] == None:
            formattedData = [courseId]
        else:
            formattedData = eval(DBdata[0])
            formattedData.append(courseId)
        con.commit()
        cur.execute(f"update users set coursesTakingId ='{formattedData}'  where id ={_id}")
        con.commit()
        con.close()
        return jsonify({'coursesTaking':formattedData}),200





if __name__ == '__main__':
    app.run(debug=True)