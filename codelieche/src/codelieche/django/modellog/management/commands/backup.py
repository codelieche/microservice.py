# -*- coding:utf-8 -*-
"""
backup执行的操作是：
1. clear：清除migration文件
2. backup：备份migration文件
3. recover：恢复migration文件
"""
import sys
import os
import time

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError


class MigrationsAction:
    """
    migration文件的操作
    """
    def __init__(self, base_dir=settings.BASE_DIR, backup_dir=os.path.join(settings.BASE_DIR, "backup")):
        self.base_dir = base_dir
        self.backup_dir = backup_dir
        # 如果备份的目录不存在我们创建
        if not os.path.exists(backup_dir):
            os.mkdir(backup_dir)

    def clear(self):
        """
        清除migrations文件
        """
        # 1. 进入base_dir
        os.chdir(self.base_dir)

        # 2. 删除migrations文件了
        if os.system("ls ./apps/**/migrations/00*.py") == 0:
            os.system("rm ./apps/**/migrations/00*.py")
            print("删除migrations文件ok")
        else:
            print("没获取到00*.py的文件，无需删除")

    def copy_migrations_to_backup_dir(self, sub_dir, clear=False):
        """
        复制migrations文件到备份目录中
        且是否清空他们(默认False),一般恢复/备份之前我们备份一下当前的migrations文件
        """
        os.chdir(self.backup_dir)
        # 1. 先查看apps: 我们命令只备份apps中的migrations文件，不遵守规范的不备份
        apps = os.listdir(os.path.join(self.base_dir, "apps"))

        for app in apps:
            # app的根目录
            app_dir = "{}/apps/{}".format(self.base_dir, app)
            if not os.path.isdir(app_dir):
                continue

            # app的migrations文件目录
            migrations_dir_path = "{}/apps/{}/migrations/".format(self.base_dir, app)
            if not os.path.exists(migrations_dir_path):
                continue
            # app的所有migrations文件：我们只备份00开头的文件
            migrations_files = os.listdir(migrations_dir_path)
            migrations_files = list(filter(lambda i: i and i.startswith("00"), migrations_files))
            print("migrations_files:", migrations_files)

            # 如果这个app有migrations文件，就开始执行复制
            if migrations_files:
                # 创建一下备份的子目录
                backup_old_migrations_dir = "{}/{}".format(self.backup_dir, sub_dir)
                if not os.path.exists(backup_old_migrations_dir):
                    os.mkdir(backup_old_migrations_dir)

                # 每个app都需要再创建一个目录的
                backup_old_migrations_dir = "{}/{}/{}".format(self.backup_dir, sub_dir, app)
                if not os.path.exists(backup_old_migrations_dir):
                    os.mkdir(backup_old_migrations_dir)

                # 判断是否是文件
                for f in migrations_files:
                    file_path = "{}/apps/{}/migrations/{}".format(self.base_dir, app, f)
                    if os.path.isfile(file_path) and f.startswith("00"):
                        basename = os.path.basename(file_path)
                        # print(file_path)
                        print("copy file:{}".format(basename))
                        # 复制文件
                        cmd = "cp -rf {} {}".format(file_path, backup_old_migrations_dir)
                        os.system(cmd)

        if clear:
            print("本次还需要删除migrations文件")
            self.clear()

    def copy_backup_files_to_apps(self, sub_dir):
        os.chdir(self.backup_dir)
        source_dir_path = "{}/{}".format(self.backup_dir, sub_dir)
        print("source_dir_path", source_dir_path)
        if not os.path.exists(source_dir_path):
            print("备份文件不存在：{}".format(source_dir_path))
            sys.exit(1)

        apps = os.listdir(source_dir_path)
        # print("apps", apps)

        # 遍历里面的app
        for app in apps:
            source_app_dir = "{}/{}".format(source_dir_path, app)
            app_migrations_dir = "{}/apps/{}/migrations".format(self.base_dir, app)
            if os.path.isdir(source_app_dir) and os.path.exists(app_migrations_dir) and os.path.isdir(
                    app_migrations_dir):
                # 开始复制文件
                files = os.listdir(source_app_dir)
                # print("files:", files)
                for f in files:
                    file_path = "{}/{}".format(source_app_dir, f)
                    if os.path.isfile(file_path) and f.startswith("00"):
                        cmd = "cp -rf {} {}".format(file_path, app_migrations_dir)
                        os.system(cmd)
                        print("复制文件：{}/{}".format(app, f))
            else:
                print("source_app_dir", source_app_dir)


class Command(BaseCommand):
    help = 'apps migrate files backup or recover'

    def add_arguments(self, parser):
        # parser.add_argument('--action', nargs='+', type=str)
        parser.add_argument(
            "args",
            metavar="action: backup/recover",
            nargs="+",
            type=str,
            help="backup migrate action is backup/recover.",
        )

    def handle(self, *args, **options):
        if not (args and len(args) >= 1 and args[0] in ["backup", "recover", "clear"]):
            raise CommandError('暂时只支持backup/recover/clear操作')
        action = args[0]
        print('action:', action, settings.BASE_DIR)

        backup_dir = os.path.join(settings.BASE_DIR, 'backup')

        # 实例化操作的api
        api = MigrationsAction(base_dir=settings.BASE_DIR, backup_dir=backup_dir)

        if action == "clear":
            sub_dir = "c_{}".format(time.strftime("%Y%m%d%H%M%S"))
            api.copy_migrations_to_backup_dir(sub_dir=sub_dir, clear=True)

        elif action == "backup":
            # 判断原有的备份apps目录是否存在
            apps_dir = "{}/apps".format(backup_dir)
            if os.path.exists(apps_dir):
                print("apps目录存在，我们需要备份一下它")
                os.rename(apps_dir, "{}_{}".format(apps_dir, time.strftime("%Y%m%d%H%M%S")))

            # 执行备份
            api.copy_migrations_to_backup_dir(sub_dir="apps", clear=False)

        elif action == "recover":
            # 执行恢复
            sub_dir = "apps"
            if not os.path.exists(os.path.join(backup_dir, sub_dir)):
                print("apps的备份目录不存在，不可恢复migrations文件")
                sys.exit(1)

            # 备份一下老的文件，防止后续需要用到
            backup_current_migrations_dir = "r_{}".format(time.strftime("%Y%m%d%H%M%S"))
            # 备份老的migrations文件，同时清除
            api.copy_migrations_to_backup_dir(sub_dir=backup_current_migrations_dir, clear=True)

            # 开始执行恢复
            api.copy_backup_files_to_apps(sub_dir=sub_dir)
        else:
            print("不支持的操作:{}".format(action))
