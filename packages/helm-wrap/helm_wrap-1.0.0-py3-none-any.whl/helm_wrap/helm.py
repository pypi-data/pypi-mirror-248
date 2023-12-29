from wrapper import ExecWrapper


class Helm(ExecWrapper):
    def __init__(self, **kwargs):
        super().__init__('helm', **kwargs)

    def __getattr__(self, item):
        h = Helm(**self._parent_kwargs)
        h._parent_attrs = self._parent_attrs.copy()
        h._parent_attrs.append(item.replace('_', '-', -1))

        return h

    def _pre(self, args, parent_kwargs, kwargs):
        ns_short = parent_kwargs.pop('n', None)
        parent_kwargs.setdefault('namespace', ns_short)

        out_short = parent_kwargs.pop('o', None)
        out = parent_kwargs.pop('output', out_short)

        out_short = kwargs.pop('o', out)
        kwargs.setdefault('output', out_short)
