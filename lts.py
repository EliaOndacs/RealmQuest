
def ListWithoutSpaceToString(list) -> str:
    string = ''
    for i in list:
        if list.index(i) != len(list)-1:
            string += i+' '
        else:
            string += i
    return string
    