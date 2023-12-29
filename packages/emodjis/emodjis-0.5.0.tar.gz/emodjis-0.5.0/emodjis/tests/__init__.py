import base64

from rest_framework.test import APIClient
from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth.models import User, Group

from emodjis.models import Emoji

username = "test"
email = "test@test.com"
password = "test"

teams = ["team1", "team2"]

test_name = "alert"
test_image = "emodjis/tests/alert.gif"
test_wrong_image = "emodjis/tests/blank.png"

emoticon_list_url = "/emoticons"
emoticon_detail_url = "/emoticon/{name}"


class TestEmoticonAPI(TestCase):
    def setUp(self):
        User.objects.create_user(
            username=username, email=email, password=password
        )
        User.objects.create_user(
            username=username + "2", email=email, password=password
        )
        for team in teams:
            Group.objects.create(name=team)

        self.test_emoji = self.create_test_image(name=test_name)
        self.private_emoji = self.create_test_image(
            name=test_name + "1", private=True
        )
        self.nsfw_emoji = self.create_test_image(
            name=test_name + "2", nsfw=True
        )
        self.team1_emoji = self.create_test_image(
            name=test_name + "3", team=Group.objects.get(name=teams[0])
        )
        self.team2_emoji = self.create_test_image(
            name=test_name + "4", team=Group.objects.get(name=teams[1])
        )

    @staticmethod
    def create_test_image(
        name: str, private: bool = False, nsfw: bool = False, team: str = None
    ):
        with open(test_image, "rb") as f:
            user = User.objects.get(username=username)
            emoji = Emoji.objects.create(
                name=name,
                image=f.read(),
                created_by=user,
                private=private,
                nsfw=nsfw,
                team=team,
            )
            return emoji

    def test_retrieve_emoticon(self):
        name = test_name
        client = APIClient()
        response = client.get(emoticon_detail_url.format(name=name))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers["Content-Type"], "image/gif")
        self.assertIsNotNone(response.content)

    def test_unknown_emoticon(self):
        name = test_name + "_unknown"
        client = APIClient()
        response = client.get(emoticon_detail_url.format(name=name))
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.headers["Content-Type"], "application/json")

    def test_create_emoticon(self):
        name = "new_emoticon"
        client = APIClient()
        basic_auth = base64.b64encode(
            f"{username}:{password}".encode("latin1")
        )
        client.credentials(
            HTTP_AUTHORIZATION="Basic " + basic_auth.decode("utf-8")
        )
        with open(test_image, "rb") as f:
            image = SimpleUploadedFile(
                f.name, f.read(), content_type="image/gif"
            )
            response = client.post(
                emoticon_detail_url.format(name=name),
                data={"image": image},
            )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.headers["Content-Type"], "application/json")
        self.assertIsNotNone(response.json())

    def test_create_emoticon_unknown_format(self):
        name = "wrong_format"
        client = APIClient()
        basic_auth = base64.b64encode(
            f"{username}:{password}".encode("latin1")
        )
        client.credentials(
            HTTP_AUTHORIZATION="Basic " + basic_auth.decode("utf-8")
        )
        response = client.post(
            emoticon_detail_url.format(name=name),
            {"image": open(test_wrong_image, "rb")},
        )
        self.assertEqual(response.status_code, 400)

    def test_create_emoticon_unauthenticated(self):
        name = "new_emoticon"
        client = APIClient()
        response = client.post(
            emoticon_detail_url.format(name=name),
            files={"image": open(test_image, "rb")},
        )
        self.assertEqual(response.status_code, 401)

    def test_delete_emoticon(self):
        name = "to_delete"
        self.create_test_image(name=name)
        client = APIClient()
        basic_auth = base64.b64encode(
            f"{username}:{password}".encode("latin1")
        )
        client.credentials(
            HTTP_AUTHORIZATION="Basic " + basic_auth.decode("utf-8")
        )
        response = client.delete(emoticon_detail_url.format(name=name))
        self.assertEqual(response.status_code, 204)

    def test_delete_emoticon_unauthenticated(self):
        name = "to_delete"
        self.create_test_image(name=name)
        client = APIClient()
        response = client.delete(emoticon_detail_url.format(name=name))
        self.assertEqual(response.status_code, 401)

    def test_delete_emoticon_wrong_user(self):
        name = "to_delete"
        self.create_test_image(name=name)
        client = APIClient()
        basic_auth = base64.b64encode(
            f"{username+'2'}:{password}".encode("latin1")
        )
        client.credentials(
            HTTP_AUTHORIZATION="Basic " + basic_auth.decode("utf-8")
        )
        response = client.delete(emoticon_detail_url.format(name=name))
        self.assertEqual(response.status_code, 404)

    def test_list_emoticons(self):
        client = APIClient()
        response = client.get(emoticon_list_url)
        print("list response", response.json())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers["Content-Type"], "application/json")
        self.assertIsNotNone(response.json())

    def test_list_filter_team(self):
        client = APIClient()
        response = client.get(emoticon_list_url + "?team=" + teams[0])
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers["Content-Type"], "application/json")
        print("team filter", response.json())
        self.assertEqual(response.json()[0]["name"], self.team1_emoji.name)

    def test_list_filter_nsfw(self):
        client = APIClient()
        response = client.get(emoticon_list_url + "?nsfw=true")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers["Content-Type"], "application/json")
        has_nsfw = False
        print("nsfw filter", response.json())
        for item in response.json():
            if item["name"] == self.nsfw_emoji.name:
                has_nsfw = True
        self.assertTrue(has_nsfw)

    def test_list_filter_private(self):
        client = APIClient()
        basic_auth = base64.b64encode(
            f"{username}:{password}".encode("latin1")
        )
        client.credentials(
            HTTP_AUTHORIZATION="Basic " + basic_auth.decode("utf-8")
        )
        response = client.get(emoticon_list_url + "?private=true")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers["Content-Type"], "application/json")
        has_private = False
        print("private filter", response.json())
        for item in response.json():
            if item["name"] == self.private_emoji.name:
                has_private = True
        self.assertTrue(has_private)

    def test_list_filter_private_unauthenticated(self):
        client = APIClient()
        response = client.get(emoticon_list_url + "?private=true")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers["Content-Type"], "application/json")
        has_private = False
        print("private filter", response.json())
        for item in response.json():
            if item["name"] == self.private_emoji.name:
                has_private = True
        self.assertFalse(has_private)

    def test_retrieve_schema(self):
        url = "/schema/?format=json"
        client = APIClient()
        response = client.get(url)
        assert response.status_code == 200
        assert response.headers["Content-Type"] in [
            "application/json",
            "application/vnd.oai.openapi+json",
        ]
        assert response.json() is not None
