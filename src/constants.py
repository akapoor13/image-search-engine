# UI constants
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

SEARCHDESCID_ = 'search_description'
SEARCHUPLOADID_ = 'search_upload_pic'
SEARCHPICID_ = 'search_pic_id'
ADDUPLOADID_ = 'upload_data'

# db columns constants
IDD_ = 'idd'
DESCRIPTION_ = 'description'
TAGS_ = 'tags'
USERS_ = 'users'
PATH_ = 'path'
DATE_ = 'date'
TAGTABLE_ = 'tag_table'
SIMILARCOL_ = 'similarity_score'
COLORDESCRIPTOR_ = 'color_descriptor'
SIFTDESCRIPTOR_ = 'sift_descriptor'

COLMAPPING_ = {
    IDD_: 'Pic Id',
    DESCRIPTION_: 'Description',
    TAGTABLE_: 'Tags',
    USERS_: 'User',
    DATE_: 'Date',
    SIMILARCOL_: 'Similarity (%)/Chi-Sq Distance'
}

TABLECOLS_ = [IDD_, DESCRIPTION_, TAGTABLE_, USERS_, DATE_, SIMILARCOL_]

DBCOLS_ = [
    DATE_, DESCRIPTION_, IDD_, PATH_, TAGS_, USERS_, COLORDESCRIPTOR_,
    SIFTDESCRIPTOR_
]
