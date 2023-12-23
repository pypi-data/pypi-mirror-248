from sodom.literals import SPECIAL_ATTRS


class Attrs(dict[str, str]):
    '''
    Allow to merge attributes.
    Merge means adding attribute values to end of existing ones or create new attribute.
    For example:
    ```python
    Attrs(foo='bar').merge(foo='baz') or Attrs(foo='bar').merge(**Attrs(foo='baz'))
    ```
    returns
    ```python
    {'foo': 'bar baz'}
    ```
    '''
    def __call__(self) -> None:
        from sodom.elements import CURRENT_ELEMENT

        if (parent := CURRENT_ELEMENT.get()) is None:
            raise RuntimeError('Attribute should be called in context of Normal Element.')

        parent.attrs.merge_update(**self)

    def merge(self, separator: str = ' ', **right: str) -> 'Attrs':
        '''Merge attributes into new Attrs instance.'''
        result = Attrs(self)
        for k, v in right.items():
            result[k] = separator.join(filter(
                bool,
                (
                    self.get(k, ''),
                    v,
                ),
            ))
        return result

    def merge_update(self, separator: str = ' ', **other: str) -> None:
        '''Merge attributes inplace.'''
        self.update(self.merge(separator, **other))

    def torows(
        self,
        *,
        quotes: str = '"',
        replace_underscores: bool = True
    ) -> list[str]:
        '''Build attrs `dict[str, str]` to `list[str]` with `f'{key}={quote}{value}{quote}'` format.'''
        form = '{k}={q}{v}{q}'.format
        result = list[str]()
        for k, v in self.items():
            if k := k.strip('_'):
                if replace_underscores:
                    k = k.replace('_', '-')
                elif k.split('_', 1)[0] in SPECIAL_ATTRS:
                    k = k.replace('_', '-', 1)
                result.append(form(k=k, q=quotes, v=v))
        return result

    def torow(
        self,
        separator: str = ' ',
        *,
        quotes: str = '"',
        replace_underscores: bool = True
    ) -> str:
        '''Build attrs to strings with `f'{key}={quote}{value}{quote}'` format and merge them into single string with `separator`.'''
        result = separator.join(self.torows(quotes=quotes, replace_underscores=replace_underscores))
        return result
