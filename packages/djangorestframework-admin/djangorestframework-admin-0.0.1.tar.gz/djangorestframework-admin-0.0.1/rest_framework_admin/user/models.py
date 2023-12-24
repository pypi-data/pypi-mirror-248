import datetime
import unicodedata

from django.conf import settings
from django.contrib.auth import password_validation
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models

# Create your models here.
from django.utils.crypto import salted_hmac
from django.utils.translation import gettext_lazy as _
from rest_framework_admin.db.models.base import BaseModel
from rest_framework_admin.db.models.manager import UserModelManager


class User(BaseModel):
    username = models.CharField(
        '用户名',
        max_length=32,
        help_text=_(
            'Required. 32 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[UnicodeUsernameValidator()],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )
    password = models.CharField('密码', max_length=128)
    nickname = models.CharField('昵称', max_length=64, blank=True, null=True)
    email = models.EmailField('邮箱')
    is_staff = models.BooleanField(
        '是否为员工',
        default=False,
        help_text=_(
            'Designates whether the user can log into this admin site.'),
    )
    is_superuser = models.BooleanField(
        '是否为超级管理员',
        default=False,
        help_text=_(
            'Designates that this user has all permissions without '
            'explicitly assigning them.'
        ),
    )
    last_login = models.DateTimeField('最后登录时间', blank=True, null=True)
    telephone = models.CharField('电话', max_length=64, blank=True, null=True)
    avatar = models.CharField('头像', max_length=256, null=True, blank=True)
    create_user = models.ForeignKey(
        'user.User',
        models.RESTRICT,
        related_name="created_%(app_label)s_%(class)ss",
        blank=True, null=True
    )
    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    objects = UserModelManager()

    # Stores the raw password if set_password() is called so that it can
    # be passed to password_changed() after the model is saved.
    _password = None

    class Meta:
        verbose_name = _('user')
        db_table = 'iam_user'

    def get_username(self):
        """Return the username for this User."""
        return getattr(self, self.USERNAME_FIELD)

    def __str__(self):
        return f'User(id={self.id}, username={self.get_username()})'

    def clean(self):
        setattr(
            self,
            self.USERNAME_FIELD,
            self.normalize_username(
                self.get_username()))
        self.email = self.__class__.objects.normalize_email(self.email)

    def set_password(self, raw_password):
        self.password = make_password(raw_password)
        self._password = raw_password

    def check_password(self, raw_password):
        """
        Return a boolean of whether the raw_password was correct. Handles
        hashing formats behind the scenes.
        """
        def setter(raw_password):
            self.set_password(raw_password)
            # Password hash upgrades shouldn't be considered password changes.
            self._password = None
            self.save(update_fields=["password"])
        return check_password(raw_password, self.password, setter)

    @classmethod
    def normalize_username(cls, username):
        return unicodedata.normalize('NFKC', username) if isinstance(
            username, str) else username

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self._password is not None:
            password_validation.password_changed(self._password, self)
            self._password = None

    def _legacy_get_session_auth_hash(self):
        # RemovedInDjango40Warning: pre-Django 3.1 hashes will be invalid.
        # key_salt = 'django.contrib.auth.models.AbstractBaseUser.get_session_auth_hash'
        key_salt = 'rest_framework_admin.user.models.User.get_session_auth_hash'
        return salted_hmac(key_salt, self.password,
                           algorithm='sha1').hexdigest()

    def get_session_auth_hash(self):
        """
        Return an HMAC of the password field.
        """
        # key_salt = "django.contrib.auth.models.AbstractBaseUser.get_session_auth_hash"
        key_salt = 'rest_framework_admin.user.models.User.get_session_auth_hash'
        return salted_hmac(
            key_salt,
            self.password,
            # RemovedInDjango40Warning: when the deprecation ends, replace
            # with:
            # algorithm='sha256',
            algorithm=settings.DEFAULT_HASHING_ALGORITHM,
        ).hexdigest()

    @property
    def is_anonymous(self):
        """
        Always return False. This is a way of comparing User objects to
        anonymous users.
        """
        return False

    @property
    def is_authenticated(self):
        """
        Always return True. This is a way to tell if the user has been
        authenticated in templates.
        """
        return True

    def filter_roles(self, is_valid=None):
        """ 过滤直接绑定的角色 """
        from role.models import Role
        from role.configs import SubjectTypeEnum
        return Role.filter_by_subject(
            self.id, SubjectTypeEnum.user.name, is_valid=is_valid)

    def save_roles(self, role_ids, **kwargs):
        from role.models import RoleSubjectRel
        from role.configs import SubjectTypeEnum
        RoleSubjectRel.save_by_subject(
            self.id, role_ids, SubjectTypeEnum.user.name, **kwargs)

    def delete_roles(self, role_ids):
        from role.models import RoleSubjectRel
        from role.configs import SubjectTypeEnum
        RoleSubjectRel.delete_by_subject(
            self.id, role_ids, SubjectTypeEnum.user.name)

    def filter_group_roles(self, is_valid=None):
        """ 过滤通过组绑定的角色 """
        from role.models import Role
        queryset = Role.objects.none()
        for group in self.groups.all():
            queryset = queryset | group.filter_roles(is_valid=is_valid)
        return queryset

    def filter_all_roles(self, is_valid=None, filter_kwargs=None):
        filter_kwargs = filter_kwargs or {}
        user_queryset = self.filter_roles(
            is_valid=is_valid).filter(
            **filter_kwargs)
        group_queryset = self.filter_group_roles(
            is_valid=is_valid).filter(
            **filter_kwargs)
        queryset = user_queryset.union(
            group_queryset, all=True)
        return queryset

    def get_max_role_rel(self):
        """ 获取最大的角色rel """
        role = self.filter_all_roles(is_valid=True).order_by('-weight').first()
        if not role:
            return None
        from role.models import RoleSubjectRel
        from role.configs import SubjectTypeEnum
        rel = RoleSubjectRel.objects.get(
            subject_id=role.subject_id,
            subject_type=SubjectTypeEnum.user.name,
            role_id=role.id)
        return rel

    def is_administrator(self):
        """ 管理员或者超级管理员 """
        from role.configs import DefaultRoleEnum
        if self.is_superuser:
            return True
        role_rel = self.get_max_role_rel()
        if not role_rel:
            return False
        return role_rel.role.code == DefaultRoleEnum.admin.name


class Group(BaseModel):
    users = models.ManyToManyField(
        User, through='UserGroupRel', through_fields=(
            'group', 'user'), related_name='groups')
    expire_datetime = models.DateTimeField('过期时间', blank=True, null=True)

    class Meta:
        db_table = 'iam_group'
        verbose_name = '用户组表'

    def __str__(self):
        return f'Group(id={self.id}, name={self.name})'

    def filter_roles(self, is_valid=None):
        """ 过滤直接绑定的角色 """
        from role.models import Role
        from role.configs import SubjectTypeEnum
        return Role.filter_by_subject(
            self.id, SubjectTypeEnum.group.name, is_valid=is_valid)

    def save_roles(self, role_ids, **kwargs):
        from role.models import RoleSubjectRel
        from role.configs import SubjectTypeEnum
        RoleSubjectRel.save_by_subject(
            self.id, role_ids, SubjectTypeEnum.group.name, **kwargs)

    def delete_roles(self, role_ids):
        from role.models import RoleSubjectRel
        from role.configs import SubjectTypeEnum
        RoleSubjectRel.delete_by_subject(
            self.id, role_ids, SubjectTypeEnum.group.name)


class UserGroupRel(BaseModel):
    user = models.ForeignKey(User, models.RESTRICT)
    group = models.ForeignKey(Group, models.RESTRICT)

    class Meta:
        db_table = 'iam_user_group_rel'
        verbose_name = '用户组关联表'
        unique_together = ('user', 'group', 'delete_datetime')

    def __str__(self):
        return f'UserGroupRel(id={self.id}, user={self.user.id}, group={self.group.id})'
