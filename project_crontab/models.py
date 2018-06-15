# coding: utf-8

from django.db import models
from django.contrib.auth.models import User
import django.utils.timezone as timezone


from asset.models import minion


class Svn(models.Model):
    """
    SVN信息
    """
    salt_minion = models.ForeignKey(minion, verbose_name=u"SVN所属salt minion", related_name="minion_of_svn")
    username = models.CharField(max_length=32)
    password = models.CharField(max_length=32)
    repo = models.CharField(max_length=128, default="http://svn.abc.com/svn/test")
    local_path = models.CharField(max_length=64, default='/srv/testsvn')
    creator = models.ForeignKey(User, verbose_name=u"创建者", related_name="creator_of_svn", default=1)
    create_time = models.DateTimeField(verbose_name=u"创建日期", auto_now_add=True, null=True, blank=True)
    updater = models.ForeignKey(User, verbose_name=u"最后更新者", related_name="updater_of_svn", blank=True, null=True)
    update_time = models.DateTimeField(verbose_name=u"最后更新日期", auto_now=True, blank=True, null=True)

    def __unicode__(self):
        return self.salt_minion.saltname, self.salt_minion.ip

    class Meta:
        verbose_name = u"SVN"
        verbose_name_plural = verbose_name


class Project(models.Model):
    """
    项目信息
    """
    name = models.CharField(max_length=64, verbose_name=u"项目名称", blank=False, null=False)
    path = models.CharField(max_length=64, verbose_name=u"本地路径", blank=False, null=False)
    svn = models.ForeignKey(Svn, verbose_name=u"项目的SVN", related_name="svn_of_project")
    creator = models.ForeignKey(User, verbose_name=u"创建者", related_name="creator_of_project", default=1)
    create_time = models.DateTimeField(verbose_name=u"创建日期", auto_now_add=True, null=True, blank=True)
    updater = models.ForeignKey(User, verbose_name=u"最后更新者", related_name="updater_of_project", blank=True, null=True)
    update_time = models.DateTimeField(verbose_name=u"最后更新日期", auto_now=True, blank=True, null=True)

    def __unicode__(self):
        return self.name, self.path

    class Meta:
        verbose_name = u"项目"
        verbose_name_plural = verbose_name


class CrontabCmd(models.Model):
    """
    crontab命令信息
    """
    project = models.ForeignKey(Project, verbose_name=u"Crontab所属项目", related_name="project_of_crontab")
    cmd = models.CharField(max_length=256, verbose_name=u"手动填入的命令", blank=False, null=False)
    auto_cmd = models.TextField(verbose_name=u"自动补全的命令", blank=False, null=False)
    frequency = models.CharField(max_length=16, verbose_name=u"执行频率", blank=False, null=False)
    creator = models.ForeignKey(User, verbose_name=u"创建者", related_name="creator_of_crontab", default=1)
    create_time = models.DateTimeField(verbose_name=u"创建日期", auto_now_add=True, null=True, blank=True)
    updater = models.ForeignKey(User, verbose_name=u"最后更新者", related_name="updater_of_crontab", blank=True, null=True)
    update_time = models.DateTimeField(verbose_name=u"最后更新日期", auto_now=True, blank=True, null=True)

    def __unicode__(self):
        return self.project.name, self.auto_cmd, self.frequency

    class Meta:
        verbose_name = u"crontab命令"
        verbose_name_plural = verbose_name
