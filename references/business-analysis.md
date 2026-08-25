# Business and product analysis

Read this reference for multi-product, technology, distribution, platform, project, manufacturing, or complex group applicants.

## Product-by-product unit of analysis

For each material product/service line, answer:

1. **Scenario and user:** who uses it, who pays, where it is used, and what event triggers purchase.
2. **Product content:** hardware, software, consumables, implementation, maintenance, data/service components, versions and price bands.
3. **Commercial model:** direct sale, distributor, project, subscription, usage fee, commission, licensing, OEM/ODM, marketplace, or bundled model.
4. **Delivery and recognition:** order, procurement/production, shipment/deployment, acceptance, invoicing, warranty and revenue-recognition point.
5. **Economics:** unit price, volume, gross margin, recurring revenue, acquisition cost, channel fee, warranty/return cost and operating leverage.
6. **Cash conversion:** advance, milestone, acceptance, credit period, retention, platform settlement and foreign-exchange exposure.
7. **Supply dependency:** core material/service, sole-source items, alternates, minimum order, lead time, bargaining power and localization.
8. **Customer quality:** top-five concentration, end-customer look-through, repeat rate, budget source, payment behavior and switching cost.
9. **Industry and competition:** addressable market, growth driver, cycle, regulation, substitutes, named competitors, product/price/channel comparison.
10. **Defensibility:** verified technology, qualification, installed base, data, channel, ecosystem, cost, brand, delivery record or customer resource.

Avoid generic “industry prospects are broad” prose. Connect the industry driver to the applicant's specific product, customer, order, margin, and cash-flow consequence.

## Flowchart specification

Each materially different model needs a diagram containing applicant, direct customer, end user, key supplier/outsourcer, platform/logistics party when relevant, and the direction/timing of consideration and delivery.

- Red solid arrow: funds, labelled with payer, payee, timing or percentage when known.
- Black solid arrow: goods, software, service, data, licence, acceptance document, or logistics.
- Dashed grey arrow may be used only for a contract/information relation and must not replace required flows.

Create a JSON file and run:

```bash
python scripts/render_business_flow.py flow.json flow.svg
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
