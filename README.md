# RitaChen_636
- COMP636 Assignment 4 & 5
- Student Name:Yingyue(Rita) Chen
- Student ID: 1126418

- Web application structure:
1. "/" 
    - Function home() is def as HomePage， and renders the template name 'base.html'. The Homepage is a public interface. 
    - 'base.html' contains basic navigation to link to the different functions. 
2. "/admin" 
    - Function admin_home() is def as admin interface, and renders the the template name 'admin.html'.
    - 'admin.html' contains basic navigation to link to the different functions.
3. "/listcourses"
    - Fucntion Listcourses() fetches a list of courses from the database and render the template name 'course_list.html' with the fetched list. 
        - Course_list: A list of courses from the database. 
4. "/driverdetails"
    - Methods: 'Get', 'POST'
    - Function driverdetails(), on 'GET' request, fetches and displays a driver list; on 'POST' request, feches and display detailed information about a specific driver details (runs and courses). Sperate table for display two details part.
        - driver_names: A list of driver names.
        - driver_name: Selected driver (POST request).
        - driver: Details of the selected driver, SQL exectute associated infomration and store query to driver (POST request).
        - runs: A list of run related to the selected driver (POST request).
        - When a user accesses "/driverdetails" :
            - The server receives a 'GET' requrest (driverdetails() function responds to this GET) and passed to the 'Selected_driver_run_details.html'.
            - After the user selects a driver from the dropdown and sumit to the server, the form sends the selected dirver's name back to the server usring the 'POST' method.
            - Function "/driverdetails" captures this 'POST' request, fetches a detailed information from the databased based on submit driver's name.
5. "/driverdetails_by_click_name/<string:driver_name>"
    - Function driverdetails_by_click_name(driver_name), fetches detailed information same with "/driverdetails", to click specific driver based on the driver_name (URL). If the driver exists in the database, the function also fetches the list of runs that related to the driver. Sperate table for display two details part.
        - driver: Detaials of the driver based on the provided driver_name(URL).
        - runs: A list of run related to the specificed driver.
        - When a user click driver name:
            - It capture by the <string:driver_name> passed to the 'driverdetails_by_click_name(driver_name)'.
            - 'driverdetails_by_click_name(driver_name)' function uses the provided 'driver_name' to fetch details of the specific driver from the database. 
            - The fethed driver details and runs are then passed to the 'driverdetails_by_click_name.html' template for rendering.
6. "/overallresult"
    - Exectues a SQL query to fetch overall results for each driver in differnet courses. Based on the ranking of the overall result then assigned awards to the top drivers. The result then passed to the template 'overall_result.html' for display.
        - overall_result: A list of driver best results (min time) in 6 courses, where each driver contains details of driver ID, driver Name, Car Model, and overall result, then store the data to the results_with_awards to calucate the award. Renders back to the 'overall_result.html'. 
        - A user accesses the '/overallresult':
            - The overallresult() function runs the SQL query to the the overall results of each driver.
            - The function processed the reults to assign awards based on the min time in best 6 courses. 
            - The processed results are then passed to the 'overall_result.html' template.
7. "/graph"
    - Use the same SQL query as overallresult to fetch overall results for each driver in different courses. Processes the results to pick the top 5 drivers based on the overall result, then passed to the template 'top5graph.html' for display. 
        - bestDriverList: Top 5 driver names.
        - resultsList: Overall result for the top 5 drivers.
8. "/juniordriverlist"
    - Exectutes a SQL query to fetch details of junior divers aged between 12 and 25. The data include the driver ID, name, date of birth, age and the name of the caregiver, then passed to the template 'junior_driverlist.html' for display. 
        - juniordriverlist: Details of each junior driver where the age between 12-25, Diver ID, name, date of birth, age, and caregiver.
        - The template uses the passed data 'juniordriverlist' to render a table displaying details of eahc junior driver. For each driver shows their ID, name, DOB, age and Caregiver (if 'N/A' no caregiver). 
9. "/driversearch"
    - Methods: 'Get', 'POST'
    - On a 'Get' request, the page allows the user to input a search term to find driver details. On a 'POST' request, it fetched driver details to match with the search term from the database and a table is rendered displaying. The error displayed that if no driver's name matches the search term.
    - The relationship is inputting a search term, extracting matching driver details, passing them to the 'driver_search.html' and displaying the result.
10. "/editruns"
    - Methods: 'Get', 'POST'
    - I have set up the edit runs in 2 steps to get the runs edit.
        - On a 'GET' request, the user allow to select a driver ID - name, course name and run number to fetch details of a specific run.
        - On a 'POST' request, it fetches the selected driver detials and run details from the database and provides: Time, Cones, and WD of that run to edit. 
    - Multiple SQL queries are used to fetch:
        - List of driver and ID, courses, run numbers, and details of runs. 
    - I have also set a function for update_run_date that receives and interacts with the database to perform the update. 
    - The fetched run details are passed to the 'edit_runs.html' template. Error or success messages are also passed to the template based on the result of the update operation. 
11. "/adddrivers"
    - Methods: 'Get', 'POST'
    - On a 'GET' request, it fetches all course names, and IDs from the course table; car data (car number, model, and driver class) from the car table; all potential caregivers from the driver table (potential caregivers are those who have NULL age). It then renders to the 'add_drivers.html' template, and recognize the condition of success and error.
    - On a 'POST' request, it retrieves the form data provided by the user, and checks the first name, surname, and car info are provided. 
        - If the driver is junior (ages 12-25), it is forced to provide a date of birth otherwise going error message. 
        - If the Junior driver is 16 or younger, it ensures a caregiver is selected otherwise an error message appears.
    - If successful it adds 12 runs empty runs for the driver and updates to SQL as well. 
    - If an error should be sent an error to the user and refresh to the web. 

-   Assumptions and design decisions:
    -   Assumptions:
        1. The Caregiver can only selected with NULL BOD and Age.
        2. NULL BOD and Age are define as a adult.
        3. Overall result gives the best time in each course and plus 6 courses best time = overall result.
        4. Not sure about the Driver's Run Details what should be displayed on the table, therefore I assume to just display everything except the Course ID letter.  

    -   Design decision:
        1. Templating consistency: As the requirement is to develop two different interfaces, therefore base.html and admin.html are the main templates for the rest of the functional page. eg: Public templates only extend base.html, and Admin templates only extend admin.html, which simply creates consistent navigation for and information to each page. 
        2. Edit Runs: I was thinking of putting in one route and one template, therefore in order to achieve this I designed two steps, one is for fetching driver details based on Driver ID, Name, Course Name and Run Number then based on the previous fetch to get the details of the specific runs to edit the run. The reason for using 'POST' is because it is designed for submitting data to the server, leading to a change in server state. 
        3. Add Drivers: I have not figured out why should set up many templates...？ My first thought of this one is to give more restrictions to the user, eg: if the user ticks the junior should show the BOD and if BOD is less than 16 give caregiver selection. However, to achieve this it may require a Javascript for help...Therefore, what I was doing was to give all selections for the user, and make restrict for them. eg, If the user ticks Junior but does not fill in the BOD it gives you an error message, but it will come a bit repeat what the user did before because when fill the wrong message it refresh the web and need to re-fill the information again. 
        4. Driver Search: I have designed to show a whole driver rather than only show the search bar, therefore when the user enters the search it gives a bit idea of search interface would look like and how it works. 
        5. Driver Run Details: I have designed to show a table for driver details then run details, two separate tables make more easier to read.

-   Database questions: Refer to the supplied motorkhana_local.sql file to answer the following questions:
    -   What SQL statement creates the car table and defines its three fields/columns? (Copy and paste the relevant lines of SQL.)
        -   (
            car_num INT PRIMARY KEY NOT NULL,
            model VARCHAR(20) NOT NULL,
            drive_class VARCHAR(3) NOT NULL
            );
    -   Which line of SQL code sets up the relationship between the car and driver tables?
        -   FOREIGN KEY (car) REFERENCES car(car_num)
    -   Which 3 lines of SQL code insert the Mini and GR Yaris details into the car table?
        -   INSERT INTO car VALUES
            (11,'Mini','FWD'),
            (17,'GR Yaris','4WD'),
    -   Suppose the club wanted to set a default value of ‘RWD’ for the driver_class field. What specific change would you need to make to the SQL to do this? (Do not implement this change in your app.)
        -   drive_class VARCHAR(3) NOT NULL DEFAULT 'RWD'
    -    Suppose logins were implemented. Why is it important for drivers and the club admin to access different routes? As part of your answer, give two specific examples of problems that could occur if all of the web app facilities were available to everyone.
        -   I think that is because: 
            1. Interface Clear: If only one route, it will confuse the public user and admin when they access the web. 
            2. Data Protection and Privacy: The admin route might be exposed to the public and the driver has the right to access and make changes to the data (delete or add the data).
            3. Easy to maintain in the future if separated into two routes. 
            
- Image sources: 
Vec, Y. (n.d). ***Racing flag icon vector . Checkered flag icon . Finishing Flags Pro Vector.*** https://www.vecteezy.com/vector-art/27881009-racing-flag-icon-vector-checkered-flag-icon-finishing-flags
