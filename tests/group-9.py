import requests


class PostTest:
    url = "http://localhost:8080/api/posts"
    reg_url = "http://localhost:8080/api/auth/register"
    sign_url = "http://localhost:8080/api/auth/sign-in"
    me_url = "http://localhost:8080/api/me/profile"
    profile_url = "http://localhost:8080/api/profiles"
    friend_url = "http://localhost:8080/api/friends"

    simple_user1 = {
        "login": "mangoMonkey",
        "email": "mangoMonkey@you.ru",
        "password": "mangoMonkey21",
        "countryCode": "RU",
        "isPublic": True,
        "phone": "+89815447641",
    }
    correct_user1 = {
        "login": "mangoMonkey",
        "email": "mangoMonkey@you.ru",
        "countryCode": "RU",
        "isPublic": True,
        "phone": "+89815447641",
    }
    login_user1 = {
        "login": "mangoMonkey",
        "password": "mangoMonkey21",
    }
    simple_user2 = {
        "login": "coconutMonkey",
        "email": "coconutMonkey@you.ru",
        "password": "coconutMonkey21",
        "countryCode": "RU",
        "isPublic": False,
    }
    correct_user2 = {
        "login": "coconutMonkey",
        "email": "coconutMonkey@you.ru",
        "countryCode": "RU",
        "isPublic": False,
    }
    login_user2 = {
        "login": "coconutMonkey",
        "password": "coconutMonkey21",
    }
    simple_user3 = {
        "login": "grapeMonkey",
        "email": "grapeMonkey@you.ru",
        "password": "grapeMonkey21",
        "countryCode": "FR",
        "isPublic": False,
    }
    correct_user3 = {
        "login": "grapeMonkey",
        "email": "grapeMonkey@you.ru",
        "countryCode": "FR",
        "isPublic": False,
    }
    login_user3 = {
        "login": "grapeMonkey",
        "password": "grapeMonkey21",
    }
    users = [[simple_user1, login_user1, correct_user1], [simple_user2, login_user2, correct_user2],
             [simple_user3, login_user3, correct_user3]]

    post1 = {
        "content": "PostText1",
        "tags": ["tag1", "Tag2", "tag3"]
    }
    post2 = {
        "content": "",
        "tags": ["he"]
    }
    post3 = {
        "content": "PostText2",
        "tags": [f"tag{i}" for i in range(50)]
    }
    post_correct = [post1, post2, post3]
    post_ids = []

    incorrect_post1 = {
        "content": "abcde"*201,
        "tags": ["tag1", "Tag2", "tag3"]
    }
    incorrect_post2 = {
        "content": "agsaffsa"

    }
    incorrect_post3 = {
        "tags": ["tag1", "Tag2", "tag3"]
    }
    incorrect_post4 = {
        "content": "PostText1",
        "tags": ["tag1", "Tag2", "tag3"],
        "author": "another user"
    }

    incorrect_posts = [incorrect_post1, incorrect_post2, incorrect_post3, incorrect_post4]

    user1_friend = {
        "login": "mangoMonkey"
    }

    tokens = []

    incorrect_token1 = {
        "Authorization": "Bearer blbhh"
    }
    incorrect_token2 = {
        "Authorization": "blbhh"
    }
    incorrect_token3 = {
        "Authorization": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzA5MzgwMDc0LCJpYXQiOjE3MDkzNzk3NzQsImp0aSI6IjRiZDRiZWJhZjY3YjQ3OGY4NTA1ZTU3ZjhhMTVkM2JjIiwidXNlcl9pZCI6MTM2fQ.jlgx837uAJkwtgAtYPyG6-9vTbGiLgzC0Xt8UBFVJrQ"
    }
    incorrect_token4 = " ada"
    incorrect_tokens401 = [incorrect_token1, incorrect_token2, incorrect_token3]


    def test(self):
        self.reg_users()
        self.correct_posts()
        self.wrong_posts()
        self.another_user()
        self.user_friends()
        self.empty_request()
        self.incorrect_token_check()

    def reg_users(self):
        for user, login, correct_data in self.users:
            response = requests.post(self.reg_url, json=user)
            assert int(
                response.status_code) == 201, f"{response.status_code} when {user}\n {response.text}"

            response = requests.post(self.sign_url, json=login)
            assert int(
                response.status_code) == 200, f"{response.status_code} when {login}\n {response.text}"
            data = response.json()
            assert "token" in data, data
            token = data['token']
            self.tokens.append(token)
            headers = {"Authorization": f"Bearer {token}"}

            response = requests.get(self.me_url, headers=headers)
            assert int(response.status_code) == 200, f"{response.status_code} when \n {response.text}"
            data = response.json()
            assert data == correct_data, f"{correct_data} when {data}"

    def correct_posts(self):
        for token in self.tokens[:2]:
            headers = {"Authorization": f"Bearer {token}"}
            last_createdat = 0
            for post in self.post_correct:
                response = requests.post(self.url+"/new", json=post, headers=headers)
                assert int(response.status_code) == 200, f"{response.status_code} when {post}\n {response.text}"
                data = response.json()
                assert data['content'] == post['content'], f"{data['content']} when {post}\n {response.text}"
                assert data['tags'] == post['tags'], f"{data['tags']} when {post}\n {response.text}"
                assert last_createdat != data['createdAt'],  f"{data['createdAt']} when {last_createdat}\n {response.text}"
                last_createdat = data['createdAt']
                self.post_ids.append(data['id'])

                response = requests.get(self.url+ f"/{data['id']}", headers=headers)
                assert int(response.status_code) == 200, f"{response.status_code} when {post}\n {response.text}"
                data2 = response.json()

                assert data == data2,  f"{data} when {post}\n {response.text}"

        assert len(set(self.post_ids)) == 6, f"{self.post_ids}"

    def wrong_posts(self):
        token = self.tokens[0]
        headers = {"Authorization": f"Bearer {token}"}
        for post in self.incorrect_posts:
            response = requests.post(self.url + "/new", json=post, headers=headers)
            assert int(response.status_code) == 400, f"{response.status_code}  {post} when\n {response.text}"
            data = response.json()
            assert "reason" in data, f"{data}"

        response = requests.get(self.url + "/18jdda", headers=headers)
        assert int(response.status_code) == 404, f"{response.status_code} when\n {response.text}"
        data = response.json()
        assert "reason" in data, f"{data}"

    def another_user(self):
        for token in self.tokens:
            headers = {"Authorization": f"Bearer {token}"}

            for post_id in self.post_ids[:3]:
                response = requests.get(self.url + f"/{post_id}", headers=headers)
                assert int(response.status_code) == 200, f"{response.status_code} when {post_id}\n {response.text}"
                data = response.json()
                assert "content" in data
                assert data['author'] == "mangoMonkey", f"{data['author']} when {post_id}\n {response.text}"

    def user_friends(self):
        token = self.tokens[0]
        headers = {"Authorization": f"Bearer {token}"}

        for post_id in self.post_ids[4:]:
            response = requests.get(self.url + f"/{post_id}", headers=headers)
            assert int(response.status_code) == 404, f"{response.status_code} when\n {response.text}"
            data = response.json()
            assert "reason" in data, f"{data}"

        token = self.tokens[1]
        headers2 = {"Authorization": f"Bearer {token}"}
        response = requests.post(self.friend_url+"/add", json=self.user1_friend, headers=headers2)
        assert int(response.status_code) == 200, f"{response.status_code} when \n {response.text}"
        data = response.json()
        assert "status" in data
        assert data["status"] == "ok"

        for post_id in self.post_ids[4:]:
            response = requests.get(self.url + f"/{post_id}", headers=headers)
            assert int(response.status_code) == 200, f"{response.status_code} when {post_id}\n {response.text}"
            data = response.json()
            assert "content" in data
            assert data['author'] == "coconutMonkey", f"{data['author']} when {post_id}\n {response.text}"

        token = self.tokens[2]
        headers3 = {"Authorization": f"Bearer {token}"}
        for post_id in self.post_ids[4:]:
            response = requests.get(self.url + f"/{post_id}", headers=headers3)
            assert int(response.status_code) == 404, f"{response.status_code} when\n {response.text}"
            data = response.json()
            assert "reason" in data, f"{data}"

        response = requests.post(self.friend_url + "/remove", json=self.user1_friend, headers=headers2)
        assert int(response.status_code) == 200, f"{response.status_code} when \n {response.text}"
        data = response.json()
        assert "status" in data
        assert data["status"] == "ok"

        for post_id in self.post_ids[4:]:
            response = requests.get(self.url + f"/{post_id}", headers=headers)
            assert int(response.status_code) == 404, f"{response.status_code} when\n {response.text}"
            data = response.json()
            assert "reason" in data, f"{data}"

    def empty_request(self):
        token = self.tokens[0]
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.post(self.url+"/new", headers=headers)
        assert int(response.status_code) == 400, f"{response.status_code} data is empty"
        data = response.json()
        assert "reason" in data, data

        response = requests.post(self.url+"/new", json="{ ", headers=headers)
        assert int(response.status_code) == 400, f"{response.status_code} json is incorrect"
        data = response.json()
        assert "reason" in data, data

    def incorrect_token_check(self):
        for token in self.incorrect_tokens401:

            response = requests.post(self.url+"/new", headers=token)
            assert int(response.status_code) == 401, f"{response.status_code} when \n {response.text}"
            data = response.json()
            assert "reason" in data, data

            response = requests.get(self.url+f"/{self.post_ids[0]}", headers=token)
            assert int(response.status_code) == 401, f"{response.status_code} when \n {response.text}"
            data = response.json()
            assert "reason" in data, data

print("Make Post test")
c = PostTest()
c.test()
print("Post tests completed")
