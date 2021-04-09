from django.test import TestCase

# Create your tests here.
from django.contrib import auth
from django.test import TestCase
import datetime
from .discussion_board.forms import CreatePostForm, CreateReplyForm
from .models import Post, Tags, Post_Tags, Reply, Meeting, MeetingUsers, Profile, Quotes, Prompts
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
                            create_date=datetime.datetime.now(),
                            user=User.objects.get(username="jthal"))
        Post.objects.create(title="Mental Help 2",
                            details="I recieved help from jthals post",
                            create_date=datetime.datetime.now(),
                            user=User.objects.get(username="jthal7"))
        Tags.objects.create(title="Loneliness")
        Tags.objects.create(title="Discussion")
        Tags.objects.create(title="Mental Help")
        Post_Tags.objects.create(post=Post.objects.get(title="Mental Help 2"),
                                 tag=Tags.objects.create(title="Mental Help"))
        Reply.objects.create(post=Post.objects.get(title="Mental Help 2"),
                             details="I would love to help.",
                             create_date=datetime.datetime.now(),
                             user=User.objects.get(username="jthal"))
        Meeting.objects.create(link="https://www.zoom.us/",
                               date_time=datetime.datetime.now(),
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
                            create_date=datetime.datetime.now(),
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
                            create_date=datetime.datetime.now(),
                            user=User.objects.get(username="jthal7"))
        Post.objects.create(title="Mental Help 3",
                            details="I recieved help from jthals post",
                            create_date=datetime.datetime.now(),
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
