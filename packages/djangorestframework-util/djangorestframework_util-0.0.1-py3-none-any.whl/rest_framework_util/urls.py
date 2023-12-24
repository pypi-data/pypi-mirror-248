#!/usr/bin/python
# -*- coding:utf-8 -*-
# Email:iamfengdy@126.com
# DateTime:2023/12/22
# Tool:PyCharm

"""  """
__version__ = '0.0.1'
__history__ = """"""
__all__ = ['load_urlpatterns']

from importlib import import_module

from django.urls import path, include


def load_urlpatterns(installed_apps, with_app_prefix=True):
    """ 根据installed_apps加载url

    :param list installed_apps: 安装的应用
    :param bool with_app_prefix: 是否以应用名为url前缀
    :return:
    """
    _urlpatterns = []
    for no, install_app in enumerate(installed_apps, start=1):
        _string = f'{install_app}.urls.urlpatterns'
        print(f'[#{no}] import {_string}')
        try:
            module_path = f'{install_app}.urls'
            module = import_module(module_path)
            __urlpatterns = getattr(module, 'urlpatterns')
        except ModuleNotFoundError as exc:
            print(f'\t{exc}')
        except ImportError as exc:
            print(f'\t{exc}')
        except BaseException as exc:
            raise exc
        else:
            if with_app_prefix:
                _urlpatterns.append(
                    path(
                        f'{install_app}/',
                        include(module_path)))
            else:
                _urlpatterns += __urlpatterns
        continue
    return _urlpatterns
