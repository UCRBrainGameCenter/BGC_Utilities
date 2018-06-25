% Hello!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
% 
% This file is going to convert any file in the folder 'json_logs' to a
% matlab data structure that you can use. You can modify the 
% `JSON_DIRECTORY` variable to change this.
%
% "Hey colan, how can I thank you?"
% Well, you can start with a "thank you!"
%
% "Hey colan, this doesn't work. What should I do?"
% That's impossible, if I wrote this then it will work. You should review
% how you pressed the run button and not bring it up with me.
%
% Best,
% Colan
%
% P.s. stop talking to me asap. It is vitally important. If you must talk
% to me I recommend getting permission from Aaron.

%% Configuration
JSON_DIRECTORY      = 'json_logs';
USER_NAME_SEPARATOR = '_';

%% Construct user structures
users = BuildUserDataFromDirectory(JSON_DIRECTORY, USER_NAME_SEPARATOR);