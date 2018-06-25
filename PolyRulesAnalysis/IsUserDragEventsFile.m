% returns 1 if summary is found else it returns 0
function true = IsUserDragEventsFile(file_name)
    true = contains(file_name, '_user_drag_events_');
end