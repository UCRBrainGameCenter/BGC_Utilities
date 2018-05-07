Expanded Metadata:

```json
{

    "session_number":"66",
    "run_number":"0",
    "device_id":"id",
    "user_name":"colan",
    "version":"0.0.3",
    "game_name":"Poly Rules",
    "delimiter":"|",
    "value_mapping":{
        "game_type":{
            "0":"ultim_eyes",
            "1":"contour"
        }
    },
    "column_mapping":{
        "0":[
            "game_type",
            "testing",
            "if",
            "this",
            "works"
        ],
        "1":[
            "game_type",
            "hope",
            "this",
            "works"
        ]
    }

}
```

BGC Input:

```
{"session_number":"66","run_number":"0","device_id":"id","user_name":"colan","version":"0.0.3","game_name":"Poly Rules","delimiter":"|","value_mapping":{"game_type": {"0": "ultim_eyes","1":"contour"}},"column_mapping":{"0":["game_type","testing","if","this","works"], "1": ["game_type", "hope", "this", "works"]}}
0|a|b|c|d
0|e|12341234|g|h
1|i|j|true
1|l|m|false
0|o|p|q|r
```

Goes To:

```json
[
	{
		"game_type": "ultim_eyes",
		"testing": "a",
		"if": "b",
		"this": "c",
		"works": "d"
	},
	{
		"game_type": "ultim_eyes",
		"testing": "e",
		"if": 12341234,
		"this": "g",
		"works": "h"
	},
	{
		"game_type": "contour",
		"hope": "i",
		"this": "j",
		"works": true,
	},
	{
		"game_type": "contour",
		"hope": "l",
		"this": "m",
		"works": false,
	},
	{
		"game_type": "ultim_eyes",
		"testing": "o",
		"if": "p",
		"this": "q",
		"works": "r"
	}
]
```
