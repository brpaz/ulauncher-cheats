"""Ulauncher extension main  class"""

import os
from ulauncher.api.client.Extension import Extension
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.event import KeywordQueryEvent, PreferencesEvent, PreferencesUpdateEvent
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.action.HideWindowAction import HideWindowAction
from ulauncher.api.shared.action.OpenAction import OpenAction
from ulauncher.api.shared.action.RunScriptAction import RunScriptAction
from ulauncher.config import CONFIG_DIR
from cheats import CheatsManager


class CheatsExtension(Extension):
    """ Main extension class """

    def __init__(self):
        """ init method """
        super(CheatsExtension, self).__init__()
        self.cheats_manager = CheatsManager(self.get_default_cheats_dir())
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())
        self.subscribe(PreferencesEvent, PreferencesEventListener())
        self.subscribe(PreferencesUpdateEvent,
                       PreferencesUpdateEventListener())

    def get_default_cheats_dir(self):
        """ Returns the place to look for the cheat sheats"""
        return os.path.join(CONFIG_DIR, 'ext_preferences', 'cheats')

    def show_empty_results_message(self):
        """ shows empty message """
        return RenderResultListAction([
            ExtensionResultItem(icon='images/icon.png',
                                name='No cheat sheets found for your query',
                                on_enter=HideWindowAction())
        ])

    def show_cheats_list(self, cheats):
        """ Shows the cheats list """

        hawkeye_bin = self.preferences['hawkeye_bin']
        use_hawkeye_default = self.preferences['use_hawkeye_as_default_action']

        items = []
        for cheat in cheats[:8]:
            if 'error' in cheat:
                items.append(ExtensionResultItem(icon='images/error.png',
                                                 name=cheat['error'],
                                                 on_enter=HideWindowAction()))
            else:
                if 'url' in cheat:
                    uri = cheat['path']
                    icon = 'images/url.png'
                else:
                    uri = 'file://%s' % cheat['path']
                    icon = 'images/icon.png'
                
                open_file_action = OpenAction(cheat['path'])
                open_in_hawkeye_action = RunScriptAction('%s --uri="%s"' % (hawkeye_bin, uri), [])

                if use_hawkeye_default == 'true':
                    primary_action = open_in_hawkeye_action
                    secondary_action = open_file_action
                else:
                    primary_action = open_file_action
                    secondary_action = open_in_hawkeye_action

                items.append(ExtensionResultItem(icon=icon,
                                                 name=cheat['normalized_name'],
                                                 on_enter=primary_action,
                                                 on_alt_enter=secondary_action))

        return RenderResultListAction(items)


class KeywordQueryEventListener(EventListener):
    """ Handles Keyboard input """

    def on_event(self, event, extension):
        """ Handles the event """
        cheats = extension.cheats_manager.find(event.get_argument())

        if not cheats:
            return extension.show_empty_results_message()

        return extension.show_cheats_list(cheats)

class PreferencesEventListener(EventListener):
    """
    Listener for prefrences event.
    It is triggered on the extension start with the configured preferences
    """

    def on_event(self, event, extension):
        if event.preferences["cheats_dir"] != "":
            extension.cheats_manager.set_cheats_dir(event.preferences['cheats_dir'])
        else:
            extension.cheats_manager.set_cheats_dir(extension.get_default_cheats_dir())
        extension.cheats_manager.set_urls_file(event.preferences['urls_file'])

class PreferencesUpdateEventListener(EventListener):
    """
    Listener for "Preferences Update" event.
    It is triggered when the user changes any setting in preferences window
    """

    def on_event(self, event, extension):
        if event.id == 'cheats_dir':
            if event.new_value != "":
                extension.cheats_manager.set_cheats_dir(event.new_value)
            else:
                extension.cheats_manager.set_cheats_dir(extension.get_default_cheats_dir())
        elif event.id == 'urls_file':
            extension.cheats_manager.set_urls_file(event.new_value)

if __name__ == '__main__':
    CheatsExtension().run()
