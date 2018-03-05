# BGC File Format

## Meta Data

Please note, the below example is spread out into multiple lines where in real log files this will be one single line.

```json
{
	"game_name":"Poly Rules",
	"version":"0.0.3",
	"user_name":"Colan",
	"device_id":"94cc6ab99c15d019e7cd9b446684059fbba37bf2",
	"session_number":"130",
	"run_number":"0",
	"delimiter":"|",
	"json_columns": [],
	"value_mapping": {
		"SwitchType": {
			"0":"TaskBlock",
			"1":"ActiveInputReceivers",
			"2":"Left",
			"3":"Right",
			"4":"VisibleInputReceivers",
			"5":"VisibleStimulusSlots",
			"6":"Layout",
			"7":"None"
		}
	},
	"column_mapping": {
		"default":[
			"level",
			"trial",
			"startTime(ms)",
			"endTime(ms)",
			"correctAnswer",
			"correctTaskBlock",
			"correctTaskCollection",
			"swapOccured",
			"swapType"
		]
	}
}
```

### Game Name

This field will be present for all log files and defines the name of the game. This should be the same value for all log files associated with a session, game, etc.

### Version

This field will be present for all log files and defines the current version of the game. Will be useful for when log files change between versions.

### User Name

This field will be present for all log files and defines the current user playing the game.

### Device ID

This field will be present for all log files and defines the current device the user is using. Will be useful for BGC studies where it may help show that a certain ipad is acting incorrectly, etc.

### Session Number

This field will be present for all log files and defines the user's current session number.

### Run Number

This field will be present for all log files and defines the user's current run number.  

### Delimeter

This field will be present for all log files and tells the parser how it can parse lines below the meta data. For example, the sample line below would have the delimeter of `|`.

```
0|123|739|1
```


### JSON Columns

This tells the parser that this column features a JSON value that is more complex than just a field value and should be parsed accordingly.

### Column Mapping

Previous BGC logs have included the functionality of allowing different log lines to have different columns. To support this, there is a column mapping JSON object that must be present in the meta data. The dictionary requries atleast one value that is the `default` colum mapping. For every line, the parser will check the first value and attempt to match it to a key in the column mapping dictionary. If nothing is found, it will go to `default`.


### Value Mapping

Previous bgc log formats often include a mapping from integers to strings and the `bgc` file format will support that for the time being. To use this behaviour, there is a json object titled `value_mapping`. The field must be present in all log files, but it can be an empty dictionary. When parsing, for columns specified in the column mapping, it will place values into the data that is the string instead of the integer.

For example, imagine there is a mapping for column 0, `task_type`, with the value mapping of `0` to `default_stimulus`. This will set the field to be like:

```json
"task_type": "default_stimulus"
```

## Data

This will be simple lines of data that are separated by the delimeter specified in the meta data. 



## Example Log File

The following is taking a sample log file from poly rules and turning it into the correct format.


BGC Format:

```
{"game_name":"Poly Rules","version":"0.0.3","user_name":"Colan","device_id":"94cc6ab99c15d019e7cd9b446684059fbba37bf2","session_number":"161","run_number":"0","delimiter":"|","value_mapping":{"Layout":{"0":"OneSS_OneTaskBlock_TwoReceivers","1":"TwoSS_TwoTaskBlock_TwoReceivers","2":"OneSS_TwoTaskBlock_TwoReceivers","3":"FourSS_FourTaskBlock_TwoReceivers","4":"TwoSS_TwoTaskBlock_FourRecievers","5":"OneSS_Two_TaskBlock_FourReceivers","6":"TwoSS_Two_TaskBlock_TwoReceivers"},"GameMode":{"0":"Progression","1":"TimeLimit","2":"XMistake"}},"column_mapping":{"default":["session","runNumber","progressionLevel","GameMode","Layout","taskType"]}}
161|0|1|0|2
161|1|2|0|2
```

JSON Output:

```json
{
	"header": {
		"game_name": "Poly Rules", 
		"version": "0.0.3", 
		"user_name": "Colan", 
		"session_number": 161, 
		"device_id": "94cc6ab99c15d019e7cd9b446684059fbba37bf2"
	},
	"data": [{
			"session": 161,
			"runNumber": 0,
			"progressionLevel":1,
			"gameMode": "Progression",
			"Layout": "OneSS_OneTaskBlock_TwoReceivers",
			"taskType": 2
		},
		{
			"session": 161,
			"runNumber": 1,
			"progressionLevel":2,
			"gameMode": "Progression",
			"Layout": "OneSS_OneTaskBlock_TwoReceivers",
			"taskType": 2
		}
	]	
}
```