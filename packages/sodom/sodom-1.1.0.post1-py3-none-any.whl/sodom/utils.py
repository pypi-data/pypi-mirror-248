__license__ = '''
sodom
Copyright (C) 2023  Dmitry Protasov (inbox@protaz.ru)

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as
published by the Free Software Foundation, either version 3 of
the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but
WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General
Public License along with this program.  If not, see <https://www.gnu.org/licenses/>.
'''

from typing import Any, LiteralString, TypeGuard, get_args

from sodom.elements import ANY_ELEMENT, NORMAL_ELEMENT, VOID_ELEMENT
from sodom.literals import USED_TAG_VALUES, VOID_TAGS, NORMAL_TAGS


def text(*_text: str) -> None:
    from sodom.elements import CURRENT_ELEMENT
    if (elem := CURRENT_ELEMENT.get()) is not None and _text:
        elem.add(*_text)


def render_py(
    *elements: ANY_ELEMENT,
    level: int = 0,
    space: str = '    ',
    quotes: str = '"',
    replace_underscore: bool = True
) -> str:
    result: list[str] = []
    for element in elements:
        if isinstance(element, str):
            result.append('{}{}(\'{}\')'.format(space * level, text.__name__, element))
        else:
            result.append(
                element.__py__(
                    level=level,
                    space=space,
                    quotes=quotes,
                    replace_underscore=replace_underscore,
                )
            )
    return '\n'.join(result)


def render(
    *elements: ANY_ELEMENT,
    level: int = 0,
    space: str = '  ',
) -> str:
    result: list[str] = []
    for element in elements:
        if isinstance(element, str):
            result.append(space * level + element)
        else:
            result.append(
                element.__html__(
                    level=level,
                    space=space,
                )
            )
    return '\n'.join(result)


def render_root(
    *elements: ANY_ELEMENT,
    level: int = 0,
    space: str = '  ',
):
    return render('<!DOCTYPE html>', *elements, level=level, space=space)


def escape_python(tag: LiteralString) -> str:
    '''Escape Python keywords and builtins.'''
    if tag.startswith(USED_TAG_VALUES):
        tag = f'{tag}_'
    return tag


def is_normal_element(element: Any) -> TypeGuard[NORMAL_ELEMENT]:
    from sodom.elements import NormalElement
    return isinstance(element, NormalElement)


def is_void_element(element: Any) -> TypeGuard[VOID_ELEMENT]:
    from sodom.elements import VoidElement
    return isinstance(element, VoidElement)


def is_tag(tag: str) -> TypeGuard[NORMAL_TAGS | VOID_TAGS]:
    return is_normal_tag(tag) or is_void_tag(tag)


def is_normal_tag(tag: str) -> TypeGuard[NORMAL_TAGS]:
    return tag in get_args(NORMAL_TAGS)


def is_void_tag(tag: str) -> TypeGuard[VOID_TAGS]:
    return tag in get_args(VOID_TAGS)
