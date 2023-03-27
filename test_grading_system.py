import pytest
import System
import Student
import Professor
import TA

# Test login
def test_login(grading_system):
    grading_system.login('akend3', '123454321')
    assert isinstance(grading_system.usr, Student.Student)
    assert grading_system.users['akend3']['role'] == 'student'

    grading_system.login('goggins', 'augurrox')
    assert isinstance(grading_system.usr, Professor.Professor)
    assert grading_system.users['goggins']['role'] == 'professor'

    grading_system.login('cmhbf5', 'bestTA')
    assert isinstance(grading_system.usr, TA.TA)
    assert grading_system.users['cmhbf5']['role'] == 'ta'

# Test check_password
def test_check_password(grading_system):
    assert grading_system.check_password('goggins','augurrox') == True
    assert grading_system.check_password('goggins','AUGURROX') == True
    assert grading_system.check_password('goggins','Augurrox') == True

# Test change_grade
def test_change_grade(grading_system):
    grading_system.login('goggins', 'augurrox')
    grading_system.usr.change_grade('akend3', 'databases', 'assignment1', 90)
    assert grading_system.users['akend3']['courses']['databases']['assignment1']['grade'] == 90

# Test create_assignment
def test_create_assignment(grading_system):
    grading_system.login('goggins', 'augurrox')
    grading_system.usr.create_assignment('assignment3', '3-20-22', 'databases')
    assert grading_system.courses['databases']['assignments']['assignment3']['due_date'] == '3-20-22'

# Test add_student
def test_add_student(grading_system):
    grading_system.login('saab', 'boomr345')
    grading_system.usr.add_student('hdjsr7', 'comp_sci')
    assert 'comp_sci' in grading_system.users['hdjsr7']['courses']

# Test drop_student
def test_drop_student(grading_system):
    grading_system.login('goggins', 'augurrox')
    grading_system.usr.drop_student('yted91', 'software_engineering')
    assert 'software_engineering' not in grading_system.users['yted91']['courses']

# Test submit_assignment
def test_submit_assignment(grading_system):
    grading_system.login('akend3', '123454321')
    grading_system.usr.submit_assignment('databases', 'assignment1', 'assignment1 submission', '3-20-22')
    assert grading_system.users['akend3']['courses']['databases']['assignment1']['submission'] == 'assignment1 submission'
    assert grading_system.users['akend3']['courses']['databases']['assignment1']['submission_date'] == '3-20-22'   

# Test check_ontime
def test_check_ontime(grading_system):
    grading_system.login('akend3', '123454321')
    assert grading_system.usr.check_ontime('3-20-22', '3-19-22') == False
    assert grading_system.usr.check_ontime('3-20-22', '3-20-22') == True

# Test check_grades
def test_check_grades(grading_system):
    grading_system.login('akend3', '123454321')
    grades = grading_system.usr.check_grades('comp_sci')
    assert grades == [['assignment1', 99], ['assignment2', 66]]

# Test view_assignments
def test_view_assignments(grading_system):
    grading_system.login('akend3', '123454321')
    assignments = grading_system.usr.view_assignments('comp_sci')
    assert assignments == [['assignment1', '2/2/20'], ['assignment2', '2/10/20']]

def test_username_format(grading_system):
    assert grading_system.login("goggins!", "augurrox") == True
    # username contains invalid characters

def test_password_format(grading_system):
    assert grading_system.login("goggins", "augurrox!") == True
    # password contains invalid characters

def test_add_student_wrong_class(grading_system):
    grading_system.login("goggins", "augurrox")
    grading_system.usr.add_student("akend3", "cloud_computing")
    # goggins should not be able to add a student to a class he does not teach

def test_drop_student_wrong_professor(grading_system):
    grading_system.login("goggins", "augurrox")
    grading_system.usr.drop_student("akend3", "software_engineering")
    # akend3 should not be dropped from a class they are not in

def test_submit_assignment_late(grading_system):
    grading_system.login("akend3", "123454321")
    grading_system.usr.submit_assignment("databases", "assignment1", "late submission", "1/7/20")
    assert grading_system.usr.check_ontime("databases", "assignment1") == False

@pytest.fixture
def grading_system():
    gradingSystem = System.System()
    gradingSystem.load_data()
    return gradingSystem

