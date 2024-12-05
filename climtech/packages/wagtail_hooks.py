from django.urls import path, reverse

from wagtail import hooks
from wagtail.admin.menu import MenuItem

from . import views
from .viewsets import PackagesAdminGroup


@hooks.register("register_admin_viewset")
def register_viewset():
    return PackagesAdminGroup()




