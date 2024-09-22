def table_exists(cursor, table_name):
  cursor.execute(f" \
    SELECT EXISTS (SELECT 1 FROM sqlite_master WHERE type='table' \
    AND name='{table_name}') AS table_exists")
  #retrieves a row from the table
  result = cursor.fetchone()
  #if we got a result we'll return not None
  return bool(result[0])


def initialize_tables(cursor):
  try:
    #create Book_Identification
    #Book_Identification (ISBN, Book_subject, title, author)
    cursor.execute("""
      CREATE TABLE IF NOT EXISTS book_identification(
        ISBN  dec(8,0),
        BOOK_SUBJECT varchar(40),
        TITLE varchar (50),
        AUTHOR varchar (50),
        PRIMARY KEY (ISBN)
      );
      """)

    
    #create Book_Copy
    #Book_Copy(Copy_id, ISBN, cover_type)
    cursor.execute("""
      CREATE TABLE IF NOT EXISTS book_copy(
        COPY_ID dec(8,0),
        ISBN dec(8,0),
        COVER_TYPE varchar (15),
        FOREIGN KEY (ISBN) REFERENCES 
        book_identification (ISBN),
        PRIMARY KEY (COPY_ID)
      );"""
)
    

    #create Membership_Card
    #Membership_Card (M,M-photo, Date_Issued)
    #To_do: How is M-Photo stored?
    cursor.execute("""
      CREATE TABLE IF NOT EXISTS membership_card(
        MEMBERSHIP_ID dec(8,0),
        MEMBER_PHOTO varchar (500),
        DATE_ISSUED date,
        PRIMARY KEY (MEMBERSHIP_ID)
        FOREIGN KEY (MEMBERSHIP_ID) REFERENCES person(PERSON_ID)
      ); """
    )

    
    #create Take_Out
    #Take_Out (Borrow_ID,Borrow_date,Returned-date,copy_id,membership_id)
    cursor.execute("""
      CREATE TABLE IF NOT EXISTS take_out(
        BORROW_ID dec(8,0),
        BORROW_DATE date,
        RETURNED_DATE date,
        COPY_ID dec(8,0),
        MEMBERSHIP_ID dec(8,0),
        PRIMARY KEY(BORROW_ID),
        FOREIGN KEY (COPY_ID) REFERENCES 
        book_copy (COPY_ID),
        FOREIGN KEY (MEMBERSHIP_ID) REFERENCES 
        membership_card (MEMBERSHIP_ID)
      );"""
    )

    #create person
    #person(person_id, SSN, address, firstname, lastname)
    cursor.execute("""
      CREATE TABLE IF NOT EXISTS person(
        PERSON_ID dec(8,0),
        SSN dec(9,0),
        ADDRESS varchar (400),
        FIRST_NAME varchar (50),
        LAST_NAME varchar (50),
        PRIMARY KEY (PERSON_ID)
      );"""
                  )

    #create Staff
    #Staff (S-id, S-role)
    cursor.execute("""
      CREATE TABLE IF NOT EXISTS staff(
        STAFF_ID dec(8,0),
        STAFF_ROLE varchar (40),
        PRIMARY KEY (STAFF_ID)
        );"""
    )


    #create Faculty
    #Faculty (F)
    cursor.execute("""
      CREATE TABLE IF NOT EXISTS faculty(
        FACULTY_ID dec(8,0),
        PRIMARY KEY (FACULTY_ID),
        FOREIGN KEY (FACULTY_ID) REFERENCES
        person (PERSON_ID)
        );"""
    )


    #create Student
    #Student (student_id, campus, phone)
    cursor.execute("""
      CREATE TABLE IF NOT EXISTS student(
        STUDENT_ID dec(8,0),
        CAMPUS varchar(40),
        PHONE dec(10,0),
        PRIMARY KEY (STUDENT_ID)
        FOREIGN KEY (STUDENT_ID) REFERENCES 
        person (PERSON_ID)
        );"""
    )

  except Exception as e:
    print(f"Error occurred while initializing database: {e}")



def Table_Check(conn):
  cursor = conn.cursor()

  #Currect Table Names
  Table_Names = [
    'book_identification', 
    'membership_card', 
    'take_out', 
    'staff', 
    'faculty',
    'student',
    'person',
    'book_copy'
  ]

  for table_name in Table_Names:
    if table_exists(cursor, table_name):
      print(f'{table_name} verified')
    else:
      print(f'{table_name} is missing. Generating')

  initialize_tables(cursor)
