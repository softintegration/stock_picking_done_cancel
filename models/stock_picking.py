# -*- coding: utf-8 -*- 

from odoo import models,fields,api,_
from odoo.exceptions import UserError


class StockPicking(models.Model):
    _inherit = "stock.picking"


    def action_force_cancel(self):
        if not self.user_has_groups('account.group_account_manager'):
            raise UserError(_("You can not cancel done pickings"))
        return self.with_context(pickings_to_cancel=self.ids)._action_force_cancel_confirm_wizard()


    def _action_force_cancel(self):
        if not self.user_has_groups('account.group_account_manager'):
            raise UserError(_("You can not cancel done pickings"))
        # the cancel process will set the initial demand of moves to zero,we have to prevent that
        product_uom_qty = {}
        for move in self.mapped('move_lines'):
            product_uom_qty.update({move.id: move.product_uom_qty})
        self.mapped('move_line_ids').write({'qty_done': 0.0})
        self.mapped('move_lines').write({'state': 'assigned'})
        for move in self.mapped('move_lines'):
            move.write({'product_uom_qty': product_uom_qty[move.id]})
        self.mapped('move_line_ids').unlink()
        self.mapped('move_lines')._action_cancel()
        self.write({'is_locked': True})
        return True


    def _action_force_cancel_confirm_wizard(self, show_transfers=False):
        view = self.env.ref('stock_picking_done_cancel.view_confirm_picking_force_cancel')
        return {
            'name': _('Cancel confirm'),
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'stock.picking.force.cancel.confirm',
            'views': [(view.id, 'form')],
            'view_id': view.id,
            'target': 'new',
            'context': dict(self.env.context, default_show_transfers=show_transfers, default_pick_ids=[(4, p.id) for p in self]),
        }