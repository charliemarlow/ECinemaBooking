from ecinema.data.db import get_db

class SearchData():

    def __init__(self):
        self.__db = get_db()
        self.__select = 'SELECT movie.movie_id, title, category, picture, video, rating, status, time FROM movie NATURAL JOIN showtime WHERE '

    def search_movies(self, date, category, term):
        args = []
        if term != '' and term is not None:
            args.append(self.get_title_arg(term))

        if date != '' and date is not None:
            args.append(self.get_date_arg(date))

        if category is not None and category != '':
            args.append(self.get_category_arg(category))

        search_arg = self.create_search_arg(args)
        return self.__db.execute(search_arg).fetchall()


    def create_search_arg(self, args):
        first = True
        final_arg = ''
        for arg in args:
            if first:
                final_arg = self.__select + arg
                first = False
            else:
                final_arg = final_arg + " AND " + arg
        print(final_arg)
        return final_arg

    def get_title_arg(self, term):
        return 'title LIKE "%{}%"'.format(term)

    def get_date_arg(self, date):
        return 'date(time) = "{}"'.format(date)

    def get_category_arg(self, category):
        return 'category = "{}"'.format(category)
