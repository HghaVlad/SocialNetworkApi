import requests


class ProfileTest:
    url = "http://localhost:8080/api/profiles"
    reg_url = "http://localhost:8080/api/auth/register"
    sign_url = "http://localhost:8080/api/auth/sign-in"
    me_url = "http://localhost:8080/api/me/profile"

    simple_user1 = {
        "login": "bananaMonkey",
        "email": "bananaMonkey@you.ru",
        "password": "bananaMonkeyPass11",
        "countryCode": "RU",
        "isPublic": True,
        "phone": "+898981",
    }
    correct_user1 = {
        "login": "bananaMonkey",
        "email": "bananaMonkey@you.ru",
        "countryCode": "RU",
        "isPublic": True,
        "phone": "+898981",
    }
    login_user1 = {
        "login": "bananaMonkey",
        "password": "bananaMonkeyPass11",
    }
    simple_user2 = {
        "login": "appleMonkey",
        "email": "appleMonkey@you.ru",
        "password": "appleMonkeyPass12",
        "countryCode": "FR",
        "isPublic": True,
        "phone": "+898972",
        "image": "https://http.cat/images/11",
    }
    correct_user2 = {
        "login": "appleMonkey",
        "email": "appleMonkey@you.ru",
        "countryCode": "FR",
        "isPublic": True,
        "phone": "+898972",
        "image": "https://http.cat/images/11",
    }
    login_user2 = {
        "login": "appleMonkey",
        "password": "appleMonkeyPass12",
    }
    simple_user3 = {
        "login": "tomatoMonkey",
        "email": "tomatoMonkey@you.ru",
        "password": "tomatoMonkeyPass13",
        "countryCode": "MX",
        "isPublic": False,
        "phone": "+898613",
    }
    correct_user3 = {
        "login": "tomatoMonkey",
        "email": "tomatoMonkey@you.ru",
        "countryCode": "MX",
        "isPublic": False,
        "phone": "+898613",
    }
    login_user3 = {
        "login": "tomatoMonkey",
        "password": "tomatoMonkeyPass13",
    }

    users = [[simple_user1, login_user1], [simple_user2, login_user2], [simple_user3, login_user3]]
    tokens = []

    change_user2 = {
        "isPublic": False
    }
    change_user3 = {
        "isPublic": True
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


    incorrect_tokens401 = [incorrect_token1, incorrect_token2, incorrect_token3]


    def test(self):
        self.reg_users()
        self.correct_user()
        self.user_2_change_public()
        self.user_3_change_public()
        self.user_2_addfriend_user1()
        # self.empty_request()
        self.incorrect_token_check()

    def reg_users(self):
        for user, login in self.users:
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
            correct_data = user
            del correct_data["password"]
            assert data == correct_data, f"{correct_data} when {data}"

    def correct_user(self):
        # 1
        for token in self.tokens[:2]:
            headers = {"Authorization": f"Bearer {token}"}

            response = requests.get(f"{self.url}/bananaMonkey", headers=headers)
            assert int(response.status_code) == 200, f"{response.status_code} when\n {response.text}"
            data = response.json()
            assert data == self.correct_user1, f"{self.correct_user1} when {data}"

            response = requests.get(f"{self.url}/appleMonkey", headers=headers)
            assert int(response.status_code) == 200, f"{response.status_code} when\n {response.text}"
            data = response.json()
            assert data == self.correct_user2, f"{self.correct_user2} when {data}"

            response = requests.get(f"{self.url}/tomatoMonkey", headers=headers)
            assert int(response.status_code) == 403, f"{response.status_code} when\n {response.text}"
            data = response.json()
            assert "reason" in data, f"{data}"

        # 3
        token = self.tokens[2]
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(f"{self.url}/bananaMonkey", headers=headers)
        assert int(response.status_code) == 200, f"{response.status_code} when\n {response.text}"
        data = response.json()
        assert data == self.correct_user1, f"{self.correct_user1} when {data}"

        response = requests.get(f"{self.url}/appleMonkey", headers=headers)
        assert int(response.status_code) == 200, f"{response.status_code} when\n {response.text}"
        data = response.json()
        assert data == self.correct_user2, f"{self.correct_user2} when {data}"

        response = requests.get(f"{self.url}/tomatoMonkey", headers=headers)
        assert int(response.status_code) == 200, f"{response.status_code} when\n {response.text}"
        data = response.json()
        assert data == self.correct_user3, f"{self.correct_user3} when {data}"

    def user_2_change_public(self):
        response = requests.post(self.sign_url, json=self.login_user2)
        assert int(response.status_code) == 200, f"{response.status_code} when {self.login_user2}\n {response.text}"
        data = response.json()
        assert "token" in data, data
        token = self.tokens[1]  # Проверяем будет ли действовать этот токен
        self.tokens.append(token)
        headers = {"Authorization": f"Bearer {token}"}

        response = requests.patch(self.me_url, json=self.change_user2, headers=headers)
        assert int(response.status_code) == 200, f"{response.status_code} when \n {response.text}"

        token = self.tokens[0]
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(f"{self.url}/appleMonkey", headers=headers)
        assert int(response.status_code) == 403, f"{response.status_code} when\n {response.text}"
        data = response.json()
        assert "reason" in data, data

    def user_3_change_public(self):
        token = self.tokens[2]
        headers = {"Authorization": f"Bearer {token}"}

        response = requests.patch(self.me_url, json=self.change_user3, headers=headers)
        assert int(response.status_code) == 200, f"{response.status_code} when \n {response.text}"

        tokens = (self.tokens[0], self.tokens[2])
        for token in tokens:
            headers = {"Authorization": f"Bearer {token}"}

            response = requests.get(f"{self.url}/bananaMonkey", headers=headers)
            assert int(response.status_code) == 200, f"{response.status_code} when\n {response.text}"
            data = response.json()
            assert data == self.correct_user1, f"{self.correct_user1} when {data}"

            response = requests.get(f"{self.url}/appleMonkey", headers=headers)
            assert int(response.status_code) == 403, f"{response.status_code} when\n {response.text}"
            data = response.json()
            assert "reason" in data, data

            response = requests.get(f"{self.url}/tomatoMonkey", headers=headers)
            assert int(response.status_code) == 200, f"{response.status_code} when\n {response.text}"
            data = response.json()
            user = self.correct_user3
            user['isPublic'] = True
            assert data == user, f"{user} when {data}"

    def user_2_addfriend_user1(self):
        token = self.tokens[1]
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.post("http://localhost:8080/api/friends/add", {"login": "bananaMonkey"}, headers=headers)
        assert int(response.status_code) == 200, f"{response.status_code} when\n {response.text}"

        token = self.tokens[0]
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(f"{self.url}/appleMonkey", headers=headers)
        assert int(response.status_code) == 200, f"{response.status_code} when\n {response.text}"
        data = response.json()
        user = self.correct_user2
        user['isPublic'] = False
        assert data == self.correct_user2, f"{self.correct_user2} when {data}"

        token = self.tokens[2]
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(f"{self.url}/appleMonkey", headers=headers)
        assert int(response.status_code) == 403, f"{response.status_code} when\n {response.text}"
        data = response.json()
        assert "reason" in data, data

        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(f"{self.url}/fsaasafsaf", headers=headers)
        assert int(response.status_code) == 403, f"{response.status_code} when\n {response.text}"
        data = response.json()
        assert "reason" in data, data


    def empty_request(self):
        token = self.tokens[0]
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(self.url, headers=headers)
        assert int(response.status_code) == 400, f"{response.status_code} data is empty"
        data = response.json()
        assert "reason" in data, data

        response = requests.get(self.url, json="{ ", headers=headers)
        assert int(response.status_code) == 400, f"{response.status_code} json is incorrect"
        data = response.json()
        assert "reason" in data, data

        response = requests.get(self.url+"/appleMonkey", json=" ", headers=headers)
        assert int(response.status_code) == 400, f"{response.status_code} json is incorrect"
        data = response.json()
        assert "reason" in data, data

    def incorrect_token_check(self):
        for token in self.incorrect_tokens401:
            response = requests.get(self.url+"/appleMonkey", headers=token)
            assert int(response.status_code) == 401, f"{response.status_code} when \n {response.text}"
            data = response.json()
            assert "reason" in data, data


print("Make Profile test")
c = ProfileTest()
c.test()
print("Profile tests completed")