from odoo import models, fields


class Test(models.Model):
    _name = "vanguard.test"
    _description = "Class to manage Test did with vanguard"
    _order = "date_check DESC"

    date_check = fields.Datetime(string="Date of check", required=True)
    state_id = fields.Many2one("vanguard.state", string="State", required=True)
    state_type = fields.Selection(related="state_id.type", readonly=True)
    url_id = fields.Many2one("vanguard.url", string="url", required=True, ondelete="cascade")
    partner_id = fields.Many2one("res.partner", related="url_id.partner_id", readonly=True)
