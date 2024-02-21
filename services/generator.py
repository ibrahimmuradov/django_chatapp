import string
import random

letter_chars = string.ascii_letters
mix_chars = string.digits + string.ascii_letters

class CodeGenerator:
    @staticmethod
    def code_link_generator(size, chars=mix_chars):
        return "".join(random.choice(chars) for _ in range(size))

    @classmethod
    def create_activation_link_code(cls, size, model_):
        new_code = cls.code_link_generator(size=size)
        qs_exists = model_.objects.filter(slug=new_code).exists()
        return cls.create_activation_link_code(size, model_) if qs_exists else new_code

    @classmethod
    def file_name_generator(cls, size, chars=letter_chars):
        return "".join(random.choice(chars) for _ in range(size))

    @classmethod
    def create_key(cls, size, model_):
        new_key = cls.code_link_generator(size=size)
        key_exists = model_.objects.filter(token_key=new_key).exists()
        return cls.create_key(size, model_) if key_exists else new_key