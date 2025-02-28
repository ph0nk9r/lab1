import json
import os
import xml.etree.ElementTree as ET


class ErrorClass(Exception):
	pass


class MovieNotFoundError(ErrorClass):
	def __init__(self, movie_id):
		self.message=f"Фильм(сериал) с ID {movie_id} не найден"
		super().__init__(self.message)


class UserNotFoundError(ErrorClass):
	def __init__(self, user_id):
		self.message=f"Пользователь с ID {user_id} не найден"
		super().__init__(self.message)


class InvalidMovieDataError(ErrorClass):
	def __init__(self, message):
		super().__init__(message)


class InvalidUserDataError(ErrorClass):
	def __init__(self, message):
		super().__init__(message)


class IODataBaseError(ErrorClass):
	def __init__(self, message):
		super().__init__(message)


class FileError(ErrorClass):
	def __init__(self, filename, message):
		super().__init__(f"{filename}: {message}")


class Movie:
	def __init__(self,  name: str ,  
						duration: int, #минуты
						year_of_release: int, 
						rating: float, 
						genre: list, #жанр
						movie_id: int):

		if not isinstance(name, str):
			raise TypeError('Некорректный тип name')
		if not isinstance(duration, int):
			raise TypeError('Некорректный тип duration')
		if not isinstance(year_of_release, int):
			raise TypeError('Некорректный тип year_of_release')
		if not isinstance(rating, float):
			raise TypeError('Некорректный тип rating')
		if not isinstance(genre, list):
			raise TypeError('Некорректный тип genre')
		if not isinstance(movie_id, int):
			raise TypeError('Некорректный тип movie_id')
		
		if duration < 0:
			raise ValueError('duration должен быть больше 0')
		if year_of_release < 0:
			raise ValueError('year_of_release должен быть больше 0')
		if movie_id < 0:
			raise ValueError('movie_id должен быть больше 0')
		if rating < 0:
			raise ValueError('rating должен быть больше 0')
		

		self.__name = name
		self.__duration = duration
		self.__year_of_release = year_of_release
		self.__rating = rating
		self.__genre = genre
		self.__movie_id = movie_id


	def to_dict(self):
		data = {
						"Name":	self.__name,
					"Duration":	self.__duration,
			 "Year_of_release":	self.__year_of_release,
				 	  "Rating":	self.__rating,
					   "Genre":	self.__genre,
			        "Movie_id":	self.__movie_id,
				}
		return data

	
	def from_dict(self, data):
		self.__name = data['Name']
		self.__duration = data['Duration'] 
		self.__year_of_release = data['Year_of_release']
		self.__rating = data['Rating']
		self.__genre = data['Genre'] 
		self.__movie_id = data['movie_id']
		

class Series(Movie):
	def __init__(self,
			  	name: str,  
				duration_each_series: int,
				year_of_release: int,
				rating: float,
				genre: list,
				movie_id: int,
				amount_of_seasons: int,
				amount_of_series: int, #количество серий во всех сезонах
				):
				
		super().__init__(name, duration_each_series, 
				   year_of_release, rating, genre, movie_id)
		

		if not isinstance(amount_of_seasons, int):
			raise TypeError('Некорректный тип amount_of_seasons')
		if amount_of_seasons < 0:
			raise ValueError('amount_of_seasons должен быть больше 0')
		
		if not isinstance(amount_of_series, int):
			raise TypeError('Некорректный тип amount_of_series')
		if amount_of_series < 0:
			raise ValueError('amount_of_series должен быть больше 0')
		
		if not isinstance(duration_each_series, int):
			raise TypeError('Некорректный тип duration_each_series')
		if duration_each_series < 0:
			raise ValueError('duration_each_series должен быть больше 0')
		
		self.__amount_of_seasons = amount_of_seasons
		self.__amount_of_series = amount_of_series
		self.__duration_each_series = duration_each_series
	

	def to_dict(self):
		data = super().to_dict()
		data.update({
			   "amount_of_seasons": self.__amount_of_seasons,
			    "amount_of_series": self.__amount_of_series,
			"duration_each_series": self.__duration_each_series
		})
		return data
	

	def from_dict(self, data):
		super().from_dict(data)
		self.__amount_of_seasons = data['amount_of_seasons']
		self.__amount_of_series = data['amount_of_series'] 
		self.__duration_each_series = data['duration_each_series']
		

class User:
	def __init__(self, login: str, 
				 password : str, 
				 email: str, 
				 user_id: int):

		if not isinstance(login, str):
			raise TypeError('Некорректный тип login')
		if not isinstance(password, str):
			raise ValueError('Некорректный тип password')

		if len(login) == 0:
			raise ValueError('login должен существовать. Введите login.')

		self.__login = login
		
		if len(password) == 0:
			raise ValueError('password должен существовать. Введите password.')

		self.__password = password

		self.__email = email

		if user_id < 0:
			raise ValueError('user_id должен быть больше 0')

		self.__user_id = user_id


	def to_dict(self):
		data = {
			   "login": self.__login,
			"password": self.__password,
			   "email": self.__email,
			 "user_id": self.__user_id
			   }
		return data
	

	def from_dict(self, data):
		self.__login = data['login']
		self.__password = data['password']
		self.__email = data['email']
		self.__user_id = data['user_id']


class File:
	def __init__(self, filename: str, read: bool, binary: bool):
		if not read:
			if (os.path.isfile(filename)):
				os.remove(filename)	
			self._file = open(filename, "wb" if binary else "w")
		else:
			self._file = open(filename, "rb" if binary else "r")


	def file(self):
		return self._file
	

	def close(self):
		self._file.close()
		pass


class JSONFile(File):
	def __init__(self, filename: str, read: bool):
		if not filename:
			raise FileError(filename, "Невозможно создать файл с таким именем") 
		if not (filename[-5:] == '.json'):
			filename += '.json'
		File.__init__(self, filename, read, False)

			
class XMLFile(File):
	def __init__(self, filename: str, read: bool):
		if not filename:
			raise FileError(filename, "Невозможно создать файл с таким именем")
		if not (filename[-4:] == '.xml'):
			filename += '.xml'
		File.__init__(self, filename, read, True)
		

class CinemaDatabase:
	def __init__(self, filename: str):
		self.__filename = filename
		self.__movies = {}


	def add_movie(self, movie: Movie):
		id_mov = movie.to_dict()['movie_id']
		if id_mov in self.__movies:
			raise InvalidMovieDataError(
				f"Фильм {id_mov} уже существует"
			)
		self.__movies[id_mov] = movie


	def get_movie(self, movie_id: int):
		if movie_id not in self.__movies:
			raise MovieNotFoundError(movie_id)
		return self.__movies[movie_id]


	def update_movie(self, movie_id: int, movie: Movie):
		if movie_id not in self.__movies:
			raise MovieNotFoundError(movie_id)
		self.__movies[movie_id] = movie


	def delete_movie(self, movie_id: int):
		if movie_id not in self.__movies:
			raise MovieNotFoundError(movie_id)
		self.__movies.pop(movie_id)


	def to_json(self):
		data = {f"ID:{movie_id}": movie.to_dict()
			for movie_id, movie in self.__movies.items()}
		with JSONFile(self.__filename, read=False).file() as file:
			json.dump(data, file, indent=4)


	def from_json(self, obj: 'CinemaDatabase' = None):
		if obj is None:
			raise IODataBaseError("Нет объекта для записи")
		
		file = JSONFile(obj.__filename, read=True).file()
		data = json.load(file)

		for cinema_ID, cinema_data in data.items():
			if 'amount_of_series' in cinema_data:
				movie = Series()
			elif 'Duration' in cinema_data:
				movie = Movie()
			else:
				continue
			
			self.add_movie(movie)
		file.close()


	def __dict_to_xml(self, tag, d):
		elem = ET.Element(str(tag))
		for key, val in d.items():
			child = ET.SubElement(elem, str(key))
			if isinstance(val, dict):
				child.append(self.__dict_to_xml(key, val))
			else:
				child.text = str(val) 
		return elem


	def to_xml(self):
		file = XMLFile(self.__filename, read=False).file()
		data = {f"ID_movie_{movie_id}": movie.to_dict()
			for movie_id, movie in self.__movies.items()}
		xml_element = self.__dict_to_xml("root", data)
		tree = ET.ElementTree(xml_element)
		ET.indent(tree, "  ")
		tree.write(file, encoding="utf-8", xml_declaration=True)
		file.close()


	def from_xml(self, obj: 'CinemaDatabase' = None):
		if obj == None:
			raise IODataBaseError("Нет объекта для записи")
		
		file = XMLFile(obj.__filename, read=True).file()
		tree = ET.parse(file)
		root = tree.getroot()

		file.close()


class UsersDatabase:
	def __init__(self, filename: str):
		self.__filename = filename
		self.__users = {}


	def add_user(self, user: User):
		id_user = user.to_dict()['user_id']
		if id_user in self.__users:
			raise InvalidUserDataError(
				f"Пользователь {id_user} уже существует"
			)
		self.__users[id_user] = user


	def get_user(self, user_id: int) -> User:
		if user_id not in self.__users:
			raise UserNotFoundError(user_id)
		return self.__users[user_id]


	def update_user(self, user_id: int, user: User):
		if user_id not in self.__users:
			raise UserNotFoundError(user_id)
		self.__users[user_id] = user


	def delete_user(self, user_id: int):
		if user_id not in self.__users:
			raise UserNotFoundError(user_id)
		self.__users.pop(user_id)


	def to_json(self):
		file = JSONFile(self.__filename, read=False).file()
		data = {f"ID:{user_id}": user.to_dict()
			for user_id, user in self.__users.items()}
		json.dump(data, file, indent=4)
		file.close()
	

	def from_json(self, obj: 'UsersDatabase' = None):
		if obj is None:
			raise IODataBaseError("Нет объекта для записи")
		file = JSONFile(obj.__filename, read=True).file()
		data = json.load(file)
		for user_ID, user_data in data.items():
			if 'user_id' in user_data:
				user = User()
			else:
				continue
			user.from_dict(user_data)
			self.add_user(user)
		file.close()
	

	def __dict_to_xml(self, tag, d):
		elem = ET.Element(str(tag))
		for key, val in d.items():
			child = ET.SubElement(elem, str(key))
			if isinstance(val, dict):
				child.append(self.__dict_to_xml(key, val))
			else:
				child.text = str(val) 
		return elem
		

	def to_xml(self):
		file = XMLFile(self.__filename, read=False).file()
		data = {f"ID_user_{user_id}": user.to_dict()
			for user_id, user in self.__users.items()}
		xml_element = self.__dict_to_xml("root", data)
		tree = ET.ElementTree(xml_element)
		ET.indent(tree, "  ")
		tree.write(file, encoding="utf-8", xml_declaration=True)
		file.close()


	def from_xml(self, obj: 'UsersDatabase' = None):
		if obj is None:
			raise IODataBaseError("Нет объекта для записи")
		
		file = XMLFile(obj.__filename, read=True).file()
		tree = ET.parse(file)
		root = tree.getroot()
		file.close()



def main():
	cinemaDB1 = CinemaDatabase("cinemaDB1")
	cinemaDB2 = CinemaDatabase("cinemaDB2")
	userDB1 = UsersDatabase("userDB1")

	movie1 = Movie("Interstellar", 169, 2014, 8.3, 
					["fantastic","drama","adventure"], 1)
	movie2 = Movie("The Shawshank Redemption", 144, 1994, 8.2, ["drama"], 2)
	movie3 = Movie("Shutter Island", 140, 2009, 8.1, 
					["thriller", "detective", "drama"], 3)
	movie4 = Movie("The Green Mile", 189, 1999, 8.1, 
					["drama", "fantasy", "crime"], 4)
	movie5 = Movie("Intouchables", 112, 2011, 8.4, ["drama", "comedy"], 5)
	movie6 = Movie("The Gentlemen", 113, 2019, 8.1, 
				["crime", "comedy", "action"], 6)
	movie7 = Movie("Fight Club", 139, 1999, 8.1, 
				["thriller", "drama", "crime"], 7)
	movie8 = Movie("The Lord of the Rings: The Return of the King", 201, 2003, 
					8.1, ["fantasy","adventure", "drama", "action"], 8)
	movie9 = Movie("Forrest Gump", 142, 1994, 8.0, 
					["drama", "comedy", "melodrama", "story", "military"], 9)
	movie10 = Movie("Gladiator", 155, 2000, 7.9, 
				 ["story", "action", "drama"], 10)
	series1 = Series("Game of Thrones", 55, 2011, 8.4,
			[
			"fantasy", "drama", 	
			"action", "melodrama", "adventure"
			 ], 
			 11, 8, 80)
	series2 = Series("Breaking Bad", 47, 2008, 8.3,
				  ["crime", "drama", "thriller"], 12, 5, 62)
	series3 = Series("Better Call Saul", 45, 2015, 7.8,["drama", "crime"], 
				  13, 6, 63)
	user1 = User("msk24", "11223344", "ivan2004@mail.ru", 1)


	userDB1.add_user(user1)
	cinemaDB1.add_movie(movie1)
	cinemaDB1.add_movie(movie2)
	cinemaDB1.add_movie(movie3)
	cinemaDB1.add_movie(movie4)
	cinemaDB1.add_movie(movie5)
	cinemaDB1.add_movie(movie6)
	cinemaDB1.add_movie(movie10)
	cinemaDB1.add_movie(series1)
	cinemaDB1.add_movie(series2)
	cinemaDB1.add_movie(series3)
	cinemaDB1.update_movie(10, movie9)


	cinemaDB1.to_json()
	#cinemaDB2.from_json(cinemaDB1)
	cinemaDB1.to_xml()

	
	#cinemaDB1.delete_movie(10)

	cinemaDB2.to_json()
	cinemaDB2.to_xml()
	userDB1.to_json()
	userDB1.to_xml()



try:
	main()
except IOError as e:
	print(f"Невозможно открыть файл {e}")
except FileError as e:
	print(e)
except MovieNotFoundError as e: 
	print(e)
except IODataBaseError as e:
	print(f"Ошибка в базе данных {e}")
except InvalidMovieDataError as e:
	print(f"Некорректные данные для транспорта {e}")
except Exception as e:
	print(e)
except Exception as e:
	print("Неизвестная ошибка")