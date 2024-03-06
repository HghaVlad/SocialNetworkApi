import requests


class FriendTest:
    url = "http://localhost:8080/api/friends"
    reg_url = "http://localhost:8080/api/auth/register"
    sign_url = "http://localhost:8080/api/auth/sign-in"
    me_url = "http://localhost:8080/api/me/profile"
    profile_url = "http://localhost:8080/api/profiles"

    simple_user1 = {
        "login": "blackberryMonkey",
        "email": "blackberryMonkey@you.ru",
        "password": "blackberryMonkey21",
        "countryCode": "RU",
        "isPublic": True,
        "phone": "+89811097641",
    }
    correct_user1 = {
        "login": "blackberryMonkey",
        "email": "blackberryMonkey@you.ru",
        "countryCode": "RU",
        "isPublic": True,
        "phone": "+89811097641",
    }
    login_user1 = {
        "login": "blackberryMonkey",
        "password": "blackberryMonkey21",
    }
    simple_user2 = {
        "login": "kiwiMonkey",
        "email": "kiwiMonkey@you.ru",
        "password": "kiwiMonkey21",
        "countryCode": "RU",
        "isPublic": False,
    }
    correct_user2 = {
        "login": "kiwiMonkey",
        "email": "kiwiMonkey@you.ru",
        "countryCode": "RU",
        "isPublic": False,
    }
    login_user2 = {
        "login": "kiwiMonkey",
        "password": "kiwiMonkey21",
    }
    simple_user3 = {
        "login": "pearMonkey",
        "email": "pearMonkey@you.ru",
        "password": "pearMonkey21",
        "countryCode": "FR",
        "isPublic": False,
        "phone": "+898110974",
    }
    correct_user3 = {
        "login": "pearMonkey",
        "email": "pearMonkey@you.ru",
        "countryCode": "FR",
        "isPublic": False,
        "phone": "+898110974",
    }
    login_user3 = {
        "login": "pearMonkey",
        "password": "pearMonkey21",
    }

    user1_friend = {
        "login": "blackberryMonkey"
    }
    user2_friend = {
        "login": "kiwiMonkey"
    }
    user3_friend = {
        "login": "pearMonkey"
    }

    user4_friend = {
        "login": "аррара"
    }

    users = [[simple_user1, login_user1, correct_user1], [simple_user2, login_user2, correct_user2],
             [simple_user3, login_user3, correct_user3]]

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
    incorrect_token5 = "{ "

    incorrect_tokens401 = [incorrect_token1, incorrect_token2, incorrect_token3]
    incorrect_tokens400 = [incorrect_token4, incorrect_token5]

    def test(self):
        self.reg_users()
        self.check_profile_user1()
        self.add_friend_user2()
        self.friend_list()
        self.remove_friend()
        self.wrong_requests()
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

    def check_profile_user1(self):
        token = self.tokens[0]
        headers = {"Authorization": f"Bearer {token}"}
        for login in ["kiwiMonkey", "pearMonkey"]:
            response = requests.get(f"{self.profile_url}/{login}", headers=headers)
            assert int(response.status_code) == 403, f"{response.status_code} when\n {response.text}"
            data = response.json()
            assert "reason" in data, f"{data}"

        response = requests.get(f"{self.url}", headers=headers)
        assert int(response.status_code) == 200, f"{response.status_code} when\n {response.text}"
        data = response.json()
        assert len(data) == 0, data



    def add_friend_user2(self):
        token = self.tokens[1]
        headers = {"Authorization": f"Bearer {token}"}

        response = requests.get(f"{self.profile_url}/blackberryMonkey", headers=headers)
        assert int(response.status_code) == 200, f"{response.status_code} when\n {response.text}"
        data = response.json()
        assert data == self.correct_user1, f"{self.correct_user1} when {data}"

        for _ in range(2):
            response = requests.post(f"{self.url}/add", json=self.user1_friend, headers=headers)
            assert int(response.status_code) == 200, f"{response.status_code} when \n {response.text}"
            data = response.json()
            assert "status" in data
            assert data["status"] == "ok"

            response = requests.post(f"{self.url}/add", json=self.user2_friend, headers=headers)
            assert int(response.status_code) == 200, f"{response.status_code} when \n {response.text}"
            data = response.json()
            assert "status" in data
            assert data["status"] == "ok"

        response = requests.get(f"{self.profile_url}/blackberryMonkey", headers=headers)
        assert int(response.status_code) == 200, f"{response.status_code} when\n {response.text}"
        data = response.json()
        assert data == self.correct_user1, f"{self.correct_user1} when {data}"

        response = requests.post(f"{self.url}/add", json=self.user3_friend, headers=headers)
        assert int(response.status_code) == 200, f"{response.status_code} when \n {response.text}"
        data = response.json()
        assert "status" in data
        assert data["status"] == "ok"

        token = self.tokens[0]
        headers = {"Authorization": f"Bearer {token}"}

        response = requests.get(f"{self.profile_url}/kiwiMonkey", headers=headers)
        assert int(response.status_code) == 200, f"{response.status_code} when\n {response.text}"
        data = response.json()
        assert data == self.correct_user2, f"{self.correct_user2} when {data}"


    def friend_list(self):
        token = self.tokens[1]
        headers = {"Authorization": f"Bearer {token}"}

        response = requests.get(f"{self.url}", headers=headers)
        assert int(response.status_code) == 200, f"{response.status_code} when\n {response.text}"
        data = response.json()
        assert len(data) == 2, data
        assert data[0]['login'] == 'pearMonkey', data
        assert data[1]['login'] == 'blackberryMonkey', data

        response = requests.get(f"{self.url}?limit=1", headers=headers)
        assert int(response.status_code) == 200, f"{response.status_code} when\n {response.text}"
        data = response.json()
        assert len(data) == 1, data
        assert data[0]['login'] == 'pearMonkey', data

        response = requests.get(f"{self.url}?limit=1&offset=1", headers=headers)
        assert int(response.status_code) == 200, f"{response.status_code} when\n {response.text}"
        data = response.json()
        assert len(data) == 1, data
        assert data[0]['login'] == 'blackberryMonkey', data

        response = requests.get(f"{self.url}?limit=1&offset=10", headers=headers)
        assert int(response.status_code) == 200, f"{response.status_code} when\n {response.text}"
        data = response.json()
        assert len(data) == 0, data

        response = requests.get(f"{self.url}?limit=0&offset=0", headers=headers)
        assert int(response.status_code) == 200, f"{response.status_code} when\n {response.text}"
        data = response.json()
        assert len(data) == 0, data




    def remove_friend(self):
        token = self.tokens[1]
        headers = {"Authorization": f"Bearer {token}"}

        response = requests.post(f"{self.url}/remove", json=self.user1_friend, headers=headers)
        assert int(response.status_code) == 200, f"{response.status_code} when \n {response.text}"
        data = response.json()
        assert "status" in data
        assert data["status"] == "ok"

        response = requests.get(f"{self.url}", headers=headers)
        assert int(response.status_code) == 200, f"{response.status_code} when\n {response.text}"
        data = response.json()
        assert len(data) == 1, data
        assert data[0]['login'] == 'pearMonkey', data

        for i in range(3):
            response = requests.post(f"{self.url}/remove", json=self.user3_friend, headers=headers)
            assert int(response.status_code) == 200, f"{response.status_code} when \n {response.text}"
            data = response.json()
            assert "status" in data
            assert data["status"] == "ok"

        response = requests.get(f"{self.url}", headers=headers)
        assert int(response.status_code) == 200, f"{response.status_code} when\n {response.text}"
        data = response.json()
        assert len(data) == 0, data

        response = requests.post(f"{self.url}/remove", json=self.user4_friend, headers=headers)
        assert int(response.status_code) == 200, f"{response.status_code} when \n {response.text}"
        data = response.json()
        assert "status" in data
        assert data["status"] == "ok"

    def wrong_requests(self):
        token = self.tokens[0]
        headers = {"Authorization": f"Bearer {token}"}

        response = requests.post(f"{self.url}/add", json=self.user4_friend, headers=headers)
        assert int(response.status_code) == 404, f"{response.status_code} when\n {response.text}"
        data = response.json()
        assert "reason" in data, f"{data}"

        response = requests.get(f"{self.url}?limit=-1", headers=headers)
        assert int(response.status_code) == 400, f"{response.status_code} when\n {response.text}"
        data = response.json()
        assert "reason" in data, f"{data}"

        response = requests.get(f"{self.url}?offset=-10", headers=headers)
        assert int(response.status_code) == 400, f"{response.status_code} when\n {response.text}"
        data = response.json()
        assert "reason" in data, f"{data}"

        response = requests.get(f"{self.url}?offset=fjfj", headers=headers)
        assert int(response.status_code) == 400, f"{response.status_code} when\n {response.text}"
        data = response.json()
        assert "reason" in data, f"{data}"


    def empty_request(self):
        token = self.tokens[0]
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.post(self.url, headers=headers)
        assert int(response.status_code) == 400, f"{response.status_code} data is empty"
        data = response.json()
        assert "reason" in data, data

        response = requests.post(self.url, json="{ ", headers=headers)
        assert int(response.status_code) == 400, f"{response.status_code} json is incorrect"
        data = response.json()
        assert "reason" in data, data

    def incorrect_token_check(self):
        for token in self.incorrect_tokens401:
            for s in ["", "/add", "/remove"]:
                response = requests.post(self.url+s, headers=token)
                assert int(response.status_code) == 401, f"{response.status_code} when \n {response.text}"
                data = response.json()
                assert "reason" in data, data

                response = requests.get(self.url+s, headers=token)
                assert int(response.status_code) == 401, f"{response.status_code} when \n {response.text}"
                data = response.json()
                assert "reason" in data, data


print("Make Friend test")
c = FriendTest()
c.test()
print("Friend tests completed")
