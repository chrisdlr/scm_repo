# -*- coding: utf-8 -*-
{
    "name": "Student Contract Management",
    "version": "1.2.2",
    "summary": "Student Contract Management",
    "sequence": -1,
    "description": """Student Contract Management""",
    "author": "Kleiver Perez",
    "company": "Kleiver Perez",
    "website": "https://www.kperez.com",
    "contributors": [
        "Kleiver Pérez - <kleiver.perez.dev@gmail.com>"
    ],
    "category": "Tools",
    "depends": ["stock", "contacts"],
    "data": [
        "security/ir.model.access.csv",
        "data/ir_sequence_students_contract_data.xml",
        "data/ir_sequence_students_contract_payment_data.xml",
        "wizards/add_contract_payment_views.xml",
        "views/students_contract_views.xml",
        "views/course_by_students_views.xml",
        "views/res_partner_inherit_views.xml",
        "views/product_template_inherit_views.xml",
        "views/menu_items.xml",
    ],

    "assets": {
        "web.assets_backend": [
            "students_contract_management/static/src/components/**/*.js",
            "students_contract_management/static/src/components/**/*.xml",
            "students_contract_management/static/src/components/**/*.scss",
        ],
    },

    "installable": True,
    "application": True,
    "license": "LGPL-3",
}
