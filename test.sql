SELECT 
	"sale_sale"."id", 
	"sale_sale"."company_id", 	
	"sale_sale"."company_worker_id", 
	"sale_sale"."value", 
	"sale_sale"."delivery", 
	"sale_sale"."canceled", 
	"sale_sale"."total", 
	"sale_sale"."created", 
	"sale_sale"."updated", 
	"default_company"."id", 
	"default_company"."owner_id", 
	"default_company"."slug", 
	"default_company"."company", 
	"default_company"."cnpj", 
	"default_company"."pix_key", 
	"default_company"."created", 
	"default_company"."updated" 
	
FROM "sale_sale" 
	INNER JOIN "default_company" ON ("sale_sale"."company_id" = "default_company"."id") 
	
ORDER BY "default_company"."company" ASC, "sale_sale"."id" ASC