### A GUI tool for making multi-label for images

### Get start
#### setting
``` json
{
	"base_dir": "./",
	"data_dir": "picts",
	"label_file": "./label_out/labels.json",
	"label_class": {
		"color": "./label_def/color_label.json",
		"car_type": {
			"big": {
				"label": 0,
				"desc": "big"
			},
			"small": {
				"label": 1,
				"desc": "small"
			}
		}
	}
}
```
#### label definition
``` json
{
	"big": {
		"label": 0,
		"desc": "big"
	},
	"small": {
		"label": 1,
		"desc": "small"
	}
}
```
#### transform the out format
``` bash
$ python test.py
```
