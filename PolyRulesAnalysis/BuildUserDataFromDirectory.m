function users = BuildUserDataFromDirectory(directory, separator)
    % sturcture keys
    SUMMARY          = 'summary';
    SESSIONS         = 'sessions';
    RUNS             = 'runs';
    GENERATED_SHAPES = 'generated_shapes';
    USER_RESPONSE    = 'user_response';
    USER_DRAG_EVENTS = 'user_drag_events';
    SWAP_LOG         = 'swap_log';
    LAYOUT_LOG       = 'layout_log';
    RULE_LOG         = 'rule_log';

    % get files and set up user dictionary
    files = dir(directory);
    users = containers.Map;

    % loop through every file to build out the data structure
    for i=1:length(files)
        file_name = files(i).name;
        user_name = GetFileUserName(files(i).name, separator);

        %Skip directories
        if files(i).isdir
            continue
        end
        
        % create values for user, session, and run that will be stored
        % back into the users container at the end of each loop
        user         = struct;
        user_session = struct;
        user_run     = struct;

        % create container for user if it doesn't exit
        if ~isKey(users, user_name)
            user = struct(SESSIONS, containers.Map);
        else
            user = users(user_name);
        end

        % get session and run number from the file name
        % session_number = GetFileSessionNumber(file_name, separator);
        session_number = GetFileDate(file_name, separator);
        run_number     = GetFileRunNumber(file_name, separator);
        
        % create container for user session number if it doesn't exist
        if ~isKey(user.sessions, session_number)
            user_session = struct(...
                SUMMARY, struct, ...
                RUNS, containers.Map);
        else
            user_session = user.sessions(session_number);
        end

        % get file contents and convert to json
        path = [directory '/' file_name];
        file_id = fopen(path, 'r');
        s = textscan(file_id, '%s', 'Delimiter', '\n');
        fclose(file_id);
        decoded_json = jsondecode(s{1}{1});

        % assign decoded json to summary
        if IsSummaryFile(file_name)
            user_session.summary = decoded_json;
        else
            % create conainer for user run number in session if it doesn't exist
            if ~isKey(user_session.runs, run_number)
                user_run = struct(...
                    GENERATED_SHAPES, struct, ...
                    USER_RESPONSE, struct, ...
                    USER_DRAG_EVENTS, struct, ...
                    SWAP_LOG, struct, ...
                    LAYOUT_LOG, struct, ...
                    RULE_LOG, struct);
            else
                user_run = user_session.runs(run_number);
            end
            
             % assign decoded json to its respective field
            if IsGeneratedShapesFile(file_name)
                user_run.generated_shapes  = decoded_json;
            elseif IsUserResponseFile(file_name)
                 user_run.user_response    = decoded_json;
            elseif IsUserDragEventsFile(file_name)
                 user_run.user_drag_events = decoded_json;
            elseif  IsUserSwapLog(file_name)
                user_run.swap_log = decoded_json;
            elseif IsUserLayoutLog(file_name)
                user_run.layout_log = decoded_json;
            else if IsUserRuleLog(file_name)
                user_run.rule_log = decoded_json;
            else
                disp([path ' is not a handled file type.']);
            end
            
            % assign run field reference
            user_session.runs(run_number) = user_run;
        end

        % reassign values so references don't break
        user.sessions(session_number) = user_session;
        users(user_name)              = user;
    end
end