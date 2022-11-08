from odoo import models, fields, api


class ResPartner(models.Model):
    _inherit = "res.partner"

    url_ids = fields.One2many("vanguard.url", "partner_id", string="Urls to check")
    has_urls_to_check = fields.Boolean(
        string="Has URL to check",
        compute="_compute_has_urls_to_check",
        store=True)
    vanguard_partner_ids = fields.Many2many(
        "res.partner",
        "vanguard_res_partner_rel",
        "res_partner_id",
        "vanguard_res_partner_id"
    )

    @api.depends('url_ids')
    def _compute_has_urls_to_check(self):
        for rec in self:
            if len(rec.url_ids):
                rec.has_urls_to_check = len(rec.url_ids) and True or False
