# Kennicutt–Schmidt Star-Formation Analysis — M100

A Python pipeline that tests the **Kennicutt–Schmidt star-formation law** in the
spiral galaxy M100, combining ALMA, GALEX and Spitzer imaging to measure how the
star-formation rate tracks the available molecular gas.

**Result:** star-formation rate scales with molecular gas mass as a power law of slope
**1.08 ± 0.05**, with a Pearson correlation of **r = 0.90** (p ≈ 10⁻¹⁷) — a tight,
statistically significant relation. Kennicutt–Schmidt relation for M100:


<img width="583" height="433" alt="ks_relation" src="https://github.com/user-attachments/assets/816b14a5-3361-4f23-90de-1348ac0d7a68" />

## What it does

The Kennicutt–Schmidt law relates star formation to available molecular gas. Across
~45 regions of M100 the pipeline:

- measures **molecular gas mass** from ALMA CO intensity maps;
- measures **star-formation rate** from a hybrid GALEX near-UV + Spitzer 24 μm mid-IR tracer;
- runs **aperture photometry** (`photutils`) with WCS coordinate handling and local
  background subtraction;
- converts fluxes to physical quantities with **full uncertainty propagation**;
- fits the log–log relation with a **robust, error-weighted linear fit and outlier clipping**
  (`ltsfit`).
  
Download notebook for more detail regarding the process.

Fitted slope 1.083 ± 0.054, intercept −10.19 ± 0.43, Pearson r = 0.90, Spearman r = 0.79 —
both p-values far below 0.05, so the correlation is highly significant (44 regions fitted,
1 clipped as an outlier).




## Notes

Emission regions are selected interactively on the CO map, so rerunning the notebook
end-to-end requires the FITS data and manual region selection.

## Author

Jacob Jones

