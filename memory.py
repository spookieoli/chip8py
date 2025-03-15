class Memory:
    def __init__(self) -> None:
        """
        Represents a memory manager for managing a byte-addressable memory space.

        This class allows for initialization of a block of memory, typically used in systems or
        applications requiring memory management functionalities. The memory is represented as
        a bytearray that can be referenced or manipulated during the program execution.

        Attributes:
            _memory (bytearray): A bytearray object initialized to a size of 4096 bytes,
                                 representing the memory space.
        """
        # Initialize the memory
        self._memory = bytearray(4096)

    def get_memory(self, address: int) -> int:
        """
        Retrieves the value from a memory address in the memory array.

        This function accesses an internal memory structure based on the provided
        address. It validates that the address falls within the acceptable range.
        If the address is invalid, a ValueError is raised. The function returns
        the integer value stored at the specified address.

        :param address: The memory address to retrieve the value from. Must be
            an integer within the range 0 to 4095.
        :type address: int
        :return: The value stored at the specified memory address.
        :rtype: int
        :raises ValueError: If the address is not within the allowed range (0-4095).
        """

        # check if address is between 0 and 4095
        if address < 0 or address > 4095:
            raise ValueError("Address must be between 0 and 4095")
        return self._memory[address]

    def set_memory(self, address: int, value: int) -> None:
        """
        Sets a value at a specified memory address in the memory object. This method
        checks if the provided address and value are within their respective valid
        ranges. The valid range for the address is 0 to 4095, and for the value, it is
        0 to 255. If the values are out of bounds, a ValueError is raised.

        :param address: Memory address to set the value. Must be between 0 and 4095.
        :type address: int
        :param value: Value to be set at the specified memory address. Must be between
            0 and 255.
        :type value: int

        :raises ValueError: If the address is not in the range between 0 and 4095 or
            if the value is not in the range between 0 and 255.

        :return: None
        """

        # check if address is between 0 and 4095
        if address < 0 or address > 4095:
            raise ValueError("Address must be between 0 and 4095")

        # check if value is between 0 and 255
        if value < 0 or value > 255:
            raise ValueError("Value must be between 0 and 255")

        # set the value of the memory address
        self._memory[address] = value

    def get_memory_range(self, start: int, end: int) -> bytearray:
        """
        Retrieves a specific range of memory from the internal memory buffer.

        This method allows access to a range of memory addresses within a defined
        memory buffer. The method ensures that the start and end addresses are valid
        and within a permissible range. The range must also be specified correctly,
        with the start address being less than or equal to the end address. If the
        conditions are not met, a `ValueError` is raised.

        :param start: The starting address of the memory range. Must be an integer
            between 0 and 4095 (inclusive).
        :param end: The ending address of the memory range. Must be an integer
            between 0 and 4095 (inclusive).
        :return: A `bytearray` containing the memory values from the specified
            range.
        :rtype: bytearray

        :raises ValueError: If `start` or `end` is outside the valid range of 0 to 4095.
        :raises ValueError: If `start` is greater than `end`.
        """

        # check if start and end are between 0 and 4095
        if start < 0 or start > 4095:
            raise ValueError("Start address must be between 0 and 4095")
        if end < 0 or end > 4095:
            raise ValueError("End address must be between 0 and 4095")

        return self._memory[start:start + end]

    def set_memory_range(self, start: int, data: bytearray) -> None:
        """
        Updates a specific range of bytes in the memory starting from the
        given address with the provided data.

        This method modifies the internal memory by replacing a portion of it
        with the provided data, starting from the specified memory address.

        :param start: The starting address in memory where data should be written.
        :type start: int
        :param data: The data as a sequence of bytes which will overwrite the
            memory range.
        :type data: bytearray
        :return: None
        """
        self._memory[start:start + len(data)] = data
