% given a string we can extract the user name from it. Please note that
% if given "." or ".." it will break

function session_number = GetFileSessionNumber(file_name, separator)
    split_file_name = strsplit(file_name, separator);
    session_number = split_file_name{2};
end