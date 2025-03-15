import tkinter as tk


class Keyboard:
    """
    Represents a Keyboard class for managing key states.

    This class is used to manage and track the state of keyboard keys. It enables
    checking whether specific keys are pressed ("down") or released ("up") and allows
    modification of those states based on key events. The implementation uses an
    internal dictionary to keep track of the current state of keys, where each key is
    mapped to a boolean value indicating whether it is active (pressed) or inactive
    (released).

    :ivar _keys: Dictionary for tracking the state of keys.
    :type _keys: dict
    """
    def __init__(self):
        """
        Represents an initializer for internal keys setting up.

        This class constructor initializes the attribute `_keys` by invoking the
        method `_set_keys`, allowing the setup of necessary internal keys when
        the object is instantiated.

        Attributes:
            _keys (Any): Represents the internal keys initialized by `_set_keys`.
        """
        self._keys = self._set_keys()

        # a dict with the key mapping
        self._key_mapping = {
            "0": 0, "1": 1, "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9, "a": 10, "b": 11, "c": 12, "d": 13, "e": 14, "f": 15
        }

    def is_key_up(self, key: str) -> bool:
        """
        Determines if a specific key is in the "up" or released state. A key is considered
        "up" if it is not currently active or pressed. Useful for input management in
        applications that rely on key states.

        :param key: The key for which the state is being checked.
        :type key: str
        :return: True if the specified key is in the "up" state, False otherwise.
        :rtype: bool
        """
        return not (self._keys[key])

    def is_key_down(self, key: int) -> bool:
        """
        Determines if a specific key is currently being pressed.

        This method checks the state of the given key to see if it is actively
        pressed and returns a boolean value indicative of its state. It uses
        the internal `_keys` attribute to determine the key's current state.

        :param key: The key to be checked.
        :type key: str
        :return: True if the given key is pressed, False otherwise.
        :rtype: bool
        """
        return self._keys[key]

    def key_down(self, key: str) -> None:
        """
        Tracks a key press event by updating the internal state to mark the key as pressed.

        :param key: The key that was pressed.
        :type key: str
        :return: None
        """
        self._keys[key] = True

    def key_up(self, key: str) -> None:
        """
        Handles the release of a specific key by marking it as unpressed in the internal
        key tracking dictionary.

        This method modifies the internal `_keys` dictionary of the instance by setting
        the provided key's value to `False`, indicating that the key is no longer being
        pressed. It assumes the key is represented as a string and exists in the `_keys`
        dictionary.

        :param key: The string representing the key to be updated in the keys tracking
            dictionary.
        :type key: str
        :return: None
        """
        self._keys[key] = False

    def _set_keys(self) -> dict:
        """
        Generates and returns a dictionary mapping specific keys to their initial
        boolean values of False. The function is primarily intended to provide a
        default setup for a key-value structure, where each key corresponds to
        a character representation from '0' to '9' and 'a' to 'f'. The values are
        set to False, representing a preliminary inactive or unchecked state.

        :return: A dictionary where character keys ('0'-'9', 'a'-'f') are
            mapped to boolean values indicating their initial inactive state.
        :rtype: dict
        """
        return {
            0: False
            , 1: False
            , 2: False
            , 3: False
            , 4: False
            , 5: False
            , 6: False
            , 7: False
            , 8: False
            , 9: False
            , 10: False
            , 11: False
            , 12: False
            , 13: False
            , 14: False
            , 15: False
        }

    def key_event(self, event):
        """
        Handles key events for both key press and key release actions. This method listens
        for key events and updates the internal state of keys accordingly.

        :param event: An event object that contains details about the type of event
            (KeyPress or KeyRelease) and the key symbol being pressed or released.
        :type event: tk.Event
        :return: None
        """
        if event.type == '2':
            if event.keysym in self._key_mapping:
                self._keys[self._key_mapping[event.keysym]] = True
        elif event.type == '3':
            if event.keysym in self._key_mapping:
                self._keys[self._key_mapping[event.keysym]] = False
