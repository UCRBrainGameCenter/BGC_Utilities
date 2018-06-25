% given a string we can extract the date from it. Please note that
% if given "." or ".." it will break.

function date = GetFileDate(str, split_char)
    if contains(str, 'level')
        split_str = split(str, 'level');
        end_str = split_str{2};
        occurrences = find(ismember(end_str, split_char));
        date = end_str(occurrences(1) + 1:length(end_str));
    else
        split_str = split(str, 'Summary');
        end_str = split_str{2};
        date = end_str(2:length(end_str));
    end
    
    date = erase(date, '.json');
    date = date(1:8);
end