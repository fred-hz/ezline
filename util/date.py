
def date_format(date, str_format):
    if '-' in date:
        date_list = date.split('-')
        year = date_list[0]
        month = date_list[1]
        day = date_list[2]

    elif '/' in date:
        date_list = date.split('/')
        month = date_list[0]
        day = date_list[1]
        year = date_list[2]

    else:
        year = date[:4]
        month = date[4:6]
        day = date[6:]

    return str_format.replace('%Y', year) \
                    .replace('%m', month) \
                    .replace('%d', day)
