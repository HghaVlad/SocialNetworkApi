import requests


class SigninTest:
    url = "http://localhost:8080/api/auth/sign-in"
    reg_url = "http://localhost:8080/api/auth/register"

    simple_user1 = {
        "login": "lineMonkey",
        "email": "lineMonkey@you.ru",
        "password": "lineMonkeyPass11",
        "countryCode": "RU",
        "isPublic": True,
        "phone": "+7111111",
        "image": "https://http.cat/images/100.jpg"
    }
    login_user1 = {
        "login": "lineMonkey",
        "password": "lineMonkeyPass11",
    }
    simple_user2 = {
        "login": "oliveMonkey",
        "email": "oliveMonkey@you.ru",
        "password": "oliveMonkeyPass12",
        "countryCode": "FR",
        "isPublic": False,
        "phone": "+7111112",
    }
    login_user2 = {
        "login": "oliveMonkey",
        "password": "oliveMonkeyPass12",
    }
    simple_user3 = {
        "login": "mintMonkey",
        "email": "mintMonkey@you.ru",
        "password": "mintMonkeyPass14",
        "countryCode": "fr",
        "isPublic": True,
    }
    login_user3 = {
        "login": "mintMonkey",
        "password": "mintMonkeyPass14",
    }
    correct_users = [[simple_user1, login_user1], [simple_user2, login_user2], [simple_user3, login_user3]]

    wrong_login1 = {
        "login": "redMonkey",
        "password": "mintMonkeyPass14",
    }
    wrong_login2 = {
        "login": "mintMonkey",
        "password": "wrongpass",
    }
    wrong_login3 = {
        "login": "",
        "password": "",
    }
    wrong_login4 = {
        "password": "dhhdhfdjjdjdd",
    }
    wrong_login5 = {
        "login": "dhhdhd",
    }
    wrong_users = [wrong_login1, wrong_login2, wrong_login3, wrong_login4, wrong_login5]

    def test(self):
        self.correct_auth()
        self.wrong_auth()
        self.empty_request()

    def correct_auth(self):
        tokens = set()
        for user, login in self.correct_users:
            response = requests.post(self.reg_url, json=user)
            assert int(response.status_code) == 201, f"{response.status_code} when {user}\n {response.text}"

            response = requests.post(self.url, json=login)
            assert int(response.status_code) == 200, f"{response.status_code} when {login}\n {response.text}"
            data = response.json()
            assert "token" in data, data
            tokens.add(data['token'])

        assert len(tokens) == len(self.correct_users), tokens

    def wrong_auth(self):
        for login in self.wrong_users:
            response = requests.post(self.url, json=login)
            assert int(response.status_code) == 401, f"{response.status_code} when {login}\n {response.text}"
            data = response.json()
            assert "reason" in data, data

    def empty_request(self):
        response = requests.post(self.url)
        assert int(response.status_code) == 401,  f"{response.status_code} data is empty"
        data = response.json()
        assert "reason" in data, data

        response = requests.post(self.url, json="{ ")
        assert int(response.status_code) == 401, f"{response.status_code} json is incorrect"
        data = response.json()
        assert "reason" in data, data

        response = requests.post(self.url, json=" ")
        assert int(response.status_code) == 401, f"{response.status_code} json is incorrect"
        data = response.json()
        assert "reason" in data, data

        response = requests.post(self.url, headers={"login":"jj"})
        assert int(response.status_code) == 401, f"{response.status_code} head is incorrect"
        data = response.json()
        assert "reason" in data, data

print("Make Sign-in test")
c = SigninTest()
c.test()
print("Sign-in tests completed")