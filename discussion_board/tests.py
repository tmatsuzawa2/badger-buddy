from django.test import TestCase

# Create your tests here.
from django.test import TestCase
import datetime
from .models import User, Post, Tags, Post_Tags, Reply, Meeting, MeetingUsers, Activity

class AnimalTestCase(TestCase):
    def setUp(self):
        User.objects.create(type="Student", username="jthal", password="pass123", email="jthalacker7@gmail.com",
                            anonymous=True, first_name="jake", last_name="thalacker")
        User.objects.create(type="Overseer", username="jthal7", password="pass1234", email="jakethalacker7@gmail.com",
                            anonymous=True, first_name="jake", last_name="thalacker")
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
        Activity.objects.create(type_id="prompt", content="What is something nice you did for someone today?")
        Activity.objects.create(type_id="quote", content="\"Every Professional was once a beginner\"-anonymous")

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





