DESINPUT_ = 'description'
UPLOADINPUT_ = 'upload_picture'
IDINPUT_ = 'idd'
INPUTTYPE_ = [DESINPUT_, UPLOADINPUT_, IDINPUT_]
DEFAULTINPUTTYPE_ = DESINPUT_

SEARCHOPTIONS_ = {
    DESINPUT_: 'Description',
    UPLOADINPUT_: 'Upload Picture',
    IDINPUT_: 'Picture Id'
}


COLMAPPING_ = {
    'idd': 'Pic Id',
    'description': 'Description',
    'tag_table': 'Tags',
    'users': 'User',
    'date': 'Date'
}
TABLECOLS_ = ['idd', 'description', 'tag_table', 'users', 'date']

SEARCHBARID_ = 'search_description'
SEARCHUPLOADID_ = 'search_upload_pic'
SEARCHPICID_ = 'search_pic_id'

IDD_ = 'idd'
DESCRIPTION_ = 'description'
TAGS_ = 'tags'
USERS_ = 'users'
PATH_ = 'path'
DATE_ = 'date'
DBCOLS_ = [IDD_, DESCRIPTION_, TAGS_, USERS_, PATH_, DATE_]
