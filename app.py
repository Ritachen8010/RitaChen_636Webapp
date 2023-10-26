from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
import re
from datetime import datetime
import mysql.connector
from mysql.connector import FieldType
import connect

app = Flask(__name__)

dbconn = None
connection = None

def getCursor():
    global dbconn
    global connection
    connection = mysql.connector.connect(user=connect.dbuser, \
    password=connect.dbpass, host=connect.dbhost, \
    database=connect.dbname, autocommit=True)
    dbconn = connection.cursor()
    return dbconn

@app.route("/")
def home():
    return render_template("base.html")

@app.route("/admin")
def admin_home():
    return render_template("admin.html")

@app.route("/listdrivers")
def listdrivers():
    connection = getCursor()
    query = """
            SELECT driver.driver_id, 
            driver.first_name, 
            driver.surname, 
            driver.date_of_birth, 
            driver.age, 
            caregiver.first_name AS caregiver_first_name, 
            caregiver.surname AS caregiver_surname
            FROM driver
            LEFT JOIN driver AS caregiver ON driver.caregiver = caregiver.driver_id
            ORDER BY driver.surname, driver.first_name;
        """
    connection.execute(query)
    driver_List = connection.fetchall()

    print(driver_List)
    return render_template("driver_list.html", driver_List=driver_List)

@app.route("/driverdetails_by_click_name/<string:driver_name>")
def driverdetails_by_click_name(driver_name):
    connection = getCursor()
    runs = []
    driver = None

    connection.execute("""
            SELECT driver.driver_id, driver.first_name, driver.surname, car.model as carModel, car.drive_class as driveClass 
            FROM driver 
            INNER JOIN car ON driver.car = car.car_num 
            WHERE CONCAT(driver.surname, ' ', driver.first_name) = %s""", (driver_name,))
    driver = connection.fetchone()

    if driver:
        connection.execute("""
            SELECT course.name as course_name, run.run_num, run.wd, run.cones, run.seconds as runDetail 
            FROM run 
            INNER JOIN course ON run.crs_id = course.course_id 
            WHERE run.dr_id = %s""", (driver[0],))
        runs = connection.fetchall()

    return render_template("driverdetails_by_click_name.html", driver=driver, runs=runs)

@app.route("/driverdetails", methods=["GET", "POST"])
def driverdetails():
    connection = getCursor()
    runs = []
    driver = None

    # Get driver list
    connection.execute("SELECT CONCAT(first_name, ' ', surname) as name FROM driver")
    driver_names = [name[0] for name in connection.fetchall()]

    if request.method == "POST":
        driver_name = request.form.get("driver_name")
        connection.execute("""
            SELECT driver.driver_id, CONCAT(driver.first_name, ' ', driver.surname) as name, car.model as carModel, car.drive_class as driveClass 
            FROM driver 
            INNER JOIN car ON driver.car = car.car_num 
            WHERE CONCAT(driver.first_name, ' ', driver.surname) = %s
            ORDER BY surname, first_name
            """, (driver_name,))
        driver = connection.fetchone()

        # If driver exists, fetch the runs for the driver
        if driver:
            connection.execute("""
            SELECT course.name as course_name, run.run_num, run.wd, run.cones, run.seconds as runDetail 
            FROM run 
            INNER JOIN course ON run.crs_id = course.course_id 
            WHERE run.dr_id = %s
            """, (driver[0],))
            runs = connection.fetchall()

        return render_template("select_driver_run_details.html", driver_names=driver_names, driver_name=driver_name, driver=driver, runs=runs)

    return render_template("select_driver_run_details.html", driver_names=driver_names)

@app.route("/listcourses")
def listcourses():
    connection = getCursor()
    connection.execute("SELECT * FROM course;")
    courseList = connection.fetchall()
    return render_template("course_list.html", course_list = courseList)

@app.route("/overallresult")
def overallresult():
    connection = getCursor()

    # Query to get all driver details along with course times
    query = """
            SELECT
                driver.driver_id,
                car.model AS carModel,
                CONCAT(driver.first_name, ' ', driver.surname, IF(driver.age < 25, ' (J)', '')) AS name,
    
                IFNULL(ROUND(MIN(CASE WHEN course.name = 'Going Loopy' THEN run.seconds ELSE NULL END), 2), 'DNF') AS course_a_time,
                IFNULL(ROUND(MIN(CASE WHEN course.name = 'Mum''s Favourite' THEN run.seconds ELSE NULL END), 2), 'DNF') AS course_b_time,
                IFNULL(ROUND(MIN(CASE WHEN course.name = 'Walnut' THEN run.seconds ELSE NULL END), 2), 'DNF') AS course_c_time,
                IFNULL(ROUND(MIN(CASE WHEN course.name = 'Hamburger' THEN run.seconds ELSE NULL END), 2), 'DNF') AS course_d_time,
                IFNULL(ROUND(MIN(CASE WHEN course.name = 'Shoulders Back' THEN run.seconds ELSE NULL END), 2), 'DNF') AS course_e_time,
                IFNULL(ROUND(MIN(CASE WHEN course.name = 'Cracked Fluorescent' THEN run.seconds ELSE NULL END), 2), 'DNF') AS course_f_time,
    
            COALESCE(
                CAST(ROUND(COALESCE(         
                    MIN(CASE WHEN course.name = 'Going Loopy' THEN run.seconds END) +         
                    MIN(CASE WHEN course.name = 'Mum''s Favourite' THEN run.seconds END) +         
                    MIN(CASE WHEN course.name = 'Walnut' THEN run.seconds END) +         
                    MIN(CASE WHEN course.name = 'Hamburger' THEN run.seconds END) +         
                    MIN(CASE WHEN course.name = 'Shoulders Back' THEN run.seconds END) +         
                    MIN(CASE WHEN course.name = 'Cracked Fluorescent' THEN run.seconds END)
                ), 2) AS CHAR),'NQ'
            ) AS overall_time

            FROM 
	            driver
            LEFT JOIN 
	            car ON driver.car = car.car_num
            LEFT JOIN 
	            run ON driver.driver_id = run.dr_id
            LEFT JOIN 
	            course ON run.crs_id = course.course_id
            GROUP BY 
	            driver.driver_id
            ORDER BY 
            CASE WHEN overall_time is NULL THEN 1 ELSE 0 END, overall_time;
        """
    connection.execute(query)
    overall_Result = connection.fetchall()

    results_with_awards = []
    for idx, driver in enumerate(overall_Result, start=1):
        driver_list = list(driver)
        if idx == 1:
            driver_list.append('Cup')  # Add "Cup" to the end of the list
        elif 2 <= idx <= 5:
            driver_list.append('Prize')  # Add "Prize" to the end of the list
        else:
            driver_list.append('')  # Add an empty string to the end of the list, indicating no award
        results_with_awards.append(tuple(driver_list))

    return render_template("overall_result.html", overall_result = results_with_awards)

@app.route("/graph")
def showgraph():
    connection = getCursor()
    query = """
            SELECT
                driver.driver_id,
                CONCAT(driver.first_name, ' ', driver.surname, IF(driver.age < 25, ' (J)', '')) AS name,
    
                IFNULL(ROUND(MIN(CASE WHEN course.name = 'Going Loopy' THEN run.seconds ELSE NULL END), 2), 'DNF') AS course_a_time,
                IFNULL(ROUND(MIN(CASE WHEN course.name = 'Mum''s Favourite' THEN run.seconds ELSE NULL END), 2), 'DNF') AS course_b_time,
                IFNULL(ROUND(MIN(CASE WHEN course.name = 'Walnut' THEN run.seconds ELSE NULL END), 2), 'DNF') AS course_c_time,
                IFNULL(ROUND(MIN(CASE WHEN course.name = 'Hamburger' THEN run.seconds ELSE NULL END), 2), 'DNF') AS course_d_time,
                IFNULL(ROUND(MIN(CASE WHEN course.name = 'Shoulders Back' THEN run.seconds ELSE NULL END), 2), 'DNF') AS course_e_time,
                IFNULL(ROUND(MIN(CASE WHEN course.name = 'Cracked Fluorescent' THEN run.seconds ELSE NULL END), 2), 'DNF') AS course_f_time,
    
            COALESCE(
                CAST(ROUND(COALESCE(         
                    MIN(CASE WHEN course.name = 'Going Loopy' THEN run.seconds END) +         
                    MIN(CASE WHEN course.name = 'Mum''s Favourite' THEN run.seconds END) +         
                    MIN(CASE WHEN course.name = 'Walnut' THEN run.seconds END) +         
                    MIN(CASE WHEN course.name = 'Hamburger' THEN run.seconds END) +         
                    MIN(CASE WHEN course.name = 'Shoulders Back' THEN run.seconds END) +         
                    MIN(CASE WHEN course.name = 'Cracked Fluorescent' THEN run.seconds END)
                ), 2) AS CHAR),'NQ'
            ) AS overall_time

            FROM 
	            driver
            LEFT JOIN 
	            run ON driver.driver_id = run.dr_id
            LEFT JOIN 
	            course ON run.crs_id = course.course_id
            GROUP BY 
	            driver.driver_id
            ORDER BY 
                CASE WHEN overall_time is NULL THEN 1 ELSE 0 END, overall_time;
        """
    connection.execute(query)
    results = connection.fetchall()

    # Extracting the top 5 drivers and their results
    top5_results = results[:5]  # Taking the first 5 results since they are sorted by overall_time

    bestDriverList = [f"{res[0]} {res[1]} " for res in top5_results]  # names with trailing space
    resultsList = [res[8] for res in top5_results]

    return render_template("top5graph.html", name_list=bestDriverList, value_list=resultsList)

    # Insert code to get top 5 drivers overall, ordered by their final results.
    # Use that to construct 2 lists: bestDriverList containing the names, resultsList containing the final result values
    # Names should include their ID and a trailing space, eg '133 Oliver Ngatai '

@app.route("/juniordriverlist")
def juniordriverlist():
    connection = getCursor()
    query = """
            SELECT
            driver.driver_id, 
            CONCAT(driver.first_name, ' ', driver.surname, IF(driver.age < 25, ' (J)', '')) AS name, 
            driver.date_of_birth, 
            driver.age,
            caregiver.first_name AS caregiver_first_name, 
            caregiver.surname AS caregiver_surname
            FROM driver
            LEFT JOIN driver AS caregiver ON driver.caregiver = caregiver.driver_id
            WHERE driver.age BETWEEN 12 AND 25
            ORDER BY driver.age DESC, driver.surname, driver.first_name;
        """
    connection.execute(query)
    juniordriverlist = connection.fetchall()
    return render_template("junior_driverlist.html", juniordriverlist = juniordriverlist)

@app.route("/driversearch", methods=["GET", "POST"])
def driversearch():
    results = []
    search_term = ""
    errors = []

    if request.method == "POST":
        search_term = request.form.get('search_term')

    connection = getCursor() 
    query = """
            SELECT
                driver.driver_id,
                CONCAT(driver.first_name, ' ', driver.surname, IF(driver.age < 25, ' (J)', '')) AS name, 
                car.model as carModel,
                car.drive_class as driveClass,
                course.name as course_name,
                run.run_num,
                run.wd,
                run.cones,
                run.seconds as runDetail
            FROM driver
            INNER JOIN car ON driver.car = car.car_num
            LEFT JOIN run ON driver.driver_id = run.dr_id
            LEFT JOIN course ON run.crs_id = course.course_id
            WHERE CONCAT(driver.first_name, ' ', driver.surname) LIKE %s
            ORDER BY driver.surname, driver.first_name, run.run_num;
            """
    connection.execute(query, ('%' + search_term + '%',))
    results = connection.fetchall()

    if not results and search_term:
        errors.append(f"No drivers found for the name '{search_term}'.")

    return render_template('driver_search.html', results = results, errors=errors)

@app.route("/editruns", methods=["GET", "POST"])
def editruns():
    connection = getCursor()  

    # Get dr name, course name, run num
    driver_id_names = []
    course_names = []  
    run_nums = []  
    errors = []
    success =[]

    run_details = None
    selected_course = None
    selected_run_num = None
    selected_driver = None
    updated_time = None
    updated_cones = None
    updated_wd = None
    update_result = None

    # Get driver id and name
    connection.execute('SELECT driver_id, CONCAT(first_name, " ", surname) as name FROM driver')
    drivers = connection.fetchall()
    driver_id_names = [(driver[0], driver[1]) for driver in drivers]

    # Get course name 
    connection.execute('SELECT course_id, name FROM course')
    courses = connection.fetchall()
    course_names = [(course[0], course[1]) for course in courses] 

    # Get run number
    connection.execute('SELECT run_num FROM run')
    run_nums = [runnumber[0] for runnumber in connection.fetchall()]


    if request.method == 'POST':
                
        print("Form data:", request.form)

        selected_driver = request.form.get('driver_id_name')
        driver_id, driver_name = selected_driver.split(' - ', 1)
        driver_id = int(driver_id)
        selected_course = request.form.get('course_name')  
        selected_run_num = request.form.get('run_num')  

        print("Selected driver:", selected_driver)

        # Fetch a details
        if selected_driver and selected_course and selected_run_num:
            connection.execute("""
                SELECT run.seconds, run.cones, run.wd
                FROM run 
                INNER JOIN driver ON run.dr_id = driver.driver_id 
                WHERE run.dr_id = %s
                AND CONCAT(driver.first_name, ' ', driver.surname) = %s
                AND run.crs_id = %s
                AND run.run_num = %s
            """, (driver_id, driver_name, selected_course, selected_run_num))
            run_details = connection.fetchone()
        
        if 'update_runs' in request.form:
        # Get updated data
            updated_time = request.form.get('updated_time')
            if updated_time is not None and updated_time.strip() != '':
                try:
                    updated_time = float(updated_time)
                except ValueError:
                    errors.append('Invalid time input. Please enter a valid number.')
            else:
                errors.append('Time input is required')


            updated_cones = request.form.get('updated_cones')
            try:
                updated_cones = int(updated_cones)
                if not (0 <= updated_cones <= 20):
                    errors.append('Please enter a value between 0 and 20 for cones.')
                elif updated_cones == 0:
                    updated_cones = None
            except ValueError:
                errors.append('Invalid cones input. Please enter a value between 0 and 20.')


            updated_wd = 1 if request.form.get('updated_wd') == '1' else 0

            if selected_driver and selected_course and selected_run_num:
            # Use update_run_date function
                update_result = update_run_data(connection, selected_driver, selected_course, selected_run_num, updated_time, updated_cones, updated_wd)

                # Re-fetch the run details after update
                connection.execute("""
                    SELECT run.seconds, run.cones, run.wd
                    FROM run 
                    INNER JOIN driver ON run.dr_id = driver.driver_id 
                    WHERE run.dr_id = %s
                    AND CONCAT(driver.first_name, ' ', driver.surname) = %s
                    AND run.crs_id = %s
                    AND run.run_num = %s
                """, (driver_id, driver_name, selected_course, selected_run_num))
                run_details = connection.fetchone()

            success = "Run details updated successfully"


    return render_template('edit_runs.html',
                           course_names=course_names,
                           driver_id_names=driver_id_names,
                           run_details=run_details,
                           selected_driver=selected_driver,
                           selected_course=selected_course,
                           selected_run_num=selected_run_num,
                           all_run_nums=run_nums,
                           update_result=update_result,
                           errors=errors,
                           success=success,
                           )

def update_run_data(connection, selected_driver, selected_course, selected_run_num, updated_time, updated_cones, updated_wd):
    try:
        driver_id, _ = selected_driver.split(' - ', 1)
        driver_id = int(driver_id)
        update_query = """
            UPDATE run 
            SET seconds = %s, cones = %s, wd = %s 
            WHERE dr_id = %s
            AND crs_id = %s 
            AND run_num = %s
        """
        connection.execute(update_query, (updated_time, updated_cones, updated_wd, driver_id, selected_course, selected_run_num))
        print(f"updated_time: {updated_time}, updated_cones: {updated_cones}, updated_wd: {updated_wd}")
        
        return True  
    except Exception as e:
        print(e)
        return False 

@app.route("/adddrivers", methods=["GET", "POST"])
def adddrivers():
    connection = getCursor()

    errors = []
    course_names = []
    car_data = []
    success= []

    car_num = ""
    car_model = ""
    drive_class = ""
    first_name = ""
    surname = ""
    date_of_birth = ""
    caregiver_id = ""

    # Get course name, id
    connection.execute('SELECT course_id, name FROM course')
    courses = connection.fetchall()
    course_names = [(course[0], course[1]) for course in courses] 

    # Get car table
    connection.execute('SELECT car_num, model, drive_class FROM car')
    car_records = connection.fetchall()
    car_data = [(car[0], car[1], car[2]) for car in car_records]

    # Get caregiver candidates (drivers with age <= 25 and NULL)
    connection.execute('SELECT driver_id, CONCAT(first_name, " ", surname) as name FROM driver WHERE (age <= 25 OR age IS NULL) AND date_of_birth IS NULL')
    caregivers = connection.fetchall()
    caregiver_data = [(caregiver[0], caregiver[1]) for caregiver in caregivers]

    if request.method == "POST":
        first_name = request.form.get('first_name')
        surname = request.form.get('surname')
        selected_car = request.form.get('car_data')
        car_num, car_model, drive_class = selected_car.split(' - ')
        date_of_birth = request.form.get('dob') or None
        is_junior = request.form.get('is_junior') == 'on' 
        caregiver_id = request.form.get('caregiver_id') or None

        # Validation
        if not first_name:
            errors.append("First Name is required.")
        if not surname:
            errors.append("Last Name is required.")
        if not selected_car:
            errors.append("Car Name is required.")

        age = None
        if is_junior:
            if not date_of_birth:
                errors.append("Date of Birth is required for junior drivers.")
            
            else:
                try:
                    dob_date = datetime.strptime(date_of_birth, "%Y-%m-%d").date()
                    today = datetime.now().date()
                    age = today.year - dob_date.year - ((today.month, today.day) < (dob_date.month, dob_date.day))
            
                    # Check if age is within the range for juniors
                    if age < 12 or age > 25:
                        errors.append("Junior drivers must be aged between 12 and 25.")
            
                    # Check for caregiver if junior is 16 or younger
                    if age <= 16:
                        if not caregiver_id:
                            errors.append("Junior drivers who are 16 or younger must select a caregiver.")
                        else:
                            # Ensure the designated caregiver is not a junior
                            caregiver_age_query = "SELECT age FROM driver WHERE driver_id = %s"
                            caregiver_age_result = connection.execute(caregiver_age_query, (caregiver_id,))
                            caregiver_age_record = caregiver_age_result.fetchone()
                            # If the caregiver's age is not NULL, they are considered a junior
                            if caregiver_age_record[0] is not None:
                                errors.append("The designated caregiver cannot be a junior.")

                except Exception as e:
                    errors.append(str(e))
                    print(f"Database error: {e}")
                    
        if not errors:
            try:
                # Check if the car already exists in the car table
                check_car_query = "SELECT car_num FROM car WHERE car_num = %s"
                connection.execute(check_car_query, (car_num,))
                car_exists = connection.fetchone()

                if not car_exists:
                # Car doesn't exist, so insert it into the car table
                    insert_car_query = "INSERT INTO car (car_num, model, drive_class) VALUES (%s, %s, %s)"
                    connection.execute(insert_car_query, (car_num, car_model, drive_class))

                # Insert the driver details into the database
                insert_driver_query = """
                INSERT INTO driver(first_name, surname, car, date_of_birth, age, caregiver)
                VALUES (%s, %s, %s, %s, %s, %s)
                """
                connection.execute(insert_driver_query, (first_name, surname, car_num, date_of_birth, age, caregiver_id))
                driver_id = connection.lastrowid  # Get the ID of the newly inserted driver

                # Now, add 2 empty runs for the new driver, for each course
                for course in courses:
                    course_id, course_name = course
                    for run_num in range(1, 3):  # Only two runs for each course
                        insert_run_query = """
                        INSERT INTO run(dr_id, crs_id, run_num, seconds, cones, wd)
                        VALUES (%s, %s, %s, NULL, NULL, 0)
                        """
                        connection.execute(insert_run_query, (driver_id, course_id, run_num))

                success = "Driver added successfully!"
            except Exception as e:
                errors.append(str(e))
                print(f"Database error: {e}")

    return render_template('add_drivers.html', errors=errors, success=success,
                           car_num=car_num, course_names=course_names,
                            car_data=car_data, car_model=car_model, drive_class=drive_class,
                            caregiver_data=caregiver_data)




