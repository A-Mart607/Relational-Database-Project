from datetime import date, timedelta, datetime
import subprocess


def add_student(connection, cursor, student_info):
    """
    This function adds a new student to the database.
    """    
    try:
        cursor.execute("""
            INSERT INTO student (student_id, campus, phone)
            VALUES (?, ?, ?)""", student_info)
        connection.commit()
        print ("Student added successfully.")
    
    except Exception as e:
        print("Error adding student:", e)

def add_person(connection,cursor,person_info):
  try:
    #person(person_id, SSN, address, firstname, lastname)
    cursor.execute("""
      INSERT into person (person_id, SSN, address, first_name, last_name)
      VALUES (?, ?, ?, ?, ?)""", person_info)
    connection.commit()
    print("Person added successfully.")
  except Exception as e:
    print ("Error adding person:", e)

def add_book(connection, cursor, book_info):
  try:
    #Book_Identification (ISBN, Book_subject, title, author)
    cursor.execute("""
    INSERT into book_identification(ISBN, book_subject, title, author)
    VALUES (?, ?, ?, ?)""", book_info)
    connection.commit()

  except Exception as e:
    print("Error adding book:", e)

def add_member(connection, cursor, member_info):
  try:
      #get today's date in SQLite format
      today = date.today()
      today = today.strftime("%Y-%m-%d")
      member_info.append(today)
      # Check if the ID we're adding is a student or faculty
      # Can't be a member if not one of those
      if record_exists(cursor, member_info[0], "student_id", "student") or \
      record_exists(cursor, member_info[0], "faculty_id", "faculty"):
          # Member(membership_id, member_photo, date_issued)
          cursor.execute("""
              INSERT INTO Membership_Card(membership_id, member_photo, date_issued)
              VALUES (?,?,?)""", member_info)
          connection.commit()
          print("Member added successfully.")
      else:
          raise Exception("ID doesn't belong to a student or faculty")
        
  except Exception as e:
      print(e)

def add_copy(connection, cursor, copy_info):
  #Book_Copy(Copy_id, ISBN, cover_type

  #generate the next copy_id sequentially 
  try:
    copy_id = f"{get_max(cursor, 'copy_id', 'book_copy'):0>8}"
    copy_info.insert(0, copy_id)
    cursor.execute("\
      INSERT INTO Book_Copy(copy_id, ISBN, cover_type)\
      Values (?,?,?)", copy_info)
    print ("Your Book copy # is:", copy_id)
    connection.commit()
  except Exception as e:
    print(e)
  

def take_out(connection, cursor, take_out_info):
  #take_out(Borrow_ID,Borrow_date,Returned-date,copy_id,membership_id)
  # check if person is a member
  if not record_exists(cursor, take_out_info[1], "membership_id", "membership_card"):
    print("Not a member")
    return 

  #check if person has more than 5 books
  count = member_book_count(connection, cursor, take_out_info[1])
  if count is not None and count >= 5:
    print("You have too many books")
    return
    
  #check if book is on loan
  if on_loan(cursor, take_out_info[0]):
    print("Already on loan")
    return 

  #check if member is expired (must be a student)
  #no need to worry about null if not member, handled above on 
  #recordexists
  check = check_expiry(connection, cursor, take_out_info[1])
  if check is not None:
    check = datetime.strptime(check, "%Y-%m-%d")
    time_difference = datetime.now() - check
    if time_difference > timedelta(days=365*4):
      print("member expired")
      return

  try:
    #get maximum Borrow_ID and + 1 to it to get a unique number
    borrowid = f"{get_max(cursor, 'borrow_id', 'take_out'):0>8}"
    # This is return date, NULL by default
    take_out_info.insert(0, None)
    #get todays date in SQL format
    today = date.today()
    today = today.strftime("%Y-%m-%d")
    take_out_info.insert(0, today)
    
    take_out_info.insert(0, borrowid)

    cursor.execute("""
      INSERT INTO take_out(Borrow_ID, Borrow_date, Returned_date, copy_id, membership_id)
      VAlUES (?,?,?,?,?)""", take_out_info)
    connection.commit()
    
    print("Take out added successfully. ID: " + str(borrowid))
  except Exception as e:
    print(e)

def check_expiry(connection, cursor, membership_id):
  #check if is a student, if a student: (faculty can't expire)
  #returns date of expiry
  try:
    if record_exists(cursor, membership_id, "faculty_id", "faculty"):
      return None
    
    cursor.execute(f"""
      SELECT * 
      FROM membership_card
      WHERE membership_id = {membership_id};"""
      )
    
    result = cursor.fetchone()
    
    return result[2]
    
  except Exception as e:
    print("Error checking expiry:", e)

def on_loan(cursor, copy_id):
    try:
      cursor.execute("""
          SELECT *
          FROM membership_card
          WHERE date_issued > date('now', '-1460 days');
      """)
      result = cursor.fetchall()
      print(result)
    
    except Exception as e:
      print(e)

def return_book(connection, cursor, id, copy_id):
  cursor.execute(f"""
    UPDATE take_out
    SET Returned_date = date('now')
    WHERE membership_id = {id}
    AND copy_id = {copy_id};
  """)
  connection.commit()


def get_max(cursor, column, tablename):
  cursor.execute(f"SELECT MAX({column}) FROM {tablename};")
  max_id = cursor.fetchone()[0]
  if not max_id:
    if max_id == 0:
      return 1
    return 0
  else:
    return max_id + 1

def check_if_on_loan(cursor, copyid):
  print(on_loan(cursor, copyid))
  
def add_faculty(connection, cursor, faculty_info):
  try:
    cursor.execute("""
      INSERT INTO faculty (faculty_id)
      VALUES (?)""", faculty_info)
    connection.commit()
    print ("Faculty added successfully.")

  except Exception as e:
    print("Error adding faculty:", e)


def add_staff(connection, cursor, staff_info):
  try:
    #Staff(staff_id,staff_role)
    cursor.execute(""" 
    INSERT into Staff(staff_id, staff_role)
    VALUES (?,?)""", staff_info)
    connection.commit()

  except Exception as e: 
    print ("Error adding staff:", e)

def get_collumn_names(connection, cursor, tablename):
  cursor.execute(f"PRAGMA table_info({tablename})")
  collumns = [row[1] for row in cursor.fetchall()]
  return collumns

def record_exists(cursor, id, column, table_name):
  try:
      cursor.execute(f"SELECT * FROM {table_name} WHERE {column} = ?", (id,))
      result = cursor.fetchone()
      return bool(result)
  except Exception as e:
      print(f"Error checking record existence: {e}")
      return False

def change_personAddress(connection,cursor,new_adress,person_id):
  try:
    cursor.execute(f"UPDATE person SET address = '{new_adress}' WHERE person_id = {person_id}")
    connection.commit()
    print("Address updated successfully.")
  except Exception as e:
    print("Error updating address:", e)

def change_personFirst(connection,cursor,new_First,person_id):
  try:
    cursor.execute(f"UPDATE person SET first_name = '{new_First}' WHERE person_id = {person_id}")
    connection.commit()
    print("First name updated successfully.")  
  except Exception as e:
    print ("Error updating person:", e)

def change_personLast(connection,cursor,new_Last,person_id):
  try:
    cursor.execute(f"UPDATE person SET last_name = '{new_Last}' WHERE person_id = {person_id}")
    connection.commit()
    print("Last name updated successfully.")  
  except Exception as e:
    print ("Error updating person:", e)
    
def change_studentPhone(connection,cursor,new_phone,student_id):
  try:
    cursor.execute(f"UPDATE student SET phone = '{new_phone}' WHERE student_id = {student_id}")
    connection.commit()
    print("student updated successfully.")
  except Exception as e:
    print ("Error updating student:", e)

def change_staffRole(connection,cursor,new_role,staff_id):
  try:
    cursor.execute(f"UPDATE Staff SET Staff_role = '{new_role}' WHERE Staff_id = {staff_id}")
    connection.commit()
    print("Staff updated successfully.")
  except Exception as e:
    print ("Error updating Staff:", e)

def change_membershipId(connection,cursor,membership_id,oldmembership_id):
  try:
    cursor.execute(f"UPDATE Membership_Card SET membership_id = '{membership_id}'WHERE membership_id = {oldmembership_id}")
    connection.commit()
    print("Membership_Card updated successfully.")
  except Exception as e:
    print ("Error updating Membership_Card:", e)


def execute_sqlite_command(command):
  try:
    result = subprocess.run(
        f'sqlite3 -header -table 331_Library_DB "{command}"',
        shell=True,
        capture_output=True,
        text=True,
        check=True
    )
    return result.stdout
  except subprocess.CalledProcessError as e:
      print(f"Error executing command: {e}")
      return None

def overdue_books(connection, cursor):
  # two types of queries, one a students, one for faculty
  
  # if a student, past 21 days is over-due
  sqlite_command = """
    SELECT p.person_id, p.first_name, p.last_name, t.borrow_date, t.copy_id
    FROM person p, Membership_Card m, take_out t, student s
    WHERE p.person_id = m.membership_id 
    AND m.membership_id = s.student_id
    AND m.membership_id = t.membership_id 
    AND t.Returned_date IS NULL 
    AND t.borrow_date < date('now', '-21 days');
  """
  
  output = execute_sqlite_command(sqlite_command)

  if output is not None:
    print ("Students: ")
    print(output)
  
  # if a faculty, past 3 months is over-due
  sqlite_command = """
    SELECT p.person_id, p.first_name, p.last_name, t.borrow_date, t.copy_id
    FROM person p, Membership_Card m, take_out t, faculty f
    WHERE p.person_id = m.membership_id 
    AND m.membership_id = f.faculty_id
    AND m.membership_id = t.membership_id 
    AND t.Returned_date IS NULL 
    AND t.borrow_date < date('now', '-90 days');  
  """
  output = execute_sqlite_command(sqlite_command)

  if output is not None:
    print("Faculty:")
    print(output)
    

def change_takeoutMembershipId(connection,cursor,membership_id,oldmembership_id, borrow_id):
  try:
    cursor.execute(f"UPDATE take_out SET membership_id = '{membership_id}'WHERE membership_id = {oldmembership_id} and borrow_id = {borrow_id}")
    connection.commit()
    print("take_out updated successfully.")
  except Exception as e:
    print ("Error updating take_out:", e)

def member_book_count(connection, cursor, membership_id):
  try:
    cursor.execute(f"\
      SELECT count(borrow_id)\
      FROM take_out\
      WHERE membership_id = {membership_id} \
      AND Returned_date IS NULL;")
    result = cursor.fetchall()
    if result is None:
      return 0
    else:
      return len(result)
  except Exception as e:
    print("Error getting member book count:", e)

def delete_staff(connection,cursor,deleted_staffId):
  try:
    cursor.execute(f"Delete FROM Staff WHERE staff_Id = {deleted_staffId}")
    connection.commit()
    print("Staff updated successfully.")
  except Exception as e:
    print ("Error updating take_out:", e)

def all_on_loan(connection, cursor, id):
  sqlite_command = f"""
    SELECT p.person_id, p.first_name, p.last_name, t.borrow_date, t.copy_id
    FROM person p, Membership_Card m, take_out t
    WHERE p.person_id = m.membership_id
      AND m.membership_id = {id}
      AND m.membership_id = t.membership_id
      AND t.returned_date IS NULL
  """
  output = execute_sqlite_command(sqlite_command)
  if output is not None:
    print(output)

def print_about_to_expire(connection, cursor):

  sqlite_command = """
  SELECT m.MEMBERSHIP_ID, m.MEMBER_PHOTO, m.DATE_ISSUED
  FROM Membership_Card m, student s
  WHERE s.student_id = m.membership_id
  AND DATE_ISSUED >= date('now', '-4 years', '+11 months')
  AND DATE_ISSUED < date('now', '-3 years', '+11 months')
  """
  output = execute_sqlite_command(sqlite_command)

  if output is not None:
      print(output)
  