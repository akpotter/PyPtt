
try:
    from . import i18n
    from . import ConnectCore
    from . import log
    from . import screens
    from . import exceptions
    from . import Command
except ModuleNotFoundError:
    import i18n
    import ConnectCore
    import log
    import screens
    import exceptions
    import Command


def get_post_index(
        api,
        board: str,
        aid: str) -> int:

    cmd_list = []
    cmd_list.append(Command.GoMainMenu)
    cmd_list.append('qs')
    cmd_list.append(board)
    cmd_list.append(Command.Enter)
    cmd_list.append(Command.Ctrl_C * 2)
    cmd_list.append(Command.Space)

    cmd_list.append('#')
    cmd_list.append(aid)
    cmd_list.append(Command.Enter)

    cmd = ''.join(cmd_list)

    no_such_post = i18n.NoSuchPost
    no_such_post = i18n.replace(no_such_post, board, aid)

    target_list = [
        ConnectCore.TargetUnit(
            no_such_post,
            '找不到這個文章代碼',
            log_level=log.Level.DEBUG,
            exceptions=exceptions.NoSuchPost(board, aid)
        ),
        # 此狀態下無法使用搜尋文章代碼(AID)功能
        ConnectCore.TargetUnit(
            i18n.CanNotUseSearchPostCodeF,
            '此狀態下無法使用搜尋文章代碼(AID)功能',
            exceptions=exceptions.CanNotUseSearchPostCode()
        ),
        ConnectCore.TargetUnit(
            i18n.NoPost,
            '沒有文章...',
            exceptions=exceptions.NoSuchPost(board, aid)
        ),
        ConnectCore.TargetUnit(
            i18n.Success,
            screens.Target.InBoard,
            break_detect=True,
            log_level=log.Level.DEBUG
        ),
        ConnectCore.TargetUnit(
            i18n.Success,
            screens.Target.InBoardWithCursor,
            break_detect=True,
            log_level=log.Level.DEBUG
        ),
        ConnectCore.TargetUnit(
            i18n.NoSuchBoard,
            screens.Target.MainMenu_Exiting,
            exceptions=exceptions.NoSuchBoard(api.config, board)
            # BreakDetect=True,
        )
    ]

    index = api.connect_core.send(
        cmd,
        target_list
    )
    ori_screen = api.connect_core.get_screen_queue()[-1]
    if index < 0:
        # print(OriScreen)
        raise exceptions.NoSuchBoard(api.config, board)

    # if index == 5:
    #     print(OriScreen)
    #     raise exceptions.NoSuchBoard(api.config, Board)

    # print(index)
    # print(OriScreen)
    screen_list = ori_screen.split('\n')

    line = [x for x in screen_list if x.startswith(api.cursor)]
    line = line[0]
    last_line = screen_list[screen_list.index(line) - 1]
    # print(LastLine)
    # print(line)

    if '編號' in last_line and '人氣:' in last_line:
        index = line[1:].strip()
        index_fix = False
    else:
        index = last_line.strip()
        index_fix = True
    while '  ' in index:
        index = index.replace('  ', ' ')
    index_list = index.split(' ')
    index = index_list[0]
    if index == '★':
        return 0
    index = int(index)
    if index_fix:
        index += 1
    # print(Index)
    return index