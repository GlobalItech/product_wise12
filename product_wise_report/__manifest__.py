{
    'name': 'Product Wise Report',
    'version': '0.2',
    'category': 'Warehouse',
    'license': "AGPL-3",
    # 'summary': "Current Stock Report for all Products in each Warehouse",
    'author': 'Itech reosurces',
    'company': 'ItechResources',
    'depends': [
                'account_accountant_cbc',
                'stock',
                'sale',
                'purchase',

                ],
    'data': [
            'views/wizard_view.xml',
            'views/pro_wise_report.xml'
            ],
    'images': ['static/description/banner.jpg'],
    'installable': True,
    'auto_install': False,
}