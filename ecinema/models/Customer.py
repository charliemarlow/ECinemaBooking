from ecinema.tools.sendEmail import send_email
from ecinema.models.User import User
from ecinema.models.model import Model
from ecinema.data.CustomerData import CustomerData


class Customer(Model, User):
    # idea: EmailTemplate DB table

    def __init__(self):
        self.__id = None
        self.__first_name = None
        self.__last_name = None
        self.__email = None
        self.__phone = None
        self.__subscribed = None
        self.__username = None
        self.__password = None
        self.__status = None
        self.__address_id = None
        self._Model__is_init = False
        self.__data_access = CustomerData()

    def obj_as_dict(self, key: str):
        return self.__data_access.get_info(key)

    def fetch(self, key: str) -> bool:
        user_data = self.obj_as_dict(key)
        if user_data is not None:
            self.set_id(user_data['customer_id'])
            self.set_first_name(user_data['first_name'])
            self.set_last_name(user_data['last_name'])
            self.set_email(user_data['email'])
            self.set_phone(user_data['phone_number'])
            self.set_promo(user_data['subscribe_to_promo'])
            self.set_username(user_data['username'])
            self.set_password(user_data['password'])
            self.set_status(user_data['status'])
            self.set_address_id(user_data['address_id'])
            self.set_is_init()
            return True

        return False

    def fetch_by_email(self, email: str):
        user_data = self.__data_access.get_info_by_email(email)
        if user_data is not None:
            self.set_id(user_data['customer_id'])
            self.set_first_name(user_data['first_name'])
            self.set_last_name(user_data['last_name'])
            self.set_email(user_data['email'])
            self.set_phone(user_data['phone_number'])
            self.set_promo(user_data['subscribe_to_promo'])
            self.set_username(user_data['username'])
            self.set_password(user_data['password'])
            self.set_status(user_data['status'])
            self.set_address_id(user_data['address_id'])
            self.set_is_init()
            return True

        return False

    def get_all_cards(self):
        # eventually, fetch all the credit cards
        # and pass back a list of the objects
        return self.__data_access.get_cards(self.get_id())

    def create(self, **kwargs):
        user = {}
        for key, value in kwargs.items():
            user[key] = value

        self.set_first_name(user['first_name'])
        self.set_last_name(user['last_name'])
        self.set_email(user['email'])
        self.set_phone(user['phone'])
        promo = (True if user['subscribe_to_promo'] == 'True'
                 else False)
        self.set_promo(promo)
        self.set_username(user['username'])
        self.set_password(user['password'])
        self.set_status('inactive')

        if 'address_id' in user:
            self.set_address_id(user['address_id'])

        self.set_is_init()

        member_tup = (self.get_first_name(), self.get_phone(),
                      self.get_last_name(), self.get_email(),
                      self.get_promo(), self.get_username(),
                      self.get_password(), self.get_status()
                      )
        # set your id
        self.set_id(self.__data_access.insert_info(member_tup))

    # this is more of an update function
    # create saves automatically

    def save(self) -> str:
        if not self.is_initialized():
            return False
        # last item is a key for the UPDATE call
        member_tup = (self.get_first_name(),
                      self.get_last_name(),
                      self.get_email(),
                      self.get_promo(),
                      self.get_username(),
                      self.get_password(),
                      self.get_phone(),
                      self.get_status(),
                      self.get_address_id(),
                      self.get_id())
        self.__data_access.update_info(member_tup)
        return True

    def is_admin(self) -> bool:
        return False

    def get_first_name(self) -> str:
        return self.__first_name

    def set_first_name(self, first: str):
        self.__first_name = first

    def get_last_name(self) -> str:
        return self.__last_name

    def set_last_name(self, last: str):
        self.__last_name = last

    def get_email(self) -> str:
        return self.__email

    def set_email(self, email: str):
        self.__email = email

    def get_promo(self) -> bool:
        return self.__subscribed

    def set_promo(self, promo: bool):
        self.__subscribed = promo

    def get_status(self):
        return self.__status

    def set_status(self, status):
        self.__status = status

    def get_address_id(self) -> str:
        return self.__address_id

    def set_address_id(self, addr_id: str):
        self.__address_id = addr_id

    def set_phone(self, phone: str):
        self.__phone = phone

    def get_phone(self):
        return self.__phone

    def send_profile_change_email(self):
        email = self.get_email()
        subject = "Profile Change Notification"

        message = """Hey {},

        Your profile information was just changed at E-Cinema Booking. """\
            + """If you did not authorize this, please reset your """\
            + """password using the forgot my password feature """\
            + """at the login page"""\
            + """

Best,

E-Cinema Booking
        """
        message = message.format(self.get_first_name())
        send_email(email, subject, message)

    def send_password_reset_email(self, email: str, name: str):
        subject = "Password Change Notification"

        message = """Hey {},

        Your password was just reset at E-Cinema Booking. """\
            + """If you did not authorize this, please reset your """\
            + """password using the forgot my password feature """\
            + """at the login page"""\
            + """

Best,

E-Cinema Booking
        """
        message = message.format(name)
        send_email(email, subject, message)

    def send_confirmation_email(self, email: str, name: str, username: str, token: str):
        subject = "Registration Confirmation"

        message = """Hey {},

        You have successfully registered an account at E-Cinema """\
            + """Booking under this email address.
            Your account ID is {}

            """\
            + """Please verify your account at this link: {} """\
            + """ -- some account information will be unavailable"""\
            + """ until you do so. """\
            + """We're looking """\
            + """forward to seeing you soon!"""\
            + """

Best,

E-Cinema Booking
        """
        url = "http://127.0.0.1:5000/confirm_account/" + token
        message = message.format(name, username, url)

        send_email(email, subject, message)
