#-*- coding: utf-8 -*-

{
	"name": "Report Balance",
	"version": "1.0", 
	"depends": [
		'base','account','mrp'
	],
	'author': 'firmanrizaldiyusup@gmail.com',
	'website': 'http://www.vitraining.com',
	"summary": "vit_report_balanced",
	"description": """

	vit_report_balanced

	Pilih Report balance ,Report yang akan tergenerate adalah
	- Product Code dan Product Name yang Product Categorynya = "Finish Good"
	- Total SO Bulan Lalu akan tampil jika kurang dari Date Start
	- Total SO Bulan ini akan tampil antara Date Start dan Date end
	- Onhand adalah quantity inventory evaluation dari produk antara Date Start dan Date end
	- Heading akan tampil pada saat ada work order dengan nama code yang huruf depannya "H" dan statusnya "in Progress" antara Date Start dan Date end
	- Rolling akan tampil pada saat ada work order dengan nama code yang huruf depannya "R" dan statusnya "in Progress" antara Date Start dan Date end
	- Furnace akan tampil pada saat ada work order dengan nama code yang hurufnya = "F" dan statusnya "in Progress" antara Date Start dan Date end
	- Plating akan tampil pada saat ada work order dengan nama code yang huruf depannya "PL" dan statusnya "in Progress" antara Date Start dan Date end
	- FQ akan tampil pada saat ada work order dengan nama code yang huruf depannya "FQ" dan statusnya "in Progress" antara Date Start dan Date end
	- WIP adalah onhand + heading + rolling + furnace + plating + fq
	- Balance adalah WIP - Total SO Bulan Lalu - Total SO Bulan ini 

""",
	"data": [
		"security/ir.model.access.csv",
		"view/menu.xml",
		"view/report_balance.xml",
		"data/work_order.xml",
		"data/report_balance.xml",
	],
	"installable": True,
	"auto_install": False,
	"application": True,
}