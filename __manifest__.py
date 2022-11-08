{
    "name": "Vanguard",
    "version": "15.0",
    "author": "Kevin COURIAT",
    "maintainer": "Kevin COURIAT",
    "category": "Technical Settings",
    "depends": ["base", "mail"],
    "description": """
Vanguard
========
Tool to check if websites are alive
""",
    "website": "https://couriat.info",
    "data": [
        "security/ir.model.access.csv",

        # Views
        "views/res_partner.xml",
        "views/state.xml",
        "views/time.xml",
        "views/url.xml",
        "views/test.xml",
        "views/menus.xml",

        # Data
        "data/cron.xml",
        "data/state.xml",
        "data/time.xml",
        "data/mail.xml",
        "data/ir_mail_server.xml",
    ],
    "demo": [],
    "test": [],
    "installable": True,
    "auto_install": False,
    "license": "AGPL-3",
    "application": True,
}
