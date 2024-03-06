import requests


class CountryTest:
    url = "http://localhost:8080/api"

    variable_1 = "AF"  # Asia
    variable_2 = "AX"  # Europe
    variable_3 = "PW"  # Oceania region
    variable_4 = "ES"  # Europe

    def test(self):

        # Надо реализовать еще проверку списка
        self.all_list()
        self.one_region()
        self.few_region()
        self.wrong_region()

    def all_list(self):
        response = requests.get(f"{self.url}/countries")

        assert int(response.status_code) == 200
        data = response.json()
        assert self.variable_1 in map(lambda x: x['alpha2'], data)
        assert self.variable_2 in map(lambda x: x['alpha2'], data)
        assert self.variable_3 in map(lambda x: x['alpha2'], data)
        assert self.variable_4 in map(lambda x: x['alpha2'], data)

    def one_region(self):
        response = requests.get(f"{self.url}/countries?region=Europe")
        assert int(response.status_code) == 200
        data = response.json()
        assert self.variable_1 not in map(lambda x: x['alpha2'], data), data
        assert self.variable_2 in map(lambda x: x['alpha2'], data), data
        assert self.variable_3 not in map(lambda x: x['alpha2'], data), data
        assert self.variable_4 in map(lambda x: x['alpha2'], data), data


    def wrong_region(self):
        response = requests.get(f"{self.url}/countries?region=Eure")
        assert int(response.status_code) == 400
        data = response.json()
        assert "reason" in data

        response = requests.get(f"{self.url}/countries?region=Europe&region=haha")
        assert int(response.status_code) == 400
        data = response.json()
        assert "reason" in data

        # response = requests.get(f"{self.url}/countries?")
        # assert int(response.status_code) == 400
        # data = response.json()
        # assert "reason" in data

    def few_region(self):
        response = requests.get(f"{self.url}/countries?region=Europe&region=Asia")
        assert int(response.status_code) == 200
        data = response.json()
        assert self.variable_1 in map(lambda x: x['alpha2'], data)
        assert self.variable_2 in map(lambda x: x['alpha2'], data)
        assert self.variable_3 not in map(lambda x: x['alpha2'], data)
        assert self.variable_4 in map(lambda x: x['alpha2'], data)



class CountryOneTest:
    url = "http://localhost:8080/api"

    variable_1 = "AF"  # Asia
    variable_2 = "AX"  # Europe
    variable_3 = "PW"  # Oceania
    variable_4 = "ES"  # Europe

    def test(self):
        self.correct_request()
        self.wrong_request()
        self.lower_or_upper()
        self.region_null()

    def correct_request(self):
        response = requests.get(f"{self.url}/countries/{self.variable_1}")
        assert int(response.status_code) == 200
        data = response.json()
        assert self.variable_1 == data['alpha2']
        assert "Asia" == data['region']

        response = requests.get(f"{self.url}/countries/{self.variable_2}")
        assert int(response.status_code) == 200
        data = response.json()
        assert self.variable_2 == data['alpha2']
        assert "Europe" == data['region']

        response = requests.get(f"{self.url}/countries/{self.variable_3}")
        assert int(response.status_code) == 200
        data = response.json()
        assert self.variable_3 == data['alpha2']
        assert "Oceania" == data['region']

        response = requests.get(f"{self.url}/countries/{self.variable_4}")
        assert int(response.status_code) == 200
        data = response.json()
        assert self.variable_4 == data['alpha2']
        assert "Europe" == data['region']

    def wrong_request(self):
        response = requests.get(f"{self.url}/countries/dd")
        assert int(response.status_code) == 404
        data = response.json()
        assert "reason" in data

        response = requests.get(f"{self.url}/countries/RUUUUUUUUUU")
        assert int(response.status_code) == 404
        data = response.json()
        assert "reason" in data

        # response = requests.get(f"{self.url}/countries/RU?alpha2=RU")
        # assert int(response.status_code) == 400
        # data = response.json()
        # assert "reason" in data
        #
        # response = requests.get(f"{self.url}/countries/RU?region=Europe")
        # assert int(response.status_code) == 400
        # data = response.json()
        # assert "reason" in data

    def lower_or_upper(self):
        response = requests.get(f"{self.url}/countries/{self.variable_1}")
        assert int(response.status_code) == 200
        data = response.json()
        assert self.variable_1 == data['alpha2']
        assert "Asia" == data['region']

        response = requests.get(f"{self.url}/countries/{self.variable_1.lower()}")
        assert int(response.status_code) == 200
        data2 = response.json()
        assert self.variable_1 == data['alpha2']
        assert "Asia" == data['region']

        assert data2 == data

    def region_null(self):
        response = requests.get(f"{self.url}/countries/st")
        assert int(response.status_code) == 200
        data = response.json()
        correct_data = {"name": "Sao Tome and Principe", "alpha2": "ST", "alpha3": "STP", "region": "Africa"}
        assert data == correct_data, data


print("Make country test")
c = CountryTest()
c.test()
print("Country tests completed")

print("Make ONEcountry test")
c = CountryOneTest()
c.test()
print("OneCountry tests completed")