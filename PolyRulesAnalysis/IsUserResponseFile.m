% returns 1 if summary is found else it returns 0
function true = IsUserResponseFile(file_name)
    true = contains(file_name, '_user_response_');
end