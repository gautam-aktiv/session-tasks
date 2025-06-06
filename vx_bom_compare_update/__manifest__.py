
{
    "name": "BOM Compare and Update",
    "version": "1.0",
    "summary": "Compare two BOMs side-by-side and selectively update differences",
    "author": "BLACKBOXAI",
    "category": "Manufacturing",
    "depends": ["mrp"],
    "data": [
        "security/ir.model.access.csv",
        "wizard/compare_bom_wizard_view.xml",
        "views/product_views.xml",

    ],
    "installable": True,
    "application": False,
    "auto_install": False
}
