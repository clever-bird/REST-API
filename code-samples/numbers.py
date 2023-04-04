import requests


class Numbers:
    def __init__(self, url: str):
        self.url = url

    def get_fact(self, number: int = 42):
        """
        Get fact about number
        :param number:
        :return:
        """
        response = requests.get(f"{self.url}/{str(number)}")
        return response.text

    def get_random_year_fact(self):
        """
        Get random fact about year
        :param number:
        :return:
        """
        response = requests.get(f"{self.url}/random/year")
        return response.text

    def get_random_date_fact(self):
        """
        Get random fact about date
        :return:
        """
        response = requests.get(f"{self.url}/random/date")
        return response.text


if __name__ == '__main__':
    # Создание экземпляра класса
    client = Numbers(url='http://numbersapi.com')
    # Случайный факт о числе 42
    print(client.get_fact(42))

    # Случайный факт о годе
    print(client.get_random_year_fact())

    # Случайный факт о дате
    print(client.get_random_date_fact())
