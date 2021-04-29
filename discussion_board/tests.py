from django.test import TestCase

# Create your tests here.
from django.contrib import auth
from django.test import TestCase
from django.utils import timezone
from .discussion_board.forms import CreatePostForm, CreateReplyForm
from .models import Post, Reply, Meeting, MeetingUsers, Profile, Quotes, Prompts
from django.contrib.auth.models import User as User


class ModelTests(TestCase):
    def setUp(self):
        user = User.objects.create(username="jthal", email="jthalacker7@gmail.com",
                                   first_name="jake", last_name="thalacker")
        user2 = User.objects.create(username="jthal7",
                                    email="jakethalacker7@gmail.com",
                                    first_name="jake", last_name="thalacker")

        user.set_password('badgerbuddy123')
        user2.set_password('badgerBuddy')
        Post.objects.create(title="Mental Help",
                            details= "I am wondering if anyone else is lonely right now",
                            create_date=timezone.now(),
                            user=User.objects.get(username="jthal"))
        Post.objects.create(title="Mental Help 2",
                            details="I recieved help from jthals post",
                            create_date=timezone.now(),
                            user=User.objects.get(username="jthal7"))
        response = self.client.post('/users/login/', {'username': 'jthal7', 'password': 'badgerBuddy'}, follow=True)
        Reply.objects.create(post=Post.objects.get(title="Mental Help 2"),
                             details="I would love to help.",
                             create_date=timezone.now(),
                             user=User.objects.get(username="jthal"))
        Meeting.objects.create(link="https://www.zoom.us/",
                               date_time=timezone.now(),
                               post=Post.objects.get(title="Mental Help 2"))
        MeetingUsers.objects.create(meeting=Meeting.objects.get(post=Post.objects.get(title="Mental Help 2")),
                                    user=User.objects.get(username="jthal7"))
        Quotes.objects.create(text="JAKE IS COOL", author="Yashash")
        Prompts.objects.create(text="Is Jake cool? (only answer is yes)")

    def test_User_objects(self):
        user = User.objects.get(username="jthal")
        user2 = User.objects.get(username="jthal7")
        self.assertEqual(user.first_name, 'jake')
        self.assertEqual(user2.first_name, 'jake')
        self.assertEqual(user.email, 'jthalacker7@gmail.com')
        self.assertEqual(user2.email, 'jakethalacker7@gmail.com')

    def test_Post_objects(self):
        user = User.objects.get(username="jthal")
        user2 = User.objects.get(username="jthal7")
        post = Post.objects.get(user=user)
        post2 = Post.objects.get(user=user2)
        self.assertEqual(post.title, "Mental Help")
        self.assertNotEqual(post2.title, "Mental Help")
        self.assertEqual(post.user.email, 'jthalacker7@gmail.com')
        self.assertEqual(post2.user.email, 'jakethalacker7@gmail.com')

    def test_change_post_title(self):
        user = User.objects.get(username="jthal")
        post = Post.objects.get(user=user)
        post.title = "Changing title"
        self.assertEqual(post.title, "Changing title")
        self.assertNotEqual(post.title, "Mental Help")

    def test_meeting_users(self):
        meeting_val = Meeting.objects.get(post=Post.objects.get(title="Mental Help 2"))
        user = MeetingUsers.objects.get(meeting=meeting_val).user
        self.assertEqual(user.username, "jthal7")

        MeetingUsers.objects.create(meeting=Meeting.objects.get(post=Post.objects.get(title="Mental Help 2")),
                                    user=User.objects.get(username="jthal"))
        meeting_val = Meeting.objects.get(post=Post.objects.get(title="Mental Help 2"))
        meeting_users_qs = MeetingUsers.objects.filter(meeting=meeting_val)
        for user in meeting_users_qs:
            test_user = User.objects.get(username=user.user.username)
            self.assertEqual(user.user.username, test_user.username)


class PostTests(TestCase):
    def setUp(self):
        user = User.objects.create(username="jthal", email="jthalacker7@gmail.com",
                                   first_name="jake", last_name="thalacker")
        user2 = User.objects.create(username="jthal7",
                                    email="jakethalacker7@gmail.com",
                                    first_name="jake", last_name="thalacker")

        user.set_password('badgerbuddy123')
        user2.set_password('badgerBuddy')
        Post.objects.create(title="Mental Help 2",
                            details="I recieved help from jthals post",
                            create_date=timezone.now(),
                            user=User.objects.get(username="jthal7"))

        self.user = User.objects.create_superuser(username="testUser", password="TestUserPass",
                                                  email="testUser@example.com")
        self.user2 = User.objects.get(username="jthal")
        self.client.force_login(self.user)

    def test_form_valid(self):
        form_data = {'title': 'Lonely', 'details': 'I am lonely'}
        form = CreatePostForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_not_empty(self):
        response = self.client.post("/board/create-post", {'title': 'something'})
        self.assertFormError(response, 'form', 'details', 'This field is required.')

    def test_post_created(self):
        response = self.client.post("/board/create-post", {'title': 'something', 'details': 'something 2'})

        post = Post.objects.get(title='something')
        self.assertEqual(post.details, 'something 2')

    def test_post_user(self):
        response = self.client.post("/board/create-post", {'title': 'something', 'details': 'something 2'})
        post = Post.objects.get(title='something')
        self.assertEqual(post.user, self.user)

    def test_post_edited(self):
        response1 = self.client.post("/board/create-post", {'title': 'something 1', 'details': 'details 1'})
        response2 = self.client.post("/board/create-post", {'title': 'something 2', 'details': 'details 2'})
        
        # Test if post is successfully edited
        edit1 = self.client.post("/board/edit-post/2", {'title': 'changed title', 'details': 'changed details'})
        post1 = Post.objects.get(title='changed title')
        self.assertEqual(post1.details, 'changed details')

        # Test if post is unable to be edited by non-owner
        self.client.logout()
        self.client.force_login(self.user2)
        edit1 = self.client.post("/board/edit-post/3", {'title': 'changed title 2', 'details': 'changed details 2'})
        try: 
            post2 = Post.objects.get(title='changed title 2')
            self.fail()
        except Post.DoesNotExist:
            post2 = Post.objects.get(title='something 2')
            self.client.logout()
            self.client.force_login(self.user)
            self.assertEqual(post2.user, self.user)

    def test_view_post(self):
        # Login
        self.client.force_login(self.user2)
        # Create post and go to post history page
        response = self.client.post("/board/create-post", {'title': 'sometitle', 'details': 'somedetails'})
        response = self.client.get("/profile/post_history/")
        # Check if the html response contains the post
        self.assertTrue("sometitle" in response.content.decode("utf-8"))

    def test_anonymous_own_post(self):
        # Create reply
        response = self.client.post("/board/create-post", {'title': 'sometitle', 'details': 'somedetails', 'anonymous': 'True'})
        # View the post
        response = self.client.get("/board/view-post/2")
        # Check if the name is hidden
        self.assertTrue("Anonymous to other students" in response.content.decode("utf-8"))

    def test_anonymous_post(self):
        self.client.logout()
        self.client.force_login(self.user2)
        # Create reply
        response = self.client.post("/board/create-post", {'title': 'sometitle', 'details': 'somedetails', 'anonymous': 'True'})
        # View the post
        response = self.client.get("/board/view-post/2")
        # Check if the name is hidden
        self.assertTrue("Anonymous" in response.content.decode("utf-8"))

    def test_post_deleted(self):
        response1 = self.client.post("/board/create-post", {'title': 'something 1', 'details': 'details 1'})
        response2 = self.client.post("/board/create-post", {'title': 'something 2', 'details': 'details 2'})

        # Test if post is successfully deleted
        delete = self.client.delete("/board/delete-post/2")
        try:
            post1 = Post.objects.get(title='something 1')
            self.fail()
        except Post.DoesNotExist:
            pass

        # Log second user in
        self.client.logout()
        self.client.force_login(self.user2)
        # Test if post not deleted by user that does not own post
        delete = self.client.delete("/board/delete-post/3")
        try:
            post2 = Post.objects.get(title='something 2')
            self.assertEqual(post2.details, 'details 2')
        except Post.DoesNotExist:
            self.fail()

    def test_not_logged_in(self):
        self.client.logout()
        try:
            response = self.client.post("/board/create-post", {'title': 'something', 'details': 'something 2'})
            post = Post.objects.get(title='something')
            self.fail()
        except ValueError:
            pass


class ReplyTests(TestCase):
    def setUp(self):
        user = User.objects.create(username="jthal", email="jthalacker7@gmail.com",
                                   first_name="jake", last_name="thalacker")
        user2 = User.objects.create(username="jthal7",
                                    email="jakethalacker7@gmail.com",
                                    first_name="jake", last_name="thalacker")

        user.set_password('badgerbuddy123')
        user2.set_password('badgerBuddy')
        Post.objects.create(title="Mental Help 2",
                            details="I recieved help from jthals post",
                            create_date=timezone.now(),
                            user=User.objects.get(username="jthal7"))
        Post.objects.create(title="Mental Help 3",
                            details="I recieved help from jthals post",
                            create_date=timezone.now(),
                            user=User.objects.get(username="jthal7"))

        self.user = User.objects.get(username="jthal7")
        self.user2 = User.objects.get(username="jthal")
        self.client.force_login(self.user)

    def test_reply_form_valid(self):
        form_data = {'details': 'I am lonely'}
        form = CreateReplyForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_reply_form_not_empty(self):
        response = self.client.post("/board/create-reply/1", {'details': ''})
        self.assertFormError(response, 'form', 'details', 'This field is required.')

    def test_reply_edited(self):
        # Test if reply is successfully edited
        response1 = self.client.post("/board/create-post", {'title': 'something', 'details': 'something 2'})
        response2 = self.client.post("/board/create-post", {'title': 'something 2', 'details': 'second test'})
        reply1 = self.client.post("/board/create-reply/3", {'details': 'first reply'})
        reply2 = self.client.post("/board/create-reply/4", {'details': 'second reply'})
        edit1 = self.client.post("/board/edit-reply/1", {'details': 'edited reply'})
        reply_edited_1 = Reply.objects.get(post=Post.objects.get(id=3))
        self.assertEqual(reply_edited_1.details, 'edited reply')

        # Test if post is unable to be edited by non-owner
        self.client.logout()
        self.client.force_login(self.user2)
        try: 
            edit2 = self.client.post("/board/edit-reply/2", {'details': 'edited reply'})
            reply_edited_2 = Reply.objects.get(post=Post.objects.get(id=4))
            self.assertEqual(reply_edited_2.details, 'edited reply')
            self.fail()
        except AssertionError:
            self.assertEqual(reply_edited_2.details, 'second reply')

    def test_reply_deleted(self):
        # Test if reply is successfully deleted by user that owns reply
        response1 = self.client.post("/board/create-reply/2", {'details': 'first reply'})
        response2 = self.client.post("/board/create-reply/2", {'details': 'second reply'})

        delete = self.client.delete("/board/delete-reply/2")
        try:
            reply2 = Reply.objects.get(post=Post.objects.get(id=2), details='second reply')
            self.fail()
        except Reply.DoesNotExist:
            reply1 = Reply.objects.get(post=Post.objects.get(id=2), details='first reply')
            self.assertEqual(reply1.details, 'first reply')

        # Log in user that does not own any replies
        # Try deleting reply made by other user
        self.client.logout()
        self.client.force_login(self.user2)
        delete = self.client.delete("/board/delete-reply/1")
        reply_not_deleted = Reply.objects.get(post=Post.objects.get(id=2))
        self.assertEqual(reply_not_deleted.details, 'first reply')

        # Log user back in
        self.client.logout()
        self.client.force_login(self.user)

    def test_reply_created(self):
        response = self.client.post("/board/create-reply/1", {'details': 'something'})

        reply = Reply.objects.get(post=Post.objects.get(title='Mental Help 2'))
        self.assertEqual(reply.details, 'something')

    def test_reply_user(self):
        response = self.client.post("/board/create-reply/1", {'details': 'something 2'})
        reply = Reply.objects.get(post=Post.objects.get(title='Mental Help 2'), details='something 2')
        self.assertEqual(reply.user, self.user)

    def test_reply_not_logged_in(self):
        self.client.logout()
        try:
            response = self.client.post("/board/create-reply/1", {'details': 'something 3'})
            reply = Reply.objects.get(post=Post.objects.get(title='Mental Help 2'), details='something 3')
            self.fail()
        except ValueError:
            pass

    def test_anonymous_reply(self):
        # Create reply
        response = self.client.post("/board/create-reply/1", {'details': 'somereply', 'anonymous': 'True'})
        # View the reply
        response = self.client.get("/board/view-reply/1")
        # Check if the name is hidden
        self.assertTrue("Anonymous" in response.content.decode("utf-8"))

    def test_view_reply(self):
        # Create reply
        response = self.client.post("/board/create-reply/1", {'details': 'somereply'})
        response = self.client.get("/profile/reply_history/")
        # Check if the html response contains the details
        self.assertTrue("somereply" in response.content.decode("utf-8"))

class AccountTest(TestCase):
    def setUp(self):
        user = User.objects.create(username="jthal", email="jthalacker7@gmail.com",
                                   first_name="jake", last_name="thalacker")
        user2 = User.objects.create(username="jthal7",
                                    email="jakethalacker7@gmail.com",
                                    first_name="jake", last_name="thalacker")

        user.set_password('badgerbuddy123')
        user2.set_password('badgerBuddy')
        user.save()
        user2.save()

    def test_change_anonyminity(self):
        prof = Profile.objects.get(user=User.objects.get(username="jthal"))
        user = User.objects.get(username="jthal")
        self.assertEqual(prof.anonymous, user.profile.anonymous)

    def test_register_login(self):
        response = self.client.post("/users/register/", {'username': 'jthal007', 'password1': 'badgerBuddy123',
                                                         'password2': 'badgerBuddy123', 'email': 'fake@wisc.edu', 'first_name': 'Jake', 'last_name': 'Thalacker', 'user_type':'Student', 'anonymous':False})
        user = auth.get_user(self.client)
        assert user.is_active == False

    def test_login(self):
        # send login data
        response = self.client.post('/users/login/', {'username': 'jthal7', 'password': 'badgerBuddy'}, follow=True)
        # should be logged in now
        user = auth.get_user(self.client)
        assert user.is_authenticated

    def test_logout(self):
        # send login data
        response = self.client.post('/users/login/', {'username': 'jthal7', 'password': 'badgerBuddy'}, follow=True)
        # should be logged in now
        user = auth.get_user(self.client)
        response = self.client.post('/users/logout/',)
        # should be logged out now
        user = auth.get_user(self.client)
        assert not user.is_authenticated

    def test_wisc_email_1(self):
        # register with not a email format
        response = self.client.post("/users/register/", {'username': 'jthal007', 'password1': 'badgerBuddy123',
                                                         'password2': 'badgerBuddy123', 'email': 'fake', 'first_name': 'Jake', 'last_name': 'Thalacker', 'user_type':'Student', 'anonymous':False})
        # should return a form error
        self.assertFormError(response, 'form', 'email', 'Please enter a wisc email')

    def test_wisc_email_2(self):
        # register with a gmail email format
        response = self.client.post("/users/register/", {'username': 'jthal007', 'password1': 'badgerBuddy123',
                                                         'password2': 'badgerBuddy123', 'email': 'fake@gmail.com', 'first_name': 'Jake', 'last_name': 'Thalacker', 'user_type':'Student', 'anonymous':False})
        # should return a form error
        self.assertFormError(response, 'form', 'email', 'Please enter a wisc email')

    def test_wisc_email_3(self):
        # register with a wisc email format
        response = self.client.post("/users/register/", {'username': 'jthal007', 'password1': 'badgerBuddy123',
                                                         'password2': 'badgerBuddy123', 'email': 'fake@wisc.edu', 'first_name': 'Jake', 'last_name': 'Thalacker', 'user_type':'Student', 'anonymous':False})
        # should return a status_code of 302 and redirection url
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/users/register/complete/')

    def test_wisc_email_4(self):
        # register with a wisc department format
        response = self.client.post("/users/register/", {'username': 'jthal007', 'password1': 'badgerBuddy123',
                                                         'password2': 'badgerBuddy123', 'email': 'fake@cs.wisc.edu', 'first_name': 'Jake', 'last_name': 'Thalacker', 'user_type':'Student', 'anonymous':False})
        # should return a status_code of 302 and redirection url
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/users/register/complete/')

    def test_view_profile(self):
        # Login
        self.user2 = User.objects.get(username="jthal7")
        self.client.force_login(self.user2)
        # Check if the profile page display the correct info
        response = self.client.post('/profile/view/')
        self.assertTrue("jthal7" in response.content.decode("utf-8"))
        self.assertTrue("jakethalacker7@gmail.com" in response.content.decode("utf-8"))

    def test_edit_profile_1(self):
        # Login
        response = self.client.post('/users/login/', {'username': 'jthal7', 'password': 'badgerBuddy'}, follow=True)
        # Edit the username, first name and last name
        response = self.client.post('/profile/edit/', {'username': 'Changed_username', 'first_name': 'Jake',
                                                       'last_name': 'thalacker', 'anonymity': 'True',
                                                       'email': 'fake@wisc.edu'}, follow=True)
        # Username should be changed now
        user = User.objects.get(username='Changed_username')
        self.assertEqual(user.first_name, "Jake")

    def test_edit_profile_2(self):
        # Login
        self.user2 = User.objects.get(username="jthal7")
        self.client.force_login(self.user2)
        # Check if it still works if we use GET request
        response = self.client.get('/profile/edit/')
        # It should not work, status code as 200
        self.assertEqual(response.status_code, 200)

    def test_edit_profile_already_existed(self):
        # Login
        response = self.client.post('/users/login/', {'username': 'jthal7', 'password': 'badgerBuddy'}, follow=True)
        # Edit the username and user information, but change to a username that already existed in the database
        response = self.client.post('/profile/edit/', {'username': 'jthal', 'first_name': 'Jake',
                                                       'last_name': 'thalacker', 'anonymity': 'True',
                                                       'email': 'fake@wisc.edu'}, follow=True)
        # Nothing should be changed since it should not pass the validator
        user = User.objects.get(username='jthal')
        self.assertEqual(user.first_name, "jake")


class HelpExerciseTest(TestCase):
    def setUp(self):
        user = User.objects.create(username="jthal", email="jthalacker7@wisc.edu",
                                   first_name="jake", last_name="thalacker")
        user2 = User.objects.create(username="jthal7",
                                    email="jakethalacker8@wisc.edu.com",
                                    first_name="jake", last_name="thalacker")

        user.set_password('badgerbuddy123')
        user2.set_password('badgerBuddy')
        user.save()
        user2.save()
        # Added quotes and prompts
        Quotes.objects.create(text="quote1", author="null")
        Quotes.objects.create(text="quote2", author="null")
        Quotes.objects.create(text="quote3", author="null")
        Prompts.objects.create(text="prompt1")
        Prompts.objects.create(text="prompt2")
        Prompts.objects.create(text="prompt3")

    def test_authentication_exercise(self):
        response = self.client.post('/exercises/')
        # should return a status_code of 200 and not showing anything
        self.assertEqual(response.status_code, 200)

    def test_authentication_help(self):
        response = self.client.post('/help/')
        # should return a status_code of 200 and not showing anything
        self.assertEqual(response.status_code, 200)

    def test_anonymous_exercise(self):
        # Login
        response = self.client.post('/users/login/', {'username': 'jthal7', 'password': 'badgerBuddy'}, follow=True)
        # If the author is null, then automatically set to anonymous
        response = self.client.post('/exercises/')
        self.assertTrue("-Anonymous" in response.content.decode("utf-8"))
        
    def test_breathe_exercise(self):
        # Login
        response = self.client.post('/users/login/', {'username': 'jthal7', 'password': 'badgerBuddy'}, follow=True)
        # If the author is null, then automatically set to anonymous
        response = self.client.post('/exercises/')
        # Check if the breathe.gif is displayed
        self.assertTrue("breathe.gif" in response.content.decode("utf-8"))

class Handle404Tests(TestCase):
    def test_handler_renders_template_response(self):
        response = self.client.get('/adsfa/')
        # The 404 page was correctly handled
        self.assertEqual(response.status_code, 200)
        # Display the right page
        self.assertTrue('404' in response.content.decode("utf-8"))
