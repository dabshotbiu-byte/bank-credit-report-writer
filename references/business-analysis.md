# Business and product analysis

Read this reference for every full credit report and every request to write or revise the operating section. The four supplied sample reports consistently use a deep sequence: explain the product in plain language, break down products/models and applications, show revenue structure, map the operating flow, analyze procurement/production/sales, connect customers and suppliers, then reach industry, competition and competitive-advantage conclusions. Match that depth rather than merely repeating headings.

## Mandatory product register

Before drafting, make a working product register from all available sources: company introduction, official website, brochures, contracts, orders, invoice descriptions, revenue ledger, inventory list, project list and interview notes. Reconcile inconsistent names and distinguish product, model/SKU, accessory/consumable, implementation and maintenance/service income.

The register must include every disclosed product or service line. Group several models only if their user scenario, commercial model, transaction parties, delivery/acceptance, settlement and risk are substantially identical. When grouping:

- list every included product/model by name;
- state why one analysis and one diagram validly cover the group;
- separately quantify or discuss any model with a different price band, margin, lifecycle, customer base or competitive position;
- never use “其他产品” to absorb a material or strategically important line.

## Required order in the report

Keep the exact headings and question order of the supplied template, while ensuring the business content covers this sequence:

1. **主营业务总览**：收入性质属于生产、贸易、项目、订阅或服务；主要收入和利润由什么产生；企业在产业链中处于哪一层。
2. **产品结构及逐产品分析**：先用非专业读者能理解的语言解释产品，再列功能、构成、型号、参数、价格带和应用。
3. **收入结构**：按产品、区域、渠道或项目列示至少两个期间的收入、占比和毛利率，并解释产品生命周期、销量、价格、促销及结构变化。
4. **经营及盈利模式**：写明采购、生产/实施、销售、交付、验收、开票、收款和售后；插入相应资金流、货物流/服务流图。
5. **客户与供应商**：将前五大明细映射回具体产品，解释合作内容、合作年限、集中度、账期、议价能力、替代性和履约表现。
6. **结算及资金占用**：把上游付款、备货/在制/项目实施、下游回款串成现金转换周期，指出资金沉淀科目和本次授信需求的形成原因。
7. **行业、竞争及核心竞争力**：行业数据必须落到申请人的产品、价格带、客户、订单、毛利和现金流；逐一比较具名竞争对手，并说明优势能否持续。
8. **经营结论**：评价收入持续性、利润质量、集中度、替代风险、营运资金压力及对第一还款来源的贡献。

## Product-by-product writing contract

For every product or valid product group, the finished report must contain all of the following. Do not place all items into one generic paragraph.

### 1. What it is and how it is used

- Explain what the product does in plain language before using technical terminology.
- Identify the actual operator/user, payer, place of use and purchase trigger.
- Describe the pain point and why the customer buys instead of continuing its prior method.
- Give concrete applications: department, process, project, production step, household/industrial setting, transaction event or use case.
- State whether it is required, optional, repeat-purchase, limited-use, consumable, upgrade-driven or one-off.

### 2. Product content and differentiation

- Break down hardware, software, consumables, accessories, implementation, maintenance and data/service components.
- List major models/versions, key parameters, price bands and intended customer tiers when available.
- Explain which feature changes the customer outcome; do not copy feature lists without interpretation.
- Identify lifecycle, replacement cycle, compatibility, qualification, patent or regulatory constraints.

### 3. Business and delivery model

- Identify direct sale, distribution, project, subscription, usage fee, commission, licensing, OEM/ODM, marketplace or bundled model.
- Trace order/contract → procurement/production/development → shipment/deployment → use/acceptance → invoice → collection → warranty/maintenance.
- State who owns inventory, provides implementation, bears returns/warranty, controls pricing and maintains the end-customer relationship.
- Explain the revenue-recognition point and whether income recurs after initial delivery.

### 4. Product economics and cash conversion

- Quantify revenue, share, volume, price, gross margin and their period-on-period movement when evidence permits.
- Explain material/labour/outsourcing/channel/platform/warranty costs and the actual gross-margin driver.
- State advance/milestone/acceptance/credit/retention/platform settlement terms and foreign-exchange exposure.
- Connect payment terms to receivables, prepayments, inventory, contract assets/liabilities and the working-capital gap.

### 5. Product-specific counterparties and competition

- Map the product to its customers, end users, suppliers/outsourcers and sales channels; do not leave the top-five tables disconnected from the product discussion.
- Analyze concentration, repeat rate, budget source, payment behaviour, switching cost, sole-source dependency, substitutes, lead time and bargaining power.
- Name relevant competitors and compare the same dimensions: use scenario, core parameters/function, price, channel, delivery, installed base/share and after-sales.
- End with the applicant's evidenced advantage and its limits, not company marketing language.

### 6. Analyst conclusion

End each product section with a reasoned view on revenue sustainability, margin quality, working-capital occupation, customer/supplier concentration, substitution or obsolescence risk and contribution to repayment. Base the view on the preceding evidence.

## Minimum depth test

A product section is incomplete if it contains only a product definition, feature table, revenue table or one general paragraph. At minimum, each product/product group needs:

- a plain-language scenario and concrete-application discussion;
- a product composition/model/function discussion;
- a commercial, delivery and settlement discussion;
- one dedicated or validly shared flowchart plus interpretation;
- customer, supplier and competitor mapping;
- a product-specific economics, working-capital and credit conclusion.

Tables and diagrams support the analysis; they never replace explanatory prose.

## Flowchart specification

Every product or valid product group needs a diagram containing the applicant, direct customer, end user, key supplier/outsourcer, platform/logistics/total contractor when relevant, and the direction/timing of consideration and delivery. A shared diagram is allowed only when the full transaction chain and settlement terms are the same; name all covered products in the title or caption.

- Red solid arrow: funds, labelled with payer, payee, timing or percentage when known.
- Black solid arrow: goods, software, service, data, licence, acceptance document, or logistics.
- Dashed grey arrow may be used only for a contract/information relation and must not replace required flows.

Create a JSON file and run:

```bash
python3 scripts/render_business_flow.py flow.json flow.svg
```

Example:

```json
{
  "title": "产品A业务模式",
  "nodes": [
    {"id": "supplier", "label": "核心供应商"},
    {"id": "applicant", "label": "申请人"},
    {"id": "customer", "label": "直接客户"},
    {"id": "user", "label": "终端用户"}
  ],
  "edges": [
    {"from": "supplier", "to": "applicant", "type": "goods", "label": "原材料/服务"},
    {"from": "applicant", "to": "supplier", "type": "funds", "label": "现款/账期"},
    {"from": "applicant", "to": "customer", "type": "goods", "label": "产品交付"},
    {"from": "customer", "to": "applicant", "type": "funds", "label": "验收后回款"},
    {"from": "customer", "to": "user", "type": "goods", "label": "使用/部署"}
  ]
}
```

## Analytical conclusion

End each product section with the analyst's view of sustainability, margin quality, working-capital occupation, concentration, substitution risk and contribution to repayment. Base the view on the preceding evidence; do not repeat product marketing language.

## Coverage gate before delivery

Create a working matrix with one row per product/product group and mark the following columns: source evidence; scenario/user/payer; concrete applications; product composition/models; business/delivery model; revenue/price/margin; fund flow; goods/service/data flow; diagram file; customers; suppliers; settlement/working capital; industry driver; named competitors; competitive advantage; repayment conclusion.

The gate passes only when:

- every product in the register has a row and appears in the report;
- every column is supported or explicitly narrowed to what can be concluded from available evidence;
- every product has a diagram, or a documented valid reason for sharing a named diagram;
- the report follows the supplied template's section order and places tables/figures beside the related analysis;
- the chain `业务模式 → 产品结构 → 客户 → 供应商 → 行业 → 竞争 → 核心竞争力` is traceable for each material product;
- the business section explains how operations create revenue, margin, working-capital occupation and repayment cash.

If any row fails, continue analysis or obtain the decisive missing fact before producing the finished report. Do not shorten the section merely to make the template look complete.
