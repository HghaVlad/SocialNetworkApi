import requests


class LikeTest:
    reg_url = "http://localhost:8080/api/auth/register"
    sign_url = "http://localhost:8080/api/auth/sign-in"
    me_url = "http://localhost:8080/api/me/profile"
    profile_url = "http://localhost:8080/api/profiles"
    friend_url = "http://localhost:8080/api/friends"
    posts_url = "http://localhost:8080/api/posts"
    feed_url = "http://localhost:8080/api/posts/feed"

    simple_user1 = {
        "login": "raspberryMonkey",
        "email": "raspberryMonkey@you.ru",
        "password": "raspberryMonkey21",
        "countryCode": "RU",
        "isPublic": True,
        "phone": "+895447641",
    }
    correct_user1 = {
        "login": "raspberryMonkey",
        "email": "raspberryMonkey@you.ru",
        "countryCode": "RU",
        "isPublic": True,
        "phone": "+895447641",
    }
    login_user1 = {
        "login": "raspberryMonkey",
        "password": "raspberryMonkey21",
    }
    simple_user2 = {
        "login": "blueberryMonkey",
        "email": "blueberryMonkey@you.ru",
        "password": "blueberryMonkey21",
        "countryCode": "RU",
        "isPublic": False,
    }
    correct_user2 = {
        "login": "blueberryMonkey",
        "email": "blueberryMonkey@you.ru",
        "countryCode": "RU",
        "isPublic": False,
    }
    login_user2 = {
        "login": "blueberryMonkey",
        "password": "blueberryMonkey21",
    }
    users = [[simple_user1, login_user1, correct_user1], [simple_user2, login_user2, correct_user2]]

    post1 = {
        "content": "PostText1",
        "tags": ["tag1", "Tag2", "tag3"]
    }
    post2 = {
        "content": "PostText2",
        "tags": ["tag1", "tag3"]
    }
    post3 = {
        "content": "PostText3",
        "tags": ["tag1", "Tag2"]
    }

    user1_friend = {
        "login": "raspberryMonkey"
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
        self.like_simple_post()
        self.anotheruser()
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

    def like_simple_post(self):
        token = self.tokens[0]
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(self.posts_url+f"/{self.post_ids[0]}", headers=headers)
        assert int(response.status_code) == 200, f"{response.status_code} when\n {response.text}"
        data = response.json()
        assert data['content'] == "PostText1", f"{data['content']} when {self.post1}\n {response.text}"
        assert data['author'] == "raspberryMonkey", f"{data} when {self.post1}\n {response.text}"
        assert data['likesCount'] == 0, f"{data} when {self.post1}\n {response.text}"
        assert data["dislikesCount"] == 0, f"{data} when {self.post1}\n {response.text}"

        for i in range(3):
            response = requests.post(self.posts_url +f"/{self.post_ids[0]}/like", headers=headers)
            assert int(response.status_code) == 200, f"{response.status_code} when \n {response.text}"
            data = response.json()
            assert data['id'] == self.post_ids[0],  f"{data} when {self.post1}\n {response.text}"
            assert data["likesCount"] == 1, f"{data} when {self.post1}\n {response.text}"
            assert data["dislikesCount"] == 0, f"{data} when {self.post1}\n {response.text}"

        response = requests.post(self.posts_url + f"/{self.post_ids[0]}/dislike", headers=headers)
        assert int(response.status_code) == 200, f"{response.status_code} when \n {response.text}"
        data = response.json()
        assert data['id'] == self.post_ids[0], f"{data} when {self.post1}\n {response.text}"
        assert data["likesCount"] == 0, f"{data} when {self.post1}\n {response.text}"
        assert data["dislikesCount"] == 1, f"{data} when {self.post1}\n {response.text}"

        response = requests.post(self.posts_url + f"/{self.post_ids[3]}/dislike", headers=headers)
        assert int(response.status_code) == 404, f"{response.status_code}  when\n {response.text}"
        data = response.json()
        assert "reason" in data, f"{data}"

        response = requests.post(self.posts_url + f"/{self.post_ids[3]}/like", headers=headers)
        assert int(response.status_code) == 404, f"{response.status_code}  when\n {response.text}"
        data = response.json()
        assert "reason" in data, f"{data}"


    def anotheruser(self):
        token = self.tokens[1]
        headers = {"Authorization": f"Bearer {token}"}
        for i in range(3):
            response = requests.post(self.posts_url +f"/{self.post_ids[0]}/like", headers=headers)
            assert int(response.status_code) == 200, f"{response.status_code} when \n {response.text}"
            data = response.json()
            assert data['id'] == self.post_ids[0],  f"{data} when {self.post1}\n {response.text}"
            assert data["likesCount"] == 1, f"{data} when {self.post1}\n {response.text}"
            assert data["dislikesCount"] == 1, f"{data} when {self.post1}\n {response.text}"

        response = requests.post(self.posts_url + f"/{self.post_ids[3]}/dislike", headers=headers)
        assert int(response.status_code) == 200, f"{response.status_code} when\n {response.text}"
        data = response.json()
        assert data['author'] == "blueberryMonkey", f"{data} when {self.post1}\n {response.text}"
        assert data['likesCount'] == 0, f"{data} when {self.post1}\n {response.text}"
        assert data["dislikesCount"] == 1, f"{data} when {self.post1}\n {response.text}"

        response = requests.post(self.friend_url + "/add", json=self.user1_friend, headers=headers)
        assert int(response.status_code) == 200, f"{response.status_code} when \n {response.text}"
        data = response.json()
        assert "status" in data
        assert data["status"] == "ok"

        token = self.tokens[0]
        headers2 = {"Authorization": f"Bearer {token}"}
        for i in range(3):
            response = requests.post(self.posts_url + f"/{self.post_ids[3]}/dislike", headers=headers2)
            assert int(response.status_code) == 200, f"{response.status_code} when\n {response.text}"
            data = response.json()
            assert data['likesCount'] == 0, f"{data} when {self.post1}\n {response.text}"
            assert data["dislikesCount"] == 2, f"{data} when {self.post1}\n {response.text}"

        response = requests.post(self.friend_url + "/remove", json=self.user1_friend, headers=headers)
        assert int(response.status_code) == 200, f"{response.status_code} when \n {response.text}"
        data = response.json()
        assert "status" in data
        assert data["status"] == "ok"

        response = requests.post(self.posts_url + f"/{self.post_ids[3]}/like", headers=headers2)
        assert int(response.status_code) == 404, f"{response.status_code}  when\n {response.text}"
        data = response.json()
        assert "reason" in data, f"{data}"

        response = requests.post(self.posts_url + f"/{self.post_ids[3]}/dislike", headers=headers)
        assert int(response.status_code) == 200, f"{response.status_code} when\n {response.text}"
        data = response.json()
        assert data['likesCount'] == 0, f"{data} when {self.post1}\n {response.text}"
        assert data["dislikesCount"] == 2, f"{data} when {self.post1}\n {response.text}"

    def wrong_requests(self):
        token = self.tokens[1]
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.post(self.posts_url + f"/akdjd/dislike", headers=headers)
        assert int(response.status_code) == 404, f"{response.status_code}  when\n {response.text}"
        data = response.json()
        assert "reason" in data, f"{data}"

        response = requests.get(self.posts_url + f"/akdjd/dislike", headers=headers)
        assert int(response.status_code) == 400, f"{response.status_code}  when\n {response.text}"
        data = response.json()
        assert "reason" in data, f"{data}"

        response = requests.post(self.posts_url + f"/akdjd/like", headers=headers)
        assert int(response.status_code) == 404, f"{response.status_code}  when\n {response.text}"
        data = response.json()
        assert "reason" in data, f"{data}"

        response = requests.post(self.posts_url + f"/akdjd", headers=headers)
        assert int(response.status_code) == 400, f"{response.status_code}  when\n {response.text}"
        data = response.json()
        assert "reason" in data, f"{data}"


    def incorrect_token_check(self):

        for token in self.incorrect_tokens401:
            response = requests.post(self.posts_url + f"/{self.post_ids[3]}/like", headers=token)
            assert int(response.status_code) == 401, f"{response.status_code} when \n {response.text}"
            data = response.json()
            assert "reason" in data, data

            response = requests.post(self.posts_url + f"/{self.post_ids[1]}/dislike", headers=token)
            assert int(response.status_code) == 401, f"{response.status_code} when \n {response.text}"
            data = response.json()
            assert "reason" in data, data

            response = requests.get(self.posts_url + f"/{self.post_ids[0]}", headers=token)
            assert int(response.status_code) == 401, f"{response.status_code} when \n {response.text}"
            data = response.json()
            assert "reason" in data, data


print("Make Like test")
c = LikeTest()
c.test()
print("Like tests completed")