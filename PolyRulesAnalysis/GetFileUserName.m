% given a string we can extract the user name from it. Please note that
% if given "." or ".." it will just return these values and you should
% handle it after calling this function

function user_name = GetFileUserName(file_name, separator)
    split_file_name = strsplit(file_name, separator);
    user_name = split_file_name{1};
end