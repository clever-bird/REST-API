'''
Class Recipes 
Создан командой "Dream Team" в рамка проекта Data Scientist. Project 04 "REST-API" Школы 21 Сбербанка
Класс предназначен для взаимодействия с API сайта https://spoonacular.com
Для Телеграм-бота CookingBot (@spoonacular_ds04_bot)

   Конструктор класса принимает один параметр типа string, содержащий ключ для доступа к API сайта

1. Метод get_random_recipe()
   Возвращает ссылку на случайный рецепт или сообщение об ошибке.

2. Метод get_recipe(string)
   Возвращает ссылку на рецепт по запросу на естественном языке/названию


3. Метод get_recipe_by(ingredients)
   Возвращает сслыку на рецепт по его ингредиентам. Работает только с ингредиентами состоящими
   из одного слова.
   ingredients : строка с ингредиентами через запятую или список таких строк.
   Корректные вызовы: 
    get_recipe_by("milk,eggs,cheese") 
    get_recipe_by(["milk" , "eggs" , "cheese"])
    get_recipe_by(["milk , eggs" , "cheese"])
'''

import requests
import json
import random

class MyError(Exception):
  def __init__(arg):
    self.msg = arg

class Recipes:
    def __init__(self, apikey: str):
        self.url_api = 'https://api.spoonacular.com/recipes'
        self.default_param = {
            "apiKey":apikey,
            "number":1
        }


    @staticmethod
    def isOK(response):
      if (response.status_code == 401):
          raise MyError("Invalid recipes API token")
      if (response.status_code // 100 == 4):
          raise MyError("Bad request")
      if (response.status_code //100 == 5):
          raise MyError("Service unavailable")
      if (response.status_code == 200):
          return True
      else:
          return False

    def get_recipe(self, query:str = "pasta"):
        """
        Get 1 random recipe satisfying the query
        :param query: string with natural language query for recipe search
        :return:  url to recipe or error message
        """
        cur_param = dict({
                          "query":query,
                          "sort":"random",
                          "addRecipeInformation":True
                          },
                          **self.default_param
                        )

        response = requests.get(f"{self.url_api}/complexSearch", params = cur_param)
        url_recip = None
        try:
          if (Recipes.isOK(response)):
            url_recip = json.loads(response.text)['results'][0]['spoonacularSourceUrl']
            return url_recip
          else:
            return("error!")
        except MyError as ex:
          return "Error! " + ex.msg
        except Exception as ex:
          return "Oops! Something happened..."


    def get_recipe_by(self, ingredients):
        """
        Get recipe by composition. In general returns one random recipe with
        some of ingredients but trying to use the whole bunch
        :param ingredients:  comma separated list of ingredients(string)
        :return: url to recipe or error message
        """
        offset = random.randint(1,99)
        if not isinstance(ingredients, list):
          l = []
          l.append(ingredients)
          ingredients = l
        ingredients = [x.replace(" ", "") for x in ingredients]
        cur_param = {
                          "query":"",
                          "includeIngredients":",".join(ingredients),
                          "sort":"max-used-ingredients",
                          "addRecipeInformation":True,
                          "number":1,
                          "apiKey":self.default_param["apiKey"],
                          "offset":offset
                  }
        response = requests.get(f"{self.url_api}/complexSearch", params = cur_param)
        url_recip = None
        try:
          if (Recipes.isOK(response)):
            url_recip = json.loads(response.text)['results'][0]['spoonacularSourceUrl']
            return url_recip
          else:
            return("error!")
        except MyError as ex:
          return "Error! " + ex.msg
        except Exception as ex:
          return "Oops! Something happened..."
        

    def get_random_recipe(self):
        """
        Get random recipe.
        :return: url to recipe or error message.
        """
        response = requests.get(f"{self.url_api}/random", params = self.default_param)
        try:
          if (Recipes.isOK(response)):
            return json.loads(response.text)["recipes"][0]['spoonacularSourceUrl']
          else:
            return("error!")
        except MyError as ex:
          return "Error! " + ex.msg
        except Exception as ex:
          return "Oops! Something happened..."
