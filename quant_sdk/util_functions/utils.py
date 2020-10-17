
def interval_converter(interval_string: str) -> str:
    try:
        # allows all seconds and interval in respective time-unit

        if interval_string[-1] == 's':
            return interval_string
        elif interval_string[-1] == 'm':
            return str(f'{int(interval_string[:-1]) * 60}s')
        elif interval_string[-1] == 'h':
            return str(f'{int(interval_string[:-1]) * 60 * 60}s')

    except Exception as ex:
        print(ex)
