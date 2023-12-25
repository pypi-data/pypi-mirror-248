import importlib
from inspect import isclass

from rest_framework.routers import DefaultRouter
from rest_framework.viewsets import ViewSet
from rest_framework.views import View

from django.urls import path, include
from django.conf import settings

from .utils import clean_app_name, get_modules_list


class Router:
    _auto_load_modules = True

    def __init__(
        self, endpoint: str, namespace: str, module: str = None, debug: bool = False
    ) -> None:
        self.endpoint: str = endpoint
        self.namespace: str = namespace
        self.module: str = module
        self._router = DefaultRouter()
        self._urls = []
        self.debug = debug

    def process_viewset(self, viewset: ViewSet, route: str, basename: str) -> None:
        pass

    def process_view(self, view: View, route: str, name: str) -> None:
        pass

    def route_viewset(self, route: str, basename: str = ""):
        def inner(viewset):
            self._log(
                "Routing viewset " + str(viewset) + " to " + self.endpoint + route
            )
            self.process_viewset(viewset, route, basename)
            self._router.register(route, viewset, basename=basename)
            return viewset

        return inner

    def route_view(self, route: str, name: str = ""):
        def inner(view):
            self._log("Routing view " + str(view) + " to " + self.endpoint + route)
            self.process_view(view, route, name)
            self._urls.append(path(route, view.as_view(), name=name))
            return view

        return inner

    def _log(self, message: str) -> None:
        if self.debug:
            print("Auto Router - " + message)

    def _load_all_modules(self) -> None:
        for module in settings.INSTALLED_APPS:
            try:
                self._log("Searching for views in app " + clean_app_name(module))
                for module_name in get_modules_list():
                    module = importlib.import_module(
                        clean_app_name(module) + "." + module_name
                    )
                    self._log("Found module " + str(module))
                    for attribute_name in dir(module):
                        attribute = getattr(module, attribute_name)

                        if isclass(attribute):
                            # Add the class to this package's variables
                            globals()[attribute_name] = attribute
            except ModuleNotFoundError:
                pass
            except Exception as e:
                raise e

    @property
    def urls(self) -> list[str]:
        return [*self._urls, *self._router.urls]

    @property
    def path(self) -> path:
        if self._auto_load_modules:
            if self.module:
                importlib.import_module(self.module)
            else:
                self._load_all_modules()

            self._log("Done loading views")

        return path(
            self.endpoint,
            include((self.urls, "main"), namespace=self.namespace),
        )
