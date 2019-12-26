from odoo import models, fields, api


class StockReport(models.TransientModel):
    _name = "wizard.sale.history"
    _description = "Current Stock History"
    date_to= fields.Date("Date To")
    date_from= fields.Date("Date From")
    report_type = fields.Selection([('indivproduct_wise','Product Wise Report')],string='Relative')
    category = fields.Many2many('product.category',  string='Categories')
    warehouse = fields.Many2many('stock.warehouse', string='Warehouse')
    indv_product = fields.Many2many('product.product',  string='Products')

    partner = fields.Many2many('res.partner',  string='Partner')

    @api.multi
    def print_report_attendance(self):
        active_ids = self.env.context.get('active_ids', [])
        datas = {
            'ids': active_ids,
            'model': 'report.model',
            'form': self.read()[0]
        }
        return self.env.ref('product_wise_report.product_sale_xlsx').report_action(self, data=datas)


class ReportCarpetPurchase(models.AbstractModel):
    _name='report.product_wise_report.pro_wise_report'




    @api.model
    def get_report_values(self, docids, data=None):
        lines = []
        dal = []

        date_to = data['form']['date_to']
        date_from = data['form']['date_from']
        product_ids = data['form']['indv_product']
        wareh = data['form']['warehouse']

        val = []

        # product_id = self.env['product.product'].search([('id', '=', v)])
        sale_obj = self.env['account.invoice.line'].search([
                                                                ('invoice_id.type', '=', 'out_invoice'),
                                                                ('invoice_id.state', 'in', ['open', 'paid']),
                                                                ('invoice_id.date_invoice', '>=', date_from),
                                                                ('invoice_id.date_invoice', '<=', date_to),
                                                                ('invoice_id.journal_id.type', '=', 'sale'),
                                                               ])
        for e in wareh:
            w_house = self.env['stock.warehouse'].search([('id', '=', e)]).name
            dal.append(w_house)
            for v in  data['form']['indv_product']:
                product_id = self.env['product.product'].search([('id', '=', v)])
                sale_qty = 0.0
                average = 0.0
                sale_amount = 0.0
                for sale in sale_obj:
                    if (v == sale.product_id.id):
                        wh = self.env['sale.order'].search([('name','=',sale.origin)])
                        if (w_house == wh.warehouse_id.name):
                            uom = sale.product_id.uom_id.name
                            sale_qty += sale.quantity
                            sale_amount += sale.price_subtotal



                if sale_qty > 0:
                    average = float(sale_amount) / float(sale_qty)
                    vals = {
                            'ware_house':w_house,
                            'name': product_id.display_name,
                            'code': product_id.default_code,
                            'description':product_id.name,
                            'uom': product_id.uom_id.name,
                            'avg': float(average),
                            'sale_qty': sale_qty,
                            'sale_amount': sale_amount,
                            # 'sale_return_qty': return_qty,
                            # 'sale_return_amount': return_amount,
                        }
                    lines.append(vals)

                    sale_qty = 0.0
                    average = 0.0
                    sale_amount = 0.0

            return {

                'datacr': lines,
                'values':dal,
                'date_order': data['form']['date_to'],
                'date_order2': data['form']['date_from']
            }
