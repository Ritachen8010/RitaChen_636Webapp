# RitaChen_636

COMP636 Assignment 4 & 5

Student Name:Yingyue(Rita) Chen

Student ID: 1126418


Web application structure:

1. "/" 
    - Function home() is def as HomePage， and renders the template name 'base.html'. The Homepage is a public interface. 
    - 'base.html' contains basic navigation to link to the different functions. 

2. "/admin" 
    - Function admin_home() is def as admin interface, and renders the the template name 'admin.html'.
    - 'admin.html' contains basic navigation to link to the different functions.

3. "/listcourses"
    - Fucntion Listcourses() fetches a list of courses from the database and render the template name 'course_list.html' with the fetched list. 
    - Data Passed: 
        - Course_list: A list of courses from the database.
        - Parent Template: base.html
        - The course_list.html template extend base.html, which likely contains common layout elments (navigate). 
    - Relation:
        - When a user request to the /listcourse:
            - The listcourse() function is exectued.
            - Fetched list is passed to the course_list.html templates as course_list.
            - The course_list.html template extends base.html, adding  content (course, name, Mpa diagram) to display the list of course in a table format. 

4. "/driverdetails"
    - Methods: 'Get', 'POST'
    - Function driverdetails(), on 'GET' request, fetches and displays a driver list; on 'POST' request, feches and display detailed information about a specific driver details (runs and courses).
    - Data Passed:
        - driver_names: A list of driver names.
        - driver_name: Selected driver (POST request).
        - driver: Details of the selected driver, SQL exectute associated infomration and store query to driver (POST request).
        - runs: A list of run related to the selected driver (POST request).
        - Parent Template: base.html
    - Relation:
        - When a user accesses "/driverdetails" :
            - The server receives a 'GET' requrest (driverdetails() function responds to this GET) and passed to the 'Selected_driver_run_details.html'.
            - After the user selects a driver from the dropdown and sumit to the server, the form sends the selected dirver's name back to the server usring the 'POST' method.
            - Function "/driverdetails" captures this 'POST' request, fetches a detailed information from the databased based on submit driver's name.

5. 


Assumptions and design decisions:






Database questions: Refer to the supplied motorkhana_local.sql file to answer the following questions:
o What SQL statement creates the car table and defines its three fields/columns? (Copy and paste the relevant lines of SQL.)
o Which line of SQL code sets up the relationship between the car and driver tables?
o Which 3 lines of SQL code insert the Mini and GR Yaris details into the car table?
o Suppose the club wanted to set a default value of ‘RWD’ for the driver_class field. What specific change would you need to make to the SQL to do this? (Do not implement this change in your app.)
o Suppose logins were implemented. Why is it important for drivers and the club admin to access different routes? As part of your answer, give two specific examples of problems that could occur if all of the web app facilities were available to everyone.



- Image sources: vec, Y. (n.d). ***Racing flag icon vector . Checkered flag icon . Finishing Flags Pro Vector.*** https://www.vecteezy.com/vector-art/27881009-racing-flag-icon-vector-checkered-flag-icon-finishing-flags
