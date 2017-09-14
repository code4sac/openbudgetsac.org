---
title: Revenues and Expenses
author: Code for Sacramento
layout: default
permalink: /revenues-expenses/
---

## Revenues and Expenses

#### Flow diagram of the City of Sacramento budget from Revenue source through Fund to Expense.

##### Based on [Open Oakland's flow diagram](http://openbudgetoakland.org/2015-17-proposed-budget-flow.html) ([GitHub repo](https://github.com/openoakland/openbudgetoakland)).

*Mouse over a flow line to highlight it; click on a bar to highlight all its flows.*

<div class="row">
  <div class="col-md-3">
    <h4>Fiscal Year</h4>
    <select id="fy" class="form-control"></select>
  </div>
</div>

<div class="row">
  <div id="sankey">
    <div id="chart"></div>
  </div>
</div>

<div id="hover_description"></div>

<script src="/js/flow.js" charset="utf-8"></script>
<script src='/js/revenues-expenses.js'></script>
