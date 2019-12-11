

from odoo import api, fields, models
import time
import datetime
import logging
_logger = logging.getLogger(__name__)


class report_balance(models.Model):

    _name = "vit.report_balance"
    
    
    date_start = fields.Date( string="Date start",  help="" ,
                                required=True, default=lambda self: time.strftime("%Y-%m-%d"), 
    )
    
    date_end = fields.Date( string="Date end",  help="",
                                required=True, default=lambda self: time.strftime("%Y-%m-%d"), 
    )
    name = fields.Char( required=True, string="Name",  help="",
    )
    
    
    name_report = fields.Selection(
        string='Report Name',
        selection=[('Report Balance SO', 'Report Balance SO'), ('Report Balance WIP', 'Report Balance WIP')], 
        required=True,readonly=True 
        
    )
    
    

    company_id = fields.Many2one(comodel_name="res.company",  string="Company",  help="" , 
    required=True
    )
    
    report_ids = fields.One2many(
        string='report',
        comodel_name='vit.report_balance_so',
        inverse_name='report_id'
    )
    
    report_wip_ids = fields.One2many(
        string='report',
        comodel_name='vit.report_balance_wip',
        inverse_name='report_id'
    )
    
    sql = """select 
            pp.id as product_id,
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
            (  
                select sum(quantity)
                from stock_quant sq 
                join stock_location loc on sq.location_id = loc.id
                where 
                sq.product_id = pp.id
                and loc.usage='internal'
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
            join res_company rs on rs.id = pt.company_id
            join product_category pc on pt.categ_id = pc.id where pc.name = 'Finish Good' and rs.id = %s
        """
    
    # //////////////////////////////////////////////////////// GENERATE MASTER //////////////////////////////////////////////////////////////////
    # //////////////////////////////////////////////////////// GENERATE MASTER //////////////////////////////////////////////////////////////////
    # //////////////////////////////////////////////////////// GENERATE MASTER //////////////////////////////////////////////////////////////////
    @api.multi
    def generate_master(self):
        if self.name_report == 'Report Balance SO' :
            return self.generate_balance_so()
        else:
            return self.generate_balance_wip()
        
    # //////////////////////////////////////////////////////// GENERATE SO //////////////////////////////////////////////////////////////////
    # //////////////////////////////////////////////////////// GENERATE SO //////////////////////////////////////////////////////////////////
    # //////////////////////////////////////////////////////// GENERATE SO //////////////////////////////////////////////////////////////////
    @api.multi
    def generate_balance_so(self):
        

        cr = self.env.cr

        cr.execute(self.sql, (self.date_start, self.date_start, self.date_end, self.company_id.id))
        result = cr.dictfetchall()

        sql = "delete from vit_report_balance_so where report_id=%s"
        cr.execute(sql, (self.id,) )

        line = self.env['vit.report_balance_so']
        for res in result:

            # cara primitif

            # if res['total_so_bln_ini'] == None :
            #     total_so_bln_ini = 0
            # else:
            #     total_so_bln_ini = float(res['total_so_bln_ini'])
                
            total_so_bln_ini = float(res['total_so_bln_ini']) if res['total_so_bln_ini'] != None else 0
                

            # if res['total_so_bln_lalu'] == None :
            #     total_so_bln_lalu = 0
            # else:
            #     total_so_bln_lalu = float(res['total_so_bln_lalu'])
            
            total_so_bln_lalu = float(res['total_so_bln_lalu']) if res['total_so_bln_lalu'] != None else 0
                
            # if res['onhand'] == None :
            #     onhand = 0
            # else:
            #     onhand = float(res['onhand'])
            
            onhand = float(res['onhand']) if res['onhand'] != None else 0
                
            # if res['heading'] == None :
            #     heading = 0
            # else:
            #     heading = float(res['heading'])
            
            heading = float(res['heading']) if res['heading'] != None else 0
                
            # if res['rolling'] == None :
            #     rolling = 0
            # else:
            #     rolling = float(res['rolling'])
            
            rolling = float(res['rolling']) if res['rolling'] != None else 0
                
            # if res['furnace'] == None :
            #     furnace = 0
            # else:
            #     furnace = float(res['furnace'])
            
            furnace = float(res['furnace']) if res['furnace'] != None else 0
                
            # if res['plating'] == None :
            #     plating = 0
            # else:
            #     plating = float(res['plating'])
            
            plating = float(res['plating']) if res['plating'] != None else 0
                
            # if res['fq'] == None :
            #     fq = 0
            # else:
            #     fq = float(res['fq'])
            
            fq = float(res['fq']) if res['fq'] != None else 0
            
            _logger.info("/////////////////////////////////////////////////////////////////////////////////////")
            _logger.info("ini SO")
            _logger.info("///////////////////////////////////////////////////////////////////////////////////////")
                
            wip = onhand + heading + rolling + furnace + plating + fq
            balance = wip - total_so_bln_lalu - total_so_bln_ini

            line.create({
                'report_id': self.id,
                'product_id': res['product_id'],
                'total_so_bln_lalu': total_so_bln_lalu,
                'total_so_bulan_ini': total_so_bln_ini,
                'onhand': onhand,
                'heading': heading,
                'rolling': rolling,
                'furnace': furnace,
                'plating': plating,
                'fq': fq,
                'wip_on_hand': wip,
                'balance_so': balance ,
                
            })
            
    # //////////////////////////////////////////////////////// GENERATE WIP //////////////////////////////////////////////////////////////////
    # //////////////////////////////////////////////////////// GENERATE WIP //////////////////////////////////////////////////////////////////
    # //////////////////////////////////////////////////////// GENERATE WIP //////////////////////////////////////////////////////////////////
    @api.multi
    def generate_balance_wip(self):

        cr = self.env.cr

        cr.execute(self.sql, (self.date_start, self.date_start, self.date_end, self.company_id.id))
        result = cr.dictfetchall()

        _logger.info("/////////////////////////////////////////////////////////////////////////////////////")
        _logger.info("ini wip")
        _logger.info("///////////////////////////////////////////////////////////////////////////////////////")
        
        sql = "delete from vit_report_balance_wip where report_id=%s"
        cr.execute(sql, (self.id,) )

        line = self.env['vit.report_balance_wip']
        for res in result:
           
            onhand = float(res['onhand']) if res['onhand'] != None else 0
            
            heading = float(res['heading']) if res['heading'] != None else 0
           
            rolling = float(res['rolling']) if res['rolling'] != None else 0
       
            furnace = float(res['furnace']) if res['furnace'] != None else 0
           
            plating = float(res['plating']) if res['plating'] != None else 0
            
            fq = float(res['fq']) if res['fq'] != None else 0
                

            line.create({
                'report_id': self.id,
                'product_id': res['product_id'],
                'onhand': onhand,
                'heading': heading,
                'rolling': rolling,
                'furnace': furnace,
                'plating': plating,
                'fq': fq,
               
            })
    
