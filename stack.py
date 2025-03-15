from register import Register

class Stack:
    """
    Represents a stack data structure.

    The Stack class is used to manage a stack stored as a bytearray. It interacts
    with a provided Register object to manage the stack pointer (SP). The stack
    supports basic push and pop operations within a limited size of 16 elements.

    :ivar _stack: Internal storage for the stack, a bytearray of size 16.
    :type _stack: list
    :ivar _register: The Register instance used for stack pointer management.
    :type _register: Register
    """
    def __init__(self, register: Register) -> None:
        """
        Represents a simple stack implementation used to store data, alongside a
        reference to a register object for additional operations.

        This class initializes a stack with a fixed size and associates it
        with an external register instance upon creation.

        :param register: The external register instance to be used with this stack.
        :type register: Register
        """
        self._stack = [0] * 16
        self._register = register

    def pop(self) -> int:
        """
        Removes and returns the top element from the stack. If the stack is empty,
        an exception is raised. This operation modifies the stack pointer by
        decrementing its value before accessing the element at the adjusted stack
        pointer index.

        :raises ValueError: If the stack is empty.
        :return: The integer value popped from the stack.
        :rtype: int
        """
        if self._register.get_sp() == 0:
            raise ValueError("Stack is empty")
        self._register.decrement_sp()
        return self._stack[self._register.get_sp()]

    def push(self, value: int) -> None:
        """
        Pushes a value onto the stack. Ensures that the stack size remains within
        defined limits by checking the stack pointer. If the stack has reached its
        maximum size, an exception will be raised. The value is added to the position
        indicated by the current stack pointer, and the stack pointer is incremented
        afterward.

        :param value: The integer value to push onto the stack.
        :type value: int
        :raises ValueError: If the stack is full when attempting to push a value.
        """
        if self._register.get_sp() == 15:
            raise ValueError("Stack is full")
        self._stack[self._register.get_sp()] = value
        self._register.increment_sp()