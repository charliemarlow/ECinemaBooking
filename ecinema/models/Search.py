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
        movies = self.__data_access.search_movies(self.__date, self.__category, self.__term)
        if len(movies) > 0:
            return self.process_results(movies), None
        else:
            if self.__term == '' and self.__category is None and self.__date == '':
                error = "At least one search field must be filled"
            else:
                # check here to find movies
                # SELECT * from movie WHERE status = "inactive" AND title LIKE "%term%"
                # return a list of movies
                # add something to the template that checks if
                # there are showtimes (maybe 3 return types?)
                # and shows coming soon instead if thats the case
                error = "No movies found"
            return None, error


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

