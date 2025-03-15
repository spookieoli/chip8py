class Register:
    """
    Represents a CHIP-8 Register system implementation to manage general-purpose registers,
    timers, program counter, and stack pointer.

    This class provides an interface to manipulate the registers, index register, timers,
    program counter, and stack pointer. It follows the constraints of the CHIP-8 system
    for allowable values and ranges for each component.

    :ivar _v: Represents the 16 general-purpose registers (V0 to VF). VF is commonly used
        as a flag register.
    :type _v: bytearray
    :ivar _i: Represents the index register. It is used to store memory addresses.
    :type _i: int
    :ivar _dt: Represents the delay timer. It is decremented at a fixed rate.
    :type _dt: int
    :ivar _st: Represents the sound timer. It produces a beep when it is nonzero and
        decremented at a fixed rate.
    :type _st: int
    :ivar _pc: Represents the program counter, which points to the address of the next
        instruction to execute in the CHIP-8 memory space.
    :type _pc: int
    :ivar _sp: Represents the stack pointer used for subroutine calls and storing return
        addresses.
    :type _sp: int
    """
    def __init__(self) -> None:
        """
        Builds the register object
        """
        self._v = bytearray(16) # the 16 general purpose registers
        self._i = 0 # the index register
        self._dt = 0 # the delay timer
        self._st = 0 # the sound timer
        self._pc = 0 # the program counter
        self._sp = 0 # the stack pointer

    def get_v(self, register: int) -> int:
        """
        Retrieves the value stored in a specified register.

        This method fetches the value of a given register by its index. The register
        index must be within the valid range of 0 to 15 (inclusive). If the index is
        out of this range, a ValueError is raised. This functionality is primarily
        useful when accessing specific registers in systems relying on a register-based
        architecture.

        :param register: The index of the register to retrieve the value from.
        :type register: int
        :return: The value stored in the specified register.
        :rtype: int
        :raises ValueError: If the register index is not within the range of 0 to 15.
        """

        # check if register is between 0 and 15
        if register < 0 or register > 15:
            raise ValueError("Register must be between 0 and 15")
        return self._v[register]

    def set_v(self, register: int, value: int) -> None:
        """
        Sets a specific register (V-register) to the provided value. Ensures that the
        register index is within the range of valid indices (0 to 15 inclusive) and that
        the value assigned to the register is within the valid range of 0 to 255
        inclusive. If either condition is violated, a ValueError is raised.

        :param register: The index of the register to be updated, restricted to values
            between 0 and 15 inclusive.
        :type register: int
        :param value: The value to set in the specified register, must be between 0
            and 255 inclusive.
        :type value: int
        :raises ValueError: If `register` is not between 0 and 15 inclusive.
        :raises ValueError: If `value` is not between 0 and 255 inclusive.
        :return: None
        """

        # check if register is between 0 and 15
        if register < 0 or register > 15:
            raise ValueError("Register must be between 0 and 15")

        # check if value is between 0 and 255
        if value < 0 or value > 255:
            raise ValueError("Value must be between 0 and 255")

        # set the value of the register
        self._v[register] = value

    def get_i(self) -> int:
        """
        Retrieves the value of the private attribute `_i`.

        This method returns the value of the private instance attribute `_i`
        that is expected to store an integer. The method is designed to provide
        read-only access to this internal attribute.

        :return: Current value of the private `_i` attribute
        :rtype: int
        """
        return self._i

    def set_i(self, value: int) -> None:
        """
        Sets the value of the index register (I) within the allowable range.

        This method is responsible for ensuring that the given value falls
        within the predetermined bounds of the index register. The index
        register is typically limited to a maximum value of 4095 due to
        the memory size constraints of 4096 bytes. If the value is outside
        of the valid range (0 to 4095), a `ValueError` will be raised.

        :param value: The new value to be assigned to the index register,
            which must be within the range of 0 to 4095.
        :type value: int
        :raises ValueError: If the provided value is less than 0 or greater
            than 4095.
        """

        # check if value is between 0 and 4095 - this is the maximum value of the index register
        # because we have a memory of 4096 bytes
        if value < 0 or value > 4095:
            raise ValueError("Value must be between 0 and 4095")

        # set the value of the index register
        self._i = value

    def get_dt(self) -> int:
        """
        Gets the value of the `_dt` attribute.

        This method is used to retrieve the integer value stored in the `_dt`
        attribute. It does not take any parameters and returns the value of `_dt`.

        :return: The value of `_dt` attribute.
        :rtype: int
        """
        return self._dt

    def set_dt(self, value: int) -> None:
        """
        Sets the delay timer to a specific value.

        The `set_dt` method assigns a new value to the delay timer after validating
        that the provided value is within the allowed range of 0 to 255. If the value
        does not fall within this range, a `ValueError` is raised to ensure that only
        valid values are set.

        :param value: The new value for the delay timer.
        :type value: int
        :raises ValueError: If the provided value is not within the valid
            range (0-255).
        :return: None
        """

        # check if value is between 0 and 255
        if value < 0 or value > 255:
            raise ValueError("Value must be between 0 and 255")

        # set the value of the delay timer
        self._dt = value

    def get_st(self) -> int:
        """
        Retrieve the value of the private attribute `_st`.

        This method returns the value of the `_st` attribute, which is an integer.
        It provides a getter interface for accessing the internal private attribute.

        :return: The value of the `_st` attribute as an integer.
        :rtype: int
        """
        return self._st

    def set_st(self, value: int) -> None:
        """
        Sets the sound timer to a specified value within an acceptable range. This method validates the given value to
        ensure it is within a permissible range of 0 to 255. If the value is out of bounds, an error is raised.

        :param value: The new value for the sound timer. Must be an integer within the range [0, 255].
        :type value: int
        :raises ValueError: If the given value is not within the acceptable range [0, 255].
        :return: This method does not return a value.
        :rtype: None
        """

        # check if value is between 0 and 255
        if value < 0 or value > 255:
            raise ValueError("Value must be between 0 and 255")

        # set the value of the sound timer
        self._st = value

    def get_pc(self) -> int:
        """
        Retrieves the current value of the private `_pc` attribute.

        This method provides access to the value of the `_pc` attribute, which is
        typically used to represent the program counter or a similar numerical
        value, in contexts where this encapsulated value must be read externally
        from the class instance.

        :return: The current value of the `_pc` attribute.
        :rtype: int
        """
        return self._pc

    def set_pc(self, value: int) -> None:
        """
        Sets the program counter value. The program counter must be assigned a value within
        the valid range of 0 to 4095 inclusive, which corresponds to the limit of a 4096-byte memory.
        If the value falls outside this range, a ValueError will be raised. This function ensures that
        only valid program counter values are set for proper memory addressing.

        :param value: The value to set as the program counter.
        :type value: int
        :raises ValueError: If the value is not in the range 0 to 4095.
        :return: None
        """

        # check if value is between 0 and 4095 - this is the maximum value of the program counter
        # because we have a memory of 4096 bytes
        if value < 0 or value > 4095:
            raise ValueError("Value must be between 0 and 4095")

        # set the value of the program counter
        self._pc = value

    def get_sp(self) -> int:
        """
        Retrieves the value of the internal `_sp` attribute.

        This method provides read-only access to the stack pointer represented
        by the `_sp` property of the object. It returns its value as an integer,
        allowing observation of the state without modifications.

        :return: The value of the `_sp` attribute.
        :rtype: int
        """
        return self._sp

    def set_sp(self, value: int) -> None:
        """
        Sets the stack pointer (SP) to a specified value after validation. The value must
        be within the permissible range (0 to 15).

        :param value: The integer value to set the stack pointer.
        :type value: int

        :raises ValueError: If the supplied value is not within the range [0, 15].

        :return: None
        """

        # check if value is between 0 and 15
        if value < 0 or value > 15:
            raise ValueError("Value must be between 0 and 15")

        # set the value of the stack pointer
        self._sp = value

    def increment_pc(self) -> None:
        """
        Increments the program counter (PC) by 2.

        This method updates the internal state of the program counter by
        adding 2 to its current value. It permanently alters the program
        counter's value.

        :return: None
        """
        self._pc += 2

    def decrement_pc(self) -> None:
        """
        Decrements the program counter (PC) by 2. This operation modifies the internal program counter state,
        reducing its value by 2, which is commonly used in scenarios where backtracking or stepping to a
        previous position within a program's execution flow is required.

        :return: None
        """
        self._pc -= 2

    def increment_sp(self) -> None:
        """
        Increments the `_sp` attribute by 1. This method is used for modifying
        the state of the `_sp` attribute while ensuring proper encapsulation
        within the class. It performs a straightforward incrementation operation
        on the integer stored in `_sp`.

        :return: None
        """
        self._sp += 1

    def decrement_sp(self) -> None:
        """
        Decrements the `_sp` attribute of the object by one unit.

        This method adjusts the `_sp` attribute's value by decreasing it. It can be
        used in contexts where decrementing this specific internal attribute is part
        of the logic flow. It does not accept arguments or return any value.

        :return: None
        """
        self._sp -= 1

    def decrement_dt(self) -> None:
        """
        Decreases the internal counter `_dt` by one. This function modifies the
        state of the object by decrementing the `_dt` attribute.
        """
        self._dt -= 1

    def decrement_st(self) -> None:
        """
        Decrements the value of the private attribute `_st` by 1.

        This method modifies the internal state of the object by reducing the value
        of `_st` by one each time it is called. It does not return any value.

        :return: None
        """
        self._st -= 1

