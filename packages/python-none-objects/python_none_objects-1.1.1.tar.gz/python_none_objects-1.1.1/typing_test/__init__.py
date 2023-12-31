"""
This file is part of python-none-objects library.

python-none-objects is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

python-none-objects is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
See the GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License
along with python-none-objects.
If not, see <http://www.gnu.org/licenses/>.

©Copyright 2023 Laurent Lyaudet
"""
import sys
from typing import Collection, Container, Iterable, Mapping

sys.path.insert(0, "../src/")
from python_none_objects import (
    NoneCollection,
    NoneContainer,
    NoneIterable,
    NoneMapping,
)


def foo_collection(x: Collection[str] = NoneCollection) -> bool:
    # Pass typing
    for y in x:
        print(f"foo {y}")
    return "toto" in x


def foo_iterable(x: Iterable[str] = NoneIterable) -> None:
    # Pass typing
    for y in x:
        print(f"foo {y}")


def foo_container(x: Container[str] = NoneContainer) -> bool:
    # Pass typing
    return "toto" in x


def foo_mapping(x: Mapping[str, str] = NoneMapping) -> None:
    # Pass typing
    for y, z in x.items():
        print(f"foo {y} bar {z}")


foo_collection()
foo_iterable()
foo_container()
foo_mapping()
