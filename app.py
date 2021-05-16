#####################################################################################################################
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
from flask import Flask, request, jsonify, redirect, Response
import json
import uuid
import time
from bson import json_util

#####################################################################################################################

# Connect to our local MongoDB
client = MongoClient('mongodb://localhost:27017/')

# Choose database
db = client['InfoSys']

# Choose collections
students = db['Students']
users = db['Users']

# Initiate Flask App
app = Flask(__name__)

users_sessions = {}

#####################################################################################################################

def create_session(username):
    user_uuid = str(uuid.uuid1())
    users_sessions[user_uuid] = (username, time.time())
    return user_uuid  

def is_session_valid(user_uuid):
    return user_uuid in users_sessions


#####################################################################################################################


#####################################################################################################################

# CreateUser

@app.route('/createUser', methods=['POST'])
def create_user():
    # Request JSON data
    data = None 
    try:
        data = json.loads(request.data)
    except Exception as e:
        return Response("bad json content",status=500,mimetype='application/json')
    if data == None:
        return Response("bad request",status=500,mimetype='application/json')
    if not "username" in data or not "password" in data:
        return Response("Information incomplete",status=500,mimetype="application/json")

    
    if  users.find({"username": data["username"]}).count()==0:
        users.insert_one({"username": data["username"] , "password": data["password"]})
        return Response(data['username']+" was added to the MongoDB",status=200, mimetype='application/json') 
    else:
        return Response("A user with the given username already exists",status=400, mimetype='application/json')
    

#####################################################################################################################


#####################################################################################################################

#Login

@app.route('/login', methods=['POST'])
def login():
    # Request JSON data
    data = None 
    try:
        data = json.loads(request.data)
    except Exception as e:
        return Response("bad json content",status=500,mimetype='application/json')
    if data == None:
        return Response("bad request",status=500,mimetype='application/json')
    if not "username" in data or not "password" in data:
        return Response("Information incomplete",status=500,mimetype="application/json")

   
    #Search if username exist
    if users.find_one({"username" : data["username"], "password" : data["password"]}):
        uuid1=create_session(data["username"])
        screen = {"uuid": uuid1, "username": data['username']}
        return Response(json.dumps(screen),status=200, mimetype='application/json') 

    else:
        return Response("Wrong username or password.",status=400,mimetype='application/json') 

#####################################################################################################################



#####################################################################################################################

# ΕΡΩΤΗΜΑ 3: Return from email
@app.route('/getStudent', methods=['GET'])
def get_student():
    # Request JSON data
    data = None 
    try:
        data = json.loads(request.data)
    except Exception as e:
        return Response("bad json content",status=500,mimetype='application/json')
    if data == None:
        return Response("bad request",status=500,mimetype='application/json')
    if not "email" in data:
        return Response("Information incomplete",status=500,mimetype="application/json")

   

    uuid = request.headers.get('authorization')
    #check uuid
    check=is_session_valid(uuid)


    if check==True:
        student= json.loads(json_util.dumps(students.find_one({"email": data['email']})))
        if  students.find({"email": data['email']}).count()==1:
           
            return Response(json.dumps(student), status=200, mimetype='application/json')
        else:
            return Response("No user with this email" , status=401,mimetype='application/json')
            
    else:

        return Response("This user hasn't been authorized", status=401,mimetype='application/json')
#####################################################################################################################



#####################################################################################################################
# Return 30 year old students
@app.route('/getStudents/thirties',methods=['GET'])
def get_students_thirty():
   

    uuid=request.headers.get("authorization")
    check=is_session_valid(uuid)
    if check==True:
        thirtiez=students.find({"yearOfBirth" : 1991})
        if thirtiez.count()==0:
            return Response("No users found.", status=400, mimetype='application/json')
        else:

            slist=[]
            for i in thirtiez:
                i['_id'] = None
                slist.append(i)
            return Response(json.dumps(slist), status=200, mimetype='application/json')
    else: 
        return Response("You have to login first.", status=401, mimetype='application/json')

#####################################################################################################################



#####################################################################################################################
# Return Students >30 years old
@app.route('/getStudents/oldies', methods=['GET'])
def get_students_oldies():
    """
        Στα headers του request ο χρήστης θα πρέπει να περνάει και το uuid το οποίο έχει λάβει κατά την είσοδό του στο σύστημα. 
            Π.Χ: uuid = request.headers.get['authorization']
        Για τον έλεγχο του uuid να καλεστεί η συνάρτηση is_session_valid() (!!! Η ΣΥΝΑΡΤΗΣΗ is_session_valid() ΕΙΝΑΙ ΗΔΗ ΥΛΟΠΟΙΗΜΕΝΗ) με παράμετρο το uuid. 
            * Αν η συνάρτηση επιστρέψει False ο χρήστης δεν έχει αυθεντικοποιηθεί. Σε αυτή τη περίπτωση να επιστρέφεται ανάλογο μήνυμα με response code 401. 
            * Αν η συνάρτηση επιστρέψει True, ο χρήστης έχει αυθεντικοποιηθεί. 
        
        Το συγκεκριμένο endpoint θα πρέπει να επιστρέφει τη λίστα των φοιτητών οι οποίοι είναι 30 ετών και άνω.
        Να περάσετε τα δεδομένα των φοιτητών σε μία λίστα που θα ονομάζεται students.
        
        Σε περίπτωση που δε βρεθεί κάποιος φοιτητής, να επιστρέφεται ανάλογο μήνυμα και όχι κενή λίστα.
    """
    
    uuid = request.headers.get('authorization')
    check=is_session_valid(uuid)

    if check==False:
         return Response("This user hasn't been authorized", status=401,mimetype='application/json')
    else:
        oldiez= students.find({"$and": [{"yearOfBirth" : {"$lt" :1991}}]})
        if oldiez.count()==0:
            return Response("No student at this age.", status=400,mimetype='application/json')
        
        else:
            xlist=[]
            for i in oldiez:
                i['_id'] = None
                xlist.append(i)
            return Response(json.dumps(xlist), status=200, mimetype='application/json')
#####################################################################################################################



#####################################################################################################################

# Return address via email
@app.route('/getStudentAddress', methods=['GET'])
def get_studentAddress():
    # Request JSON data
    data = None 
    try:
        data = json.loads(request.data)
    except Exception as e:
        return Response("bad json content",status=500,mimetype='application/json')
    if data == None:
        return Response("bad request",status=500,mimetype='application/json')
    if not "email" in data:
        return Response("Information incomplete",status=500,mimetype="application/json")

    
    uuid = request.headers.get('authorization')
    check=is_session_valid(uuid)

    if check==False:
         return Response("This user hasn't been authorized", status=401,mimetype='application/json')
    else:
        c=students.find({"$and":[{"email" : data['email']}, {"address": { "$exists": True }}]})
        if c.count()==1:
            addressz= students.find_one({"email" : data["email"]})
            naddress=json.loads(json_util.dumps(addressz))

            #Create A Dictionary
            student={}
            student['name']= naddress['name']
            #Insert in the student dictionary, the first dictionary ([0]) from the list 
            student['street']= naddress['address'][0]['street']
            student['postcode']= naddress['address'][0]['postcode']

            return Response(json.dumps(student), status=200, mimetype='application/json')
        else:
            return Response("This email or address does not exist. Try again.", status=400,mimetype='application/json')

#####################################################################################################################


#####################################################################################################################
    # Remove a Student via email
@app.route('/deleteStudent', methods=['DELETE'])
def delete_student():
    # Request JSON data
    data = None 
    try:
        data = json.loads(request.data)
    except Exception as e:
        return Response("bad json content",status=500,mimetype='application/json')
    if data == None:
        return Response("bad request",status=500,mimetype='application/json')
    if not "email" in data:
        return Response("Information incomplete",status=500,mimetype="application/json")



    uuid = request.headers.get('authorization')
    check=is_session_valid(uuid)

    if check==True:
        student= json.loads(json_util.dumps(students.find_one({"email": data['email']})))
        if  students.find({"email": data['email']}).count()==1:
           
            students.delete_one({"email": data['email']})
            msg= "User" + student['name'] + "has been removed"


            return Response(msg, status=200, mimetype='application/json')
        else:
            msg="No user with this email"
            return Response(msg , status=401,mimetype='application/json')
            

    else:

        return Response("This user hasn't been authorized", status=401,mimetype='application/json')


#####################################################################################################################


#####################################################################################################################

# Add courses via email
@app.route('/addCourses', methods=['PATCH'])
def add_courses():
    # Request JSON data
    data = None 
    try:
        data = json.loads(request.data)
    except Exception as e:
        return Response("bad json content",status=500,mimetype='application/json')
    if data == None:
        return Response("bad request",status=500,mimetype='application/json')
    if not "email" in data or not "courses" in data:
        return Response("Information incomplete",status=500,mimetype="application/json")

   


    uuid=request.headers.get("authorization")
    check=is_session_valid(uuid)

    if check==True:
        coursez=students.find({"email" : data['email']})
        if coursez.count()==0:
            return Response("No users found.", status=400, mimetype='application/json')
        else:
            #Update our db
            students.update_one({"email" : data['email']}, {'$set': {"courses" : data['courses']}})
            
            return Response("Successfully imported", status=200, mimetype='application/json')
    else: 
        return Response("You have to login first.", status=401, mimetype='application/json')

#####################################################################################################################


#####################################################################################################################
  
# Return passed courses via email
@app.route('/getPassedCourses', methods=['GET'])
def get_courses():
    # Request JSON data
    data = None 
    try:
        data = json.loads(request.data)
    except Exception as e:
        return Response("bad json content",status=500,mimetype='application/json')
    if data == None:
        return Response("bad request",status=500,mimetype='application/json')
    if not "email" in data:
        return Response("Information incomplete",status=500,mimetype="application/json")


    uuid=request.headers.get("authorization")
    check=is_session_valid(uuid)

    if check==True:
        coursezz=students.find({"$and":[{"email" : data['email']}, {"courses": { "$exists": True }}]})

        if coursezz.count()==0:
            return Response("No users with this email or courses found.", status=400, mimetype='application/json')
        else:
            courseh=students.find_one({"email" : data['email']})
            student=json.loads(json_util.dumps(courseh))
            list_courses=student['courses']

            dict1={}
            dict2={}
            course=0

            while course<len(list_courses):
                dict1.update(list_courses[course])
                course=course+1

            for i in dict1:
                if dict1[i]>=5:
                    dict2[i]=dict1[i]
                
            
            return Response(json.dumps(dict2), status=200, mimetype='application/json')

    else: 
        return Response("You have to login first.", status=401, mimetype='application/json')

#####################################################################################################################
    

#####################################################################################################################
# Run flask in debugging mode in port 5000
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)