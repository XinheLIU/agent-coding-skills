# Scenario Patterns for Operational Ontology Design

> Last updated: 2026-07-14

## Contents

1. [How to use these patterns](#how-to-use-these-patterns)
2. [O2O campaign delivery](#o2o-campaign-delivery)
3. [B2C commerce](#b2c-commerce)
4. [Quantitative trading](#quantitative-trading)
5. [Cross-scene transfer rules](#cross-scene-transfer-rules)

## How to use these patterns

Treat every item below as a hypothesis to verify, not a canonical ontology. Select one decision loop before selecting Object Types.

Do not import every candidate into the first slice. An Object belongs only when it affects identity, lifecycle, permission, source authority, action, or a competency question.

## O2O campaign delivery

### Clarify the meaning

`O2O 投放` may mean advertising delivery, coupon/promotion allocation, local-store traffic acquisition, or resource dispatch. Ask which meaning applies and which outcome matters: incremental store visits, orders, contribution margin, merchant ROI, or service capacity utilization.

### Recommended first decision loop

```text
performance/inventory event
  -> evaluate audience, channel, store, budget, and eligibility
  -> choose allocation/bid/offer adjustment
  -> approve or auto-execute within limits
  -> write to delivery platform
  -> observe delivery, visit/order, settlement, and incremental lift
```

### Candidate Semantic model

| Category | Candidates |
|---|---|
| Core entities | Campaign, Offer, AudienceSegment, Channel, Store, GeoArea, Creative, Budget |
| Operational relationship Objects | DeliveryPlan, BudgetAllocation, Placement, AttributionClaim |
| Events/observations | ExposureEvent, ClickEvent, StoreVisitEvent, ConversionEvent, SpendObservation, InventoryObservation |
| Decisions | AllocationDecision, EligibilityDecision, PauseDecision |

Identity needs special care across ad-platform user IDs, first-party customers, devices, merchants, stores, and offline transactions. Preserve consent, purpose, provenance, match confidence, and attribution windows.

### Logic candidates

- Deterministic: consent/eligibility, channel constraints, budget caps, pacing bounds, store hours, inventory availability.
- ML/statistical: response propensity, fraud/invalid traffic, attribution, incremental lift, demand forecast.
- Optimizer: budget allocation or bid selection under spend, capacity, and ROI constraints.
- LLM: campaign brief parsing, explanation, anomaly triage, creative hypothesis proposal—not eligibility, pacing arithmetic, or financial settlement.

### Kinetic Action candidates

| Action | Typical risk/control |
|---|---|
| CreateDeliveryPlanDraft | Medium; human confirmation before activation |
| ReallocateBudgetWithinBounds | Medium/high; hard daily and channel caps, idempotency, audit |
| AdjustBid | Medium/high; bounded change rate and rollback |
| PauseCampaignOrCreative | Medium; clear scope and restore Action |
| IssueOffer | High when financial/customer-visible; eligibility, consent, budget, expiry |

### Dynamic context

Model inventory, store capacity/hours, spend, pacing, channel performance, audience eligibility, market events, attribution lag, and delayed offline conversion. Use event time and replay because late conversion events can change evaluation without justifying retroactive Action changes.

### Useful metrics

Incremental visits/orders, contribution margin, cost per incremental outcome, budget utilization, pacing violations, invalid-traffic rate, writeback success, manual override rate, and decision reproducibility.

## B2C commerce

### Choose one operating decision

“Customer 360” is not an outcome. Prefer a bounded loop such as:

- Which fulfillment path should satisfy this order?
- Should this return/refund be approved, and through which path?
- Which offer is eligible and economically justified now?
- Which at-risk service case requires intervention?

### Recommended first decision loop: fulfillment

```text
OrderPlaced
  -> resolve customer, order lines, inventory, promises, payment, and location
  -> calculate available-to-promise and fulfillment options
  -> select option under cost/SLA/policy constraints
  -> reserve inventory and create fulfillment request
  -> observe shipment/delivery/cancellation and measure promise accuracy
```

### Candidate Semantic model

| Category | Candidates |
|---|---|
| Core entities | Customer, Product, SKU, Order, Payment, Store/Warehouse, Shipment, ServiceCase |
| Relationship Objects | OrderLine, InventoryPosition, Reservation, OfferEligibility, CustomerConsent |
| Events/observations | OrderPlaced, PaymentAuthorized, InventoryChanged, ShipmentUpdated, ReturnRequested |
| Decisions | FulfillmentDecision, RefundDecision, OfferDecision |

Do not collapse Customer, account, household, device, and consent into one record. Define identity resolution, survivorship, lawful-purpose access, and attribute provenance.

### Logic candidates

- Deterministic: price/discount policy, consent, return eligibility, inventory bounds, tax, payment state.
- ML/statistical: demand forecast, fraud/risk, churn, return propensity, ETA prediction.
- Optimizer: inventory allocation, routing, promised-date/cost tradeoff.
- LLM: service intent, case summarization, explanation, product-language matching, Action draft.

### Kinetic Action candidates

| Action | Typical risk/control |
|---|---|
| ReserveInventory | Medium; idempotent reservation, expiry, release compensation |
| SelectFulfillmentPath | Medium; state guard and capacity check |
| IssueRefund | High; amount limits, separation of duties, payment-system reconciliation |
| ApplyOffer | High when margin/customer fairness matters; eligibility and budget policy |
| UpdateServiceCase | Medium; provenance and customer-visible audit |

### Dynamic context

Represent rapidly changing inventory, price/offer validity, shipment status, customer consent, channel session, fraud signals, and delayed fulfillment outcomes. Keep current state as a projection over immutable events when audit and replay matter.

### Useful metrics

Promise accuracy, fulfillment cost, cancellation rate, stockout/oversell rate, refund leakage, customer resolution time, consent violations, Action failure/compensation rate, and human override rate.

## Quantitative trading

### Safety boundary

Quantitative trading is a high-consequence, low-latency domain. Do not put an LLM in the deterministic execution or pre-trade risk fast path. Use LLMs for research coordination, hypothesis documentation, incident explanation, and governed order-intent drafting unless the user supplies evidence that another bounded role is safe.

Any live order routing, cancellation, or position-changing Action requires explicit user authority, hard risk controls, complete lineage, and a tested kill switch. A design artifact never authorizes live trading.

### Recommended first decision loop

Start with simulation or paper trading:

```text
market/portfolio event
  -> construct versioned features and signal
  -> create OrderIntent
  -> run portfolio, pre-trade risk, compliance, and venue constraints
  -> approve/reject
  -> route in simulation or authorized venue
  -> ingest execution and market outcome
  -> attribute PnL, slippage, and risk to exact versions
```

### Candidate Semantic model

| Category | Candidates |
|---|---|
| Core entities | Instrument, Venue, Account, Portfolio, Position, StrategyVersion, RiskLimit, TradingSession |
| Relationship Objects | Listing, OrderIntent, Order, Execution, Allocation, LimitAssignment |
| Events/observations | MarketObservation, SignalObservation, RiskObservation, OrderEvent, ExecutionEvent, CorporateAction |
| Decisions | TradeDecision, RiskDecision, RoutingDecision |

Separate stable Instrument identity from listings/symbols and time-varying market observations. Exact event time, sequence, market calendar, corporate-action adjustment, data provenance, and strategy/model version are mandatory for replay.

### Logic candidates

- Deterministic: position/accounting, price/quantity normalization, market session, pre-trade limits, compliance, kill switch.
- ML/statistical: signal generation, volatility/liquidity forecast, regime classification.
- Optimizer: portfolio construction, execution schedule, routing under explicit constraints.
- LLM: research synthesis, natural-language query, exception explanation, playbook selection—not pricing arithmetic, limit enforcement, or direct fast-path routing.

### Kinetic Action candidates

| Action | Typical risk/control |
|---|---|
| CreateOrderIntent | Medium; no market effect, typed strategy/version/context |
| ApproveOrderIntent | High; independent risk policy and separation of duties |
| RouteOrder | Critical; hard limits, idempotency, venue acknowledgment, kill switch |
| CancelOrReplaceOrder | Critical; race/partial-fill handling and reconciliation |
| HaltStrategy | Critical but protective; independent control path and audit |

Compensation is not “undo trade.” Model cancel, hedge, flatten, or manual escalation as distinct risk-bearing Actions. Partial fills, duplicates, rejected cancels, disconnects, and stale market data require explicit state machines.

### Dynamic context

Model event-time ordering, market regime, trading session, venue status, liquidity, positions, exposures, pending orders, limit usage, strategy/model/data versions, and operational incidents. Use immutable event history plus derived current state.

### Decision lineage

Every OrderIntent and Order should be reproducible from:

```yaml
market_data_snapshot: "source + event-time range + adjustment version"
strategy_version: "immutable version"
model_and_feature_versions: []
portfolio_and_positions_as_of: "event time"
risk_and_policy_versions: []
approvals: []
execution_events: []
outcome_attribution: "PnL/slippage/risk horizon"
```

### Useful metrics

Risk-adjusted return, slippage, fill rate, limit breaches, stale-data blocks, rejected/canceled order rate, kill-switch latency, decision replay success, model drift, and human override rate. Report backtest and live/paper metrics separately.

## Cross-scene transfer rules

| Pattern | O2O | B2C | Quant trading |
|---|---|---|---|
| Stable entity vs observation | Campaign vs delivery event | SKU vs inventory observation | Instrument vs market observation |
| Relationship Object | BudgetAllocation | InventoryReservation | Order/Execution |
| Hard policy before Action | Consent/budget cap | Eligibility/payment/inventory | Pre-trade risk/compliance |
| Delayed outcome | Offline conversion/lift | Delivery/return | PnL/slippage horizon |
| Protective Action | PauseCampaign | ReleaseReservation/hold refund | HaltStrategy/cancel order |
| AI role | Brief/explanation/proposal | Intent/service/draft | Research/explanation only by default |

Transfer the decision-loop structure, Action discipline, provenance, and governance—not the domain nouns.
