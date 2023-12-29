import os
import pickle


def checkpoint_factory(temp_path):
    def checkpoint(func):
        def wrapper():
            if os.path.exists(temp_path):
                with open(temp_path, "rb") as f:
                    mouse_all = pickle.load(f)
            else:
                mouse_all = func()
                with open(temp_path, "wb") as f:
                    pickle.dump(mouse_all, f)
            return mouse_all

        return wrapper

    return checkpoint
