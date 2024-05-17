import mysql.connector as my
import random

# Database connection
conn = my.connect(host="localhost", user="root", password="123(Naman)@###", database="ayush")
cur = conn.cursor()

username = ""
logged_in = False

def main():
    global logged_in
    while True:
        print("#" * 30)
        print("#" * 5 + " QUIZ ")
        print("""
                1. Register
                2. Login
                3. Exit
        """)
        choice = input("Choose an option 1/2/3 to process: ")
        if choice == '1':
            register()
        elif choice == '2':
            login()
        elif choice == '3':
            exit_app()
        else:
            print("Please enter the correct option")

def validate_password(psw):
    l = u = d = s = 0
    for i in psw:
        if i.isupper():
            u += 1
        elif i.islower():
            l += 1
        elif i.isdigit():
            d += 1
        else:
            s += 1
    return l > 0 and u > 0 and s > 0 and d > 0

def register():
    while True:
        name = input("NAME: ")
        enr = input("Enrollment: ")
        clg = input("College: ")
        psw = input("Password: ")
        is_ps_valid = validate_password(psw)
        con = input("Contact: ")

        if is_ps_valid:
            try:
                data = (name, enr, clg, psw, con)
                sql = "INSERT INTO register (name, enrollment, college, password, contact) VALUES (%s, %s, %s, %s, %s)"
                cur.execute(sql, data)
                conn.commit()
                print("Thanks for registering")
                break
            except my.Error as e:
                print(f"Error: {e}")
                break
        else:
            print("\nPlease make a strong password (Use Number, Uppercase, Lowercase, Special Characters)")
            print("Try again")

def login():
    global username, logged_in
    uname = input("Enter enrollment: ")
    cur.execute('SELECT * FROM register WHERE enrollment = %s', (uname,))
    data = cur.fetchone()

    if data:
        pwd = input("Enter password: ")
        if data[3] == pwd:
            print(f"Welcome {data[0]}")
            username = uname
            logged_in = True
            after_login_menu()
        else:
            print("Wrong password!!!")
    else:
        print("Wrong Username or you didn't register with us!!!")
        ch = input("Do you want to register? y/n: ")
        if ch.lower() == 'y':
            register()
        else:
            login()

def after_login_menu():
    global logged_in
    while logged_in:
        print("""
            Choose an option:
            1. Attempt Quiz
            2. View Result
            3. Show Profile
            4. Update Profile
            5. Logout
        """)
        choice = input("Enter your choice: ")
        if choice == '1':
            attempt_quiz()
        elif choice == '2':
            show_result()
        elif choice == '3':
            show_profile()
        elif choice == '4':
            update_profile()
        elif choice == '5':
            logout()
        else:
            print("Please enter a correct option")

def attempt_quiz():
    global username
    subject_choice = input("Choose a subject\n 1. Python\n 2. Maths\n 3. Java\nYour choice: ")
    subjects = {'1': 'Python', '2': 'Maths', '3': 'Java'}
    subject = subjects.get(subject_choice, None)

    if subject:
        sql = f"SELECT * FROM questions WHERE subject = %s"
        cur.execute(sql, (subject,))
        questions = cur.fetchall()

        if not questions:
            print(f"No questions found for {subject}")
            return

        selected_questions = random.sample(questions, min(5, len(questions)))
        correct_answers = 0

        for n, question in enumerate(selected_questions, start=1):
            print(f"Q{n}: {question[1]}\n A. {question[2]}\n B. {question[3]}\n C. {question[4]}\n D. {question[5]}")
            answer = input("Your Answer A/B/C/D: ").upper()
            if answer == question[6]:
                correct_answers += 1

        print(f"Your Result is {correct_answers} out of {len(selected_questions)}")
        save_result(username, correct_answers)
    else:
        print("Invalid subject choice. Try again.")

def save_result(username, score):
    try:
        sql = "INSERT INTO result (enrollment, score) VALUES (%s, %s)"
        cur.execute(sql, (username, score))
        conn.commit()
    except my.Error as e:
        print(f"Error: {e}")

def show_result():
    global username
    sql = 'SELECT register.name, result.score FROM register JOIN result ON register.enrollment = result.enrollment WHERE register.enrollment = %s'
    cur.execute(sql, (username,))
    data = cur.fetchone()

    if data:
        print(f"Name: {data[0]}, Score: {data[1]}")
    else:
        print("No result found for this user")

def show_profile():
    global username
    sql = 'SELECT * FROM register WHERE enrollment = %s'
    cur.execute(sql, (username,))
    data = cur.fetchone()
    
    if data:
        print(f"Name: {data[0]}, Enrollment: {data[1]}, College: {data[2]}, Contact: {data[4]}")
    else:
        print("Profile not found")

def update_profile():
    global username
    cur.execute('SELECT * FROM register WHERE enrollment = %s', (username,))
    data = cur.fetchone()

    if data:
        new_name = input(f"Enter new name (leave blank to keep current: {data[0]}): ")
        new_college = input(f"Enter new college (leave blank to keep current: {data[2]}): ")
        new_contact = input(f"Enter new contact (leave blank to keep current: {data[4]}): ")

        try:
            if new_name or new_college or new_contact:
                sql = "UPDATE register SET name = %s, college = %s, contact = %s WHERE enrollment = %s"
                cur.execute(sql, (new_name or data[0], new_college or data[2], new_contact or data[4], username))
                conn.commit()
                print("Profile updated")
            else:
                print("No changes made")
        except my.Error as e:
            print(f"Error: {e}")
    else:
        print("Profile not found")

def logout():
    global logged_in, username
    logged_in = False
    username = ""
    print("You have been logged out")

def exit_app():
    print("Thanks for visiting!!!")
    if conn.is_connected():
        cur.close()
        conn.close()
    exit()

if __name__ == "__main__":
    main()
