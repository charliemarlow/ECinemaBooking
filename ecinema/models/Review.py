
from ecinema.models.model import Model
from ecinema.data.ReviewData import ReviewData


class Review(Model):

    def __init__(self):
        self.__id = None

        self.__customer_id = None
        self.__movie_id = None
        self.__rating = None
        self.__subject = None
        self.__review = None
        self._Model__is_init = False
        self._Model__id = None
        self.__data_access = ReviewData()

    def obj_as_dict(self, key: str):
        return self.__data_access.get_info(key)

    def get_all_reviews_by_movie(self, mid):
        return self.__data_access.get_all_reviews_by_movie(mid)

    def get_customer_name(self, cid):
        first, last = self.__data_access.get_name(cid)
        print(first)
        print(last)
        return first + " " + last[0]

    def fetch(self, key: str):
        review = self.obj_as_dict(key)

        if review is not None:
            self.set_id(review[review_id])

            self.set_customer_id(review['customer_id'])
            self.set_movie_id(review['movie_id'])
            self.set_rating(review['rating'])
            self.set_subject(review['subject'])
            self.set_review(review['review'])
            self.set_is_init()

            return True

        return False

    def create(self, **kwargs):
        review = {}
        for key, value in kwargs.items():
            review[key] = value

        self.set_customer_id(review['customer_id'])
        self.set_movie_id(review['movie_id'])
        self.set_rating(review['rating'])
        self.set_subject(review['subject'])
        self.set_review(review['review'])
        self.set_is_init()

        member_tup = (self.get_customer_id(),
                      self.get_movie_id(),
                      self.get_rating(),
                      self.get_subject(),
                      self.get_review())

        self.set_id(self.__data_access.insert_info(member_tup))

    def save(self) -> bool:
        if not self.is_initialized():
            return False

        member_tup = (
            self.get_customer_id(),
            self.get_movie_id(),
            self.get_rating(),
            self.get_subject(),
            self.get_review(),
            self.get_id())

        self.__data_access.update_info(member_tup)
        return True

    def delete(self, key: str):
        self.__data_access.delete(key)

    def get_customer_id(self) -> str:
        return self.__customer_id

    def set_customer_id(self, customer_id: str):
        self.__customer_id = customer_id

    def get_movie_id(self) -> str:
        return self.__movie_id

    def set_movie_id(self, movie_id: str):
        self.__movie_id = movie_id

    def get_rating(self) -> int:
        return self.__rating

    def set_rating(self, rating: int):
        self.__rating = rating

    def get_subject(self) -> str:
        return self.__subject

    def set_subject(self, subject: str):
        self.__subject = subject

    def get_review(self) -> str:
        return self.__review

    def set_review(self, review: str):
        self.__review = review
