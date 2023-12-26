from . import g_var


def set_log_level(debug_level):
    g_var.set_var(g_var.GVarKey.Log.LOG_LEVEL, debug_level)


def get_log_level(default_level=g_var.LogLevel.INFO_LEVEL):
    if not g_var.has_var(g_var.GVarKey.Log.LOG_LEVEL):
        return default_level
    return g_var.get_var(g_var.GVarKey.Log.LOG_LEVEL)
