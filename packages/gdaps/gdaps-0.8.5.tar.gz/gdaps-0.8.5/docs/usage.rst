.. usage:

*****
Usage
*****

Creating plugins
================
If you use git in your project, install the ``gitpython`` module (``pip install gitpython``). ``startplugin`` will determine your git user/email automatically and use it.

Create a plugin using a Django management command:

.. code-block:: bash

    ./manage.py startplugin fooplugin

This command asks a few questions, creates a basic Django app in the plugin path chosen in ``PluginManager.find_plugins()``. It provides useful defaults as well as a setup.py/setup.cfg file.

You now have two choices for this plugin:

* add it statically to ``INSTALLED_APPS``: see `Static plugins <#static-plugins>`_.
* make use of the dynamic loading feature: see `Dynamic plugins <#dynamic-plugins>`_.

Static plugins
--------------

In most of the cases, you will ship your application with a few
"standard" plugins that are statically installed. These plugins must be
loaded *after* the ``gdaps`` app.

.. code-block:: python

    # ...

    INSTALLED_APPS = [
        # ... standard Django apps and GDAPS
        "gdaps",

        # put "static" plugins here too:
        "myproject.plugins.fooplugin",
    ]

This plugin app is loaded as usual, but your GDAPS enhanced Django application
can make use of it's GDAPS features.

Dynamic plugins
---------------

By installing a plugin with pip, you can make your application
aware of that plugin too:

.. code:: bash

    pip install -e myproject/plugins/fooplugin

This installs the plugin as python module into the site-packages and
makes it discoverable using setuptools. From this moment on it should be
already registered and loaded after a Django server restart.

Of course this also works when plugins are installed from PyPi or from other directories, they don't have to be in the project's ``plugins`` folder. You can conveniently start developing plugins in there, and later move them into their own repository.


The plugin AppConfig
--------------------

Plugins' AppConfigs must provide an inner class named ``PluginMeta``, or a so named attribute pointing to an external class. For more information see :class:`gdaps.apps.PluginMeta`.

.. _Interfaces:

Interfaces
----------

Plugins can define interfaces, which can then be implemented by other
plugins. The cookiecutter template contains an ``<app_name>/api/interfaces.py`` file automatically.
It's not obligatory to put all Interface definitions in ``api.interfaces``, but it is a recommended coding style for GDAPS plugins:

.. code-block:: python

    from gdaps import Interface

    @Interface
    class ITextRenderer:
        """Documentation of the interface"""

        __service__ = True  # is the default
        text_type = None

        def render(self):
            pass

Predefined attributes are:

.. _service:

__service__
    If ``__service__ = True`` is set (which is the default), implementations are **instantiated when registered**. Iterating over the interface directly returns **instances** of the plugin.

    .. code-block:: python

        for plugin in ITextRenderer:
            compiled_text = plugin.render()

..

    If you use ``__service__ = False``, the plugins are not instantiated at registration, and
    iterations over instances will return **classes**, not instances.
    This may be desired for reducing memory footprint, for data classes, or plugin classes that just contain static or class methods.

    .. code-block:: python

        for plugin in INonServiceInterface:
            print(plugin.name)  # class attribute
            plugin.some_classmethod()

            # if you need instances, you have to instantiate the plugin here.
            # this is not recommended.
            p = plugin()
            p.do_something()

Interfaces can not be inherited to create other interfaces. If you inherit from an interface, you create an :ref:`Implementation <Implementations>`.

If you want to create some similar interfaces, use Mixins:

.. code-block:: python

    class IQuackWalkMixin:
        def do_something(self):
            pass

        def walk(self):
            pass

    @Interface
    class IDuck(IQuackWalkMixin):
        name = "Duck"

    @Interface
    class IGoose(IQuackWalkMixin)
        name = "Goose"

This way you can create interfaces that inherit from one or more mixins.


.. _Implementations:

Implementations
---------------

You can then easily implement this interface in any other file (in this
plugin or in another plugin) by subclassing the interface. Let's imagine a simple interface for letting plugins modify persons after creating them in a view:

.. code-block:: python

    @Interface
    class IModifyPersonAfterCreate
        """Modify persons after creating them in a view"""
        def modify(self, person: Person):
            """modify the person"""

You can straight-forwardly use implementations that are bound to an interface by iterating over that interface,
anywhere in your code - here in the CreateView of the main app:

.. code-block:: python

    from django.views.generic import CreateView
    from myproject.plugins.fooplugin.api.interfaces import IModifyPersonAfterCreate

    class CreatePersonView(CreateView):
        ...

        def form_valid(self, form):
            for plugin in IModifyPersonAfterCreate:
                plugin.modify(form.instance)

After defining an interface, any plugin found by GDAPS can implement this interface, let's say we want to capitalize the first name of the person:

.. code-block:: python

    from myproject.plugins.fooplugin.api.interfaces import IModifyPersonAfterCreate

    class PersonFirstnameCapitalizer(IModifyPersonAfterCreate):
        weight = 10

        def modify(self, person):
            person.first_name = person.first_name.capitalize()


Depending on the `__service__ <#service>`__ Meta flag, iterating over an Interface
returns either a **class** (``__service__ = False``) or an **instance** (``__service__ = True``), which is the default.


.. _template-support:

Template support
----------------

Plugins usually provide not only interfaces for the backend, but also for the frontend.
GDAPS supports plugin rendering in Django templates, which have to follow a certain
pattern. Define your interface in the providing app, e.g. as usually in
``.api.interfaces``, and let it inherit :class:`gdaps.api.interfaces.ITemplatePluginMixin`.
Don't forget to document your interface, so that the implementor knows what to expect.

.. code-block:: python

    # main_app/api/interfaces.py

    from gdaps.api import Interface
    from gdaps.api.interfaces import ITemplatePluginMixin

    @Interface
    class AnyItem(ITemplatePluginMixin):
        """Any list item, must contain a <li> element as root."""

This defines the plugin hook your plugins can implement.
You have to follow a certain pattern here, or let your interface inherit from ``ITemplatePluginMixin``, which helps your IDE with auto-suggestions.
The mixin defines a few methods and attributes you can make use of:

ITemplatePluginMixin
^^^^^^^^^^^^^^^^^^^^
.. _template:

template
    A string that is rendered as Template. For simple & small templates, e.g. one-liners. If this attribute is present, it is used.

.. _template_name:

template_name
    The usual django-like template name, where to find the template file within the ``templates`` directory, like "my_app/any_item.html"
    This attribute is used, if no ``template`` attribute is provided.

.. _context:

context
    a dict that provides the context for template rendering. It updates the global context.

If you want to customize it further, see :class:`gdaps.api.interfaces.ITemplatePluginMixin`

Now, in your other plugins, create the implementation:

.. code-block:: python

    # in plugin A

    from main_app.api.interfaces import AnyItem

    class SayFooItem(AnyItem):
        template = "<li>Foo!</li>"


    # in plugin B

    from main_app.api.interfaces import AnyItem

    class SayBarItem(AnyItem):
        template = "<li>Bar!</li>"

render_plugin hook
^^^^^^^^^^^^^^^^^^

Now in your main app's template, render the plugins using the ``render_plugins`` tag, with the interface name as parameter:

.. code-block:: django

    {% load gdaps %}

    <h1>Plugin sandbox</h1>
    <ul>
        {% render_plugins IAnyItem %}
    </ul>

That's all. GDAPS finds any plugins implementing this interface and renders them, one after another, in place. In this example, the resulting HTML code would be:

.. code-block:: html

    <li>Foo</li><li>Bar!</li>


As said before, the plugin templates can contain anything you like, not only ``<li>`` elements. You can use it for select options, cards on a dashboard, or whole page contents - it's up to you.


Extending Django's URL patterns
-------------------------------

App URLs
^^^^^^^^

App URLs are automatically detected by GDAPS/Django and put into your app's namespace. First, you have to add a code fragment to your global urls.py file:

.. code-block:: python

    from gdaps.pluginmanager import PluginManager
    urlpatterns = PluginManager.urlpatterns() + [
        # add your usual, fixed, non-plugin paths here.
    ]


GDAPS then loads and imports all available plugins' *urls.py*  files,
collects their ``urlpatterns`` variables and merges them into your application's global urlpattern, using your plugin's ``app_name`` as namespace:

.. code-block:: python

    from .views import MyUrlView, SomeViewSet
    from django.views.generic import TemplateView
    # fooplugin/urls.py

    app_name = "foo"

    # This will be included under the "foo/" namespace
    urlpatterns = [
        path("", TemplateView("foo/index.html").as_view(), name="index"),
        path("detail/", MyUrlView.as_view(), name="detail"),

        # ...
    ]


Global URLs
^^^^^^^^^^^

Sometimes, plugins need to provide top level URLs like `/about`
GDAPS also lets your plugin create those global, not namespaced URLs easily by using the ``root_urlpatterns`` attribute in your plugin's urls.py.

.. code-block:: python

    app_name = "about"

    # This will be merged into the global "/" urlpattern
    root_urlpatterns = [
        path("about/", SomeViewSet.as_view(), name="api")
    ]

    # and the ones under "/about/..."
    urlpatterns =  [...]

.. note::
    Plugins are self-responsible for their URLs and namespaces, and that they don't collide with others.

URL hooks
^^^^^^^^^

A third option which is a common pattern is that a plugin provides a "hook" under which *other* plugins can create sub-URLs. This is needed when you e.g. create an API, or a dashboard, or administration sites that should be pluggable.
This is easy too with GDAPS. In `your_app/api/interfaces`, create a plugin interface:

.. code-block:: python

    @Interface
    class IDashboardURL:
        urlpatterns = []

This interface offers a urlpattern that is included dynamically into the dashboard.

In your `global urls.py` file, you can include the interface as `dashboard/`:

.. code-block:: python

    urlpatterns = [
        ...
    ]
    for plugin in IDashboardURL:
        urlpatterns += plugin.urlpattern


Add an IDashBoardURL implementation to your plugin's urls.py, and its
urlpatterns will show up in the dashboard automatically:

.. code-block:: python

    # in myplugin
    from your_app.api.interfaces import IDashboardURL
    from . import views

    class MyPluginDashboardURL(IDashboardURL):  # class name doesn't matter.
        urlpatterns = [
            path("about/", views.DashboardIndexView.as_view(), name="index/")
        ]

All patterns that are listed here are merged into the global
.. _Settings:

Per-plugin Settings
-------------------

GDAPS allows your application to have own settings for each plugin
easily, which provide defaults, and can be overridden in the global
``settings.py`` file. Look at the example conf.py file (created by
``./manage.py startplugin fooplugin``), and adapt to your needs:

.. code-block:: python

    from django.test.signals import setting_changed
    from gdaps.conf import PluginSettings

    NAMESPACE = "FOOPLUGIN"

    # Optional defaults. Leave empty if not needed.
    DEFAULTS = {
        "MY_SETTING": "somevalue",
        "FOO_PATH": "django.blah.foo",
        "BAR": [
            "baz",
            "buh",
        ],
    }

    # Optional list of settings that are allowed to be in "string import" notation. Leave empty if not needed.
    IMPORT_STRINGS = (
        "FOO_PATH"
    )

    # Optional list of settings that have been removed. Leave empty if not needed.
    REMOVED_SETTINGS = ( "FOO_SETTING" )


    fooplugin_settings = PluginSettings("FOOPLUGIN", None, DEFAULTS, IMPORT_STRINGS)

Detailed explanation:

DEFAULTS
   The ``DEFAULTS`` are, as the name says, a default array of settings. If
   ``fooplugin_setting.BLAH`` is not set by the user in settings.py, this
   default value is used.

IMPORT_STRINGS
   Settings in a *dotted* notation are evaluated, they return not the
   string, but the object they point to. If it does not exist, an
   ``ImportError`` is raised.

REMOVED_SETTINGS
   A list of settings that are forbidden to use. If accessed, an
   ``RuntimeError`` is raised.

   This allows very flexible settings - as dependant plugins can easily
   import the ``fooplugin_settings`` from your ``conf.py``.

   However, the created conf.py file is not needed, so if you don't use
   custom settings at all, just delete the file.


Admin site
----------
GDAPS provides support for the Django admin site. The built-in ``GdapsPlugin`` model automatically
are added to Django's admin site, and can be administered there.

.. note::

    As GdapsPlugin database entries must not be edited directly, they are shown read-only in the admin.
    **Please use the 'syncplugins' management command to
    update the fields from the file system.**
    However, you can enable/disable or hide/show plugins via the admin interface.

If you want to disable the built-in admin site for GDAPS, or provide a custom GDAPS ModelAdmin, you can do this using:

.. code-block:: python

    GDAPS = {
        "ADMIN": False
    }


Signals
^^^^^^^
If you are using Django signals in your plugin, we recommend to put them into a ``signals`` submodule. Import it then from the ``AppConfig.ready()`` method.

.. code-block:: python

        def ready(self):
            # Import signals if necessary:
            from . import signals  # NOQA

.. seealso::
    Don't overuse the ``ready`` method. Have a look at the `Django documentation of ready() <https://docs.djangoproject.com/en/stable/ref/applications/#django.apps.AppConfig.ready>`_.
