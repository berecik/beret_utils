import pprint
import sys

_pp = pprint.PrettyPrinter(indent=2)

LOG_EVENTS = ('return', 'call')


def log_fun(*args, **kwargs):
    """
    decorator
    log call, arguments, local variables values and returned value
    :param call: log call
    :param ret:  log return
    :param content: log all local variables value at return
    :param path: log call and return point path and line number
    :param args: log args
    :param log_fun: custom log function, default is print
    """
    show_call = kwargs.get("call", True)
    show_return = kwargs.get("ret", True)
    show_content = kwargs.get("content", True)
    show_path = kwargs.get("path", True)
    show_args = kwargs.get("args", True)
    log_fun = kwargs.get("log_fun", print)

    def log_content(fun):

        def print_log(frame, event):
            co = frame.f_code
            line_no = frame.f_lineno
            filename = co.co_filename
            path = "{}:{}".format(filename, line_no) if show_path else ""
            variables = ["%s=%s" % (key, _pp.pformat(val)) for key, val in frame.f_locals.items()]

            args = "({})".format(",".join(variables)) if show_args else ""
            if event == 'call':
                if show_call:
                    func_name = co.co_name
                    log_fun("{}{}{}".format("%s " % path, func_name, args))
            elif show_content:
                log_fun("\n".join(variables))
                if show_path:
                    log_fun(path)

        def log_return(old_log=None):
            def _log_return_wrapper(frame, event, arg):
                if frame.f_code == fun.__code__ and event in LOG_EVENTS:
                    print_log(frame, event)
                if callable(old_log):
                    old_log(frame, event, arg)

                return _log_return_wrapper

            return _log_return_wrapper

        def _wrapper(*args, **kwargs):
            old_log = sys.gettrace()
            sys.settrace(log_return(old_log))
            try:
                result = fun(*args, **kwargs)
            except:
                raise
            else:
                if (show_return):
                    log_fun("return {}\n".format(result))
                return result
            finally:
                sys.settrace(old_log)

        return _wrapper

    if args and hasattr(args[0], "__call__"):
        return log_content(args[0])

    return log_content


def info(object, spacing=10, collapse=1):
    "print any object's method and their docs"
    methodList = [method for method in dir(object) if callable(getattr(object, method))]
    processFunc = collapse and (lambda s: " ".join(s.split())) or (lambda s: s)
    print(
        "\n".join(["%s %s" %
                   (method.ljust(spacing),
                    processFunc(str(getattr(object, method).__doc__)))
                   for method in methodList])
    )
