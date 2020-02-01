import progressbar
try:
    from . import i18n
    from . import ConnectCore
    from . import log
    from . import screens
    from . import Command
except ModuleNotFoundError:
    import i18n
    import ConnectCore
    import log
    import screens
    import Command


def get_board_list(api) -> list:

    # log.showValue(
    #     api.config,
    #     log.Level.INFO,
    #     [
    #         i18n.PTT,
    #         i18n.Msg
    #     ],
    #     i18n.MarkPost
    # )

    cmd_list = []
    cmd_list.append(Command.GoMainMenu)
    cmd_list.append('F')
    cmd_list.append(Command.Enter)
    cmd_list.append('y')
    cmd_list.append('$')
    cmd = ''.join(cmd_list)

    target_list = [
        ConnectCore.TargetUnit(
            i18n.BoardList,
            screens.Target.InBoardList,
            break_detect=True
        )
    ]

    api.connect_core.send(
        cmd,
        target_list,
        screen_timeout=api.config.screen_long_timeout
    )
    ori_screen = api.connect_core.get_screen_queue()[-1]

    max_no = 0
    for line in ori_screen.split('\n'):
        if '◎' not in line and '●' not in line:
            continue

        if line.startswith(api.cursor):
            line = line[len(api.cursor):]

        # print(f'->{line}<')
        if '◎' in line:
            front_part = line[:line.find('◎')]
        else:
            front_part = line[:line.find('●')]
        front_part_list = [x for x in front_part.split(' ')]
        front_part_list = list(filter(None, front_part_list))
        # print(f'FrontPartList =>{FrontPartList}<=')
        max_no = int(front_part_list[0])

    log.show_value(
        api.config,
        log.Level.DEBUG,
        'MaxNo',
        max_no
    )

    if api.config.log_level == log.Level.INFO:
        pb = progressbar.ProgressBar(
            max_value=max_no,
            redirect_stdout=True
        )

    cmd_list = []
    cmd_list.append(Command.GoMainMenu)
    cmd_list.append('F')
    cmd_list.append(Command.Enter)
    cmd_list.append('y')
    cmd_list.append('0')
    cmd = ''.join(cmd_list)

    board_list = []
    while True:

        api.connect_core.send(
            cmd,
            target_list,
            screen_timeout=api.config.screen_long_timeout
        )

        ori_screen = api.connect_core.get_screen_queue()[-1]
        # print(OriScreen)
        for line in ori_screen.split('\n'):
            if '◎' not in line and '●' not in line:
                continue

            if line.startswith(api.cursor):
                line = line[len(api.cursor):]

            # print(f'->{line}<')

            if '◎' in line:
                front_part = line[:line.find('◎')]
            else:
                front_part = line[:line.find('●')]
            front_part_list = [x for x in front_part.split(' ')]
            front_part_list = list(filter(None, front_part_list))
            # print(f'FrontPartList =>{FrontPartList}<=')
            no = int(front_part_list[0])
            # print(f'No  =>{No}<=')
            # print(f'LastNo =>{LastNo}<=')

            log.show_value(
                api.config,
                log.Level.DEBUG,
                'Board NO',
                no
            )

            board_name = front_part_list[1]
            if board_name.startswith('ˇ'):
                board_name = board_name[1:]

            log.show_value(
                api.config,
                log.Level.DEBUG,
                'Board Name',
                board_name
            )

            board_list.append(board_name)

            if api.config.log_level == log.Level.INFO:
                pb.update(no)

        if no >= max_no:
            break
        cmd = Command.Ctrl_F

    if api.config.log_level == log.Level.INFO:
        pb.finish()

    return board_list