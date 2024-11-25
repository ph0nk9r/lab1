import json
import os
import array
import xml.etree.ElementTree as ET


        

class movie:
        def __init__(self, name: str = "", 
                     Leading_actors: array = [], 
                     Duration: int = 0, 
                     Year_of_release: int = 0, 
                     MPAA_rating: str = "", 
                     Genre: array = [], 
                     Country_of_production: str = "",
                     movie_id: int = 0):


                self.__name = name
                self.__Leading_actors = Leading_actors
                self.__Duration = Duration
                self.__Year_of_release = Year_of_release
                if not MPAA_rating in ["G", "PG", "PG-13", "R", "NC-17"]:
			                raise ValueError('MPAA_rating должен быть соответсвующего значения рейтинга: "G", "PG", "PG-13", "R", "NC-17"')
                self.__MPAA_rating = MPAA_rating
                self.__Genre = Genre
                self.__Country_of_production = Country_of_production

                if movie_id < 0:
			                raise ValueError('movie_id должен быть больше 0')
                self._movie_id = movie_id

        def get_movie_id(self):
		        return self._movie_id

                
class user:
        def __init__(self, login: str = "" , password : str = "" , email: str = "", user_id: int = 0):
                
                self.__login = login
                self.__password = password
                self.__email = email

                if user_id < 0:
			                raise ValueError('user_id должен быть больше 0')
                self._user_id = user_id

                


class series(movie):
        def __init__(self, 
                amount_of_seasons: int = 0,
                amount_of_series: int = 0):

                self.__amount_of_seasons = amount_of_seasons
                self.__amount_of_series = amount_of_series