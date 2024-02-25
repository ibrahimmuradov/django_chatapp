
def message_type(message_obj=None):
    music_types = ['mp3', 'mpeg', 'oog']
    video_types = ['mp4', 'mkv', 'mov', 'avi']
    image_types = ['png', 'jpg', 'jpeg', 'svg']
    file_types = ['pdf', 'zip', 'rar', 'txt', 'doc', 'docx', 'rtf', 'xls', 'xlsx', 'ppt', 'pptx'];

    if message_obj:
        if message_obj.message:
            getMessage = {message_obj.message: message_obj.created_date}
        elif message_obj.file:
            if message_obj.file_type in image_types:
                getMessage = {'Image': message_obj.created_date}
            elif message_obj.file_type in music_types:
                getMessage = {'Music': message_obj.created_date}
            elif message_obj.file_type in video_types:
                getMessage = {'Video': message_obj.created_date}
            elif message_obj.file_type in file_types:
                getMessage = {'File': message_obj.created_date}
        else:
            getMessage = None

        return getMessage

    return None