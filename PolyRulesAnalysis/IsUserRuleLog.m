% returns 1 if summary is found else it returns 0
function true = IsUserResponseFile(file_name)
    true = contains(file_name, '_rule_log_');
end