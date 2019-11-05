from ecinema.models.model import Model
from ecinema.data.MovieData import MovieData

class Movie(Model):

    def __init__(self):
        self.__id = None
        self.__title = None
        self.__category = None
        self.__director = None
        self.__producer = None
        self.__synopsis = None
        self.__picture = None
        self.__video = None
        self.__duration = None
        self.__rating = None
        self._Model__is_init = False
        self._Model__id = None
        self.__data_access = MovieData()

    def obj_as_dict(self, key: str):
        return self.__data_access.get_info(key)

    def get_all_movies(self):
        return self.__data_access.get_all_movies()

    def fetch(self, key: str):
        movie = self.obj_as_dict(key)

        if movie is not None:
            self.set_id(movie['movie_id'])
            self.set_title(movie['title'])
            self.set_category(movie['category'])
            self.set_director(movie['director'])
            self.set_producer(movie['producer'])
            self.set_synopsis(movie['synopsis'])
            self.set_picture(movie['picture'])
            self.set_video(movie['video'])
            self.set_duration(movie['duration_as_minutes'])
            self.set_rating(movie['rating'])
            self.set_is_init()
            
            return True

        return False

    def create(self, **kwargs):
        movie = {}
        for key, value in kwargs.items():
            movie[key] = value

        self.set_title(movie['title'])
        self.set_category(movie['category'])
        self.set_director(movie['director'])
        self.set_producer(movie['producer'])
        self.set_synopsis(movie['synopsis'])
        self.set_picture(movie['picture'])
        self.set_video(movie['video'])
        self.set_duration(movie['duration_as_minutes'])
        self.set_rating(movie['rating'])
        self.set_is_init()

        member_tup = (self.get_title(), self.get_category(),
                      self.get_director(), self.get_producer(),
                      self.get_synopsis(), self.get_picture(),
                      self.get_video(), self.get_duration(),
                      self.get_rating())

        self.set_id(self.__data_access.insert_info(member_tup))

    def save(self) -> bool:
        if not self.is_initialized():
            return False

        member_tup = (self.get_title(), self.get_category(),
                      self.get_director(), self.get_producer(),
                      self.get_synopsis(), self.get_picture(),
                      self.get_video(), self.get_duration(),
                      self.get_rating(), self.get_id())

        self.__data_access.update_info(member_tup)
        return True

    def delete(self, key: str):
        self.__data_access.delete(key)

    def get_title(self) -> str:
        return self.__title

    def set_title(self, title: str):
        self.__title = title

    def get_category(self) -> str:
        return self.__category

    def set_category(self, category: str) -> str:
        self.__category = category

    def get_director(self) -> str:
        return self.__director

    def set_director(self, director: str) -> str:
        self.__director = director

    def get_producer(self) -> str:
        return self.__producer

    def set_producer(self, producer: str):
        self.__producer = producer

    def get_synopsis(self) -> str:
        return self.__synopsis

    def set_synopsis(self, synopsis: str):
        self.__synopsis = synopsis

    def get_picture(self) -> str:
        return self.__picture

    def set_picture(self, picture: str):
        self.__picture = picture

    def get_video(self) -> str:
        return self.__video

    def set_video(self, video: str):
        self.__video = video

    def get_duration(self) -> int:
        return self.__duration

    def set_duration(self, duration: int):
        self.__duration = duration

    def get_rating(self) -> str:
        return self.__rating

    def set_rating(self, rating: str):
        self.__rating = rating
