import traceback

import pyblish.api
import pyblish.util
from Qt import QtCore, QtGui, QtWidgets  # pylint: disable=no-name-in-module


class Ui_Form(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(Ui_Form, self).__init__(parent)
        self.create_ui()
        self.populate_ui()

    def create_ui(self):

        # optional stylesheet
        try:
            import PyQt5_stylesheets
            self.setStyleSheet(PyQt5_stylesheets.load_stylesheet_pyqt5(style="style_Dark"))
        except ImportError:
            pass
        
        self.dropdown_families = QtWidgets.QComboBox()
        # self.dropdown_validators = QtWidgets.QComboBox()
        self.list_instance = QtWidgets.QListWidget()
        self.list_validators = QtWidgets.QListWidget()
        self.button_check = QtWidgets.QPushButton('Check All')
        self.button_fix = QtWidgets.QPushButton('Fix All')
        self.textbox_validator_info = QtWidgets.QTextEdit()

        # get list of collector plugins we just ran
        # self.collectors = list(p for p in self.plugins if pyblish.lib.inrange(
        #     number=p.order,
        #     base=pyblish.api.CollectorOrder))

        vlayout_instances = QtWidgets.QVBoxLayout()
        vlayout_instances.addWidget(self.dropdown_families)
        vlayout_instances.addWidget(self.list_instance)
        vlayout_instances.addWidget(self.button_check)

        vlayout_validators = QtWidgets.QVBoxLayout()
        # vlayout_validators.addWidget(self.dropdown_validators)
        vlayout_validators.addWidget(self.textbox_validator_info)
        vlayout_validators.addWidget(self.list_validators)
        vlayout_validators.addWidget(self.button_fix)

        hlayout = QtWidgets.QHBoxLayout()
        hlayout.addLayout(vlayout_instances)
        hlayout.addLayout(vlayout_validators)
        self.setLayout(hlayout)

        # hookup button click
        self.button_check.clicked.connect(self.clicked_check)
        self.button_fix.clicked.connect(self.clicked_fix)
        self.dropdown_families.currentIndexChanged.connect(self.family_selected)
        # TODO self.dropdown_validators.currentIndexChanged.connect(self.family_changed)
        self.list_instance.currentItemChanged.connect(self.instance_selected)
        self.list_validators.currentItemChanged.connect(self.validator_selected)
        self.list_validators.installEventFilter(self)

        # font = self.textbox_validator_info.font()
        # font.setPointSize(12)
        # self.textbox_validator_info.setFont(font)
        self.textbox_validator_info.setReadOnly(True)
        # dont wrap text
        self.textbox_validator_info.setLineWrapMode(QtWidgets.QTextEdit.NoWrap)

    # todo use action.on to filter when to show. ex. "failedOrWarning"

    def populate_ui(self):
        # get data from pyblish
        self.plugins = pyblish.api.discover()
        self.context = pyblish.util.collect(plugins=self.plugins)
        self.context = pyblish.util.validate(context=self.context, plugins=self.plugins)

        # fill in data in UI
        self.populate_families_dropdown()
        self.populate_instances_list()

    def clicked_check(self):
        self.plugins = pyblish.api.discover()
        self.context = pyblish.util.collect(plugins=self.plugins)
        self.context = pyblish.util.validate(context=self.context, plugins=self.plugins)

        self.populate_families_dropdown()
        self.populate_instances_list()
        # rerun validation plugins

    def clicked_fix(self):
        # TODO run fix action on plugins that failed/warning
        # get all plugins for this instance

        for plugin in self.plugins:
            try:
                if hasattr(plugin, 'fix'):
                    pyblish_action = plugin.fix
                    pyblish_action.process(self=pyblish_action, context=self.context, plugin=plugin)
            except Exception as e:
                print(traceback.print_tb(e.__traceback__))
                print('failed to fix:', e)

        # TODO rerun validation
        # TODO update UI
        self.clicked_check()

    # TODO make actions feel less hacky
    def eventFilter(self, source, event):
        menu = QtWidgets.QMenu()

        if event.type() == QtCore.QEvent.ContextMenu and source is self.list_validators:
            item = source.itemAt(event.pos())
            plugin = item.pyblish_data
            for action in plugin.actions:
                q_action = menu.addAction(action.label)
                q_action.triggered.connect(
                    lambda action=action, item=item: self.clicked_action(pyblish_action=action, item=item)
                )

            menu.exec_(event.globalPos())
            return True
        return super(Ui_Form, self).eventFilter(source, event)

    # TODO make actions feel less hacky
    def clicked_action(self, pyblish_action=None, item=None):
        plugin = item.pyblish_data
        try:
            pyblish_action.process(self=pyblish_action, context=self.context, plugin=plugin)
        except Exception as e:
            print(traceback.print_tb(e.__traceback__))
            print(e)
            # todo show failed action in UI

    def populate_families_dropdown(self):
        self.dropdown_families.clear()
        self.dropdown_families.addItem('All')
        families = set([*(instance.data['family'] for instance in self.context)])
        for family in families:
            self.dropdown_families.addItem(family)

    def populate_instances_list(self):
        self.list_instance.clear()
        for instance in self.context:
            item = QtWidgets.QListWidgetItem()
            item.setText(instance.data["family"].upper() + ': ' + str(instance))
            item.pyblish_data = instance
            self.color_item(item, instance)
            self.list_instance.addItem(item)

    def populate_validation_plugins_list(self, selected_instance):
        self.list_validators.clear()

        if selected_instance is None:
            return

        plugins = pyblish.api.plugins_by_instance(self.plugins, selected_instance)
        for plugin in plugins:
            if not issubclass(plugin, pyblish.api.InstancePlugin):
                continue

            item = QtWidgets.QListWidgetItem()
            item.setText(plugin.label)
            item.pyblish_data = plugin
            self.color_item(item, selected_instance)
            self.list_validators.addItem(item)

    def family_selected(self):
        """
        when user selects family/category from dropdown, we hide/show matching instances
        """
        current_family = self.dropdown_families.currentText()

        # show all instances
        if current_family == 'All':
            for index in range(self.list_instance.count()):
                self.list_instance.item(index).setHidden(False)
            return

        # hide instances by family
        for index in range(self.list_instance.count()):
            item = self.list_instance.item(index)
            instance = item.pyblish_data
            if instance.data['family'] == current_family:
                item.setHidden(False)
            else:
                item.setHidden(True)

        self.list_validators.clear()

    def instance_selected(self, arg=None):
        if not arg:
            return

        # # if we click on an instance, we run plugins_by_instance and fill list with match
        selected_instance = arg.pyblish_data
        self.populate_validation_plugins_list(selected_instance)

    def validator_selected(self, arg=None):
        if not arg:
            return
        selected_plugin = arg.pyblish_data
        self.textbox_validator_info.setText(selected_plugin.__doc__)

    def color_item(self, item, related_instance):
        item_data = item.pyblish_data

        errors = False
        warning = False
        has_run = False

        # item_data is an instance, so the item is in the isntance list
        # parse through results because pyblish doesnt do Object Oriented results yet :(
        if type(item_data) == pyblish.plugin.Instance:
            instance = item.pyblish_data

            plugins = pyblish.api.plugins_by_instance(self.plugins, instance)
            # check if all these were success.

            # import pprint
            # try:
            #     print("------------------")
            #     print(instance)
            #     data = instance.data
            #     print("------------------")
            #     pprint.pprint(data)
            #     print("------------------")
            # except:
            #     pass

            for entry in self.context.data['results']:
                results_plugin = entry.get('plugin', None)
                results_instance = entry.get('instance', None)

                if not results_plugin:
                    continue

                if instance != results_instance:
                    continue

                if results_plugin not in plugins:
                    continue

                if not issubclass(results_plugin, pyblish.api.InstancePlugin):
                    continue

                has_run = True

                for record in entry["records"]:
                    warning |= record.levelname == "WARNING"
                    errors |= record.levelname == "ERROR"

                if not entry['success']:
                    errors = True
                    # todo append errors?
                    break

        # item_data is a plugin, so the item is in the plugins list
        # elif issubclass(data, pyblish.api.InstancePlugin):
        elif issubclass(item_data, pyblish.api.InstancePlugin):
            plugin = item_data
            for result in self.context.data['results']:
                results_plugin = result.get('plugin', None)
                results_instance = result.get('instance', None)

                if not results_instance:
                    continue

                if results_instance != related_instance:
                    continue

                if plugin != results_plugin:
                    continue

                has_run = True

                for record in result["records"]:
                    warning |= record.levelname == "WARNING"
                    errors |= record.levelname == "ERROR"

                if not result['success']:
                    errors = True
                    break
        else:
            print(item_data)
            print(type(item_data))
            print(item_data.__class__)
            print(issubclass(type(item_data), pyblish.api.InstancePlugin))

        # get_failed_instances(self.context, plugin)
        # # TODO get result of instance/plugin: success, warning or error
        # errors = self.context.data[plugin.label]

        # if issubclass(data, pyblish.api.InstancePlugin):
        #     pass

        color = 'white'
        if errors:
            color = 'red'
        elif warning:
            color = 'orange'
        elif has_run:
            color = 'lime'

        # item.setBackground(QtGui.QBrush(QtGui.QColor((color))))
        item.setForeground(QtGui.QBrush(QtGui.QColor((color))))
        # item.setForeground(QtGui.QBrush(QtGui.QColor('white')))

# # todo add this to pyblish: plugin.get_failed_instances(SELF, context)
# # there is also instances_by_plugin
# def get_failed_instances(context, plugin):
#     instances = []
#     for result in context.data["results"]:
#         if result["error"] and result["plugin"] == plugin:
#             instance = result["instance"]
#             instances.extend(instance)
#     return instances


def show(parent=None):
    app = QtWidgets.QApplication.instance()

    new_app_created = False
    if not app:
        app = QtWidgets.QApplication([])
        new_app_created = True

    window = Ui_Form(parent=parent)
    window.show()

    if new_app_created:
        app.exec()

    return window
