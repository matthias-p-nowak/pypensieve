print("loading " + __file__)

import pickle
import atexit
from platformdirs import user_data_dir
import os
import sys
import logging
import re
import weakref
import time
import tkinter as tk


class Pensieve:
    config = None
    wk = weakref.WeakKeyDictionary()
    lastSaved = time.time()

    def __init__(self, obj, key, *attrs):
        print(f"initializing Pensieve {obj} {key} {attrs}")
        self.key = key
        self.attrs = attrs
        if Pensieve.config is None:
            Pensieve.getConfig()
        cfg = Pensieve.config
        for kp in re.split("\\.", key):
            cfg = cfg.setdefault(kp, {})
        for attr in attrs:
            if attr in cfg:
                if hasattr(obj, attr):
                    oa = getattr(obj, attr)
                    if callable(oa):
                        oa(cfg[attr])
                    else:
                        setattr(obj, attr, cfg[attr])
        Pensieve.wk[obj] = self
        if isinstance(obj, tk.Tk):
            obj.after(5000, Pensieve.saveAll)

    def saveAttrs(self, obj2):
        cfg = Pensieve.config
        for kp in re.split("\\.", self.key):
            cfg = cfg.setdefault(kp, {})
        for attr in self.attrs:
            if hasattr(obj2, attr):
                oa = getattr(obj2, attr)
                if callable(oa):
                    cfg[attr] = oa()
                else:
                    cfg[attr] = getattr(obj2, attr)

    @staticmethod
    def saveAll():
        if time.time() - Pensieve.lastSaved < 5:
            return
        for obj in Pensieve.wk:
            Pensieve.wk[obj].saveAttrs(obj)
            if isinstance(obj, tk.Tk):
                obj.after(5000, Pensieve.saveAll)
        Pensieve.lastSaved = time.time()

    @staticmethod
    def getConfig():
        fileName = Pensieve.getFileName()
        if not os.path.exists(fileName):
            Pensieve.config = {}
            return
        with open(fileName, "rb") as f:
            Pensieve.config = pickle.load(f)
            return

    @staticmethod
    def getFileName():
        app_name = os.path.basename(sys.argv[0])
        app_name = os.path.splitext(app_name)[0]
        cfgDir = user_data_dir(app_name)
        os.makedirs(cfgDir, exist_ok=True)
        return os.path.join(cfgDir, "pensieve.db")

    @staticmethod
    def saveOnExit():
        print("Saving config on exit")
        with open(Pensieve.getFileName(), "wb") as f:
            pickle.dump(Pensieve.config, f)


atexit.register(Pensieve.saveOnExit)
