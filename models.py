from datetime import datetime
from database import db
import bcrypt
from bson.objectid import ObjectId
class Student:
    collection = db.get_collection('students')
   
    @classmethod
    def create(cls, data):
        data['createdAt'] = datetime.utcnow()
        data['passwordHash'] = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())
        del data['password']
        return cls.collection.insert_one(data)
   
    @classmethod
    def find_by_id(cls, student_id):
        return cls.collection.find_one({'studentID': student_id})
   
    @classmethod
    def verify_password(cls, student_id, password):
        student = cls.find_by_id(student_id)
        if student and bcrypt.checkpw(password.encode('utf-8'), student['passwordHash']):
            return student
        return None
   
    @classmethod
    def get_by_campus_grade(cls, campus, grade):
        return list(cls.collection.find({'campus': campus, 'grade': grade}))
   
    @classmethod
    def get_all(cls):
        return list(cls.collection.find().sort('createdAt', -1))
   
    @classmethod
    def count_by_campus(cls, campus):
        return cls.collection.count_documents({'campus': campus})
   
    @classmethod
    def get_total_count(cls):
        return cls.collection.count_documents({})
   
    @classmethod
    def get_by_campus_grade_section(cls, campus, grade, section):
        return list(cls.collection.find({
            'campus': campus,
            'grade': grade,
            'section': section
        }))
   
    @classmethod
    def update(cls, student_id, data):
        if 'password' in data:
            data['passwordHash'] = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())
            del data['password']
        return cls.collection.update_one(
            {'studentID': student_id},
            {'$set': data}
        )
   
    @classmethod
    def delete(cls, student_id):
        return cls.collection.delete_one({'studentID': student_id})
class Task:
    collection = db.get_collection('tasks')
   
    @classmethod
    def create(cls, data):
        data['createdAt'] = datetime.utcnow()
        return cls.collection.insert_one(data)
   
    @classmethod
    def find_by_id(cls, task_id):
        try:
            return cls.collection.find_one({'_id': ObjectId(task_id)})
        except:
            return None
   
    @classmethod
    def get_all(cls):
        return list(cls.collection.find().sort('createdAt', -1))
   
    @classmethod
    def get_for_student(cls, campus, grade):
        return list(cls.collection.find({
            'campusTarget': campus,
            'gradeTarget': grade
        }))
   
    @classmethod
    def delete(cls, task_id):
        return cls.collection.delete_one({'_id': ObjectId(task_id)})
   
    @classmethod
    def update(cls, task_id, data):
        return cls.collection.update_one(
            {'_id': ObjectId(task_id)},
            {'$set': data}
        )
   
    @classmethod
    def get_total_count(cls):
        return cls.collection.count_documents({})
class Submission:
    collection = db.get_collection('submissions')
   
    @classmethod
    def create(cls, data):
        data['submittedAt'] = datetime.utcnow()
        data['status'] = 'completed'
        return cls.collection.insert_one(data)
   
    @classmethod
    def find_by_student_task(cls, student_id, task_id):
        try:
            return cls.collection.find_one({
                'studentId': student_id,
                'taskId': ObjectId(task_id)
            })
        except:
            return None
   
    @classmethod
    def get_by_student(cls, student_id):
        return list(cls.collection.find({'studentId': student_id}))
   
    @classmethod
    def get_task_completions(cls, task_id):
        try:
            return list(cls.collection.find({'taskId': ObjectId(task_id)}))
        except:
            return []
   
    @classmethod
    def get_completion_count(cls, task_id):
        try:
            return cls.collection.count_documents({'taskId': ObjectId(task_id)})
        except:
            return 0
   
    @classmethod
    def get_student_completions(cls, student_id):
        return list(cls.collection.find({'studentId': student_id}))
   
    @classmethod
    def get_completed_students_for_task(cls, task_id):
        """Get list of students who completed a specific task"""
        completions = cls.get_task_completions(task_id)
        completed_students = []
        for completion in completions:
            student = Student.find_by_id(completion['studentId'])
            if student:
                completed_students.append(student)
        return completed_students
class Admin:
    collection = db.get_collection('admins')
   
    @classmethod
    def create_default(cls):
        if cls.collection.count_documents({}) == 0:
            password_hash = bcrypt.hashpw('admin123'.encode('utf-8'), bcrypt.gensalt())
            cls.collection.insert_one({
                'username': 'admin',
                'passwordHash': password_hash,
                'role': 'super_admin',
                'createdAt': datetime.utcnow()
            })
            print("✅ Default admin created: admin / admin123")
   
    @classmethod
    def verify_password(cls, username, password):
        admin = cls.collection.find_one({'username': username})
        if admin and bcrypt.checkpw(password.encode('utf-8'), admin['passwordHash']):
            return admin
        return None
class Teacher:
    collection = db.get_collection('teachers')
   
    @classmethod
    def create(cls, data):
        data['createdAt'] = datetime.utcnow()
        data['passwordHash'] = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())
        del data['password']
        # Ensure permissions are explicitly set
        data['can_manage_students'] = data.get('can_manage_students', False)
        data['can_manage_tasks'] = data.get('can_manage_tasks', False)
        return cls.collection.insert_one(data)
   
    @classmethod
    def find_by_id(cls, teacher_id):
        return cls.collection.find_one({'teacherID': teacher_id})
   
    @classmethod
    def verify_password(cls, teacher_id, password):
        teacher = cls.find_by_id(teacher_id)
        if teacher and bcrypt.checkpw(password.encode('utf-8'), teacher['passwordHash']):
            return teacher
        return None
   
    @classmethod
    def get_by_campus(cls, campus):
        return list(cls.collection.find({'campus': campus}))
   
    @classmethod
    def get_all(cls):
        return list(cls.collection.find().sort('createdAt', -1))
   
    @classmethod
    def count_by_campus(cls, campus):
        return cls.collection.count_documents({'campus': campus})
   
    @classmethod
    def get_total_count(cls):
        return cls.collection.count_documents({})
   
    @classmethod
    def update(cls, teacher_id, data):
        if 'password' in data:
            data['passwordHash'] = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())
            del data['password']
        # Update permissions if provided
        if 'can_manage_students' in data:
            data['can_manage_students'] = data['can_manage_students'] == 'on'
        if 'can_manage_tasks' in data:
            data['can_manage_tasks'] = data['can_manage_tasks'] == 'on'
        return cls.collection.update_one(
            {'teacherID': teacher_id},
            {'$set': data}
        )
   
    @classmethod
    def delete(cls, teacher_id):
        return cls.collection.delete_one({'teacherID': teacher_id})
class Campus:
    collection = db.get_collection('campuses')
   
    @classmethod
    def initialize_defaults(cls):
        if cls.collection.count_documents({}) == 0:
            default_campuses = [
                {'name': 'Subhash Nagar', 'code': 'SUB', 'createdAt': datetime.utcnow()},
                {'name': 'Yamuna', 'code': 'YAM', 'createdAt': datetime.utcnow()},
                {'name': 'I20', 'code': 'I20', 'createdAt': datetime.utcnow()}
            ]
            cls.collection.insert_many(default_campuses)
            print("✅ Default campuses initialized")
   
    @classmethod
    def get_all(cls):
        return list(cls.collection.find().sort('name', 1))
class Grade:
    collection = db.get_collection('grades')
   
    @classmethod
    def initialize_defaults(cls):
        if cls.collection.count_documents({}) == 0:
            default_grades = []
            for grade_level in range(1, 11): # Grades 1 to 10
                grade_name = f"{grade_level}th Class"
                default_grades.append({
                    'name': grade_name,
                    'level': grade_level,
                    'createdAt': datetime.utcnow()
                })
            cls.collection.insert_many(default_grades)
            print("✅ Default grades initialized (1st to 10th Class)")
   
    @classmethod
    def get_all(cls):
        return list(cls.collection.find().sort('level', 1))
class Notification:
    collection = db.get_collection('notifications')
   
    @classmethod
    def create(cls, data):
        data['createdAt'] = datetime.utcnow()
        data['isRead'] = False
        return cls.collection.insert_one(data)
   
    @classmethod
    def get_for_user(cls, user_type, user_id=None, campus=None, grade=None):
        """Get notifications based on user type and access level"""
        query = {}
       
        if user_type == 'admin':
            # Admin gets all notifications
            query = {}
        elif user_type == 'teacher':
            # Teachers get notifications for their campus
            if campus:
                query = {
                    '$or': [
                        {'targetUserType': 'teacher', 'targetCampus': campus},
                        {'targetUserType': 'all_teachers'},
                        {'targetUserType': 'admin_and_teachers'}
                    ]
                }
        elif user_type == 'student':
            # Students get notifications for their campus and grade
            if campus and grade:
                query = {
                    '$or': [
                        {'targetUserType': 'student', 'targetCampus': campus, 'targetGrade': grade},
                        {'targetUserType': 'all_students'},
                        {'targetUserType': 'admin_and_students'}
                    ]
                }
       
        return list(cls.collection.find(query).sort('createdAt', -1).limit(50))
   
    @classmethod
    def get_unread_count(cls, user_type, user_id=None, campus=None, grade=None):
        """Get count of unread notifications"""
        query = {'isRead': False}
       
        if user_type == 'admin':
            # Admin gets all notifications
            pass
        elif user_type == 'teacher':
            # Teachers get notifications for their campus
            if campus:
                query['$or'] = [
                    {'targetUserType': 'teacher', 'targetCampus': campus},
                    {'targetUserType': 'all_teachers'},
                    {'targetUserType': 'admin_and_teachers'}
                ]
        elif user_type == 'student':
            # Students get notifications for their campus and grade
            if campus and grade:
                query['$or'] = [
                    {'targetUserType': 'student', 'targetCampus': campus, 'targetGrade': grade},
                    {'targetUserType': 'all_students'},
                    {'targetUserType': 'admin_and_students'}
                ]
       
        return cls.collection.count_documents(query)
   
    @classmethod
    def mark_as_read(cls, notification_id, user_type, user_id=None, campus=None, grade=None):
        """Mark a notification as read with access validation"""
        query = {'_id': ObjectId(notification_id)}
       
        # Add access control based on user type
        if user_type == 'teacher' and campus:
            query['$or'] = [
                {'targetUserType': 'teacher', 'targetCampus': campus},
                {'targetUserType': 'all_teachers'},
                {'targetUserType': 'admin_and_teachers'}
            ]
        elif user_type == 'student' and campus and grade:
            query['$or'] = [
                {'targetUserType': 'student', 'targetCampus': campus, 'targetGrade': grade},
                {'targetUserType': 'all_students'},
                {'targetUserType': 'admin_and_students'}
            ]
       
        return cls.collection.update_one(query, {'$set': {'isRead': True}})
   
    @classmethod
    def mark_all_as_read(cls, user_type, user_id=None, campus=None, grade=None):
        """Mark all notifications as read for a user"""
        query = {'isRead': False}
       
        if user_type == 'admin':
            # Admin gets all notifications
            pass
        elif user_type == 'teacher':
            # Teachers get notifications for their campus
            if campus:
                query['$or'] = [
                    {'targetUserType': 'teacher', 'targetCampus': campus},
                    {'targetUserType': 'all_teachers'},
                    {'targetUserType': 'admin_and_teachers'}
                ]
        elif user_type == 'student':
            # Students get notifications for their campus and grade
            if campus and grade:
                query['$or'] = [
                    {'targetUserType': 'student', 'targetCampus': campus, 'targetGrade': grade},
                    {'targetUserType': 'all_students'},
                    {'targetUserType': 'admin_and_students'}
                ]
       
        return cls.collection.update_many(query, {'$set': {'isRead': True}})
   
    @classmethod
    def create_task_notification(cls, task, action="created"):
        """Create notification for a new/updated task"""
        # Notify admin
        cls.create({
            'type': 'task',
            'title': f'Task {action.capitalize()}',
            'message': f'Task "{task["title"]}" has been {action}',
            'relatedId': str(task['_id']),
            'targetUserType': 'admin',
            'icon': 'fas fa-tasks'
        })
       
        # Notify teachers in target campuses
        for campus in task.get('campusTarget', []):
            cls.create({
                'type': 'task',
                'title': f'New Task {action.capitalize()}',
                'message': f'New task "{task["title"]}" has been {action} for {campus} campus',
                'relatedId': str(task['_id']),
                'targetUserType': 'teacher',
                'targetCampus': campus,
                'icon': 'fas fa-tasks'
            })
           
            # Notify students in target campuses and grades
            for grade in task.get('gradeTarget', []):
                cls.create({
                    'type': 'task',
                    'title': 'New Task Assigned',
                    'message': f'New task "{task["title"]}" has been assigned to your class',
                    'relatedId': str(task['_id']),
                    'targetUserType': 'student',
                    'targetCampus': campus,
                    'targetGrade': grade,
                    'icon': 'fas fa-tasks'
                })
   
    @classmethod
    def create_student_notification(cls, student, action="added"):
        """Create notification for a new/updated student"""
        # Notify admin
        cls.create({
            'type': 'student',
            'title': f'Student {action.capitalize()}',
            'message': f'Student "{student["name"]}" has been {action} to {student["campus"]} campus',
            'relatedId': student['studentID'],
            'targetUserType': 'admin',
            'icon': 'fas fa-user-graduate'
        })
       
        # Notify teachers in the same campus
        cls.create({
            'type': 'student',
            'title': f'New Student {action.capitalize()}',
            'message': f'New student "{student["name"]}" has been {action} to your campus',
            'relatedId': student['studentID'],
            'targetUserType': 'teacher',
            'targetCampus': student['campus'],
            'icon': 'fas fa-user-graduate'
        })
   
    @classmethod
    def create_teacher_notification(cls, teacher, action="added"):
        """Create notification for a new/updated teacher"""
        # Notify admin
        cls.create({
            'type': 'teacher',
            'title': f'Teacher {action.capitalize()}',
            'message': f'Teacher "{teacher["name"]}" has been {action} to {teacher["campus"]} campus',
            'relatedId': teacher['teacherID'],
            'targetUserType': 'admin',
            'icon': 'fas fa-chalkboard-teacher'
        })
   
    @classmethod
    def create_submission_notification(cls, submission, student, task):
        """Create notification for task submission"""
        # Notify admin
        cls.create({
            'type': 'submission',
            'title': 'Task Submitted',
            'message': f'Student "{student["name"]}" submitted task "{task["title"]}"',
            'relatedId': str(submission['_id']),
            'targetUserType': 'admin',
            'icon': 'fas fa-check-circle'
        })
       
        # Notify teachers in the same campus
        cls.create({
            'type': 'submission',
            'title': 'Task Submission',
            'message': f'Student "{student["name"]}" submitted task "{task["title"]}"',
            'relatedId': str(submission['_id']),
            'targetUserType': 'teacher',
            'targetCampus': student['campus'],
            'icon': 'fas fa-check-circle'
        })
# Initialize default data function
def initialize_default_data():
    Admin.create_default()
    Campus.initialize_defaults()
    Grade.initialize_defaults()
    print("✅ All default data initialized successfully!")