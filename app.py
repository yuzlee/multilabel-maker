# -*- coding: utf-8 -*-

from Tkinter import *
from PIL import Image, ImageTk
import os
import sys
import json


DOC_TYPE = {
	"CAFFE": "caffe",
	"JSON": "json"
}

def label_format(src, dest, src_type, dest_type):
	if src_type is DOC_TYPE["JSON"] and dest_type is DOC_TYPE["CAFFE"]:
		with open(src, "r") as f:
			src = f.read()
		content = json.loads(src)
		result = []
		label_index = []
		for l in content:
			_l = content[l]
			line_result = []
			line_result.append(l)
			if len(label_index) is 0:
				_i = 0
				for c in _l:
					label_index.append("%s: %s" % (c, _i))
					_i = _i + 1
			for c in _l:
				line_result.append(str(_l[c]))
			result.append(line_result)
			print result
		with open(dest, "w") as f:
			f.write("\n".join([" ".join(x) for x in result ]))
		with open("%s.tag" % (dest), "w") as f:
			f.write("\n".join([ x for x in label_index ]))
	else:
		print "Unknow format tranformation."



def read_json(path, relative_path=True):
    if relative_path:
        path = os.path.join(base_dir, path)
    assert os.path.exists(path), "Can not find file."
    json_file = open(path, "r")
    json_string = json_file.read()
    _setting = json.loads(json_string, encoding="utf-8")
    return _setting


def load_image(path):
    size = 500.0
    _img = Image.open(path)
    _w, _h = _img.size
    resize_rate = 0
    if _w > _h:
        resize_rate = size / _w
    else:
        resize_rate = size / _h
    _img = _img.resize((int(_w * resize_rate), int(_h * resize_rate)))
    img = ImageTk.PhotoImage(_img)
    return img


class Application(Frame):
    def __init__(self, image_dir, label_file, master=None):
        Frame.__init__(self, master)

        self.image_dir = image_dir
        self.label_file = label_file
        self.image_list = []
        self.image_list_index = 0
        self.label_result = {}

        self.radiobutton_var = {}

        self.load_image_list()

        self.create_widgets()


    # ---------- Method -------------------------------------------------

    def load_image_list(self):
        assert os.path.isdir(self.image_dir), "Not a valid directory."

        self.image_list = []
        for parent, dirname, files in os.walk(self.image_dir):
            for file in files:
                if os.path.splitext(file)[1] in [ ".jpg", ".png", ".bmp" ]:
                    self.image_list.append(os.path.join(parent, file))
        assert len(self.image_list) > 2, "Too fewer images."


    def register_label(self, _dict):
    	key = self.image_list[self.image_list_index]
    	value = _dict
        self.label_result[key] = value
        print "Update image [%s] with label %s" % (key, value)

    # ---------- GUI ----------------------------------------------------

    # Add a control to the frame
    def add_control(self, _name, _object, _grid_option):
        setattr(self, _name, _object)
        getattr(self, _name).grid(**_grid_option)

    # Change the src in the image docker
    def change_image(self):
        image_file_path = self.image_list[self.image_list_index]
        img = load_image(image_file_path)
        self.image_label.config(image=img)
        self.image_label.img = img
        self.path_label.config(text=image_file_path)

        return image_file_path

    # Goto the prev image
    def prev_image(self):
        if self.image_list_index > 0:
            self.image_list_index = self.image_list_index - 1
            
    	    print "Load prev image from ", self.change_image()
        else:
            print "Already the first image"

    # Goto the next image
    def next_image(self):
        if self.image_list_index < len(self.image_list) - 1:
            self.image_list_index = self.image_list_index + 1
 
            print "Load next image from ", self.change_image()
        else:
            print "Already the last image"

    def save_label_change(self):
    	#print "radiobutton changed."
    	_dict = {}
        for l in self.radiobutton_var:
        	_var = self.radiobutton_var[l]
        	#print l, _var.get()
        	_dict[l] = _var.get()
        self.register_label(_dict)

    def save(self):
    	_result = self.label_result
    	json_content = json.dumps(_result)

    	with open(label_file, "w") as f:
    		f.write(json_content)
    	print "Saved to", label_file

    # Create a radiobutton group for a class of labels
    def create_label_area(self, row, col):
        docker = PanedWindow()

        label_class = setting["label_class"]
        row_count = 0
        for key in label_class:
            labels = label_class[key]

            print "Load %s labels from %s" % (key, type(labels))
            # the labels should be a json object or a relative path to the definition json file.
            if type(labels) is unicode:
                labels = read_json(labels)
            elif type(labels) is dict:
                pass

            vLabel = IntVar()
            vLabel.set(0)
            self.radiobutton_var[key] = vLabel
            for l in labels:
                label = labels[l]
                index = label["label"]
                desc = label["desc"]

                self.add_control("%s_label" % (key),
                    Label(docker, text="[%s]" % (key)),
                    { "row":row_count, "column":0, "sticky":E })

                ctl_name = "%s_%s_%s" % (key, l, index)
                self.add_control(ctl_name,
                    Radiobutton(docker, variable=vLabel, text=desc, value=index, 
                        indicatoron=0, width=6, height=2,
                        command=self.save_label_change),
                    { "row":row_count, "column":index + 1, "sticky":W })

            row_count = row_count + 1
        docker.grid(row=row, column=col, sticky=W)

    # Draw the main frame
    def create_widgets(self):
        #self.master.geometry("640x480+10+10")
        self.master.title('Multi-Label Maker')
        self.grid()

        image_area = PanedWindow()
        self.add_control("path_label", 
            Label(image_area, text='Path', width=50), 
            { "row":0, "column":0, "columnspan":3 })

        img = load_image(self.image_list[0])
        self.image_label = Label(image_area, image=img, 
                                    width=500, height=400,
                                    borderwidth=3, relief="ridge")
        self.image_label.img = img
        self.image_label.grid(row=1, column=0, columnspan=3)

        op_area = PanedWindow()
        self.add_control("prev_img", 
            Button(op_area, text='Prev', width=6, height=2,
                command=self.prev_image), 
            { "row":0, "column":0, "sticky":E })
        self.add_control("next_img", 
            Button(op_area, text='Next', width=6, height=2,
                command=self.next_image), 
            { "row":0, "column":1, "sticky":E })
        self.add_control("save_label",
            Button(op_area, text="Save", width=6, height=2,
                command=self.save),
            { "row":0, "column":3, "sticky":E })

        image_area.grid(row=0, column=0, rowspan=2)
        op_area.grid(row=0, column=1, columnspan=3, sticky=W)
        self.create_label_area(1, 1)


def main():
    global setting
    global base_dir
    global data_dir
    global label_file
    setting = read_json("setting.json", False)
    base_dir = setting["base_dir"]
    data_dir = os.path.join(base_dir, setting["data_dir"])
    label_file = os.path.join(base_dir, setting["label_file"])

    app = Application(data_dir, label_file)
    
    app.mainloop()


if __name__ == '__main__':
    main()