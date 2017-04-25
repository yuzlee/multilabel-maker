### A GUI tool for making multi-label for images

### Get Started
#### setting
``` json
{
	"base_dir": "./",
	"data_dir": "picts",
	"label_file": "label_out/labels.json",
	"label_class": {
		"color": "label_def/color_label.json",
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
* `base_dir`: the basic directory for all the other path in the setting.
* `data_dir`: the directory for image files.
* `label_file`: the target path for generated label.
* `label_class`: the definition for all labels, supporting a json text or a path of other json file.

#### label definition
For defining a label we should provide a `label_name` likes `big` and an `index` of it, the `desc` is optional.
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
The app generates labels of json format, a tool for transformation is necessary.
``` bash
$ python test.py
```
