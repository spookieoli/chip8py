import time
import random

from register import Register
from memory import Memory
from stack import Stack
from keyboard import Keyboard
from screen import Screen
from romloader import RomLoader


class Chip:
    """
    Represents a Chip-8 emulator class, responsible for the emulation of the
    Chip-8 system's core functionality.

    This class is designed to emulate the primary components of the Chip-8 system
    including memory, registers, a stack, and keyboard, along with loading and
    running ROMs to display interactive games or applications on a screen. It also
    implements default system behavior like loading character sets, updating timers,
    and executing opcodes. The screen rendering can be scaled using a screen
    multiplier for better visualization.

    :ivar _screen_multiplier: The factor by which to scale the screen resolution.
    :type _screen_multiplier: int
    :ivar _register: Instance of a general purpose register set of the Chip-8 system.
    :type _register: Register
    :ivar _memory: Emulation of the Chip-8 memory (4 KB in total).
    :type _memory: Memory
    :ivar _stack: An abstraction of the stack used to manage subroutine calls.
    :type _stack: Stack
    :ivar _keyboard: Simulated keyboard interface for Chip-8 key inputs.
    :type _keyboard: Keyboard
    :ivar _screen: Instance of the screen rendering and display handler.
    :type _screen: Screen
    :ivar _romloader: Component responsible for loading game/application ROMs.
    :type _romloader: RomLoader
    """

    def __init__(self, game: str, screen_multiplier: int = 10):
        """
        Initialize the main Chip-8 emulator components and begin execution.

        The class is responsible for setting up the necessary components of the Chip-8
        emulator, including screen, memory, registers, stack, keyboard, and ROM loader.
        It also loads the default character set into memory and schedules the execution
        logic for screen updates. The `game` parameter specifies the path to the game
        ROM to be loaded, while the `screen_multiplier` parameter scales the size of the
        emulated screen rendering.

        :param game: Represents the path to the game ROM that will be loaded into memory.
        :type game: str
        :param screen_multiplier: Factor by which the screen size is scaled for display.
        :type screen_multiplier: int
        """
        # Screen multiplier is used to scale the screen size
        self._screen_multiplier = screen_multiplier

        # Initialize the registers
        self._register = Register()

        # Initialize the memory
        self._memory = Memory()

        # Initialize the stack
        self._stack = Stack(self._register)

        # initialize the Keyboard
        self._keyboard = Keyboard()

        # Initialize the screen
        self._screen = Screen("Chip-8 Emulator", 64, 32, 10, self._keyboard)

        # Load the given Rom into Memory
        self._romloader = RomLoader(game)

        # Load the ROM data into memory
        self._load_rom_data()

        # Load the default character set
        self._load_default_character_set()

        # Execute Logic and write screen
        self.logic()

        # enter the mainloop
        self._screen.mainloop()

    def _load_rom_data(self) -> None:
        """
        Loads the ROM data into memory, sets the memory data in a specific range,
        and initializes the program counter (PC) register to the designated
        starting address for execution. This process prepares the system for
        running applications by ensuring proper memory and register initialization.

        :raises Exception: If loading ROM data or setting memory fails.
        :raises Exception: If program counter (PC) register initialization fails.
        """
        data = self._romloader.get_rom_data()
        self._memory.set_memory_range(512, data)
        self._register.set_pc(0x200)

    def _load_default_character_set(self) -> None:
        """
        Loads the default character set into memory.

        This method initializes the system by storing a predefined set of characters
        into the system memory. The characters are represented as arrays of bytes and
        are used as a default character set. Each byte in the predefined list is loaded
        sequentially into memory at a predefined address.

        :raises MemoryError: If memory allocation fails.
        """

        # the default character set
        default_character_set = [0xF0, 0x90, 0x90, 0x90, 0xF0,
                                 0x20, 0x60, 0x20, 0x20, 0x70,
                                 0xF0, 0x10, 0xF0, 0x80, 0xF0,
                                 0xF0, 0x10, 0xF0, 0x10, 0xF0,
                                 0x90, 0x90, 0xF0, 0x10, 0x10,
                                 0xF0, 0x80, 0xF0, 0x10, 0xF0,
                                 0xF0, 0x80, 0xF0, 0x90, 0xF0,
                                 0xF0, 0x10, 0x20, 0x40, 0x40,
                                 0xF0, 0x90, 0xF0, 0x90, 0xF0,
                                 0xF0, 0x90, 0xF0, 0x10, 0xF0,
                                 0xF0, 0x90, 0xF0, 0x90, 0x90,
                                 0xE0, 0x90, 0xE0, 0x90, 0xE0,
                                 0xF0, 0x80, 0x80, 0x80, 0xF0,
                                 0xE0, 0x90, 0x90, 0x90, 0xE0,
                                 0xF0, 0x80, 0xF0, 0x80, 0xF0,
                                 0xF0, 0x80, 0xF0, 0x80, 0x80,
                                 ]

        # load the default characters into the memory
        for i, byte in enumerate(default_character_set):
            self._memory.set_memory(i, byte)

    def _read_short(self, index: int) -> int:
        """
        Reads a 16-bit short value from memory at the given index. The value is
        composed by reading two consecutive bytes from memory. The first byte
        is shifted 8 bits to the left, and the second byte is ORed with it to
        form the final short value.

        :param index: The starting index in memory from which the 16-bit short
            value will be read.
        :type index: int
        :return: A 16-bit integer value read from memory.
        :rtype: int
        """
        return self._memory.get_memory(index) << 8 | self._memory.get_memory(index + 1)

    def logic(self) -> None:
        """
        Contains the implementation of a logic function responsible for processing
        specific operational tasks and updating the current display of a screen.

        The function ensures that a sequence of operations is correctly executed and the
        result is visually reflected on the screen, maintaining state consistency.

        :return: None
        """
        # clear the screen
        # self._screen.clear()

        # check if the delaytimer is set
        delay_time = self._register.get_dt()
        if delay_time > 0:
            time.sleep(0.0001 * delay_time)
            self._register.decrement_dt()

        # play a sound if soundtimer is set
        if self._register.get_st() > 0:
            self._play_sound()
            self._register.decrement_st()

        # read next data from
        opcode = self._read_short(self._register.get_pc())

        # increment the programm counter
        self._register.increment_pc()

        # excute the opcode
        self._execute_opcode(opcode)

        # write to the canvas
        self._screen.write_screen()

        # call the logic function again
        self._screen.master.after(1, self.logic)

    def _play_sound(self):
        pass

    def _execute_opcode(self, opcode: int) -> None:
        """
        Executes the given opcode by performing the associated operation.

        This method handles specific operation codes defined by the system.
        Each opcode matches a predefined functionality that can manipulate the screen,
        the program counter, or other system components. Invalid opcodes (not explicitly
        handled) are ignored.

        :param opcode: The operation code to be executed.
        :type opcode: int
        :return: None
        """
        match opcode:
            case 0x00E0:
                # Clear the screen
                self._screen.clear_screen_array()
            case 0x00EE:
                # return from a subroutine
                self._register.set_pc(self._stack.pop())
            case _:
                # execute extended opcodes
                self._execute_extended(opcode)

    def _execute_extended(self, opcode: int) -> None:
        """
        Executes the provided opcode by parsing its components and performing the relevant
        operation. The operation is determined based on the highest nibble of the opcode
        and can include actions such as modifying registers, skipping instructions,
        manipulating the stack, or executing extended opcode sets.

        :param opcode: The 16-bit machine code instruction to be executed.
        :type opcode: int
        :return: This method does not return a value as its execution modifies the
            state of various internal components, like registers, program counter,
            or stack.
        :rtype: None
        """
        # extract the opcode parts
        nnn = opcode & 0x0FFF
        n = opcode & 0x000F
        x = (opcode & 0x0F00) >> 8
        y = (opcode & 0x00F0) >> 4

        # a match statement to handle the extended opcodes
        match opcode & 0xF000:
            case 0x1000:
                # jump to address nnn
                self._register.set_pc(nnn)
            case 0x1000:
                # jump to address nnn
                self._register.set_pc(nnn)

            case 0x2000:
                # call subroutine at nnn
                self._stack.push(self._register.get_pc())
                self._register.set_pc(nnn)

            case 0x3000:
                # skip next instruction if Vx == nn
                if self._register.get_v(x) == (opcode & 0x00FF):
                    self._register.increment_pc()
            case 0x4000:
                # skip next instruction if Vx != nn
                if self._register.get_v(x) != (opcode & 0x00FF):
                    self._register.increment_pc()
            case 0x5000:
                # skip next instruction if Vx == Vy
                if self._register.get_v(x) == self._register.get_v(y):
                    self._register.increment_pc()
            case 0x6000:
                # set Vx to nn
                self._register.set_v(x, opcode & 0x00FF)
            case 0x7000:
                # add nn to Vx
                self._register.set_v(x, (self._register.get_v(x) + (opcode & 0x00FF)) & 0xFF)
            case 0x8000:
                # execute extended 8 opcodes
                self._execute_extended_8(opcode)
            case 0x9000:
                # skip next instruction if Vx != Vy
                if self._register.get_v(x) != self._register.get_v(y):
                    self._register.increment_pc()
            case 0xA000:
                # set I to nnn
                self._register.set_i(nnn)
            case 0xB000:
                # jump to address nnn + V0
                self._register.set_pc(nnn + self._register.get_v(0))
            case 0xC000:
                # set Vx to random number AND nn
                self._register.set_v(x, random.randint(0, 255) & (opcode & 0x00FF))
            case 0xD000:
                # draw a sprite at position Vx, Vy with n bytes of sprite data
                self._screen.draw_sprite(self._register.get_v(x), self._register.get_v(y),
                                         self._memory.get_memory_range(self._register.get_i(), n))
            case 0xE000:
                # execute extended E opcodes
                self._execute_extended_e(opcode)
            case 0xF000:
                # execute extended F opcodes
                self._execute_extended_f(opcode)
            case _:
                # ignore invalid opcodes
                pass

    def _execute_extended_8(self, opcode: int) -> None:
        """
        Handles the execution of extended opcodes in the 0x8XY_ category. This method decodes
        the given opcode, extracts its components, and performs the operation based on the
        instruction type specified in the least significant nibble of the opcode. Operations
        executed by this method include logical operations (OR, AND, XOR), register
        assignments, and arithmetic operations with optional flag adjustments in the VF
        register.

        :param opcode: The 16-bit opcode to be executed. Encodes the operation to perform and
                       the registers it operates on.
        :type opcode: int
        :return: None
        :rtype: None
        """
        # extract the opcode parts
        n = opcode & 0x000F
        x = (opcode & 0x0F00) >> 8
        y = (opcode & 0x00F0) >> 4

        # a match statement to handle the extended 8 opcodes
        match n:
            case 0x0000:
                # set Vx to Vy
                self._register.set_v(x, self._register.get_v(y))
            case 0x0001:
                # set Vx to Vx OR Vy
                self._register.set_v(x, self._register.get_v(x) | self._register.get_v(y))
            case 0x0002:
                # set Vx to Vx AND Vy
                self._register.set_v(x, self._register.get_v(x) & self._register.get_v(y))
            case 0x0003:
                # set Vx to Vx XOR Vy
                self._register.set_v(x, self._register.get_v(x) ^ self._register.get_v(y))
            case 0x0004:
                # add Vy to Vx, set VF to carry
                result = self._register.get_v(x) + self._register.get_v(y)
                self._register.set_v(x, result & 0xFF)
                self._register.set_v(0xF, 1 if result > 0xFF else 0)
            case 0x0005:
                # subtract Vy from Vx, set VF to NOT borrow
                self._register.set_v(0xF, 1 if self._register.get_v(x) > self._register.get_v(y) else 0)
                self._register.set_v(x, (self._register.get_v(x) - self._register.get_v(y)) & 0xFF)
            case 0x0006:
                # shift Vx right by 1, set VF to LSB of Vx
                self._register.set_v(0xF, self._register.get_v(x) & 0x1)
                self._register.set_v(x, self._register.get_v(x) >> 1)
            case 0x0007:
                # set Vx to Vy - Vx, set VF to NOT borrow
                self._register.set_v(0xF, 1 if self._register.get_v(y) > self._register.get_v(x) else 0)
                self._register.set_v(x, (self._register.get_v(y) - self._register.get_v(x)) & 0xFF)
            case 0x000E:
                # shift Vx left by 1, set VF to MSB of Vx
                self._register.set_v(0xF, (self._register.get_v(x) & 0x80) >> 7)
                self._register.set_v(x, (self._register.get_v(x) << 1) & 0xFF)
            case _:
                # ignore invalid opcodes
                pass

    def _execute_extended_e(self, opcode: int) -> None:
        """
        Handles the execution of extended opcodes in the 0xEX__ category. This method decodes
        the given opcode, extracts its components, and performs the operation based on the
        instruction type specified in the least significant byte of the opcode. Operations
        executed by this method include key press checks and conditional skips based on key
        states.

        :param opcode: The 16-bit opcode to be executed. Encodes the operation to perform and
                       the registers it operates on.
        :type opcode: int
        :return: None
        :rtype: None
        """
        # extract the opcode parts
        x = (opcode & 0x0F00) >> 8

        # a match statement to handle the extended E opcodes
        match opcode & 0x00FF:
            case 0x009E:
                # skip next instruction if key in Vx is pressed
                if self._keyboard.is_key_down(self._register.get_v(x)):
                    self._register.increment_pc()

            case 0x00A1:
                # skip next instruction if key in Vx is not pressed
                if not self._keyboard.is_key_down(self._register.get_v(x)):
                    self._register.increment_pc()
            case _:
                # ignore invalid opcodes
                pass

    def _execute_extended_f(self, opcode: int) -> None:
        """
        Handles the execution of extended opcodes in the 0xFX__ category. This method decodes
        the given opcode, extracts its components, and performs the operation based on the
        instruction type specified in the least significant byte of the opcode. Operations
        executed by this method include setting register values based on key states, updating
        the delay timer, and waiting for key presses.

        :param opcode: The 16-bit opcode to be executed. Encodes the operation to perform and
                       the registers it operates on.
        :type opcode: int
        :return: None
        :rtype: None
        """
        # extract the opcode parts
        x = (opcode & 0x0F00) >> 8

        # a match statement to handle the extended F opcodes
        match opcode & 0x00FF:
            case 0x0007:
                # set Vx to delay timer value
                self._register.set_v(x, self._register.get_dt())
            case 0x000A:
                # wait for key press, store key in Vx
                self._register.set_v(x, self._keyboard.is_key_down(int(self._register.get_v(x))))
            case 0x0015:
                # set delay timer to Vx
                self._register.set_dt(self._register.get_v(x))
            case 0x0018:
                # set sound timer to Vx
                self._register.set_st(self._register.get_v(x))
            case 0x001E:
                # add Vx to I
                self._register.set_i((self._register.get_i() + self._register.get_v(x)) & 0xFFFF)
            case 0x0029:
                # set I to the location of the sprite for the character in Vx
                self._register.set_i(self._register.get_v(x) * 5)
            case 0x0033:
                # store BCD representation of Vx in memory locations I, I+1, I+2
                value = self._register.get_v(x)
                self._memory.set_memory(self._register.get_i(), value // 100)
                self._memory.set_memory(self._register.get_i() + 1, (value // 10) % 10)
                self._memory.set_memory(self._register.get_i() + 2, value % 10)
            case 0x0055:
                # store registers V0 through Vx in memory starting at location I
                for i in range(x + 1):
                    self._memory.set_memory(self._register.get_i() + i, self._register.get_v(i))
            case 0x0065:
                # read registers V0 through Vx from memory starting at location I
                for i in range(x + 1):
                    self._register.set_v(i, self._memory.get_memory(self._register.get_i() + i))
            case _:
                # ignore invalid opcodes
                pass


if __name__ == "__main__":
    chip = Chip("PONG")
