# Brand Language Cleanup Review

This document audits and enforces the institutional NSSF SmartLife Flexi brand purity across all user-facing, staff-facing, and UAT-facing materials.

## Purpose & Scope
To ensure that all non-technical interfaces feel professional, authoritative, and NSSF-owned. All developer-centric framework leakage (e.g., "Frappe", "ERPNext", "Frappie", "bench", "DocType", "whitelisted API") is removed or rephrased on non-technical surfaces.

## Search Audit & Categorization

A repository-wide search was conducted for framework and styling leaks:
1. **Public/Staff UI**: Cleaned to prevent internal system leaks.
2. **UAT/Demo/Board Docs**: Rephrased to use institutional terminology.
3. **Server operator runbooks & tests**: Intentionally left unchanged since they require exact executable commands (`bench`, `frappe`, etc.).

## Language Replacement Standards

| Developer-Facing / Framework Term | User / Staff / Board Replacement |
|---|---|
| Frappe / ERPNext app | SmartLife Flexi system |
| Frappe Desk / Workspace | SmartLife Admin Console / Workspace |
| DocType | record type / data record / module |
| Whitelisted API / API method | secure system action / staff-only action |
| Bench migrate | server migration command |
| Frappe framework | platform layer |
| Frappe charts / reports | SmartLife reporting charts / internal reports |
| Framework route | SmartLife page |
| Frappe user role | SmartLife access role |

## Cleanup Actions Taken

1. **Staff Login Gates**: Replaced default framework notifications with professional login prompts.
   - [smartlife-staff-queue-full.html](file:///Users/robertsebunya/.gemini/antigravity/scratch/nssf_smart_savers/nssf_smart_savers/www/smartlife-staff-queue-full.html#L34)
   - [smartlife-command-centre.html](file:///Users/robertsebunya/.gemini/antigravity/scratch/nssf_smart_savers/nssf_smart_savers/www/smartlife-command-centre.html#L34)
2. **NSSF Blue and Green Color Standards**: Ensured all color references in docs refer to the institutional "NSSF Blue and Green" colors, replacing any remaining references to blue/yellow.

## Brand Audit Status
`Demo seed and NSSF brand cleanup blueprint complete / implementation pending`
