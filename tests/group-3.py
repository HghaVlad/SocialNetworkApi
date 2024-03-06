import requests


class RegisterTest:
    url = "http://localhost:8080/api/auth/register"

    # Status code 201
    simple_user1 = {
        "login": "greenMonkey",
        "email": "greenMonkey@you.ru",
        "password": "greenMonkeyPass12",
        "countryCode": "RU",
        "isPublic": True,
        "phone": "+711111112",
        "image": "https://http.cat/images/100.jpg"
    }
    simple_user2 = {
        "login": "yellowMonkey",
        "email": "yellowMonkey@you.ru",
        "password": "yellowMonkeyPass13",
        "countryCode": "RU",
        "isPublic": True,
        "phone": "+711111113",
    }
    simple_user3 = {
        "login": "orangeMonkey",
        "email": "orangeMonkey@you.ru",
        "password": "orangeMonkeyPass14",
        "countryCode": "RU",
        "isPublic": True,
    }
    simple_user4 = {
        "login": "lemonMonkey",
        "email": "lemonMonkey@you.ru",
        "password": "lemonMonkeyPass14",
        "countryCode": "fr",
        "isPublic": True,
    }
    simple_user5 = {
        "login": "teaMonkey",
        "email": "teaMonkey@you.ru",
        "password": "teaMonkeyPass14",
        "countryCode": "fr",
        "isPublic": True,
        "image": "ya.ru/img"
    }
    correct_users = [simple_user1, simple_user2, simple_user3, simple_user4]

    different_user = {
        "login": "peachMonkey",
        "countryCode": "RU",
        "email": "peachMonkey@you.ru",
        "isPublic": True,
        "password": "peachMonkeyPass14",
    }
    different_user_correct = {
        "login": "peachMonkey",
        "email": "peachMonkey@you.ru",
        "password": "peachMonkeyPass14",
        "countryCode": "RU",
        "isPublic": True,
    }

    different_user2 = {
        "login": "pineappleMonkey",
        "countryCode": "FR",
        "image": "https://http.cat/images/100.jpg",
        "email": "pineappleMonkey@you.ru",
        "isPublic": True,
        "password": "pineappleMonkeyPass14",

    }
    different_user2_correct = {
        "login": "pineappleMonkey",
        "email": "pineappleMonkey@you.ru",
        "password": "pineappleMonkeyPass14",
        "countryCode": "FR",
        "isPublic": True,
        "image": "https://http.cat/images/100.jpg",
    }
    different_order_users = [[different_user, different_user_correct], [different_user2, different_user2_correct]]

    # Status code 409
    wrong_user1 = {
        "login": "orangeMonkey",
        "email": "redMonkey@you.ru",
        "password": "redMonkeyPass15",
        "countryCode": "RU",
        "isPublic": True,
    }
    wrong_user2 = {
        "login": "redMonkey",
        "email": "orangeMonkey@you.ru",
        "password": "redMonkeyPass15",
        "countryCode": "RU",
        "isPublic": True,
    }
    wrong_user3 = {
        "login": "redMonkey",
        "email": "redMonkey@you.ru",
        "password": "redMonkeyPass15",
        "countryCode": "RU",
        "isPublic": True,
        "phone": "+711111113"
    }
    wrong409 = [wrong_user1, wrong_user2, wrong_user3]

    # Status code = 400
    wrong_user4 = {
        "login": "redMonkey"*10,
        "email": "redMonkey@you.ru",
        "password": "redMonkeyPass15",
        "countryCode": "RU",
        "isPublic": True,
        "phone": "+711111114"
    }
    wrong_user5 = {
        "login": "",
        "email": "redMonkey@you.ru",
        "password": "redMonkeyPass15",
        "countryCode": "RU",
        "isPublic": True,
        "phone": "+711111114"
    }
    wrong_user6 = {
        "login": "redMonkey",
        "email": "redMonkey@you.ru" * 10,
        "password": "redMonkeyPass15",
        "countryCode": "RU",
        "isPublic": True,
        "phone": "+711111114"
    }
    wrong_user7 = {
        "login": "redMonkey",
        "email": "",
        "password": "redMonkeyPass15",
        "countryCode": "RU",
        "isPublic": True,
        "phone": "+711111114"
    }
    wrong_user8 = {
        "login": "redMonkey",
        "email": "redMonkey@you.ru",
        "password": "11111",
        "countryCode": "RU",
        "isPublic": True,
        "phone": "+711111114"
    }
    wrong_user9 = {
        "login": "redMonkey",
        "email": "redMonkey@you.ru",
        "password": "1111111",
        "countryCode": "RU",
        "isPublic": True,
        "phone": "+711111114"
    }
    wrong_user10 = {
        "login": "redMonkey",
        "email": "redMonkey@you.ru",
        "password": "1111111A",
        "countryCode": "RU",
        "isPublic": True,
        "phone": "+711111114"
    }
    wrong_user11 = {
        "login": "redMonkey",
        "email": "redMonkey@you.ru",
        "password": "1111111b",
        "countryCode": "RU",
        "isPublic": True,
        "phone": "+711111114"
    }
    wrong_user12 = {
        "login": "redMonkey",
        "email": "redMonkey@you.ru",
        "password": "1111111b"*15,
        "countryCode": "RU",
        "isPublic": True,
        "phone": "+711111114"
    }
    wrong_user13 = {
        "login": "redMonkey",
        "email": "redMonkey@you.ru",
        "password": "1111111Ab",
        "countryCode": "",
        "isPublic": True,
        "phone": "+711111114"
    }
    wrong_user14 = {
        "login": "redMonkey",
        "email": "redMonkey@you.ru",
        "password": "1111111Ab",
        "countryCode": "AFG",
        "isPublic": True,
        "phone": "+711111114"
    }
    wrong_user15 = {
        "login": "redMonkey",
        "email": "redMonkey@you.ru",
        "password": "1111111Ab",
        "countryCode": "RU",
        "isPublic": "11",
        "phone": "+711111114"
    }
    wrong_user16 = {
        "login": "redMonkey",
        "email": "redMonkey@you.ru",
        "password": "1111111Ab",
        "countryCode": "RU",
        "isPublic": 11,
        "phone": "+711111114"
    }
    wrong_user17 = {
        "login": "redMonkey",
        "email": "redMonkey@you.ru",
        "password": "1111111Ab",
        "countryCode": "RU",
        "isPublic": "True",
        "phone": "+711111114"
    }
    wrong_user18 = {
        "login": "redMonkey",
        "email": "redMonkey@you.ru",
        "password": "1111111Ab",
        "countryCode": "RU",
        "isPublic": False,
        "phone": "+7abcdab"
    }
    wrong_user19 = {
        "login": "redMonkey",
        "email": "redMonkey@you.ru",
        "password": "1111111Ab",
        "countryCode": "RU",
        "isPublic": True,
        "phone": "+"
    }
    wrong_user20 = {
        "login": "redMonkey",
        "email": "redMonkey@you.ru",
        "password": "1111111Ab",
        "countryCode": "RU",
        "isPublic": True,
        "phone": "+7"+"11111114"*5
    }
    wrong_user21 = {
        "login": "redMonkey",
        "email": "redMonkey@you.ru",
        "password": "1111111Ab",
        "countryCode": "RU",
        "isPublic": True,
        "phone": "+711111114",
        "image": "abc"*100
    }
    wrong_user22 = {
        "login": "redMonkey",
        "email": "redMonkey@you.ru",
        "password": "1111111Ab",
        "countryCode": "RU",
        "isPublic": True,
        "phone": "+711111114",
        "image": ""
    }
    wrong_user23 = {
        "login": "redMonkey",
        "email": "redMonkey@you.ru",
        "password": "1111111Ab",
        "countryCode": "JJ",
        "isPublic": True,
        "phone": "+711111114"
    }
    wrong_user24 = {
        "login": "redMonkey",
        "email": "redMonkey@you.ru",

        "countryCode": "RU",
        "isPublic": True,
        "phone": "+711111114"
    }
    wrong_user25 = {
        "login": "redMonkey",

        "password": "1111111Ab",
        "countryCode": "RU",
        "isPublic": True,
        "phone": "+711111114"
    }
    wrong_user26 = {

        "email": "redMonkey@you.ru",
        "password": "1111111Ab",
        "countryCode": "RU",
        "isPublic": True,
        "phone": "+711111114"
    }
    wrong_user27 = {
        "login": "redMonkey",
        "email": "redMonkey@you.ru",
        "password": "1111111Ab",

        "isPublic": True,
        "phone": "+711111114"
    }
    wrong_user28 = {
        "login": "redMonkey",
        "email": "redMonkey@you.ru",
        "password": "1111111Ab",
        "countryCode": "RU",

        "phone": "+711111114"
    }
    wrong400 = [wrong_user4, wrong_user5, wrong_user6, wrong_user7, wrong_user8, wrong_user9, wrong_user10,
                     wrong_user11, wrong_user12, wrong_user13, wrong_user14, wrong_user15, wrong_user16,
                     wrong_user17, wrong_user18, wrong_user19, wrong_user20, wrong_user21, wrong_user22,
                     wrong_user23, wrong_user24, wrong_user25, wrong_user26, wrong_user27, wrong_user28]

    def test(self):
        self.correct_register()
        self.different_order()
        self.wrong_users409()
        self.wrong_users400()
        self.empty_request()

    def correct_register(self):
        for user in self.correct_users:
            response = requests.post(self.url, json=user)
            assert int(response.status_code) == 201, f"{response.status_code} when {user}\n {response.text}"
            data = response.json()
            del user["password"]
            user['countryCode'] = user['countryCode'].upper()
            correct_data = {'profile': user}

            assert data == correct_data, correct_data

    def different_order(self):
        for user, correct_user in self.different_order_users:
            response = requests.post(self.url, json=user)
            assert int(response.status_code) == 201, f"{response.status_code} when {user}\n {response.text}"
            data = response.json()
            del correct_user["password"]
            correct_data = {'profile': correct_user}
            assert data == correct_data, f"{data} when {correct_data}"

    def wrong_users409(self):
        requests.post(self.url, json=self.simple_user3)
        for user in self.wrong409:
            response = requests.post(self.url, json=user)
            assert int(response.status_code) == 409, f"{response.status_code} when {user}\n {response.text}"
            data = response.json()
            assert "reason" in data, data

    def wrong_users400(self):
        for user in self.wrong400:
            response = requests.post(self.url, json=user)
            assert int(response.status_code) == 400, f"{response.status_code} when {user}\n {response.text}"
            data = response.json()
            assert "reason" in data, data

    def empty_request(self):
        response = requests.post(self.url)
        assert int(response.status_code) == 400, f"{response.status_code} data is empty"
        data = response.json()
        assert "reason" in data, data

        response = requests.post(self.url, json="{ ")
        assert int(response.status_code) == 400, f"{response.status_code} json is incorrect"
        data = response.json()
        assert "reason" in data, data

        response = requests.post(self.url, json=" ")
        assert int(response.status_code) == 400, f"{response.status_code} json is incorrect"
        data = response.json()
        assert "reason" in data, data




print("Make Register test")
c = RegisterTest()
c.test()
print("Register tests completed")