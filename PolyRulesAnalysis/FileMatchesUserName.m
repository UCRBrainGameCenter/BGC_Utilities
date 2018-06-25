% returns 1 if the user is found in the file. Else it will return a 0.

function user_name_matches = FileMatchesUserName(file_name, user_name, separator)
    file_user_name = GetFileUserName(file_name, separator);
    user_name_matches = strcmp(file_user_name, user_name);
end