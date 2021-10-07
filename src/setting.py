import json
import os
setting_folder = "{}/.config/my_dict".format(os.environ["HOME"])
setting_filename = "{}/setting.json".format(setting_folder)


class Setting:
    support_clipboard = True
    show_main_window_when_startup = True

    def __init__(self):
        self.load()

    def load(self):
        if not os.path.exists(setting_folder):
            os.makedirs(setting_folder)
        txt = ""
        if os.path.exists(setting_filename):
            with open(setting_filename, 'r') as f:
                txt = f.read()
        try:
            if len(txt) <= 2:
                return
            json_setting = json.loads(txt)
            for i in json_setting.keys():
                self.__setattr__(i, json_setting[i])
        except Exception as err:
            print(err)

    def dump(self):
        obj = {}
        for i in self.__dir__():
            if i.startswith("__"):
                continue
            attr = self.__getattribute__(i)
            if callable(attr):
                continue
            obj[i] = attr
        return obj

    def save(self):
        if not os.path.exists(setting_folder):
            os.makedirs(setting_folder)
        with open(setting_filename, 'w+') as f:
            f.write(json.dumps(self.dump(), indent=4, ensure_ascii=False))


setting = Setting()
