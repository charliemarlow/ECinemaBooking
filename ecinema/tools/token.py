from itsdangerous import URLSafeTimedSerializer


def generate_confirmation_token(email):
    serializer = URLSafeTimedSerializer('IAMSOFLUBINSECUREuuKEY')
    return serializer.dumps(email,
                            salt='THl72DfWa36wdEPJOEGbe71GSCDWADuuSALT')


def confirm_token(token, expiration=1200):
    serializer = URLSafeTimedSerializer('IAMSOFLUBINSECUREuuKEY')
    try:
        email = serializer.loads(
            token,
            salt='THl72DfWa36wdEPJOEGbe71GSCDWADuuSALT',
            max_age=expiration
        )
    except BaseException:
        return False
    return email
