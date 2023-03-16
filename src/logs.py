
__log_level = 0


def log(msg: str, prefix: str = 'ℹ️'):
  print(f'{"  " * __log_level}{prefix} {msg}')


def log_start(msg: str):
  global __log_level
  log(msg, '⏩')
  __log_level = __log_level + 1


def log_close():
  global __log_level
  __log_level = __log_level - 1

  if __log_level < 0:
    __log_level = 0


def log_end(msg: str):
  log(msg, '⏪')
  log_close()


def log_title(msg: str):
  global __log_level
  __log_level = 0
  log_start(f'🚧🚧🚧 {msg} 🚧🚧🚧')
