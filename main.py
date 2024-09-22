import sqlite3
import create_DB
import access_DB
from datetime import date, timedelta, datetime

"""" sx
Intent: 
Create a library database

Files: 
- Main.py: 
  interaction with DB and command execution
- Create_DB:
  If the DB doesn't exist or is missing tables, create it
- Access_DB:
  - Interact and access DB commands

"""
# Define global variables for connection and cursor 
# and commands
connection = None
cursor = None

#all main.py functions are meant to grab data
#and then funnel to the access_DB.py to interact with DB

# takes member information:
# SSN, campus and home mailing addresses, and phone numbers
# then the create library card is immediately called

def add_student(connection, cursor):
  student_info = []
  columns = access_DB.get_collumn_names(connection, cursor, "student")
  for column in columns:
    print ("Insert" + column + " : ")
    student_info.append(input())
  access_DB.add_student(connection, cursor, student_info)

def add_faculty(connection, cursor):
  faculty_info = []
  columns = access_DB.get_collumn_names(connection, cursor, "Faculty")
  for column in columns:
    print ("Insert" + column + " : ")
    faculty_info.append(input())
    access_DB.add_faculty(connection, cursor, faculty_info)

def add_person(connection, cursor):
  person_info = []
  columns = access_DB.get_collumn_names(connection, cursor, "person")
  for column in columns:
    print ("Insert" + column + " : ")
    person_info.append(input())
  access_DB.add_person(connection, cursor, person_info)

def add_staff(connection,cursor):
  staff_info = []
  columns = access_DB.get_collumn_names(connection, cursor, "staff")
  for column in columns:
    print ("Insert" + column + " : ")
    staff_info.append(input())
  access_DB.add_staff(connection, cursor, staff_info)

def take_out(connection, cursor):
  #take_out(B-id,B-date,Returned-date,copy_id,M)
  take_out_info = []
  take_out_info.append(input("Enter Book copy_id: "))
  take_out_info.append(input("Enter MemberID: "))
  access_DB.take_out(connection, cursor, take_out_info)

def return_book(connection,cursor):
  member_id = input("MemberID: ")
  copy_id = input("copy_id: ")
  access_DB.return_book(connection, cursor, member_id, copy_id)

def add_member(connection, cursor):
  member_info = []
  columns = access_DB.get_collumn_names(connection, cursor, "membership_card")
  for column in columns[:-1]:
    print ("Insert" + column + " : ")
    member_info.append(input())
  access_DB.add_member(connection, cursor, member_info)

def add_book(connection, cursor):
  book_info = []
  columns = access_DB.get_collumn_names(connection, cursor, "book_identification")
  for column in columns:
    print ("Insert" + column + " : ")
    book_info.append(input())
  
  access_DB.add_book(connection, cursor, book_info)

def custom(connection,cursor):
  command = input("Enter SQL command: ")
  output = access_DB.execute_sqlite_command(command)
  print (output)

def add_copy(connection, cursor):
  copy_info = []
  columns = access_DB.get_collumn_names(connection, cursor, "book_copy")
  for column in columns[1:]:
    print ("Insert" + column + " : ")
    copy_info.append(input())
  access_DB.add_copy(connection, cursor, copy_info)

def check_if_on_loan(connection, cursor):
  copy_id = input("Insert copy_id")
  access_DB.check_if_on_loan(connection, cursor, copy_id)

def change_personAddress(connection,cursor):
  new_address = input("Insert new address: ")
  person_id = int(input("Insert person_id: "))
  access_DB.change_personAddress(connection,cursor,new_address,person_id)

def change_personFirst(connection,cursor):
  new_First = input("Insert new first name: ")
  person_id = int(input("Insert person_id: "))
  access_DB.change_personFirst(connection,cursor,new_First,person_id)

def change_personLast(connection,cursor):
  new_Last = input("Insert new last_name: ")
  person_id = int(input("Insert person_id: "))
  access_DB.change_personLast(connection,cursor,new_Last,person_id)

def change_studentPhone(connection,cursor):
  new_phone = int(input("Insert new phone number "))
  student_id = int(input("Insert student_id "))
  access_DB.change_studentPhone(connection,cursor,new_phone,student_id)

def change_staffRole(connection,cursor):
  new_role = input("Insert new role: ")
  staff_id = int(input("Insert staff_id: "))
  access_DB.change_staffRole(connection,cursor,new_role,staff_id)

def change_membershipId(connection,cursor):
  membership_id = int(input("Insert Membership_id: "))
  oldmembership_id = int(input("Insert Old membership_id "))
  access_DB.change_membershipId(connection,cursor,membership_id,oldmembership_id)


def change_takeoutMembershipId(connection,cursor):
  membership_id = int(input("Insert Membership_id: "))
  oldmembership_id = int(input("Insert Old membership_id "))
  borrow_id = int(input("Insert borrow_id: "))
  access_DB.change_takeoutMembershipId(connection, cursor, membership_id,oldmembership_id,borrow_id)

def delete_staff(connection,cursor):
  deleted_staffId= int(input("Input the staff id you wish to delete "))
  access_DB.delete_staff(connection, cursor,deleted_staffId)

def not_returned(connection,cursor):
  cursor.execute("""Select copy_id FROM take_out WHERE returned_date is null""")
  x = cursor.fetchall()
  for x in x:
    print(*x, end = "| ")

def multiple_copies(connection,cursor):
  cursor.execute("""SELECT ISBN FROM book_copy Group by ISBN having count() >1""")
  x = cursor.fetchall()
  for x in x:
    print(*x, end = "| ")

def members_with_books(connection,cursor):
    cursor.execute("""SELECT membership_id FROM take_out WHERE returned_date is null""")
    x = cursor.fetchall()
    for x in x:
      print(*x, end = "| ")
  
def returning_customer(connection,cursor):
  cursor.execute("""SELECT membership_id FROM take_out Group by membership_id having count() > 4""")
  x = cursor.fetchall()
  for x in x:
    print(*x, end = "| ")

def print_all_studentid(connection,cursor):
  cursor.execute("""SELECT student_id FROM student""")
  x = cursor.fetchall()
  for x in x:
    print(*x, end = "| ")

def print_all_facultyid(connection,cursor):
  cursor.execute("""SELECT faculty_id FROM faculty""")
  x = cursor.fetchall()
  for x in x:
    print(*x, end = "| ")

def report(connection,cursor):
  print("Copy ID of books on loan: ")
  not_returned(connection,cursor)
  print("\nAll student ID: ")
  print_all_studentid(connection,cursor)
  print("\nMembers with books on loan: ")
  members_with_books(connection,cursor)
  print("\nAll faculty ID:")
  print_all_facultyid(connection,cursor)
  print("\nMembers with overdue books: ")
  access_DB.overdue_books(connection, cursor)
  #find all members who are about to expire in one month
  print("\nSend notices to the following members about expiry:")
  access_DB.print_about_to_expire(connection, cursor)
def all_on_loan(connection,cursor):
  id = input("insert member ID: ")
  access_DB.all_on_loan(connection, cursor, id)

def member_book_count(connection,cursor):
  mem_id = input("Enter member ID: ")
  print(\
    access_DB.member_book_count(connection, cursor, mem_id))

def help(connection, cursor):
  for command in commands:
    print(command)

def check_expiry(connection, cursor):
  id = input("Member_ID: ")
  if not access_DB.record_exists(cursor, id, "membership_id", "membership_card"):
      print("Not a member.")
  else:
      expiry_date = access_DB.check_expiry(connection, cursor, id)
      print(f"Expiry Date: {expiry_date}")

def renew_membership(connection, cursor):
  id = input("What member would you like to update?")
  if not access_DB.record_exists(cursor, id, "membership_id", "membership_card"):
    print("not a member")
  else: 
    today_date = datetime.now().date()
    sqlite_command = f"""
      UPDATE membership_card
      SET date_issued = '{today_date}'
      WHERE membership_id = {id}
    """
    access_DB.execute_sqlite_command(sqlite_command)
    
commands = {
  'add_person' : add_person,
  'add_student': add_student,
  'add_staff' : add_staff,
  'add_faculty': add_faculty,
  'add_member': add_member,
  'take_out' : take_out,
  'add_book' : add_book,
  'add_copy': add_copy,
  'check_if_on_loan': check_if_on_loan,
  'check_expiry': check_expiry,
  'custom' : custom,
  'change_personAddress' : change_personAddress,
  'change_personFirst' : change_personFirst,
  'change_personLast' : change_personLast,
  'change_studentPhone' : change_studentPhone,
  'change_staffRole' : change_staffRole,
  'change_membershipId' : change_membershipId,
  'change_takeoutMembershipId' : change_takeoutMembershipId,
  'delete_staff' : delete_staff,
  'return_book' : return_book,
  'not_returned' : not_returned,
  'multiple_copies' : multiple_copies,
  'members_with_books' : members_with_books,
  'member_book_count' : member_book_count,
  'returning_customer' : returning_customer,
  'print_all_studentid' : print_all_studentid,
  'print_all_facultyid' : print_all_facultyid,
  'all_on_loan' : all_on_loan,
  'help': help,
  'renew_membership': renew_membership,
  'report' : report
}

#When we boot up our program, displays 
#relevant matierial on terminal line
#Generate daily report
def On_Startup():
  global connection, cursor
  connection = sqlite3.connect('331_Library_DB')
  cursor = connection.cursor()
  cursor.execute("PRAGMA foreign_keys = ON;")
  
  create_DB.Table_Check(connection)

#where program begins
On_Startup()
report(connection,cursor)

while True:
  execute = input()
  if execute == 'quit':
    connection.commit()
    connection.close()
    break
  else:
    try:
      commands[execute](connection, cursor)
    except Exception as e:
      print(f"Command {e} doesn't exist")



