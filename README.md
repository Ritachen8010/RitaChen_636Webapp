# RitaChen_636
- COMP636 Assignment 4 & 5
- Student Name:Yingyue(Rita) Chen
- Student ID: 1126418
Web application structure:
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
    - On a 'Get' request, the page allows user to input a search term to find driver details. On a 'POST' request, it fetched divrer details to match with search term from the database, and a tbale is rendered displaying. Error for dislayed that if no drivers name match the search term.
    - The relationship is inputting a search term, extracting matching driver details, passing them to the 'driver_search.html' and displaying the result.

10. "/editruns"
    - 
11. 



Assumptions and design decisions:






Database questions: Refer to the supplied motorkhana_local.sql file to answer the following questions:
o What SQL statement creates the car table and defines its three fields/columns? (Copy and paste the relevant lines of SQL.)
o Which line of SQL code sets up the relationship between the car and driver tables?
o Which 3 lines of SQL code insert the Mini and GR Yaris details into the car table?
o Suppose the club wanted to set a default value of ‘RWD’ for the driver_class field. What specific change would you need to make to the SQL to do this? (Do not implement this change in your app.)
o Suppose logins were implemented. Why is it important for drivers and the club admin to access different routes? As part of your answer, give two specific examples of problems that could occur if all of the web app facilities were available to everyone.



- Image sources: 
vec, Y. (n.d). ***Racing flag icon vector . Checkered flag icon . Finishing Flags Pro Vector.*** https://www.vecteezy.com/vector-art/27881009-racing-flag-icon-vector-checkered-flag-icon-finishing-flags
