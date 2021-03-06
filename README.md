# Badger Buddy Final Demo
Hello there! It has been a great semester, and thank you so much for your help!

Badger Buddy is a website that gives UW students a platform to communicate with their peers about important issues such as mental health struggles. 

Prior to iteration 3, we accomplished the following features: 
* Account creation and management
* Help Resource and Journal Prompt pages
* Forum board: create posts, reply to individual post, edit and delete posts and replies

During iteration 3, we accomplished the following features:
* Forum board: anonymity option for posts and replies
* Forum board: search posts based on keyword in post title or details
* User dashboard: display post or reply history
* Breathing Exercise
* Custom 404 page
* Major UI improvements

## Setup
1. Download the Final demo release
2. Install and create a virtual environment (commands may vary depend on OS): https://docs.python.org/3/tutorial/venv.html 
3. Open the virtual environment and install following packages:
   * Django: <code>pip install django</code>
   * Django-registration: <code>pip install django-registration</code>
4. Inside the virtual environment, run the server <code>python3 manage.py runserver --insecure</code> if you are using python3; <code>python manage.py runserver --insecure</code> if you are using python. <br/> **Please note that we have changed the command because we have to be out of debug mode in order to display the custom 404 page, and in that case Django won't handle loading the static files (e.g. images) unless the "--insecure" flag is used.**
5. In your browser, redirect to http://localhost:8000/users/login/ to start the adventure!

## Testing
40 Tests have been created (project_directory/discussion_board/test.py) to test implemented features. 
Run tests: <code>python3 manage.py test</code> if you are using python3; <code>python manage.py test</code> if you are using python. 

## Code Coverage
For the code coverage, we used coverage.py, a helper tool for measuring code coverage of Python programs. It allows us to run through tests and present the statement coverage of each individual file we have implemented.
1. Download the package using <code>pip install coverage</code>
2. Run the coverage using <code>coverage run manage.py test discussion_board</code>
3. Display the report using <code>coverage report</code>
4. If you want to see a html version of the report, you can <code>coverage html</code> that generate a folder named htmlcov and go to the index.html inside the folder. **We have the htmlcov folder included in the parent directory if you have any trouble installing the coverage package**  

![code_coverage](/readme_images/iteration_3_code_coverage.png)

## URLs
* Login: http://localhost:8000/users/login/
* Register: http://localhost:8000/users/register/
* Forget Password: http://localhost:8000/users/password_reset/
* Post Dashboard (logged in required): http://localhost:8000/board/
* Create Post (logged in required): http://localhost:8000/board/create-post/
* Emergency help page (logged in required): http://localhost:8000/help/
* Mindfulness exercise page (logged in required): http://localhost:8000/exercises/


## Walkthrough
### Please note that the UI of this release are different than examples shown below, but the features are identical. 

### Register an account
Go to the register page: http://localhost:8000/users/register/
Type in the username, email and password you desired. Restrictions are as follows: 
* Username (Required): 50 characters or fewer. Letters, digits and @/./+/-/_ only.
* Email (Required): Email format, **restrict to wisc email**
* User type (Required): Type of the account, could be either Student or Overseer, user type makes no difference for now.   
* Anonymity (Required): Whether your first and last name will be shown to public in your posts
* First and Last name (Required): 3-15 characters. Letters only.
* Password (Required):
  * **Compared to four restrictions before, now we only have one for easier user inputs.**
  * Your password must contain at least 8 characters.

In our walkthrough, we will set our username as "badgerbuddy", email as "badger.buddy@wisc.edu", password as "iteration", and the rest of information as shown in the picture below.

![iteration_2_register](/readme_images/iteration_2_register.png)

![iteration_2_register_2](/readme_images/iteration_2_register_2.png)

### Verification Email
We added an additional step for registration in this iteration so your account is currently in the database yet not active. A success page will show up and remind you to check your email inbox for the verification email. 

![iteration_2_register_complete](/readme_images/iteration_2_complete.png)

In this iteration, we will "send" the email within our project folder, so go to "project_directory/discussion_board/sent_emails", and this should generate a log file containing the email template, format like below: 

> Content-Type: text/plain; charset="utf-8"\
> MIME-Version: 1.0\
> Content-Transfer-Encoding: 7bit\
> Subject: localhost:8000 - Please activate your account\
> From: webmaster@localhost\
> To: badger.buddy@wisc.edu\
> Date: Fri, 09 Apr 2021 07:16:25 -0000\
> Message-ID: <161795258588.28232.7450407282895504597@LAPTOP-N3QN2KP3>

> Dear Mr/Ms. Buddy

> Welcome to BadgerBuddy! Here is your activate link for registration:\
> http://localhost:8000/users/activate/ImJhZGdlcmJ1ZGR5Ig:1lUlNR:3Rb4oHzaCTXAlZFK0XS-ugIPZ4HkzARB55J2fXRkYi8

> Please note that this page will expire in 1 day.
> If you didn't register the account, please inform us by badger@buddy.com. Thank you for you cooperation!
-------------------------------------------------------------------------------

Copy the url in the browser and go to the page. Now your account is activated and you can login now! 
Please note that the url from the example above may not be valid in your attempt, you should use the link from the log file generated in your system.

![iteration_1_login](/readme_images/iteration_1_login.png)

### User Dashboard and Edit Profile

If you click on the "User Dashboard" tab on the navigation bar, you will be at the user dashboard page. You can change your user information (username, first and last name and anoynmity) by clicking the "Edit Profile" button. Feel free to change whatever you prefer, yet in this walkthrough we will keep everything the same.

![iteration_2_user_dashboard](/readme_images/iteration_2_user_dashboard.png)

![iteration_2_edit_profile](/readme_images/iteration_2_edit_profile.png)

### Post Dashboard and Create Post

Click on the logo or "Post Dashboard" on the navigation bar will redirect you to the post dashboard. As you can see, we have created four posts for testing purposes, and posts are ordered from the latest to the oldest. Click on the "Create Post" button to create another one.


![iteration_2_board](/readme_images/iteration_2_board.png)

This will lead you to the create post page. In our example: we will enter "Hello World" in the title field, and "Goodnight World" in the detail field. Click on "Create Post" to create the post.

![iteration_2_post_create](/readme_images/iteration_2_post_create.png)

You will see your post at the top now!

![iteration_2_board_2](/readme_images/iteration_2_board_2.png)
**Please note that on the front page you will not able to see the content anymore.**

### View individual posts
When you click on your post, you will be able to see your post content "Goodnight World". If someone replied your post, you will see the reply content at below. 

![iteration_2_board_3](/readme_images/iteration_2_board_3.png)

### Edit and delete post
Now you can edit or delete your post by clicking the corresponding button. Feel free to change it according to your preferences, yet in this walkthrough we will not edit or delete it. 

![iteration_2_post_edit](/readme_images/iteration_2_edit_post.png)

![iteration_2_post_delete](/readme_images/iteration_2_post_delete.png)

### Reply to the post

Great, we will now try to reply on one of the posts. Click on the last post, and click on the "Create Reply" button.
We can enter what we want to say, such as "I believe you, you can get through it!", and click the button.

![iteration_1_reply](/readme_images/iteration_1_reply.png)

Scroll down to the buttom, and you can see the post with your reply now.

![iteration_2_board_4](/readme_images/iteration_2_board_4.png)

### Edit and delete reply
Click on the reply box. Now you can edit or delete your reply by clicking the corresponding button. Again, please feel free to change it according to your preferences. 

![iteration_2_reply_edit](/readme_images/iteration_2_edit_reply.png)

![iteration_2_reply_delete](/readme_images/iteration_2_reply_delete.png)

### Resource and Help Page

On the navigation bar at the top, click on the "Resource" to Emergency help page. The page lists contact information that user can get direct mental help from. 

![iteration_2_help](/readme_images/iteration_2_help.png)

### Mindfulness Exercise Page

On the navigation bar at the top, click on the "Mindfulness Exercise" to exercise page. The page will show a random Inspirational Quote (on the left) and Journal Entry (on the right). New messages will show up when you refresh the page. 

![iteration_2_exercise](/readme_images/iteration_2_exercise.png)

### Logout and Reset Password

On the navigation bar at the top, click on the "Log Out" to logout

![iteration_1_logout](/readme_images/iteration_1_logout.png)

Oh no! We forgot what our password was! No worry, we can reset them. Go to the login page and click on the "Forgot Password?" link at the buttom. 

Then enter our email: "badger@buddy.com". If the input email is not found in the database, you will receive an alert message that tells you the email is not registered.

![iteration_1_reset_password_1](/readme_images/iteration_1_reset_password_1.png)

A page will show up saying that an verfication email has been sent. 

![iteration_1_reset_password_2](/readme_images/iteration_1_reset_password_2.png)

In this iteration, we will "send" the email within our project folder, so go to "project_directory/discussion_board/sent_emails", and this should generate a log file containing the email template, like below: 

> Content-Type: text/plain; charset="utf-8"\
> MIME-Version: 1.0\
> Content-Transfer-Encoding: 7bit\
> Subject: Password reset on localhost:8000\
> From: webmaster@localhost\
> To: badger.buddy@wisc.com\
> Date: Fri, 26 Mar 2021 02:33:32 -0000\
> Message-ID: not-shown-in-this-walkthrough\
> \
> You recently requested to reset your password for your badger buddy account: badger@buddy.com. \
> Please follow the link below to reset:\
> http://localhost:8000/users/reset/NQ/ak357w-eb34d8313b65bbd891b49ad937b15b4d/
-------------------------------------------------------------------------------

Copy the url in the browser and go to that page. You can enter your new password now. The restrictions are the same as in registration process. In our walkthrough, let us enter "iteration1" as the new password.

![iteration_1_reset_password_3](/readme_images/iteration_1_reset_password_3.png)

Here we go! You can feel free to login again using username: "badgerbuddy" and the new password: "iteration1", and the old password "iteration" will not work anymore.

![iteration_1_reset_password_4](/readme_images/iteration_1_reset_password_4.png)

### Anonymity, Search Function, etc.
Please note that features implemented in iteration 3 are not included in this walkthrough. Please feel free to test those features!

**Congratulations :tada: you have finished the walkthrough! Thanks for spending the time to read this document, we really appreciate it!**
