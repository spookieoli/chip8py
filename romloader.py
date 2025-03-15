class RomLoader:
    def __init__(self, rom: str):
        """
        Represents a ROM-based class for processing and managing ROM data.

        This class provides functionality to initialize and manage a ROM resource,
        ensuring that the data is read appropriately on initialization.

        :param rom: A file path or identifier representing the ROM to be processed.
        :type rom: str
        """
        self.rom = rom
        self._data = self._read_rom()

    def _read_rom(self) -> bytearray:
        """
        Reads the ROM file specified by the `rom` attribute in binary mode and
        returns its contents as a bytearray. This method is intended for internal
        use only.

        :return: The contents of the ROM file as a bytearray.
        :rtype: bytearray
        """
        with open(self.rom, "rb") as f:
            return bytearray(f.read())

    def get_rom_data(self) -> bytearray:
        """
        Retrieves the data stored in the ROM as a bytearray.

        This method provides access to the internal storage of ROM data and
        returns it as a bytearray. The data represents the content currently
        stored in the ROM.

        :return: The data stored in the ROM as a bytearray
        :rtype: bytearray
        """
        return self._data
