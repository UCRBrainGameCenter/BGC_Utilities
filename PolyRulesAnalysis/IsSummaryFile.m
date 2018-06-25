% returns 1 if summary is found else it returns 0
function isSummary = IsSummaryFile(file_name)
    isSummary = contains(file_name, 'Summary');
end