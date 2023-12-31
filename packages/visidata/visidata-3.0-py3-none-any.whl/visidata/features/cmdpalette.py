import collections
from functools import partial
from visidata import DrawablePane, BaseSheet, vd, VisiData, CompleteKey, clipdraw, HelpSheet, colors, AcceptInput, AttrDict, drawcache_property


vd.theme_option('color_cmdpalette', 'black on 72', 'base color of command palette')
vd.theme_option('disp_cmdpal_max', 10, 'max number of suggestions for command palette')

def add_to_input(v, i, value=''):
    items = list(v.split())
    if not v or v.endswith(' '):
        items.append(value)
    else:
        items[-1] = value
    v = ' '.join(items) + ' '
    return v, len(v)


def accept_input(v, i, value=None):
    raise AcceptInput(v if value is None else value)


@VisiData.lazy_property
def usedInputs(vd):
    return collections.defaultdict(int)

@DrawablePane.after
def execCommand2(sheet, cmd, *args, **kwargs):
    vd.usedInputs[cmd.longname] += 1

@BaseSheet.api
def inputPalette(sheet, prompt, items,
                 value_key='key',
                 formatter=lambda m, item, trigger_key: f'{trigger_key} {item}',
                 multiple=False,
                 **kwargs):
    bindings = dict()

    tabitem = -1

    def tab(n, nitems):
        nonlocal tabitem
        tabitem = (tabitem + n) % nitems

    def _draw_palette(value):
        words = value.lower().split()

        if multiple and words:
            if value.endswith(' '):
                finished_words = words
                unfinished_words = []
            else:
                finished_words = words[:-1]
                unfinished_words = [words[-1]]
        else:
            unfinished_words = words
            finished_words = []

        unuseditems = [item for item in items if item[value_key] not in finished_words]

        matches = vd.fuzzymatch(unuseditems, unfinished_words)

        h = sheet.windowHeight
        w = min(100, sheet.windowWidth)
        nitems = min(h-1, sheet.options.disp_cmdpal_max)

        useditems = []
        palrows = []

        for m in matches[:nitems]:
            useditems.append(m.match)
            palrows.append((m, m.match))

        favitems = sorted([item for item in unuseditems if item not in useditems],
                          key=lambda item: -vd.usedInputs.get(item[value_key], 0))

        for item in favitems[:nitems-len(palrows)]:
            palrows.append((None, item))

        navailitems = min(len(palrows), nitems)

        bindings['^I'] = lambda *args: tab(1, navailitems) or args
        bindings['KEY_BTAB'] = lambda *args: tab(-1, navailitems) or args

        for i in range(nitems-len(palrows)):
            palrows.append((None, None))

        for i, (m, item) in enumerate(palrows):
            trigger_key = ' '
            if tabitem >= 0 and item:
                trigger_key = f'{i+1}'[-1]
                bindings[trigger_key] = partial(add_to_input if multiple else accept_input, value=item[value_key])

            attr = colors.color_cmdpalette

            if tabitem < 0 and palrows:
                _ , topitem = palrows[0]
                bindings['^J'] = partial(accept_input, value=None)
                if multiple:
                    bindings[' '] = partial(add_to_input, value=topitem[value_key])
            elif item and i == tabitem:
                bindings['^J'] = partial(accept_input, value=None)
                if multiple:
                    bindings[' '] = partial(add_to_input, value=item[value_key])
                attr = colors.color_menu_spec

            match_summary = formatter(m, item, trigger_key) if item else ' '

            clipdraw(sheet._scr, h-nitems-1+i, 0, match_summary, attr, w=w)

        return None

    completer = CompleteKey(sorted(item[value_key] for item in items))
    return vd.input(prompt,
            completer=completer,
            updater=_draw_palette,
            bindings=bindings,
            **kwargs)


def cmdlist(sheet):
    return [
            AttrDict(longname=row.longname,
                     description=sheet.cmddict[(row.sheet, row.longname)].helpstr)
        for row in sheet.rows
    ]
HelpSheet.cmdlist = drawcache_property(cmdlist)


@BaseSheet.api
def inputLongname(sheet):
    prompt = 'command name: '
    # get set of commands possible in the sheet
    this_sheets_help = HelpSheet('', source=sheet)
    this_sheets_help.ensureLoaded()

    def _fmt_cmdpal_summary(match, row, trigger_key):
        keystrokes = this_sheets_help.revbinds.get(row.longname, [None])[0] or ' '
        formatted_longname = match.formatted.get('longname', row.longname) if match else row.longname
        formatted_name = f'[:onclick {row.longname}]{formatted_longname}[/]'
        if vd.options.debug and match:
            keystrokes = f'[{match.score}]'
        r = f' [:keystrokes]{keystrokes.rjust(len(prompt)-5)}[/]  '
        r += f'[:keystrokes]{trigger_key}[/] {formatted_name}'
        if row.description:
            formatted_desc = match.formatted.get('description', row.description) if match else row.description
            r += f' - {formatted_desc}'
        return r

    return sheet.inputPalette(prompt, this_sheets_help.cmdlist,
                              value_key='longname',
                              formatter=_fmt_cmdpal_summary,
                              type='longname')


@BaseSheet.api
def exec_longname(sheet, longname):
    if not sheet.getCommand(longname):
        vd.fail(f'no command {longname}')
    sheet.execCommand(longname)


vd.addCommand('Space', 'exec-longname', 'exec_longname(inputLongname())', 'execute command by its longname')
