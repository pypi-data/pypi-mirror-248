from wrapper import ExecWrapper


class Helm(ExecWrapper):
    def __init__(self, **kwargs):
        super().__init__('helm', **kwargs)

    def __getattr__(self, item):
        h = Helm(**self._parent_kwargs)
        h._parent_attrs = self._parent_attrs.copy()
        h._parent_attrs.append(item.replace('_', '-', -1))

        return h

    def _pre(self, args, parent_kwargs, kwargs) -> tuple:
        ns_short = parent_kwargs.pop('n', None)
        parent_kwargs.setdefault('namespace', ns_short)

        out_short = parent_kwargs.pop('o', None)
        out = parent_kwargs.pop('output', out_short)

        if self._parent_attrs[-1] in ['history', 'install', 'list', 'status', 'upgrade'] or \
                ".".join(self._parent_attrs) in ['repo.list', 'search.hub', 'search.repo', 'get.values']:
            out_short = kwargs.pop('o', out)
            kwargs.setdefault('output', out_short)

        args = list(args)
        for arg_name in ['values', 'set', 'set_file', 'set_string', 'show_only']:
            v = kwargs.pop(arg_name, None)
            if v:
                arg_name.replace('_', '-')
                args.extend(f'--{arg_name}={v}' for v in v)

        return tuple(args)
