import requests


class FeedTest:

    url = "http://localhost:8080/api/posts/feed"
    reg_url = "http://localhost:8080/api/auth/register"
    sign_url = "http://localhost:8080/api/auth/sign-in"
    me_url = "http://localhost:8080/api/me/profile"
    profile_url = "http://localhost:8080/api/profiles"
    friend_url = "http://localhost:8080/api/friends"
    posts_url = "http://localhost:8080/api/posts"


    simple_user1 = {
        "login": "potatoMonkey",
        "email": "potatoMonkey@you.ru",
        "password": "potatoMonkey21",
        "countryCode": "RU",
        "isPublic": True,
        "phone": "+898154947641",
    }
    correct_user1 = {
        "login": "potatoMonkey",
        "email": "potatoMonkey@you.ru",
        "countryCode": "RU",
        "isPublic": True,
        "phone": "+898154947641",
    }
    login_user1 = {
        "login": "potatoMonkey",
        "password": "potatoMonkey21",
    }
    simple_user2 = {
        "login": "eggplantMonkey",
        "email": "eggplantMonkey@you.ru",
        "password": "eggplantMonkey21",
        "countryCode": "RU",
        "isPublic": False,
    }
    correct_user2 = {
        "login": "eggplantMonkey",
        "email": "eggplantMonkey@you.ru",
        "countryCode": "RU",
        "isPublic": False,
    }
    login_user2 = {
        "login": "eggplantMonkey",
        "password": "eggplantMonkey21",
    }
    users = [[simple_user1, login_user1, correct_user1], [simple_user2, login_user2, correct_user2]]

    post1 = {
        "content": "PostText1",
        "tags": ["tag1", "Tag2", "tag3"]
    }
    post2 = {
        "content": "PostText2",
        "tags": ["tag1","tag3"]
    }
    post3 = {
        "content": "PostText3",
        "tags": ["tag1", "Tag2"]
    }

    user1_friend = {
        "login": "potatoMonkey"
    }

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

    tokens = []
    post_ids = []

    def test(self):
        self.reg_users()
        self.make_post()
        self.see_mypage()
        self.see_user_page()
        self.user_friends()
        self.wrong_requests()
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

    def make_post(self):
        token = self.tokens[0]
        headers = {"Authorization": f"Bearer {token}"}
        for post in [self.post1, self.post2, self.post3]:
            response = requests.post(self.posts_url + "/new", json=post, headers=headers)
            assert int(response.status_code) == 200, f"{response.status_code} when {post}\n {response.text}"
            data = response.json()
            assert data['content'] == post['content'], f"{data['content']} when {post}\n {response.text}"
            assert data['tags'] == post['tags'], f"{data['tags']} when {post}\n {response.text}"
            self.post_ids.append(data['id'])

        token = self.tokens[1]
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.post(self.posts_url + "/new", json=self.post1, headers=headers)
        assert int(response.status_code) == 200, f"{response.status_code} when {self.post1}\n {response.text}"
        data = response.json()
        assert data['content'] == self.post1['content'], f"{data['content']} when {self.post1}\n {response.text}"
        assert data['tags'] == self.post1['tags'], f"{data['tags']} when {self.post1}\n {response.text}"
        self.post_ids.append(data['id'])

        response = requests.post(self.posts_url + "/new", json=self.post3, headers=headers)
        assert int(response.status_code) == 200, f"{response.status_code} when {self.post3}\n {response.text}"
        data = response.json()
        assert data['content'] == self.post3['content'], f"{data['content']} when {self.post3}\n {response.text}"
        assert data['tags'] == self.post3['tags'], f"{data['tags']} when {self.post3}\n {response.text}"
        self.post_ids.append(data['id'])

    def see_mypage(self):
        token = self.tokens[0]
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(self.url+"/my", headers=headers)
        assert int(response.status_code) == 200, f"{response.status_code} when {response.text}"
        data = response.json()
        assert len(data) == 3, data
        assert data[0]['content'] == "PostText3", data
        assert data[2]['content'] == 'PostText1', data
        assert data[1]['author'] == "potatoMonkey", data

        response = requests.get(self.url + "/my?limit=1", headers=headers)
        assert int(response.status_code) == 200, f"{response.status_code} when {response.text}"
        data = response.json()
        assert len(data) == 1, data
        assert data[0]['content'] == "PostText3", data

        response = requests.get(self.url + "/my?limit=2&offset=1", headers=headers)
        assert int(response.status_code) == 200, f"{response.status_code} when {response.text}"
        data = response.json()
        assert len(data) == 2, data
        assert data[0]['content'] == "PostText2", data

        response = requests.get(self.url + "/my?offset=2", headers=headers)
        assert int(response.status_code) == 200, f"{response.status_code} when {response.text}"
        data = response.json()
        assert len(data) == 1, data
        assert data[0]['content'] == "PostText1", data

    def see_user_page(self):
        for token in self.tokens:
            headers = {"Authorization": f"Bearer {token}"}
            response = requests.get(self.url + "/potatoMonkey", headers=headers)
            assert int(response.status_code) == 200, f"{response.status_code} when {response.text}"
            data = response.json()
            assert len(data) == 3, data
            assert data[0]['content'] == "PostText3", data
            assert data[2]['content'] == 'PostText1', data
            assert data[1]['author'] == "potatoMonkey", data
            assert data[0]['author'] == 'potatoMonkey'

            response = requests.get(self.url + "/potatoMonkey?limit=1", headers=headers)
            assert int(response.status_code) == 200, f"{response.status_code} when {response.text}"
            data = response.json()
            assert len(data) == 1, data
            assert data[0]['content'] == "PostText3", data
            assert data[0]['author'] == 'potatoMonkey'

            response = requests.get(self.url + "/potatoMonkey?limit=2&offset=1", headers=headers)
            assert int(response.status_code) == 200, f"{response.status_code} when {response.text}"
            data = response.json()
            assert len(data) == 2, data
            assert data[0]['content'] == "PostText2", data
            assert data[0]['author'] == 'potatoMonkey'

            response = requests.get(self.url + "/potatoMonkey?offset=2", headers=headers)
            assert int(response.status_code) == 200, f"{response.status_code} when {response.text}"
            data = response.json()
            assert len(data) == 1, data
            assert data[0]['content'] == "PostText1", data
            assert data[0]['author'] == 'potatoMonkey'

        token = self.tokens[0]
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(self.url + "/eggplantMonkey", headers=headers)
        assert int(response.status_code) == 404, f"{response.status_code}  when\n {response.text}"
        data = response.json()
        assert "reason" in data, f"{data}"

        response = requests.get(self.url + "/fassaf", headers=headers)
        assert int(response.status_code) == 404, f"{response.status_code}  when\n {response.text}"
        data = response.json()
        assert "reason" in data, f"{data}"

    def user_friends(self):
        token = self.tokens[0]
        headers = {"Authorization": f"Bearer {token}"}


        token = self.tokens[1]
        headers2 = {"Authorization": f"Bearer {token}"}
        response = requests.post(self.friend_url+"/add", json=self.user1_friend, headers=headers2)
        assert int(response.status_code) == 200, f"{response.status_code} when \n {response.text}"
        data = response.json()
        assert "status" in data
        assert data["status"] == "ok"

        response = requests.get(self.url + "/eggplantMonkey", headers=headers)
        assert int(response.status_code) == 200, f"{response.status_code} when \n {response.text}"
        data = response.json()
        assert len(data) == 2
        assert data[0]['content'] == self.post3['content'], f"{data} when {self.post3}\n {response.text}"
        assert data[0]['tags'] == self.post3['tags'], f"{data} when {self.post3}\n {response.text}"
        assert data[1]['content'] == self.post1['content'], f"{data} when {self.post3}\n {response.text}"
        assert data[1]['author'] == 'eggplantMonkey', f"{data} when\n {response.text}"

        response = requests.get(self.url + "/eggplantMonkey?limit=1", headers=headers)
        assert int(response.status_code) == 200, f"{response.status_code} when \n {response.text}"
        data = response.json()
        assert len(data) == 1
        assert data[0]['content'] == self.post3['content'], f"{data} when {self.post3}\n {response.text}"
        assert data[0]['tags'] == self.post3['tags'], f"{data} when {self.post3}\n {response.text}"

        response = requests.get(self.url + "/eggplantMonkey?offset=1", headers=headers)
        assert int(response.status_code) == 200, f"{response.status_code} when \n {response.text}"
        data = response.json()
        assert len(data) == 1
        assert data[0]['content'] == self.post1['content'], f"{data} when {self.post1}\n {response.text}"
        assert data[0]['tags'] == self.post1['tags'], f"{data} when {self.post1}\n {response.text}"

        response = requests.post(self.friend_url + "/remove", json=self.user1_friend, headers=headers2)
        assert int(response.status_code) == 200, f"{response.status_code} when \n {response.text}"
        data = response.json()
        assert "status" in data
        assert data["status"] == "ok"

        response = requests.get(self.url + "/eggplantMonkey", headers=headers)
        assert int(response.status_code) == 404, f"{response.status_code}  when\n {response.text}"
        data = response.json()
        assert "reason" in data, f"{data}"


    def wrong_requests(self):
        token = self.tokens[1]
        headers = {"Authorization": f"Bearer {token}"}

        response = requests.get(self.url + "/potatoMonkey?limit=1000", headers=headers)
        assert int(response.status_code) == 400, f"{response.status_code}  when\n {response.text}"
        data = response.json()
        assert "reason" in data, f"{data}"

        response = requests.get(self.url + "/potatoMonkey?offset=-1", headers=headers)
        assert int(response.status_code) == 400, f"{response.status_code}  when\n {response.text}"
        data = response.json()
        assert "reason" in data, f"{data}"

        response = requests.get(self.url + "/potatoMonkey?offset=ffa", headers=headers)
        assert int(response.status_code) == 400, f"{response.status_code}  when\n {response.text}"
        data = response.json()
        assert "reason" in data, f"{data}"

        response = requests.get(self.url + "/potatoMonkey?limit=ffa", headers=headers)
        assert int(response.status_code) == 400, f"{response.status_code}  when\n {response.text}"
        data = response.json()
        assert "reason" in data, f"{data}"

        response = requests.get(self.url + "/my?limit=1000", headers=headers)
        assert int(response.status_code) == 400, f"{response.status_code}  when\n {response.text}"
        data = response.json()
        assert "reason" in data, f"{data}"

        response = requests.get(self.url + "/my?offset=-1", headers=headers)
        assert int(response.status_code) == 400, f"{response.status_code}  when\n {response.text}"
        data = response.json()
        assert "reason" in data, f"{data}"

        response = requests.get(self.url + "/my?offset=ffa", headers=headers)
        assert int(response.status_code) == 400, f"{response.status_code}  when\n {response.text}"
        data = response.json()
        assert "reason" in data, f"{data}"

        response = requests.get(self.url + "/my?limit=ffa", headers=headers)
        assert int(response.status_code) == 400, f"{response.status_code}  when\n {response.text}"
        data = response.json()
        assert "reason" in data, f"{data}"

    def incorrect_token_check(self):
        for token in self.incorrect_tokens401:

            response = requests.post(self.url+"/my", headers=token)
            assert int(response.status_code) == 401, f"{response.status_code} when \n {response.text}"
            data = response.json()
            assert "reason" in data, data

            response = requests.get(self.url+f"/{self.post_ids[0]}", headers=token)
            assert int(response.status_code) == 401, f"{response.status_code} when \n {response.text}"
            data = response.json()
            assert "reason" in data, data

print("Make Feed test")
c = FeedTest()
c.test()
print("Feed tests completed")
