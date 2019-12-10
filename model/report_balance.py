#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _


import logging
_logger = logging.getLogger(__name__)



class report_balance(models.Model):

    _name = "vit.report_balance"
    date_start = fields.Date( string="Date start",  help="" ,
    required=True
    )
    date_end = fields.Date( string="Date end",  help="",
    required=True
    )
    name = fields.Char( required=True, string="Name",  help="",
    )


    company_id = fields.Many2one(comodel_name="res.company",  string="Company",  help="" , 
    required=True
    )
    
    report_ids = fields.One2many(
        string='report',
        comodel_name='vit.report_balance_so',
        inverse_name='report_id'
    )
    
    @api.multi
    def generate_report(self):
        sql = """select pp.id,
       pt.name,
       pt.default_code,
            (
                select sum(product_uom_qty - qty_delivered)
                from sale_order_line sol 
                join sale_order so on sol.order_id = so.id
                where so.state in ('sale','done')
                and so.date_order < %s
                and sol.product_id = pp.id
            ) as total_so_bln_lalu,
            (
                select sum(product_uom_qty - qty_delivered)
                from sale_order_line sol 
                join sale_order so on sol.order_id = so.id
                where so.state in ('sale','done')
                and so.date_order between %s and %s
                and sol.product_id = pp.id
            ) as total_so_bln_ini,
            (  select sum(sq.quantity)
	       from product_template pt
		    join product_product pp on pp.product_tmpl_id = pt.id 
		    join stock_quant sq on sq.product_id = pp.id 
		    join stock_location sl on sl.id = sq.location_id
		    join product_category pc on pt.categ_id = pc.id where pc.name = 'Finish Good' and sl.name = 'Stock'
            ) as onhand,
          
            (
                select sum(qty_producing) 
                from mrp_workorder wo
                where wo.state = 'progress' and wo.product_id = pp.id and wo.name like 'H%%'
            ) as heading,
            (
                select sum(qty_producing) 
                from mrp_workorder wo
                where wo.state = 'progress' and wo.product_id = pp.id and wo.name like 'R%%'
            ) as rolling, 
            (
                select sum(qty_producing) 
                from mrp_workorder wo
                where wo.state = 'progress' and wo.product_id = pp.id and wo.name = 'F'
            ) as furnace, 
            (
                select sum(qty_producing) 
                from mrp_workorder wo
                where wo.state = 'progress' and wo.product_id = pp.id and wo.name like 'P%%'
            ) as plating, 
            (
                select sum(qty_producing) 
                from mrp_workorder wo
                where wo.state = 'progress' and wo.product_id = pp.id and wo.name like 'FQ%%'
            ) as fq
        from
            product_template pt
            join product_product pp on pp.product_tmpl_id = pt.id 
            join stock_quant sq on sq.product_id = pp.id 
            join res_company rs on rs.id = pt.company_id
            join stock_location sl on sl.id = sq.location_id
            join product_category pc on pt.categ_id = pc.id where pc.name = 'Finish Good' and sl.name = 'Stock' and rs.id =%s
        """

        cr = self.env.cr

        cr.execute(sql, (self.date_start, self.date_start, self.date_end, self.company_id.id))
        result = cr.fetchall()

        sql = "delete from vit_report_balance_so where report_id=%s"
        cr.execute(sql, (self.id,) )

        for res in result:
            line = self.env['vit.report_balance_so']
            
            # cara primitif
            if res[5] == None :
                onhand = 0
            else:
                onhand = float(res[3])
                
            if res[4] == None :
                total_so_bln_lalu = 0
            else:
                total_so_bln_lalu = float(res[4])
                
            if res[3] == None :
                total_so_bulan_ini = 0
            else:
                total_so_bulan_ini = float(res[5])
                
            if res[6] == None :
                heading = 0
            else:
                heading = float(res[6])
                
            if res[7] == None :
                rolling = 0
            else:
                rolling = float(res[7])
                
            if res[8] == None :
                furnace = 0
            else:
                furnace = float(res[8])
                
            if res[9] == None :
                plating = 0
            else:
                plating = float(res[9])
                
            if res[10] == None :
                fq = 0
            else:
                fq = float(res[10])
                
            wip = onhand + heading + rolling + furnace + plating + fq
                
            balance = wip - total_so_bln_lalu - total_so_bulan_ini
            
            

            line.create({
                'report_id': self.id,
                'product_id': res[0],
                'total_so_bln_lalu': res[3],
                'total_so_bulan_ini': res[4],
                'onhand': res[5],
                'heading': res[6],
                'rolling': res[7],
                'furnace': res[8],
                'plating': res[9],
                'fq': res[10],
                'wip_on_hand': wip,
                'balance_so': balance ,
                
            })
    
