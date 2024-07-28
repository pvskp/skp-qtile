import psutil


def get_current_wireless_interface() -> str:
    interfaces = [iface for iface, stats in psutil.net_if_stats().items() if stats.isup]
    for iface in interfaces:
        if len(iface) > 2:
            if iface[0:2] == "wl":
                return iface
    return ""
