#!/usr/bin/python
# @author: COlan Biemer

NewLine   = "\n"
Default   = "default"
Delimiter = "delimiter"
ColumnMapping = "column_mapping"
ValueMapping  = "value_mapping"
RequiredFields  = ["game_name", "version", "user_name", "device_id", "session_number", "run_number", Delimiter, ColumnMapping, ValueMapping]
RedundantFields = [ColumnMapping, ValueMapping]
MetaData = "meta_data"
Data = "data"