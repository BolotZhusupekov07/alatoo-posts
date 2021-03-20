from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse

from .models import Post

class BlogTests(TestCase):


    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username = "testusername",
            email = "test@email.com",
            password = "secret"
        )

        self.post = Post.objects.create(
            title = 'A good title', 
            body = 'Nice body content', 
            author = self.user
        )


    def test_string_representation(self):
        post = Post(title = "A good title")
        self.assertEqual(str(post), post.title)


    def test_get_absolute_url(self):
        self.assertEqual(self.post.get_absolute_url(), '/post/1/')


    def test_post_content(self):
        self.assertEqual(f'{self.post.title}', 'A good title')
        self.assertEqual(f'{self.post.body}', 'Nice body content')
        self.assertEqual(f'{self.post.author}', 'testusername')


    def test_post_list_view(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response,"Nice body content")
        self.assertTemplateUsed(response,"home.html")


    def test_post_detail_view(self):
        no_response = self.client.get('/post/10000/')
        response = self.client.get('/post/1/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
        self.assertContains(response, "A good title")
        self.assertTemplateUsed(response, 'post_detail.html')

    def test_create_post(self):
        
        response = self.client.post(reverse("post_new"), {
            "title" : "New title",
            "body" :"New body", 
            "author" : self.user,
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "New title")
        self.assertContains(response, "New body")

    
    def test_update_post(self):

        response = self.client.post(reverse("post_edit", args = "1") , {
            "title":"Update title", 
            "body":"Update body",
        })

        self.assertEqual(response.status_code, 302)

    
    def test_delete_post(self):
        response = self.client.post(reverse("post_delete", args = "1"))
        self.assertEqual(response.status_code, 302)