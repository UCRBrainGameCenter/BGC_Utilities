% This function gets the users from the given directory and returns an
% array where each element is a unique user found in the given directory.

function users = GetUsers(directory, separator)
    files = dir(directory);
    users = cell(0);

    for i=1:length(files)
       user_name = GetFileUserName(files(i).name, separator);

       if strcmp(user_name,'.') || strcmp(user_name,'..')
          continue 
       end

        for j=1:length(users)
            if strcmp(users(j), user_name)
               found = 1;
               break
            end
        end

        if found == 0
            users{end+1} = user_name;
        end
    end
end