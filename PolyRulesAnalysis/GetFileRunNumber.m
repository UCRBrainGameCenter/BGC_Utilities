% given a string we can extract the user name from it. Please note that
% if given "." or ".." it break.

function run_number = GetFileRunNumber(file_name, separator)
    split_file_name = strsplit(file_name, separator);
    run_number = split_file_name{3};
end