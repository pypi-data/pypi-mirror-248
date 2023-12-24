class Popup:
    """The Popup class represents a popup dialog in the page."""

    def __init__(self, popup_tree: dict, popup_name: str):
        self._tree = popup_tree
        self._name = popup_name

    def __str__(self):
        return f"Popup {self._name}"

    def accessibility_tree(self) -> dict:
        """
        Returns the part of accessibility tree where the popup node as the parent.

        Returns:
        dict: The part of accessibility tree wheree the popup no9de as the parent.
        """
        return self._tree

    def name(self) -> str:
        """
        Returns the name of the popup.

        Returns:
        str: The name of the popup.
        """
        return self._name
