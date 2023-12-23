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


from abc import ABC, abstractmethod
from contextlib import AbstractContextManager
from contextvars import ContextVar, Token
from itertools import chain
from typing import Any, Hashable, MutableSequence, Self, Sequence

from sodom.literals import ANY_TAGS, NORMAL_TAGS, VOID_TAGS, SPECIAL_ATTRS



CURRENT_ELEMENT = ContextVar['NORMAL_ELEMENT | None']("CURRENT_ELEMENT", default=None)


def build_html_attrs(
    attrs: dict[str, str],
    quotes: str = '"',
    replace_underscores: bool = True
) -> list[str]:
    '''Merge attrs (dict[str, str]) to f'{key}={quote}{value}{quote}' format.'''
    form = '{k}={q}{v}{q}'
    result = list[str]()
    for k, v in attrs.items():
        if k := k.strip('_'):
            if replace_underscores:
                k = k.replace('_', '-')
            elif k.split('_', 1)[0] in SPECIAL_ATTRS:
                k = k.replace('_', '-', 1)
            result.append(form.format(k=k, q=quotes, v=v))
    return result


def merge_tag_header(
    tag: ANY_TAGS,
    attrs: dict[str, str],
    quotes: str = '"',
    replace_under_score: bool = True
) -> str:
    result = ' '.join(filter(
        bool,
        chain((tag,), build_html_attrs(attrs, quotes, replace_under_score)),
    ))

    return result


class HTMLElement[TAG: ANY_TAGS](ABC):
    tag: TAG
    attrs: dict[str, str]
    parent: 'HasChildren | None'

    def __call__(self) -> None:
        new_parent = CURRENT_ELEMENT.get()
        if new_parent is not None:
            new_parent.add(self)
        else:
            self.parent = None

    @abstractmethod
    def __html__(self, *, level: int = 0, space: str = '  ') -> str:
        ...

    @abstractmethod
    def __py__(
        self,
        *,
        level: int = 0,
        space: str = '    ',
        quotes: str = '"',
        replace_underscore: bool = True
    ) -> str:
        ...


class HasChildren(ABC):
    _children: MutableSequence['ANY_ELEMENT']

    @property
    def children(self) -> Sequence['ANY_ELEMENT']:
        return tuple(self._children)

    def add(self, *children: 'ANY_ELEMENT') -> None:
        for child in children:
            if isinstance(child, HTMLElement):
                if child.parent is not None:
                    child.parent.remove(child)
                child.parent = self
        self._children.extend(children)

    def remove(self, *children: 'ANY_ELEMENT') -> None:
        for child in children:
            if isinstance(child, (NormalElement, VoidElement)):
                child.parent = None
            self._children.remove(child)


class VoidElement[HTML_TAGS: VOID_TAGS](HTMLElement[HTML_TAGS]):
    __slots__ = (
        'tag',
        'attrs',
        'parent',
    )

    def __init__(self, _tag: HTML_TAGS, *_: Any, **attrs: str) -> None:
        self.tag = _tag
        self.attrs = attrs
        self.parent = None
        self()

    ##### HASHING #####
    def __eq__(self, other: Hashable) -> bool:
        return hash(self) == hash(other)

    def __hash__(self) -> int:
        return hash((self.tag, tuple(self.attrs.items())))

    ##### RENDERING #####
    def __str__(self) -> str:
        return self.__repr__()

    def __html__(self, *, level: int = 0, space: str = '  ') -> str:
        tag_content = merge_tag_header(self.tag, self.attrs)
        result = '{}<{}>'.format(space * level, tag_content)
        return result

    def __py__(
        self,
        *,
        level: int = 0,
        space: str = '    ',
        quotes: str = '"',
        replace_underscore: bool = True
    ) -> str:
        from sodom.utils import escape_python

        attrs = ', '.join(build_html_attrs(self.attrs, quotes, replace_underscore))

        result = '{}{}({})'.format(space * level, escape_python(self.tag), attrs)
        return result

    def __repr__(self) -> str:
        tag_content = merge_tag_header(self.tag, self.attrs)
        result = '<{} @{}>'.format(tag_content, id(self))
        return result


class NormalElement[TAG: NORMAL_TAGS](
    AbstractContextManager, # type: ignore
    HTMLElement[TAG],
    HasChildren,
):
    __slots__ = (
        'tag',
        'attrs',
        'parent',
        '_children',
        '_context_token',
    )

    _context_token: Token['NORMAL_ELEMENT | None']

    def __init__(self, _tag: TAG, *_children: 'ANY_ELEMENT', **attrs: str) -> None:
        self.tag = _tag
        self.attrs = attrs
        self.parent = None
        self()
        self._children = []
        self.add(*_children)

    ##### CONTEXT MANAGEMENT #####
    def __enter__(self) -> Self:
        self._context_token = CURRENT_ELEMENT.set(self)
        return self

    def __exit__(self, *_) -> None:
        CURRENT_ELEMENT.reset(self._context_token)

    ##### RENDERING #####
    def __html__(self, *, level: int = 0, space: str = '  ') -> str:
        from sodom.utils import render as _render

        tag = self.tag
        tag_content = merge_tag_header(self.tag, self.attrs)

        tag_begin = '{}<{}>'.format(space * level, tag_content)
        body_content = '\n'.join(map(
            lambda c: _render(c, level=level+1, space=space),
            self._children,
        ))
        tag_end = f'</{tag}>'

        if body_content:
            tag_end = space * level + tag_end

        result = ('\n' if body_content else '').join((
            tag_begin,
            body_content,
            tag_end,
        ))
        return result

    def __py__(
        self,
        *,
        level: int = 0,
        space: str = '    ',
        quotes: str = '"',
        replace_underscore: bool = True
    ) -> str:
        from sodom.utils import escape_python, render_py

        attrs = ', '.join(build_html_attrs(self.attrs, quotes, replace_underscore))

        if self._children:
            children = render_py(
                *self._children,
                level=level+1,
                space=space,
                quotes=quotes,
                replace_underscore=replace_underscore,
            )

            result = '{}with {}({}):\n{}'.format(
                space * level,
                escape_python(self.tag),
                attrs,
                children,
            )
        else:
            result = '{}{}({})'.format(
                space * level,
                escape_python(self.tag),
                attrs,
            )

        return result

    def __repr__(self) -> str:
        tag = self.tag
        tag_content = merge_tag_header(self.tag, self.attrs)
        body_content = len(self._children)

        result = '<{} @{}>:{}</{}>'.format(
            tag_content,
            id(self),
            body_content,
            tag,
        )

        return result


VOID_ELEMENT = VoidElement[VOID_TAGS]
NORMAL_ELEMENT = NormalElement[NORMAL_TAGS]
ANY_ELEMENT = HTMLElement[Any] | str
