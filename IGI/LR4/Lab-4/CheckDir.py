import os


class CheckDirMixin:
    """Проверка существования путя"""

    def check_dir(self, path):
        if not os.path.exists(path):
            os.mkdir(path)
