from django.contrib import admin
from django.urls import path

class InfoRouterManager:
    def __init__(self, routeHome):
        self.routeHome  = routeHome
        self.urls       = []
    def route(self, cls):
        if not hasattr(cls, 'path'):  
            cls.path = cls.__name__.lower()
        if cls.path[-1]!='/':   cls.path+='/'
        self.urls.append(
            path(f"{self.routeHome}/{cls.path}", cls.as_view())
        )
        return cls
infonowRouter = InfoRouterManager('info')

from .views import *
