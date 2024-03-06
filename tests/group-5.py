import requests


class MyProfileTest:
    url = "http://localhost:8080/api/me/profile"
    reg_url = "http://localhost:8080/api/auth/register"
    sign_url = "http://localhost:8080/api/auth/sign-in"

    simple_user1_step1 = {
        "login": "pickleMonkey",
        "email": "pickleMonkey@you.ru",
        "password": "pickleMonkeyPass11",
        "countryCode": "RU",
        "isPublic": True,
        "phone": "+711101",
        "image": "https://http.cat/images/100.jpg"
    }
    login_user_1 = {
        "login": "pickleMonkey",
        "password": "pickleMonkeyPass11",
    }
    change_user1_step1 = {
        "countryCode": "GM"
    }
    simple_user1_step2 = {
        "login": "pickleMonkey",
        "email": "pickleMonkey@you.ru",
        "countryCode": "GM",
        "isPublic": True,
        "phone": "+711101",
        "image": "https://http.cat/images/100.jpg"
    }
    change_user1_step2 = {
        "phone": "+71388383",
        "isPublic": False
    }
    simple_user1_step3 = {
        "login": "pickleMonkey",
        "email": "pickleMonkey@you.ru",
        "countryCode": "GM",
        "isPublic": False,
        "phone": "+71388383",
        "image": "https://http.cat/images/100.jpg"
    }
    change_user1_step3 = {
        "phone": "+7138223",
        "image": "https://http.cat/images/11",
        "isPublic": False,
    }
    simple_user1_step4 = {
        "login": "pickleMonkey",
        "email": "pickleMonkey@you.ru",
        "countryCode": "GM",
        "isPublic": False,
        "phone": "+7138223",
        "image": "https://http.cat/images/11"
    }

    user_1_steps = [[change_user1_step1, simple_user1_step2], [change_user1_step2, simple_user1_step3],
                    [change_user1_step3, simple_user1_step4]]

    simple_user2_step1 = {
        "login": "crocodileMonkey",
        "email": "crocodileMonkey@you.ru",
        "password": "crocodileMonkeyPass11",
        "countryCode": "RU",
        "isPublic": True,
        "phone": "+12732",
    }
    login_user_2 = {
        "login": "crocodileMonkey",
        "password": "crocodileMonkeyPass11",
    }
    change_user2_step1 = {
        "phone": "+1737470"
    }
    simple_user2_step2 = {
        "login": "crocodileMonkey",
        "email": "crocodileMonkey@you.ru",
        "countryCode": "RU",
        "isPublic": True,
        "phone": "+1737470",
    }
    change_user2_step2 = {
        "login": "newlogin"
    }
    change_user2_step3 = {
        "phone": ""
    }
    change_user2_step4 = {
        "countryCode": "FFF"
    }
    change_user2_step5 = {
        "login": "pickleMonkey"
    }
    change_user2_step6 = {
        "password": "1234"
    }
    change_user2_step7 = {
        "password": "1234567Ab"
    }
    change_user2_step8 = {
        "isPublic": "hh"
    }
    change_user2_step9 = {
        "ff": "hh"
    }
    change_user2_step10 = {
        "image": "hhh"*100
    }
    change_user2_step11 = {
        "phone": "hhh"
    }
    change_user2_step12 = {
        "phone": "+7"+"10111114"*5
    }
    change_user2_step13 = {
        "phone": "+7138223"
    }
    incorrect_changes = [change_user2_step2, change_user2_step3, change_user2_step4, change_user2_step5,
                         change_user2_step6, change_user2_step7, change_user2_step8, change_user2_step9,
                         change_user2_step10, change_user2_step11, change_user2_step12]

    incorrect_token1 = {
        "Authorization": "Bearer blbhh"
    }
    incorrect_token2 = {
        "Authorization": "blbhh"
    }
    incorrect_token3 = {
        "Authorization": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzA5MzgwMDc0LCJpYXQiOjE3MDkzNzk3NzQsImp0aSI6IjRiZDRiZWJhZjY3YjQ3OGY4NTA1ZTU3ZjhhMTVkM2JjIiwidXNlcl9pZCI6MTM2fQ.jlgx837uAJkwtgAtYPyG6-9vTbGiLgzC0Xt8UBFVJrQ"
    }
    incorrect_token4 = {
        "haha": "blbhh"
    }

    incorrect_tokens401 = [incorrect_token1, incorrect_token2, incorrect_token3, incorrect_token4]

    tokens = []

    def test(self):
        self.correct_user()
        self.wrong_user()
        self.incorrect_token_check()
        self.empty_request()
    def correct_user(self):
        response = requests.post(self.reg_url, json=self.simple_user1_step1)
        assert int(response.status_code) == 201, f"{response.status_code} when {self.simple_user1_step1}\n {response.text}"

        response = requests.post(self.sign_url, json=self.login_user_1)
        assert int(response.status_code) == 200, f"{response.status_code} when {self.login_user_1}\n {response.text}"
        data = response.json()
        assert "token" in data, data
        token = data['token']
        headers = {"Authorization": f"Bearer {token}"}
        self.tokens.append(headers)

        response = requests.get(self.url, headers=headers)
        assert int(response.status_code) == 200, f"{response.status_code} when first me \n {response.text}"
        data = response.json()
        correct_data = self.simple_user1_step1
        del correct_data["password"]
        assert data == correct_data, f"{correct_data} when {data}"

        for change_req, correct_data in self.user_1_steps:
            response = requests.patch(self.url, json=change_req, headers=headers)
            assert int(response.status_code) == 200, f"{response.status_code} when \n {response.text}"
            data = response.json()
            assert data == correct_data, f"{correct_data} when {data}"

            response = requests.get(self.url, headers=headers)
            assert int(response.status_code) == 200, f"{response.status_code} when \n {response.text}"
            data = response.json()
            assert data == correct_data, f"{correct_data} when {data} After patch"

    def wrong_user(self):
        response = requests.post(self.reg_url, json=self.simple_user2_step1)
        assert int(
            response.status_code) == 201, f"{response.status_code} when {self.simple_user2_step1}\n {response.text}"

        response = requests.post(self.sign_url, json=self.login_user_2)
        assert int(response.status_code) == 200, f"{response.status_code} when {self.login_user_2}\n {response.text}"
        data = response.json()
        assert "token" in data, data
        token = data['token']
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(self.url, headers=headers)
        assert int(response.status_code) == 200, f"{response.status_code} when first me \n {response.text}"
        data = response.json()
        correct_data = self.simple_user2_step1
        del correct_data["password"]
        assert data == correct_data, f"{correct_data} when {data}"

        response = requests.patch(self.url, json=self.change_user2_step1, headers=headers)
        assert int(response.status_code) == 200, f"{response.status_code} when \n {response.text}"
        data = response.json()
        assert data == self.simple_user2_step2, f"{self.simple_user2_step2} when {data}"

        for change in self.incorrect_changes:
            response = requests.patch(self.url, json=change, headers=headers)
            assert int(response.status_code) == 400, f"{response.status_code} when \n {response.text} and {change}"
            data = response.json()
            assert "reason" in data, data

            response = requests.get(self.url, headers=headers)
            assert int(response.status_code) == 200, f"{response.status_code} when first me \n {response.text}"
            data = response.json()
            assert data == self.simple_user2_step2, f"{self.simple_user2_step2} when {data}"

        # Отдельно случай 13 так как там ошибка 409
        response = requests.patch(self.url, json=self.change_user2_step13, headers=headers)
        assert int(response.status_code) == 409, f"{response.status_code} when \n {response.text}"
        data = response.json()
        assert "reason" in data, data
        response = requests.get(self.url, headers=headers)
        assert int(response.status_code) == 200, f"{response.status_code} when first me \n {response.text}"
        data = response.json()
        assert data == self.simple_user2_step2, f"{self.simple_user2_step2} when {data}"

    def incorrect_token_check(self):
        for token in self.incorrect_tokens401:
            response = requests.patch(self.url, headers=token)
            assert int(response.status_code) == 401, f"{response.status_code} when \n {response.text}"
            data = response.json()
            assert "reason" in data, data

            response = requests.get(self.url, headers=token)
            assert int(response.status_code) == 401, f"{response.status_code} when \n {response.text}"
            data = response.json()
            assert "reason" in data, data

    def empty_request(self):
        header = self.tokens[0]
        response = requests.patch(self.url, headers=header)
        assert int(response.status_code) == 200,  f"{response.status_code} data is empty"
        data = response.json()


        response = requests.patch(self.url, json="{ ", headers=header)
        assert int(response.status_code) == 400, f"{response.status_code} json is incorrect"
        data = response.json()
        assert "reason" in data, data

        response = requests.patch(self.url, json=" ", headers=header)
        assert int(response.status_code) == 400, f"{response.status_code} json is incorrect"
        data = response.json()
        assert "reason" in data, data

        response = requests.patch(self.url, json=" ", headers=header)
        assert int(response.status_code) == 400, f"{response.status_code} json is incorrect"
        data = response.json()
        assert "reason" in data, data

print("Make MyProfile test")
c = MyProfileTest()
c.test()
print("MyProfile tests completed")
