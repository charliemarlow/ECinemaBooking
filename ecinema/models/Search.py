from ecinema.data.SearchData import SearchData
from ecinema.tools.clean import create_datetime_from_sql

class Search():

    def __init__(self):
        self.__term = ''
        self.__category = None
        self.__date = ''
        self.__data_access = SearchData()

    def set_category(self, category):
        self.__category = category

    def set_date(self, date):
        self.__date = date

    def set_term(self, term):
        self.__term = term

    def execute(self):
        coming_soon = []

        movies = self.__data_access.search_movies(self.__date, self.__category, self.__term)
        if self.__date == '' or self.__date is None:
            coming_soon = self.__data_access.search_coming_soon(self.__category, self.__term)

        if len(movies) <= 0 and len(coming_soon) <= 0:
            if self.__term == '' and self.__category is None and self.__date == '':
                error = "At least one search field must be filled"
            else:
                error = "No movies found"
            return None, error

        if len(movies) > 0:
            movies = self.process_results(movies)
        else:
            movies = []

        if len(coming_soon) > 0:
            coming_soon = self.process_coming_soon(coming_soon)

        for movie in coming_soon:
            movies.append(movie)

        return movies, None

    def process_coming_soon(self, coming):
        movies = []
        single_movie = []

        for movie in coming:
            movie = dict(movie)
            movie['time'] = None
            single_movie = [movie]
            movies.append(single_movie)
        return movies

    def process_results(self, results):
        curr_id = results[0]['movie_id']
        single_movie = []
        all_movies = []

        movies = sorted(results, key=lambda k: k['time'])

        for mov in movies:
            mov = dict(mov)
            mov['time'] = create_datetime_from_sql(mov['time'])
            if curr_id != mov['movie_id']:
                all_movies.append(list(single_movie))
                curr_id = mov['movie_id']
                single_movie.clear()

            single_movie.append(mov)

        all_movies.append(single_movie)
        return all_movies

