import requests


class PasswordTest:
    url = "http://localhost:8080/api/me/updatePassword"
    reg_url = "http://localhost:8080/api/auth/register"
    sign_url = "http://localhost:8080/api/auth/sign-in"
    me_url = "http://localhost:8080/api/me/profile"

    simple_user1 = {
        "login": "plumMonkey",
        "email": "plumMonkey@you.ru",
        "password": "plumMonkey21",
        "countryCode": "RU",
        "isPublic": True,
        "phone": "+898997641",
    }
    correct_user1 = {
        "login": "plumMonkey",
        "email": "plumMonkey@you.ru",
        "countryCode": "RU",
        "isPublic": True,
        "phone": "+898997641",
    }
    login_user1_step1 = {
        "login": "plumMonkey",
        "password": "plumMonkey21",
    }
    change_user1 = {
        "oldPassword": "plumMonkey21",
        "newPassword": "plumMonkey222"
    }
    login_user1_step2 = {
        "login": "plumMonkey",
        "password": "plumMonkey222",
    }
    change_user1_wrong = {
        "oldPassword": "plumMonkey21",
        "newPassword": "plumMonkey2223"
    }
    change_user1_wrong_2 = {
        "oldPassword": "plumMonkey222",
        "newPassword": "123"
    }
    change_user1_wrong_3 = {
        "oldPassword": "plumMonkey222",
        "newPassword": "1234567"
    }
    change_user1_wrong_4 = {
        "oldPassword": "plumMonkey222",
        "newPassword": "1234567A"
    }

    wrong_changes = [change_user1_wrong_2, change_user1_wrong_3, change_user1_wrong_4]
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

    incorrect_tokens401 = [incorrect_token1, incorrect_token2]

    def test(self):
        self.reg_user()
        self.update_password()
        self.wrong_password()
        self.empty_request()
        self.incorrect_token_check()

    def reg_user(self):
        response = requests.post(self.reg_url, json=self.simple_user1)
        assert int(response.status_code) == 201, f"{response.status_code} when {self.simple_user1}\n {response.text}"

        response = requests.post(self.sign_url, json=self.login_user1_step1)
        assert int(
            response.status_code) == 200, f"{response.status_code} when {self.login_user1_step1}\n {response.text}"
        data = response.json()
        assert "token" in data, data
        token = data['token']
        self.tokens.append(token)
        headers = {"Authorization": f"Bearer {token}"}

        response = requests.get(self.me_url, headers=headers)
        assert int(response.status_code) == 200, f"{response.status_code} when \n {response.text}"
        data = response.json()
        assert data == self.correct_user1, f"{self.correct_user1} when {data}"

    def update_password(self):
        token = self.tokens[0]
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(self.me_url, headers=headers)
        assert int(response.status_code) == 200, f"{response.status_code} when \n {response.text}"
        data = response.json()
        assert data == self.correct_user1, f"{self.correct_user1} when {data}"

        response = requests.post(self.url, json=self.change_user1, headers=headers)
        assert int(response.status_code) == 200, f"{response.status_code} when \n {response.text}"
        data = response.json()
        assert "status" in data
        assert data["status"] == "ok"

        response = requests.get(self.me_url, headers=headers)
        assert int(response.status_code) == 401, f"{response.status_code} when \n {response.text}"
        data = response.json()
        assert "reason" in data, data

    def wrong_password(self):
        response = requests.post(self.sign_url, json=self.login_user1_step2)
        assert int(response.status_code) == 200, f"{response.status_code} when{self.login_user1_step2}\n{response.text}"
        data = response.json()
        assert "token" in data, data
        token = data['token']
        self.tokens.append(token)
        headers = {"Authorization": f"Bearer {token}"}

        response = requests.get(self.me_url, headers=headers)
        assert int(response.status_code) == 200, f"{response.status_code} when \n {response.text}"
        data = response.json()
        assert data == self.correct_user1, f"{self.correct_user1} when {data}"

        response = requests.post(self.url, json=self.change_user1_wrong, headers=headers)
        assert int(response.status_code) == 403, f"{response.status_code} when \n {response.text}"
        data = response.json()
        assert "reason" in data, data

        for change in self.wrong_changes:
            response = requests.post(self.url, json=change, headers=headers)
            assert int(response.status_code) == 400, f"{response.status_code} when \n {response.text}"
            data = response.json()
            assert "reason" in data, data

    def empty_request(self):
        response = requests.post(self.sign_url, json=self.login_user1_step2)
        assert int(response.status_code) == 200, f"{response.status_code} when{self.login_user1_step2}\n{response.text}"
        data = response.json()
        assert "token" in data, data
        token = data['token']
        headers = {"Authorization": f"Bearer {token}"}

        response = requests.post(self.url, headers=headers)
        assert int(response.status_code) == 400, f"{response.status_code} data is empty"
        data = response.json()
        assert "reason" in data, data

        response = requests.post(self.url, json="{ ", headers=headers)
        assert int(response.status_code) == 400, f"{response.status_code} json is incorrect"
        data = response.json()
        assert "reason" in data, data

        response = requests.post(self.url, json=" ", headers=headers)
        assert int(response.status_code) == 400, f"{response.status_code} json is incorrect"
        data = response.json()
        assert "reason" in data, data

    def incorrect_token_check(self):

        for token in self.incorrect_tokens401:
            response = requests.post(self.url, headers=token)
            assert int(response.status_code) == 401, f"{response.status_code} when \n {response.text}"
            data = response.json()
            assert "reason" in data, data

            response = requests.get(self.url, headers=token)
            assert int(response.status_code) == 401, f"{response.status_code} when \n {response.text}"
            data = response.json()
            assert "reason" in data, data


print("Make Password test")
c = PasswordTest()
c.test()
print("Password tests completed")