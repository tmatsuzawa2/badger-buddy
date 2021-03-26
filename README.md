# Badger Buddy Iteration 1
Hi Siyang! Thanks for reviewing our project!

In this iteration, we have accomplished the following features: 
* Account creation, user authentication, and password reset
* Post dashboard, post creation, post replies and anonymous setting
* Navigation header and footer
* Emergency help page

## Setup
1. Download the source code iteration 1 branch from https://github.com/BadgerBuddy/badger-buddy/releases/tag/v1.0
2. Install and create a virtual environment (commands may vary depend on OS): https://docs.python.org/3/tutorial/venv.html 
3. Open the virtual environment and install following packages:
   * Django: <code>pip install django</code>
   * Django-registration: <code>pip install django-registration</code>
4. Inside the virtual environment, go to the project directory and run the surver <code>python3 manage.py runserver</code> if you are using python3; <code>python manage.py runserver</code> if you are using python.
5. In your browser, redirect to http://localhost:8000/users/login/ to start the adventure!

## Testing
18 Tests have been created (project_directory/discussion_board/test.py) to test implemented features. 
Run tests: <code>python3 manage.py test</code> if you are using python3; <code>python manage.py test</code> if you are using python. 

## URLs
Since we haven't made a 404 page for now, any wrong urls will direct to an error message.
* Login: http://localhost:8000/users/login/
* Register: http://localhost:8000/users/register/
* Forget Password: http://localhost:8000/users/password_reset/
* Post Dashboard (logged in required): http://localhost:8000/board/
* Create Post (logged in required): http://localhost:8000/board/create-post/
* Reply Post (logged in required): Click on the post to reply
* Emergency help page: http://localhost:8000/help/

## Walkthrough
### Register an account
Go to the register page: http://localhost:8000/users/register/
Type in the username, email and password you desired. Restrictions are as follows **(Note: if your input does not meet any of the restrictions, only one type of error message will be shown: "Your username or password didn't match. Please try again." We will need to change that in the future)**:
* Username (Required): 50 characters or fewer. Letters, digits and @/./+/-/_ only.
* Email (Required): Email format, (will restrict to wisc email in later iteration)
* Password (Required):
  * Your password can’t be too similar to your username or email.
  * Your password must contain at least 8 characters.
  * Your password can’t be a commonly used password (e.g. 123).
  * Your password can’t be entirely numeric.


In our walkthrough, we will set our username as "badgerbuddy", email as "badger@buddy.com", and password as "iteration".


![iteration_1_register](/readme_images/iteration_1_register.png)


The success page will show up and display the username, email, anonymity (set to True as default) and user role (set to Student as default). We will add anonymity and user_role fields into register page in future implementation.

![iteration_1_register_complete](/readme_images/iteration_1_register_complete.png)

### Post Dashboard and Create Post

Click on the button will redirect you to the post dashboard. As you can see, we have created four posts for testing purposes, and posts are ordered from the latest to the oldest. Click on the "Create Post" button to create another one.

![iteration_1_board](/readme_images/iteration_1_board.png)

This will lead you to the create post page. In our example: we will enter "Hello World" in the title field, and "Goodnight World" in the detail field. Note that tags and anonymity doesn't do anything. Click on "Create Post" to create the post.

![iteration_1_post_create](/readme_images/iteration_1_post_create.png)

You will see your post at the top now!

![iteration_1_board_2](/readme_images/iteration_1_board_2.png)

### Reply to the post

Great, we will now try to reply on one of the posts. Click on the last post.\
We can enter what we want to say, such as "I believe you, you can get through it!", and click the button.

![iteration_1_reply](/readme_images/iteration_1_reply.png)

Scroll down to the buttom, and you can see the post with your reply now. Remember the user was set to Anonymous as default? The comment you posted will not reveal your username.

![iteration_1_board_3](/readme_images/iteration_1_board_3.png)

### Resource and Help Page

On the navigation bar at the top, click on the "Resource" to Emergency help page. The page lists contact information that user can get direct mental help from. 

![iteration_1_help](/readme_images/iteration_1_help.png)

### Logout and Reset Password

On the navigation bar at the top, click on the "Log Out" to logout

![iteration_1_logout](/readme_images/iteration_1_logout.png)

Oh no! We forgot what our password was! No worry, we can reset them. Go to the login page and click on the "Forgot Password?" link at the buttom. 

Then enter our email: "badger@buddy.com". If the input email is not found in the database, you will receive an alert message that tells you the email is not registered.

![iteration_1_reset_password_1](/readme_images/iteration_1_reset_password_1.png)

A page will show up saying that an verfication email has been sent. 

![iteration_1_reset_password_2](/readme_images/iteration_1_reset_password_2.png)

In iteration 1, we will "send" the email within our project folder, so go to **"project_directory/discussion_board/sent_emails"**, a log file with the hashed link will be generated, such as the below example: 

> Content-Type: text/plain; charset="utf-8"\
> MIME-Version: 1.0\
> Content-Transfer-Encoding: 7bit\
> Subject: Password reset on localhost:8000\
> From: webmaster@localhost\
> To: badger@buddy.com\
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

Congradulation :tada: you have finished the walkthrough in iteration 1! Thanks for spending the time reading this document, I really appreciate it!
