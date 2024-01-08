from __future__ import annotations

import os
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum

from utils.exercise import Exercise


class Pulse(Enum):
    LOW = 0
    HIGH = 1


@dataclass
class Module(ABC):
    name: str
    destination_modules: list[Module] = field(default_factory=list)
    pulse_queue: list[tuple[Pulse, str]] = field(default_factory=list)
    counter: complex = complex(0, 0)

    def add_destination_module(self, module: Module) -> None:
        self.destination_modules.append(module)

    def send_pulse_to_all(self, pulse: Pulse) -> None:
        for module in self.destination_modules:
            self.send_pulse_to(pulse, module)

    def send_pulse_to(self, pulse: Pulse, module: Module) -> None:
        module.receive_pulse(pulse, self.name)

    def receive_pulse(self, pulse: Pulse, from_module: str) -> None:
        self.pulse_queue.append((pulse, from_module))
        # print(f'{from_module} -{pulse}> {self.name}')
        # counter
        is_low_pulse: bool = pulse == Pulse.LOW
        self.counter += complex(is_low_pulse, not is_low_pulse)

        # part 2
        if self.name == 'rx' and is_low_pulse:
            print('STOP', self.counter)

    def reset_pulse_queue(self):
        self.pulse_queue = []

    @abstractmethod
    def handle_pulses(self) -> list[Module]:
        pass


@dataclass
class BroadcasterModule(Module):
    def handle_pulses(self) -> list[Module]:
        for pulse, module_name in self.pulse_queue:
            self.send_pulse_to_all(pulse)
        self.reset_pulse_queue()
        return self.destination_modules


@dataclass
class FlipFlopModule(Module):
    state: bool = False

    def handle_pulses(self) -> list[Module]:
        res: list[Module] = []

        for pulse, module_name in self.pulse_queue:
            if pulse == Pulse.HIGH:
                continue

            self.switch_state()
            pulse_to_send: Pulse = self.get_pulse_to_send()
            self.send_pulse_to_all(pulse_to_send)
            res += self.destination_modules

        self.reset_pulse_queue()
        return res

    def switch_state(self):
        self.state = not self.state

    def get_pulse_to_send(self) -> Pulse:
        return Pulse.HIGH if self.state else Pulse.LOW


@dataclass
class ConjunctionModule(Module):
    memory: dict[str, Pulse] = field(default_factory=dict)

    def add_connected_module(self, module_name: str) -> None:
        self.memory[module_name] = Pulse.LOW

    def handle_pulses(self) -> list[Module]:
        res: list[Module] = []
        for pulse, module_name in self.pulse_queue:
            self.update_memory(module_name, pulse)

            pulse_to_send: Pulse
            is_only_high: bool = self.is_memory_only_high()
            if is_only_high:
                pulse_to_send = Pulse.LOW
            else:
                pulse_to_send = Pulse.HIGH
            self.send_pulse_to_all(pulse_to_send)
            res += self.destination_modules

        self.reset_pulse_queue()
        return res

    def update_memory(self, module_name: str, pulse: Pulse) -> None:
        self.memory[module_name] = pulse

    def is_memory_only_high(self) -> bool:
        return all([value == Pulse.HIGH for value in self.memory.values()])


class Problem(Exercise):
    modules: dict[str, Module]
    modules_to_handle: list[Module]

    def add_module(self, module: Module) -> None:
        self.modules[module.name] = module

    def push_button(self) -> None:
        broadcaster = self.modules.get('broadcaster')
        broadcaster.receive_pulse(Pulse.LOW, 'button')
        self.modules_to_handle = [broadcaster]

    def resolve(self, data: list[str], part: int) -> int | str:
        self.modules = {}
        self.modules_to_handle = []

        # first parsing
        for line in data:
            split: list[str] = line.split(' -> ')
            name: str = split[0]
            module: Module

            if name.startswith('&'):
                module = ConjunctionModule(name[1:])
            elif name.startswith('%'):
                module = FlipFlopModule(name[1:])
            else:  # name == 'broadcaster'
                module = BroadcasterModule(name)
            self.add_module(module)

        # second parsing
        for line in data:
            split: list[str] = line.split(' -> ')
            name: str = split[0]
            module: Module
            destination_modules_names: list[str] = split[1].split(', ')

            if name[0] in '&%':
                name = name[1:]

            module = self.modules.get(name)

            for destination_module_name in destination_modules_names:
                destination_module = self.modules.get(destination_module_name, None)

                if destination_module is not None:
                    module.add_destination_module(destination_module)

                    if isinstance(destination_module, ConjunctionModule):
                        destination_module.add_connected_module(module.name)

        iterations: int = 0
        while iterations < 1000 or part == 2:
            self.push_button()

            while len(self.modules_to_handle) > 0:
                module: Module = self.modules_to_handle.pop(0)
                next_modules_to_handle: list[Module] = module.handle_pulses()

                for next_module_to_handle in next_modules_to_handle:
                    self.modules_to_handle.append(next_module_to_handle)

            iterations += 1

        # [print(module) for module in self.modules.values()]

        return self.counter()

    def counter(self) -> int:
        counter_low_pulses: int = sum([int(module.counter.real) for module in self.modules.values()])
        counter_high_pulses: int = sum([int(module.counter.imag) for module in self.modules.values()])
        return counter_low_pulses * counter_high_pulses

    def part1(self, data: list[str]) -> int | str:
        return self.resolve(data, 1)

    def part2(self, data: list[str]) -> int | str:
        return self.resolve(data, 2)


def main() -> None:
    directory = os.path.dirname(__file__)
    problem = Problem(directory)

    problem.exec_part(1, True)
    problem.exec_part(2, False)


if __name__ == "__main__":
    main()
