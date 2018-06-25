% returns 1 if summary is found else it returns 0
function true = IsGeneratedShapesFile(file_name)
    true = contains(file_name, '_generated_shapes_');
end