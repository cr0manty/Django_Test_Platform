# Test Platform

#### Platform for passing / creating tests

1. user registration / authorization
2. The possibility of authorization through the social network.
3. add a personal account - add a profile photo, name, surname, 
date of birth, information about yourself
4. the user can create his own test (at least 5 questions,
 4 answers for each question, one correct; test name, description, number for search)
5. create a page with a view of all tests, filter 
by name, sort by access
6. page for a detailed presentation of the test - 
name, description, comments, button "pass the test"
* if the test is passed, show the test result 
(number of correct answers and result in %)
Passing the test can be done separately.
7. tests can be commented
8. create fixture or migration
9. configure django admin panel for viewing users,
 in a detailed display of the user inlines display test results.
 
#### Rest Framework
 ##### GET
 * `/api/users/` - all users info
 * `/api/users/cr0manty/` - one user info
 * `/api/users/cr0manty/comments/` - user comments
 * `/api/users/cr0manty/tests/created/` - user created tests
 * `/api/users/cr0manty/tests/pass` - user passed tests
 * `/api/tests/` - all tests
