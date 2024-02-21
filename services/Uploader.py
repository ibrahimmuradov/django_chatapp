
class Upload_to:
    @staticmethod
    def user_file(objName, fileName):
        return f'userFiles/{objName.user.username}/{fileName}'

    @staticmethod
    def user_profile_photo(objName, fileName):
        return f'userProfilePhoto/{objName.username}/{fileName}'
