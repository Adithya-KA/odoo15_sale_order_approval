from odoo import fields, models, api


class SoApproval(models.Model):
    _inherit = 'sale.order'

    state = fields.Selection(selection_add=[('waiting_for_approval', 'Waiting for Approval'), ('sent',)])
    price_flag = fields.Boolean(default=False)

    @api.onchange('order_line')
    def compute_change(self):
        if self.partner_id and self.pricelist_id:
            self.price_flag = False
            for rec in self.order_line:
                if rec.product_template_id.list_price != rec.price_unit:
                    self.price_flag = True
                    return {
                        'warning': {
                            'title': 'Warning!',
                            'message': 'Need the Approval of Manager'}
                    }

    def button_approval_request(self):
        if self.price_flag:
            self.state = 'waiting_for_approval'

    def button_approve(self):
        self.state = 'sale'

    def button_reject(self):
        self.state = 'draft'
