from repository import repos


def inject_global_variables():
    return dict(
        nav_menu=repos.common.get_main_menu(),
        footer_menu=repos.common.get_footer(),
    )