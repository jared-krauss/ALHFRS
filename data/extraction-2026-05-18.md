# LFR Data Extraction — 2026-05-18

## Files Found

**Priority 1 — deployment records (NEC & Met Files):**
- `live-facial-recognition-deployment-record-2025.pdf`
- `live-facial-recognition-deployment-record-2026.pdf`

**Priority 2 — Excel/structured data:**
- `Copy of Live Facial Recognition Deployments.xlsx`

**Priority 3 — deployment grids:**
- `lfr-deployment-grid-2020-2022.pdf` (appears in both Deployment Data/ and NEC & Met Files/)
- `lfr-deployment-grid-2020-2022 (1).pdf` (duplicate in NEC & Met Files/)
- `lfr-deployment-grid-2023-to-2024.pdf` (appears in both folders)
- `lfr-deployment-grid-2025-up-to-May20-.pdf` (Deployment Data only)

**Priority 4 — Garbett / investigative:**
- `The unchecked expansion of live facial recognition technology in London - Zoë Garbet.pdf`

**Priority 4 — Garbett report (processed):**
- `The unchecked expansion of live facial recognition technology in London - Zoë Garbet.pdf` ← READ pages 1–18 of 34

**Priority 5 — Inbox CSV:**
- `Data Extraction on Facial REcogniton Technology in London - Sheet1.csv`

**Not deployment data (skip):**
- `lfr-policy-document2.pdf` — policy doc
- `mps-lfr-1-v.3.0-web.pdf` — policy doc
- `NEC-FR_white-paper-It'sAllAboutTheFace.pdf` — vendor white paper
- `Intimate alienation -reduced.pdf` — unrelated
- `Public expects facial recognition system policing in the UK - Facewatch.pdf` — Facewatch PR
- `facial_recognition_delivering_more_precise_policing-science-police-met.pdf` — policy
- `FRS_Consultation_FINAL-2026-new-legal-framework.pdf` — consultation doc
- `frt-equitability-study_mar2023.pdf` — academic study
- `ICO-guidance-on-video-surveillance-including-cctv-1-0.pdf` — guidance
- `London-Met-Police-Trial-of-Facial-Recognition-Tech-Report-2.pdf` — early trial report
- `mayorsquestions-2016-boris-comissioner-how-to-convict-more-criminals.pdf` — policy
- `npia--capture-and-interchange-standard-for-facial-and-smt-images2.pdf` — technical standard
- `scc_self_assessment_tool-23-web.pdf` — regulatory tool
- `website-audit-12mo-full-horizon.pdf` — unrelated

## Existing DB Summary (pre-extraction)
- `met-police-lfr.json`: 8 deployments (lfr-001 to lfr-008)
- `btp-lfr.json`: 2 deployments (btp-001, btp-002)
- `private-operators.json`: 5 deployments (priv-001 to priv-005)
- `retrospective-fr.json`: multiple rfr incidents

**Status: in progress**

---

## Source: Copy of Live Facial Recognition Deployments.xlsx

**Sheet structure:** Notes | Sheet6 (258 data rows) | Deployment Data (254 data rows) | Census data (683 wards)
**Author:** Zoë Garbett — enriched from MPS public data, adds postcode (approx), ward name, ward code, and 2021 census ethnicity data per ward
**Primary sheet used:** "Deployment Data" — 254 records, years 2020–2025 (partial)
**Year distribution:** 2020 (3) · 2022 (6) · 2023 (23) · 2024 (180) · 2025 (40 — subset overlapping with 2025 PDF)

**Overlap with existing JSON:** 2020 and 2022 rows correspond to lfr-001 through lfr-005 era entries already in met-police-lfr.json. The Excel adds ward codes and postcodes to those records.
**Net new deployment records:** 2023 (23 records) + 2024 (180 records) = 203 new deployments not captured elsewhere in this session.
**2025 rows:** 40 records — these overlap with the 2025 PDF extract above; key added value is ward/postcode enrichment.
**Key enrichment fields:** Post code (approx) · Ward (approx) · Ward Code (ONS E05...) · Census Black% · Census Asian% · Census Mixed% · Census Other% (ward vs London average)

---

### 2020 — 3 records (overlap with lfr-001/002/003 in JSON)

| Date | Location | Borough | Ward | Postcode | Faces | Alerts | Arrests | FA Rate | Notes |
|------|----------|---------|------|----------|-------|--------|---------|---------|-------|
| 2020-02-21 | Oxford Circus | Westminster | West End | W1C 1DE | n/a | n/a | n/a | 0 | Technical fault stopped deployment |
| 2020-02-27 | Oxford Circus | Westminster | West End | W1C 1DE | 8,600 | 8 | 1 | 0.0008 | 7 false alerts |
| 2020-11-02 | Stratford | Newham | Stratford | E15 1BB | 4,600 | - | - | 0 | Data incomplete |

### 2022 — 6 records (overlap with lfr-003/004/005 era in JSON)

| Date | Location | Borough | Ward | Postcode | Faces | Alerts | Arrests | FA Rate | Notes |
|------|----------|---------|------|----------|-------|--------|---------|---------|-------|
| 2022-01-28 | Oxford Circus | Westminster | West End | W1C 1DE | 12,120 | 11 | 4 | 0.00008 | |
| 2022-07-07 | Oxford Circus | Westminster | West End | W1C 1DE | 34,286 | 4 | 3 | 0 | |
| 2022-07-14 | Oxford Circus | Westminster | West End | W1C 1DE | 34,360 | 3 | 1 | 0 | |
| 2022-07-16 | Oxford Circus | Westminster | West End | W1C 1DE | 36,420 | 1 | - | 0 | |
| 2022-07-28 | Piccadilly Circus | Westminster | St James's | W1J 9HP | 16,440 | 1 | - | 0 | |
| 2022-10-03 | Leicester Square | Westminster | St James's | WC2H 7DE | 10,740 | - | - | 0 | |

### 2023 — 23 records (NET NEW)

| Date | Location | Borough | Ward | Postcode | Faces | Alerts | Arrests | FA Rate | Notes |
|------|----------|---------|------|----------|-------|--------|---------|---------|-------|
| 2023-04-14 | Camden (NW1) | Camden | Regent's Park | NW1 8QH | 6,790 | - | - | 0 | |
| 2023-04-20 | Islington (N1) | Islington | St Mary's & St James' | N1 2TU | 3,930 | 1 | - | 0 | |
| 2023-06-04 | Camden (NW1) | Camden | Regent's Park | NW1 8QH | 5,460 | 1 | 1 | 0 | |
| 2023-06-05 | Westminster, Bridge Street | Westminster | St James's | SW1A 2JH | 20,578 | - | - | 0 | Multi-point same-day operation |
| 2023-06-05 | Westminster, Savoy Place | Westminster | St James's | WC2R 0BL | 17,250 | - | - | 0 | Multi-point same-day operation |
| 2023-06-05 | Westminster, Piccadilly | Westminster | St James's | W1J 9BR | 30,633 | 2 | 1 | 0 | Multi-point same-day operation |
| 2023-06-11 | Haringey, Love Lane | Haringey | Bruce Castle | N17 8DB | 8,285 | 2 | - | 0.0001 | Same-day paired deployment |
| 2023-06-11 | Haringey, High Rd | Haringey | Noel Park | N22 6BX | 45,930 | 1 | 1 | 0 | Same-day paired deployment |
| 2023-06-17 | Westminster, The Mall | Westminster | St James's | SW1Y 5DG | 8,630 | 1 | - | 0 | Same-day paired deployment |
| 2023-06-17 | Westminster, Birdcage Walk | Westminster | St James's | SW1E 6HQ | 4,650 | - | - | 0 | Same-day paired deployment |
| 2023-07-12 | Croydon George Street | Croydon | Fairfield | CR0 1PE | 3,940 | 6 | 4 | 0.00025 | Same-day paired deployment |
| 2023-07-12 | Croydon North End | Croydon | Fairfield | CR0 1UB | 3,820 | 3 | 3 | 0 | Same-day paired deployment |
| 2023-08-09 | Wardour St, W1 | Westminster | West End | W1F 0TH | 28,750 | 2 | 1 | 0 | 1 of 3 Wardour St deployments |
| 2023-08-18 | Wardour St, W1 | Westminster | West End | W1F 0TH | 48,700 | 3 | 2 | 0 | 2 of 3 Wardour St deployments |
| 2023-09-09 | Islington (N1) | Islington | St Mary's & St James' | N1 2TU | 34,200 | 1 | 1 | 0 | |
| 2023-09-11 | Westminster | Westminster | St James's | SW1A 2HQ | 4,863 | 7 | 6 | 0 | |
| 2023-09-24 | Camden High Street | Camden | Regent's Park | NW1 8QH | 9,973 | 4 | 3 | 0 | |
| 2023-11-08 | Wardour St, W1 | Westminster | West End | W1F 0TH | 28,220 | 3 | 3 | 0 | 3 of 3 Wardour St deployments |
| 2023-11-16 | Westminster | Westminster | St James's | SW1A 2HQ | 530 | - | - | 0 | Very low face count — partial/short |
| 2023-12-14 | Croydon George Street | Croydon | Fairfield | CR0 1PE | 3,015 | 10 | 3 | 0 | Same-day paired deployment |
| 2023-12-14 | Croydon North End | Croydon | Fairfield | CR0 1UB | 3,496 | 11 | 5 | 0 | Same-day paired deployment |
| 2023-12-21 | Selhurst Park, Holmesdale Rd | Croydon | South Norwood | SE25 6PJ | 3,600 | - | - | 0 | Crystal Palace football — Event PSO? |
| 2023-12-21 | Selhurst Park, Norwood Junction | Croydon | South Norwood | SE25 6PJ | 1,149 | - | - | 0 | Crystal Palace football — Event PSO? |

### 2024 — 180 records (NET NEW)

| Date | Location | Borough | Ward | Postcode | Faces | Alerts | Arrests | FA Rate | Notes |
|------|----------|---------|------|----------|-------|--------|---------|---------|-------|
| 2024-01-02 | Croydon, Church St | Croydon | Fairfield | CR0 1RH | 924 | 9 | 3 | 0 | |
| 2024-01-02 | Westminster | Westminster | St James's | SW1A 2HQ | 2,795 | - | - | 0 | |
| 2024-01-03 | London Bridge | Southwark | Borough & Bankside | SE1 9RA | 2,439 | 2 | 1 | 0 | |
| 2024-01-03 | Westminster | Westminster | St James's | SW1A 2HQ | 2,720 | 3 | 2 | 0.0004 | |
| 2024-01-10 | George St, Croydon | Croydon | Fairfield | CR0 1PE | 6,181 | 9 | 4 | 0 | Crime Hotspot |
| 2024-01-10 | Wealdstone, High St | Harrow | Wealdstone South | HA3 5DL | 1,878 | 2 | 1 | 0 | Crime Hotspot |
| 2024-01-11 | Walworth Rd | Southwark | North Walworth | SE17 1JE | 10,510 | 11 | 3 | 0 | Crime Hotspot |
| 2024-01-11 | South St, Romford | Havering | St Alban's | RM1 1TR | 13,771 | 12 | 4 | 0 | Crime Hotspot |
| 2024-01-19 | Croydon North End | Croydon | Fairfield | CR0 1UB | 1,512 | 13 | 5 | 0 | |
| 2024-01-19 | Westminster | Westminster | St James's | SW1A 2HQ | 12,080 | - | - | 0 | |
| 2024-01-23 | Croydon George Street | Croydon | Fairfield | CR0 1PE | 1,879 | 8 | 3 | 0 | |
| 2024-01-23 | Croydon North End | Croydon | Fairfield | CR0 1UB | 1,123 | 10 | 5 | 0.0009 | |
| 2024-01-25 | Croydon, London Rd | Croydon | West Thornton | CR7 7PA | 785 | 9 | 3 | 0 | |
| 2024-01-25 | Croydon, Church St | Croydon | Fairfield | CR0 1RH | 1,222 | 14 | 6 | 0 | |
| 2024-01-30 | Croydon, Church St | Croydon | Fairfield | CR0 1RH | 2,205 | 12 | 7 | 0 | |
| 2024-01-30 | Westminster | Westminster | St James's | SW1A 2HQ | 959 | 2 | 1 | 0 | |
| 2024-02-05 | Westminster | Westminster | St James's | SW1A 2HQ | 1,534 | - | - | 0 | |
| 2024-02-05 | Kingston | Kingston | Kingston Town | KT1 1SW | 1,425 | 4 | - | 0 | |
| 2024-02-08 | Ilford | Redbridge | Fullwell | IG6 2AH | 1,643 | 2 | 2 | 0 | |
| 2024-02-08 | East Ham | Newham | East Ham | E6 1HZ | 1,921 | 8 | 5 | 0 | |
| 2024-02-21 | Clapham Junction | Wandsworth | Falconbrook | SW11 1SA | 2,913 | 5 | 2 | 0 | |
| 2024-02-21 | Tooting Broadway | Wandsworth | Tooting Broadway | SW17 0RN | 1,792 | 13 | 5 | 0 | |
| 2024-02-23 | London Bridge | Southwark | Borough & Bankside | SE1 9RA | 1,562 | 2 | - | 0 | |
| 2024-02-23 | London Bridge | Southwark | Borough & Bankside | SE1 9RA | 2,160 | 4 | 2 | 0.0009 | 2nd deployment same location/day |
| 2024-02-28 | Tottenham Ct Rd | Camden | Bloomsbury | W1T 1BG | 1,516 | 2 | - | 0 | |
| 2024-02-28 | Tottenham Ct Rd | Camden | Bloomsbury | W1T 1BG | 2,176 | 5 | 1 | 0 | 2nd deployment same location/day |
| 2024-03-04 | Romford | Havering | St Alban's | RM1 1PL | 1,803 | 7 | 2 | 0.0006 | |
| 2024-03-04 | Ealing Broadway Stn | Ealing | Ealing Broadway | W5 2HZ | 2,446 | 4 | - | 0 | |
| 2024-03-10 | High St, East Ham | Newham | East Ham | E6 1HZ | 3,750 | 7 | 5 | 0 | Crime Hotspot |
| 2024-03-10 | Wimbledon Bridge | Merton | Hillside | SW19 7NL | 11,145 | 6 | - | 0 | Crime Hotspot |
| 2024-03-12 | Powis St, Woolwich | Greenwich | Woolwich Arsenal | SE18 6LQ | 9,351 | 9 | 5 | 0 | Crime Hotspot |
| 2024-03-12 | Kingsland High St | Hackney | Dalston | E8 2PB | 10,960 | 12 | 5 | 0 | Crime Hotspot |
| 2024-03-14 | Clapham Junction | Wandsworth | Falconbrook | SW11 1SA | 2,372 | 7 | 2 | 0 | |
| 2024-03-14 | Bromley | Bromley | Bromley Town | BR1 1DN | 1,723 | 5 | 1 | 0 | |
| 2024-03-19 | Croydon, Church St | Croydon | Fairfield | CR0 1RH | 1,277 | 12 | 5 | 0 | |
| 2024-03-19 | Croydon, North End | Croydon | Fairfield | CR0 1UB | 1,321 | 14 | 4 | 0 | |
| 2024-03-21 | Croydon, North End | Croydon | Fairfield | CR0 1UB | 1,286 | 16 | 5 | 0 | |
| 2024-03-21 | Tooting Broadway | Wandsworth | Tooting Broadway | SW17 0RN | 2,003 | 8 | 3 | 0 | |
| 2024-03-26 | Catford | Lewisham | Rushey Green | SE6 2EF | 697 | 6 | 4 | 0 | |
| 2024-03-26 | Lewisham | Lewisham | Lewisham Central | SE13 5JH | 750 | 6 | 1 | 0 | |
| 2024-03-28 | Woolwich | Greenwich | Woolwich Arsenal | SE18 7BZ | 1,146 | 12 | 6 | 0 | |
| 2024-03-28 | Romford | Havering | St Alban's | RM1 1PL | 1,066 | 9 | 3 | 0 | |
| 2024-04-06 | Harlesden | Brent | Harlesden & Kensal Green | NW10 4TS | 442 | 6 | 3 | 0 | |
| 2024-04-06 | Wembley | Brent | Wembley Central | HA9 7BS | 2,123 | 8 | 3 | 0.0009 | |
| 2024-04-09 | Woolwich | Greenwich | Woolwich Arsenal | SE18 7BZ | 8,873 | 9 | 3 | 0 | |
| 2024-04-09 | Woolwich | Greenwich | Woolwich Arsenal | SE18 7BZ | 7,315 | 5 | 5 | 0 | 2nd deployment same location/day |
| 2024-04-16 | Romford | Havering | St Alban's | RM1 1PL | 1,400 | 3 | 2 | 0 | |
| 2024-04-16 | High St, Sutton | Sutton | Sutton Central | SM1 1JG | 756 | 3 | 1 | 0 | |
| 2024-04-18 | North End, Croydon | Croydon | Fairfield | CR0 1UB | 1,330 | 14 | - | 0.0008 | |
| 2024-04-18 | Woolwich | Greenwich | Woolwich Arsenal | SE18 7BZ | 2,299 | 14 | 7 | 0 | |
| 2024-04-23 | Catford | Lewisham | Rushey Green | SE6 2EF | 899 | 11 | 6 | 0 | |
| 2024-04-25 | Woolwich | Greenwich | Woolwich Arsenal | SE18 7BZ | 2,495 | 11 | 5 | 0 | |
| 2024-04-28 | Northumberland Park | Haringey | Northumberland Park | N17 0QU | 1,997 | 1 | - | 0 | |
| 2024-04-28 | Haringey, Love Lane | Haringey | Bruce Castle | N17 8DB | 2,767 | 4 | 1 | 0 | |
| 2024-04-30 | Oxford Circus | Westminster | West End | W1C 1DE | 2,812 | 4 | 4 | 0 | |
| 2024-04-30 | Whitechapel | Tower Hamlets | Whitechapel | E1 1BJ | 1,465 | 4 | 2 | 0 | |
| 2024-05-03 | Tooting Broadway | Wandsworth | Tooting Broadway | SW17 0RN | 2,040 | 12 | 4 | 0.001 | |
| 2024-05-03 | Oxford Circus | Westminster | West End | W1C 1DE | 4,810 | 9 | 5 | 0 | |
| 2024-05-04 | Croydon, Church St | Croydon | Fairfield | CR0 1RH | 1,481 | 7 | 1 | 0 | |
| 2024-05-04 | Lewisham | Lewisham | Lewisham Central | SE13 5JH | 1,275 | 5 | 1 | 0 | |
| 2024-05-11 | Crisp St, Poplar | Tower Hamlets | Lansbury | E14 6GG | 3,492 | 6 | 2 | 0 | Crime Hotspot |
| 2024-05-11 | Bethnal Green Rd | Tower Hamlets | Weavers | E2 0AA | 5,809 | 6 | 4 | 0 | Crime Hotspot |
| 2024-05-12 | High St, Lewisham | Lewisham | Lewisham Central | SE13 6JL | 10,660 | 14 | 5 | 0 | Crime Hotspot |
| 2024-05-12 | Edgware Rd, Westminster | Westminster | Church Street | W2 1ED | 9,595 | 11 | 4 | 0 | Crime Hotspot |
| 2024-05-15 | O2 Arena | Greenwich | Greenwich Peninsula | SE10 0BB | 2,381 | 4 | 3 | 0 | |
| 2024-05-15 | Bethnal Green | Tower Hamlets | Weavers | E2 0AA | 1,160 | 7 | 3 | 0 | |
| 2024-05-17 | Thornton Heath | Croydon | Thornton Heath | CR7 7JG | 762 | 4 | 3 | 0 | |
| 2024-05-17 | O2 Arena | Greenwich | Greenwich Peninsula | SE10 0BB | 1,813 | - | - | 0 | |
| 2024-05-21 | Hounslow | Hounslow | Hounslow Central | TW3 1ES | 769 | 3 | 2 | 0 | Same-day double deployment |
| 2024-05-21 | Hounslow | Hounslow | Hounslow Central | TW3 1ES | 576 | 7 | 4 | 0 | Same-day double deployment |
| 2024-05-23 | Westminster | Westminster | St James's | SW1A 2HQ | 1,638 | 3 | 1 | 0 | Same-day double deployment |
| 2024-05-23 | Westminster | Westminster | St James's | SW1A 2HQ | 1,862 | - | - | 0 | Same-day double deployment |
| 2024-05-29 | Croydon | Croydon | Fairfield | CR0 1UB | 1,023 | 13 | 6 | 0 | |
| 2024-05-29 | Woolwich | Greenwich | Woolwich Arsenal | SE18 7BZ | 1,451 | 12 | 10 | 0 | |
| 2024-06-02 | Croydon, North End | Croydon | Fairfield | CR0 1UB | 1,011 | 9 | 2 | 0.001 | |
| 2024-06-02 | Westminster | Westminster | St James's | SW1A 2HQ | 1,103 | 5 | 3 | 0 | |
| 2024-06-06 | Peckham | Southwark | Rye Lane | SE15 4BQ | 1,717 | 13 | 7 | 0 | Same-day double deployment |
| 2024-06-06 | Peckham | Southwark | Rye Lane | SE15 4BQ | 798 | 6 | 3 | 0.0013 | Same-day double deployment |
| 2024-06-08 | Stratford | Newham | Stratford | E15 1XE | 11,460 | 15 | 7 | 0 | |
| 2024-06-08 | Earls Court | Kensington and Chelsea | Earl's Court | SW5 9QG | 1,562 | 6 | 4 | 0 | |
| 2024-06-09 | Croydon | Croydon | Fairfield | CR0 1UB | 2,175 | 9 | 4 | 0 | |
| 2024-06-09 | Lewisham | Lewisham | Lewisham Central | SE13 5JH | 8,715 | 9 | 3 | 0 | |
| 2024-06-13 | Haringey | Haringey | Bruce Castle | N17 8DB | 1,589 | 7 | 3 | 0 | |
| 2024-06-13 | Enfield | Enfield | Town | EN2 6AA | 680 | 2 | 1 | 0 | |
| 2024-06-19 | Barking | Barking and Dagenham | Northbury | IG11 8EB | 697 | 9 | 5 | 0.0014 | |
| 2024-06-19 | Ilford | Redbridge | Fullwell | IG6 2AH | 1,388 | 10 | 8 | 0.0007 | |
| 2024-06-21 | Haringey | Haringey | Bruce Castle | N17 8DB | 711 | 3 | 1 | 0 | |
| 2024-06-21 | Southwark | Southwark | Borough & Bankside | SE1 1LL | 1,684 | 9 | 5 | 0 | |
| 2024-06-26 | Haringey | Haringey | Bruce Castle | N17 8DB | 1,150 | 14 | 8 | 0.0017 | |
| 2024-06-26 | Peckham | Southwark | Rye Lane | SE15 4BQ | 843 | 9 | 2 | 0 | |
| 2024-06-28 | Brent | Brent | Harlesden & Kensal Green | NW10 4TS | 1,650 | 7 | 2 | 0.0018 | |
| 2024-06-28 | Barnet | Barnet | Underhill | EN5 2ED | 454 | 4 | 3 | 0 | |
| 2024-07-03 | Croydon, Church St | Croydon | Fairfield | CR0 1RH | 1,443 | 12 | 3 | 0 | |
| 2024-07-03 | Bromley | Bromley | Bromley Town | BR1 1DN | 1,766 | 4 | 3 | 0 | |
| 2024-07-11 | Clapham Common | Lambeth | Clapham East | SW4 7AA | 3,910 | 1 | - | 0 | Crime Hotspot |
| 2024-07-11 | High St, Ilford | Redbridge | Fullwell | IG6 2AH | 11,760 | 16 | 10 | 0 | Crime Hotspot |
| 2024-07-13 | Shepherds Bush | Hammersmith and Fulham | Shepherd's Bush Green | W12 8LP | 1,649 | 8 | 4 | 0 | Same-day double deployment |
| 2024-07-13 | Shepherds Bush | Hammersmith and Fulham | Shepherd's Bush Green | W12 8LP | 3,705 | 6 | 4 | 0.0003 | Same-day double deployment |
| 2024-07-16 | Walthamstow | Waltham Forest | William Morris | E17 4PH | 815 | 2 | 2 | 0 | |
| 2024-07-16 | East Ham | Newham | East Ham | E6 1HZ | 419 | 7 | 5 | 0 | |
| 2024-07-18 | Acton | Ealing | South Acton | W3 9BY | 319 | - | - | 0 | |
| 2024-07-18 | Uxbridge | Hillingdon | Uxbridge | UB8 1JZ | 616 | 2 | 1 | 0.0016 | |
| 2024-07-23 | Ilford | Redbridge | Fullwell | IG6 2AH | 1,870 | 8 | 4 | 0.0011 | |
| 2024-07-23 | Romford | Havering | St Alban's | RM1 1PL | 5,500 | 5 | 4 | 0 | |
| 2024-07-25 | Dagenham | Barking and Dagenham | Goresbrook | RM9 5AN | 12,480 | 5 | 3 | 0 | |
| 2024-07-25 | Westminster | Westminster | St James's | SW1A 2HQ | 1,292 | 9 | 3 | 0 | |
| 2024-07-31 | Hammersmith | Hammersmith and Fulham | Hammersmith Broadway | W6 0DZ | 1,448 | 2 | - | 0 | |
| 2024-07-31 | Hounslow | Hounslow | Hounslow Central | TW3 1ES | 2,367 | 2 | 1 | 0 | |
| 2024-08-05 | Southall | Ealing | Southall Broadway | UB2 4AA | 1,324 | 3 | 1 | 0.0008 | |
| 2024-08-05 | Hounslow | Hounslow | Hounslow Central | TW3 1ES | 1,954 | 2 | 1 | 0 | |
| 2024-08-20 | Catford | Lewisham | Rushey Green | SE6 2EF | 1,606 | 7 | 2 | 0 | |
| 2024-08-20 | Bexleyheath | Bexley | Bexleyheath | DA6 7BD | 9,500 | 7 | 3 | 0 | |
| 2024-08-22 | Westminster | Westminster | St James's | SW1A 2HQ | 2,864 | 2 | 2 | 0 | Multi-deployment day (4 ops) |
| 2024-08-22 | Westminster | Westminster | St James's | SW1A 2HQ | 3,233 | 2 | 2 | 0 | Multi-deployment day (4 ops) |
| 2024-08-22 | Westminster | Westminster | St James's | SW1A 2HQ | 14,210 | 6 | 3 | 0 | Multi-deployment day (4 ops) |
| 2024-08-22 | Westminster | Westminster | St James's | SW1A 2HQ | 3,657 | - | - | 0 | Multi-deployment day (4 ops) |
| 2024-08-28 | Croydon | Croydon | Fairfield | CR0 1UB | 10,455 | 8 | 3 | 0 | |
| 2024-08-28 | Westminster | Westminster | St James's | SW1A 2HQ | 8,325 | 2 | 2 | 0 | |
| 2024-08-30 | Croydon | Croydon | Fairfield | CR0 1UB | 13,755 | 12 | 6 | 0 | Multi-deployment day (3 ops) |
| 2024-08-30 | Westminster | Westminster | St James's | SW1A 2HQ | 2,655 | 3 | - | 0 | Multi-deployment day (3 ops) |
| 2024-08-30 | Westminster | Westminster | St James's | SW1A 2HQ | 2,235 | - | - | 0 | Multi-deployment day (3 ops) |
| 2024-09-02 | Croydon, George St | Croydon | Fairfield | CR0 1PE | 3,149 | 5 | 3 | 0 | |
| 2024-09-02 | Croydon, North End | Croydon | Fairfield | CR0 1UB | 1,950 | 13 | 8 | 0 | |
| 2024-09-04 | Woolwich | Greenwich | Woolwich Arsenal | SE18 7BZ | 1,446 | 11 | 6 | 0.0007 | |
| 2024-09-04 | High St, Sutton | Sutton | Sutton Central | SM1 1JG | 793 | 6 | 5 | 0 | |
| 2024-09-10 | Broadway, Stratford | Newham | Stratford | E15 1XE | 9,870 | 19 | 9 | 0 | Crime Hotspot |
| 2024-09-10 | Kings St, Hammersmith | Hammersmith and Fulham | Hammersmith Broadway | W6 9JT | 11,900 | 8 | 6 | 0 | Crime Hotspot |
| 2024-09-17 | Brigstock Rd, Thornton Heath | Croydon | Bensham Manor | CR7 7JL | 2,695 | 5 | 3 | 0 | Crime Hotspot |
| 2024-09-17 | Coventry St, Piccadilly | Westminster | St James's | W1J 9HR | 14,245 | 2 | 1 | 0 | Crime Hotspot |
| 2024-09-19 | George St, Croydon | Croydon | Fairfield | CR0 1PE | 9,375 | 12 | 6 | 0 | Crime Hotspot |
| 2024-09-19 | High St, Sutton | Sutton | Sutton Central | SM1 1JG | 7,925 | 9 | 1 | 0 | Crime Hotspot |
| 2024-09-24 | Walthamstow | Waltham Forest | William Morris | E17 4PH | 5,565 | 5 | 3 | 0 | Crime Hotspot |
| 2024-09-24 | Tooting Broadway | Wandsworth | Tooting Broadway | SW17 0RN | 11,105 | 12 | 3 | 0 | Crime Hotspot |
| 2024-09-26 | St John's Hill, Clapham Junction | Wandsworth | Falconbrook | SW11 1SA | 11,065 | 5 | 1 | 0 | Crime Hotspot |
| 2024-09-26 | St Ann's, Harrow | Harrow | Marlborough | HA1 1ST | 4,970 | 6 | 2 | 0 | Crime Hotspot |
| 2024-10-01 | Westminster | Westminster | St James's | SW1A 2HQ | 14,280 | 1 | 1 | 0 | |
| 2024-10-05 | Tooting | Wandsworth | Tooting Broadway | SW17 0RN | 1,543 | 10 | 4 | 0 | |
| 2024-10-05 | Kingston | Kingston | Kingston Town | KT1 1SW | 2,008 | 10 | 3 | 0.0005 | |
| 2024-10-09 | Croydon | Croydon | Fairfield | CR0 1UB | 9,985 | 10 | 3 | 0 | |
| 2024-10-09 | Westminster | Westminster | St James's | SW1A 2HQ | 12,705 | 5 | 3 | 0 | |
| 2024-10-12 | Hammersmith Broadway | Hammersmith and Fulham | Brook Green | W6 7AN | 16,645 | 4 | 1 | 0 | Crime Hotspot |
| 2024-10-12 | Camden High Rd | Camden | Regent's Park | NW1 7JY | 1,225 | 2 | 1 | 0 | Crime Hotspot |
| 2024-10-16 | High St, East Ham | Newham | East Ham | E6 1HZ | 9,261 | 10 | 7 | 0 | Crime Hotspot |
| 2024-10-16 | St Ann's, Harrow | Harrow | Marlborough | HA1 1ST | 9,375 | 3 | - | 0 | Crime Hotspot |
| 2024-10-17 | Broadway, Stratford | Newham | Stratford | E15 1XE | 14,030 | 10 | 6 | 0 | Crime Hotspot |
| 2024-10-17 | Westfield, Stratford | Newham | Stratford Olympic Park | E20 1EJ | 13,800 | 10 | 6 | 0 | Crime Hotspot |
| 2024-10-22 | Stn Parade, Barking | Barking and Dagenham | Northbury | IG11 8RU | 8,650 | 9 | 7 | 0 | Crime Hotspot |
| 2024-10-22 | High St, Uxbridge | Hillingdon | Uxbridge | UB8 1JZ | 14,694 | 3 | 1 | 0 | Crime Hotspot |
| 2024-10-24 | Seven Sisters High Rd | Haringey | Seven Sisters | N15 5BT | 7,793 | 9 | 2 | 0 | Crime Hotspot |
| 2024-10-24 | Belvedere Rd, Waterloo | Lambeth | Waterloo & South Bank | SE1 7GQ | 10,520 | - | - | 0 | Crime Hotspot |
| 2024-10-30 | High St, Hounslow | Hounslow | Hounslow Central | TW3 1ES | 11,120 | 3 | 2 | 0 | Crime Hotspot |
| 2024-10-30 | Ealing Broadway | Ealing | Ealing Broadway | W5 5JN | 10,780 | 5 | 2 | 0 | Crime Hotspot |
| 2024-11-06 | Barking | Barking and Dagenham | Northbury | IG11 8EB | 1,310 | 8 | 3 | 0 | |
| 2024-11-06 | Dagenham | Barking and Dagenham | Goresbrook | RM9 5AN | 1,461 | 9 | 6 | 0 | |
| 2024-11-07 | Hackney | Hackney | Hackney Central | E8 1PE | 1,094 | 6 | 4 | 0 | |
| 2024-11-07 | Dalston | Hackney | De Beauvoir | E8 4AR | 602 | 10 | 3 | 0 | |
| 2024-11-10 | Tooting Broadway | Wandsworth | Tooting Broadway | SW17 0RN | 19,090 | 8 | 2 | 0 | Crime Hotspot |
| 2024-11-10 | Earls Ct Rd, Earls Court | Kensington and Chelsea | Earl's Court | SW5 9QG | 5,895 | - | 1 | 0 | Crime Hotspot |
| 2024-11-13 | North End, Croydon | Croydon | Fairfield | CR0 1UB | 12,820 | 24 | 11 | 0 | Crime Hotspot |
| 2024-11-13 | High Rd, Wood Green | Haringey | Noel Park | N22 6EB | 9,395 | 12 | 9 | 0 | Crime Hotspot |
| 2024-11-15 | Stn Parade, Barking | Barking and Dagenham | Northbury | IG11 8RU | 11,883 | 8 | 3 | 0 | Crime Hotspot |
| 2024-11-15 | Heathway, Dagenham | Barking and Dagenham | Goresbrook | RM10 8RE | 9,147 | 2 | 1 | 0 | Crime Hotspot |
| 2024-11-19 | South St, Romford | Havering | St Alban's | RM1 1TR | 8,927 | 8 | 4 | 0 | Crime Hotspot |
| 2024-11-19 | Palace Exchange, Enfield | Enfield | Town | EN2 6SN | 5,475 | 2 | 1 | 0 | Crime Hotspot |
| 2024-11-21 | Walworth Rd | Southwark | North Walworth | SE17 1JE | 7,230 | 8 | 4 | 0 | Crime Hotspot |
| 2024-11-21 | High St, Ilford | Redbridge | Fullwell | IG6 2AH | 9,717 | 11 | 6 | 0 | Crime Hotspot |
| 2024-11-27 | Mare St, Hackney | Hackney | Hackney Central | E8 1HY | 3,096 | 3 | 2 | 0 | Crime Hotspot |
| 2024-11-27 | North End, Croydon | Croydon | Fairfield | CR0 1UB | 9,635 | 10 | 3 | 0 | Crime Hotspot |
| 2024-11-29 | Westfield, Shepherds Bush | Hammersmith and Fulham | Shepherd's Bush Green | W12 7GB | 39,111 | 18 | 7 | 0 | Crime Hotspot — highest 2024 face count |
| 2024-11-29 | Kings Cross | Camden | King's Cross | N1C 4TB | 13,365 | 4 | 1 | 0 | Crime Hotspot |
| 2024-12-03 | Croydon, North End | Croydon | Fairfield | CR0 1UB | 1,336 | 15 | 3 | 0 | |
| 2024-12-03 | Tooting Broadway | Wandsworth | Tooting Broadway | SW17 0RN | 2,047 | 11 | 3 | 0.0005 | |
| 2024-12-04 | Thornton Heath | Croydon | Thornton Heath | CR7 7JG | 1,068 | 8 | 5 | 0 | |
| 2024-12-04 | Ealing Broadway | Ealing | Ealing Broadway | W5 5JN | 3,064 | 6 | 2 | 0 | |
| 2024-12-12 | North End, Croydon | Croydon | Fairfield | CR0 1UB | 15,105 | 11 | 6 | 0 | Crime Hotspot |
| 2024-12-12 | Powis St, Woolwich | Greenwich | Woolwich Arsenal | SE18 6LQ | 8,940 | 10 | 3 | 0 | Crime Hotspot |
| 2024-12-18 | Uxbridge Rd, Shepherds Bush | Hammersmith and Fulham | Shepherd's Bush Green | W12 8LR | 11,560 | 12 | 5 | 0 | Crime Hotspot |
| 2024-12-18 | Kingsland High St | Hackney | Dalston | E8 2PB | 10,668 | 14 | 7 | 0 | Crime Hotspot |
| 2024-12-20 | Rushey Green, Catford | Lewisham | Rushey Green | SE6 4HW | 5,180 | 3 | 1 | 0 | Crime Hotspot |
| 2024-12-20 | George St, Croydon | Croydon | Fairfield | CR0 1PE | 8,250 | 7 | 4 | 0 | Crime Hotspot |

### 2025 — 40 records (OVERLAP with 2025 PDF; key added value = ward codes + postcodes)

These 40 records correspond to Jan–Mar 2025 deployments already captured in the 2025 PDF source section. The Excel adds postcode (approx) and ward code (ONS) data that the PDF does not contain. See "Garbett enrichment" note.

| Date | Location | Borough | Ward | Postcode | Ward Code | Faces | Arrests | FA Rate |
|------|----------|---------|------|----------|-----------|-------|---------|---------|
| 2025-01-08 | High St North, East Ham | Newham | East Ham | E6 1HZ | E05013909 | 9,780 | 4 | 0 |
| 2025-01-08 | Green St, Newham | Newham | Green Street West | E7 8LE | E05013914 | 8,480 | 3 | 0 |
| 2025-01-10 | Camberwell Green | Southwark | St Giles | SE5 7AN | E05011115 | 3,975 | 3 | 0 |
| 2025-01-10 | Powis St, Woolwich | Greenwich | Woolwich Arsenal | SE18 6HQ | E05014092 | 15,480 | 5 | 0 |
| 2025-01-14 | Rye Lane, Peckham | Southwark | Rye Lane | SE15 5DW | E05011113 | 10,245 | 4 | 0 |
| 2025-01-14 | Wembley Central | Brent | Wembley Central | HA9 7AJ | E05013514 | 13,950 | 7 | 0 |
| 2025-01-16 | Streatham High Rd | Lambeth | Streatham Wells | SW16 1PS | E05014116 | 3,890 | 2 | 0 |
| 2025-01-16 | Stratford Broadway | Newham | Stratford | E15 1XE | E05013924 | 25,335 | 11 | 0 |
| 2025-01-22 | Walworth Rd | Southwark | North Walworth | SE17 1JE | E05011107 | 5,200 | 1 | 0 |
| 2025-01-22 | Town Sq, Walthamstow | Waltham Forest | High Street | E17 7JN | E05013891 | 12,120 | 6 | 0.00008 |
| 2025-01-24 | Powis St, Woolwich | Greenwich | Woolwich Arsenal | SE18 6HQ | E05014092 | 15,711 | 6 | 0 |
| 2025-01-24 | High St North, East Ham | Newham | East Ham | E6 1HZ | E05013909 | 17,265 | 4 | 0 |
| 2025-01-28 | Kilburn High Rd | Camden | Kilburn | NW6 7JR | E05013503 | 9,581 | 9 | 0 |
| 2025-01-28 | Wembley Central | Brent | Wembley Central | HA9 7AJ | E05013514 | 9,990 | 6 | 0 |
| 2025-01-30 | Leyton | Waltham Forest | Leyton | E10 5NH | E05013896 | 5,645 | - | 0 |
| 2025-01-30 | Stratford Broadway | Newham | Stratford | E15 1XE | E05013924 | 21,050 | 3 | 0 |
| 2025-02-13 | Barking | Barking and Dagenham | Northbury | IG11 8EB | E05014066 | 13,695 | 10 | 0 |
| 2025-02-13 | Oxford St | Westminster | West End | W1C 2DZ | E05013808 | 29,025 | 6 | 0 |
| 2025-02-19 | Hammersmith Broadway | Hammersmith and Fulham | Brook Green | W6 7AN | E05013735 | 21,940 | 4 | 0 |
| 2025-02-19 | Clarence St, Kingston | Kingston | Kingston Town | KT1 1NX | E05013938 | 17,850 | 3 | 0 |
| 2025-02-21 | Westfield, Shepherds Bush | Hammersmith and Fulham | Shepherd's Bush Green | W12 7GB | E05013748 | 30,305 | 5 | 0 |
| 2025-02-21 | High St, Ilford | Redbridge | Fullwell | IG6 2AH | E05011243 | 16,485 | 7 | 0 |
| 2025-02-25 | Tooting Broadway | Wandsworth | Tooting Broadway | SW17 0RN | E05014024 | 16,380 | 3 | 0 |
| 2025-02-25 | Oxford Circus | Westminster | West End | W1C 1DE | E05013808 | 32,160 | 5 | 0 |
| 2025-02-27 | North End, Croydon | Croydon | Fairfield | CR0 1UB | E05011468 | 24,365 | 8 | 0.00004 |
| 2025-02-27 | South St, Romford | Havering | St Alban's | RM1 1TR | E05013981 | 14,160 | 5 | 0 |
| 2025-03-05 | Deptford High St | Lewisham | Deptford | SE8 4NS | E05013719 | 8,440 | 3 | 0 |
| 2025-03-05 | West Croydon | Croydon | Fairfield | CR0 2RD | E05011468 | 15,875 | 7 | 0 |
| 2025-03-07 | Wood Green | Haringey | Noel Park | N22 6EB | E05013595 | 15,315 | 7 | 0 |
| 2025-03-07 | High St, Hounslow | Hounslow | Hounslow Central | TW3 1ES | E05013620 | 21,810 | 1 | 0 |
| 2025-03-11 | Edmonton Green | Enfield | Edmonton Green | N9 0TR | E05013679 | 10,260 | 2 | 0 |
| 2025-03-11 | Dalston Kingsland | Hackney | Dalston | E8 2PB | E05009370 | 13,210 | 5 | 0 |
| 2025-03-13 | Lewisham High St | Lewisham | Lewisham Central | SE13 6JL | E05013727 | 11,080 | 8 | 0 |
| 2025-03-13 | Ealing Broadway | Ealing | Ealing Broadway | W5 5JN | E05013520 | 19,320 | 4 | 0.00005 |
| 2025-04-02 | South St, Romford | Havering | St Alban's | RM1 1TR | E05013981 | 13,110 | 5 | 0 |
| 2025-04-02 | Clapham Junction | Wandsworth | Lavender | SW11 1PW | E05014014 | 10,625 | 2 | 0 |
| 2025-06-02 | Dagenham Heathway | Barking and Dagenham | Goresbrook | RM10 8RE | E05014062 | 12,660 | 3 | 0.00008 |
| 2025-06-02 | High St, Ilford | Redbridge | Fullwell | IG6 2AH | E05011243 | 19,733 | 3 | 0 |
| 2025-11-02 | Shepherds Bush Green | Hammersmith and Fulham | Addison | W12 8PY | E05013733 | 17,310 | 4 | 0 |
| 2025-11-02 | High St, Sutton | Sutton | Sutton Central | SM1 1JG | E05013765 | 14,430 | 2 | 0 |

**Gaps/uncertainties:**
- Use case not consistently recorded in Excel pre-Sept 2024 (assumed Crime Hotspot for all based on programme context; exceptions: Selhurst Park 21/12/23 = likely Event PSO for Crystal Palace football match; Westminster 05/06/23 multi-point = possibly Event PSO)
- All 2020/2022 records = overlap with lfr-001 through lfr-005 in met-police-lfr.json; Excel adds ward/postcode data not in JSON
- Date parsing from Excel: datetime objects parsed unambiguously; string dates in DD/MM/YYYY format converted to ISO
- Some rows lack total alerts breakdown (true/false split absent for early 2024 rows); FA rate derived from Met column
- 2025 dates in Excel (e.g. "2025-08-01") may reflect Excel date serial ambiguity — compare with 2025 PDF for verification
- Ward codes are ONS 2021 edition (E05...) — these are the granularity needed for map component geospatial joins

---

## Source: lfr-deployment-grid-2023-to-2024.pdf

**Path:** Deployment Data/ and NEC & Met Files/ (identical copies)
**Pages read:** 1–9 (page 10 blank) | **Records found:** 203 (23 × 2023 + 180 × 2024)
**Authoritative MPS source** — this is the raw deployment grid. The Garbett Excel is Garbett's enriched derivative of this document.

**Key structural observations:**
- 2023 records (pages 1–2 partial): LFR Purpose listed as references 1,2,3,4 (standard Crime Hotspot battery); threshold 0.60 throughout
- 2024 records: threshold transitions — 0.60 (Jan–Jun 2024) → 0.62 (from 11 Jul 2024: Hackney/Dalston entries) → 0.64 (from 25 Jul 2024: Dagenham/Westminster entries onwards)
- From September 2024 (page 6): Use Case column added explicitly, all labelled "Crime Hotspot"
- Duration column present throughout (not in PDFs previously processed)

**Data quality notes vs Excel:**
- **Dalston date anomaly**: PDF page 4 lists "Dalston 11/07/23" — but watchlist 15,695 and threshold 0.62 confirm this is 11/07/24 (typo in PDF — Excel correctly shows 11/07/24)
- **Camden High Rd date/face discrepancy**: PDF shows "Camden High Rd 10/12/24, faces 12,225" but Excel parsed this as Oct-12 with faces 1,225. PDF is authoritative — correct date is 10 December 2024, correct face count is 12,225 (Excel has date-format and possible transcription errors for this record)
- This PDF confirms the Excel data is essentially accurate except for the above two anomalies

**Overlap with other sources:** All 203 records here are already captured in the Garbett Excel section above. The PDF adds: duration data, exact threshold progression, full alert split (TC/TU/FC/FU — identical to what Excel shows). No net new deployment records vs Excel. Key value: authoritative MPS source confirmation and threshold timeline.

**Threshold progression timeline (significant for project context):**
- 0.60 → all 2023 deployments + Jan–Jun 2024
- 0.62 → from 11 Jul 2024 (Hackney/Dalston)  
- 0.64 → from 25 Jul 2024 (Dagenham/Westminster) — this is the value seen in all 2025 and 2026 PDFs

**No table reproduced here** — data identical to Garbett Excel section above. For duration data, refer to PDF directly.

---

## Source: lfr-deployment-grid-2020-2022.pdf

**Path:** Deployment Data/ and NEC & Met Files/ (identical copies; `lfr-deployment-grid-2020-2022 (1).pdf` in NEC & Met Files/ is also a duplicate)
**Pages read:** 1–2 | **Records found:** 9 (3 × 2020, 6 × 2022; one 2020 record has N/A data)

All 9 records are already captured in `met-police-lfr.json` (lfr-001 through lfr-007 era). This source confirms existing JSON data and provides the authoritative column structure for early-era deployments.

**Column structure (differs from later PDFs):**
- No "Duration" column  
- "Purpose Reference" (not "LFR Use Case")  
- "False Alert / Confirmed False Alerts" + "False Alert Rate" in separate columns  
- "True Alerts" + "Engagements" + "Arrests/Disposals" (combined)

**Date note — Stratford entry:** PDF says "11/02/20" (DD/MM/YY) = 11 February 2020. The Garbett Excel parsed this as 2020-11-02 (2 November 2020) — a MM/DD swap error in the Excel. PDF is authoritative.

**Purpose references (2020-2022 era):**
- 1 = Targeting violent and serious crime
- 2 = Outstanding warrants
- 3 = Equitability study (applies to Jul-Aug 2022 Oxford Circus deployments only)

| Date | Location | Borough | Faces | Total Alerts | True Alerts | FA Rate | Arrests | Watchlist | Notes |
|------|----------|---------|-------|-------------|-------------|---------|---------|-----------|-------|
| 2020-02-11 | Stratford | Newham | 4,600 | 0 | 0 | 0.00% | 0 | 5,816 | Refs 1,2 |
| 2020-02-21 | Oxford Circus | Westminster | N/A | N/A | N/A | N/A | N/A | 7,316 | Technical fault stopped deployment |
| 2020-02-27 | Oxford Circus | Westminster | 8,600 | 8 | 1 | 0.08% | 1 | 7,292 | Refs 1,2 |
| 2022-01-28 | Oxford Circus | Westminster | 12,120 | 11 | 10 | 0.008% | 4 | 9,756 | Refs 1,2 |
| 2022-03-10 | Leicester Square | Westminster | 10,740 | 0 | 0 | 0.00% | 0 | 6,793 | Refs 1,2 |
| 2022-07-07 | Oxford Circus | Westminster | 34,286 | 4 | 4 | 0.00% | 3 | 6,699 | Refs 1,2,3 (equitability study) |
| 2022-07-14 | Oxford Circus | Westminster | 34,360 | 3 | 2 | 0.003% | 1 | 6,713 | Refs 1,2,3 |
| 2022-07-16 | Oxford Circus | Westminster | 36,420 | 1 | 0 | 0.003% | 0 | 6,747 | Refs 1,2,3 |
| 2022-07-28 | Piccadilly Circus | Westminster | 16,440 | 1 | 1 | 0.00% | 0 | 6,858 | Refs 1,2,3 |

**Gaps/uncertainties:** Leicester Square entry date is 10/03/22 = 10 March 2022 (not to be confused with 3 October). Oxford Circus 21/02/20 fully aborted — no face data. Column naming differs enough from 2023+ PDFs that alert split columns (TC/TU/FC/FU) are not separately distinguished in this document.

---

## Source: lfr-deployment-grid-2025-up-to-May20-.pdf

**Path:** Deployment Data/ only (not duplicated in NEC & Met Files/)
**Pages read:** 1–4 (page 4 contains last records + purpose refs) | **Records found:** 66
**Date range:** 08/01/25 – 10/05/25

This is an earlier release of the 2025 deployment data, covering only Jan–May 10, 2025. All 66 records overlap with the Jan–May portion of `live-facial-recognition-deployment-record-2025.pdf` (already extracted above). The main 2025 PDF is authoritative as the complete year record.

**Key observations vs 2025 main PDF:**
- Duration data present in both
- **Watchlist anomaly:** Bond St Stn 02/05/25 shows watchlist 19,199 — anomalous vs surrounding records (~16,200). Main 2025 PDF should be checked for the correct value; may be a typo for 16,199
- **Station Lane, Hornchurch (08/05/25):** Havering borough — new location not seen in 2022-2024 data. 4,895 faces, 3 alerts (all TC), 0 arrests. Verify this appears in the main 2025 PDF extraction
- All records are "Crime Hotspot" use case, threshold 0.64 throughout

**No full table reproduced** — data subset of 2025 deployment record PDF already extracted above. Notable additional records vs data already captured:

| Date | Location | Borough | Faces | Alerts | Arrests | Notes |
|------|----------|---------|-------|--------|---------|-------|
| 2025-03-19 | Seven Sisters Rd | Haringey | 7,695 | 10 | 5 | Verify vs main 2025 PDF |
| 2025-03-19 | High St North, East Ham | Newham | 12,083 | 9 | 3 | Verify vs main 2025 PDF |
| 2025-04-01 | High St, Bromley | Bromley | 11,835 | 8 | 3 | Verify vs main 2025 PDF |
| 2025-04-01 | High St, Camden | Camden | 12,915 | 6 | 1 | Verify vs main 2025 PDF |
| 2025-04-11 | Walthamstow Central | Waltham Forest | 19,240 | 20 | 7 | Verify vs main 2025 PDF |
| 2025-04-11 | Kings Cross | Camden | 8,385 | 6 | 4 | Verify vs main 2025 PDF |
| 2025-04-22 | George St, Croydon | Croydon | 8,030 | 9 | 3 | Verify vs main 2025 PDF |
| 2025-04-22 | Walthamstow Central | Waltham Forest | 17,755 | 18 | 10 | Verify vs main 2025 PDF |
| 2025-04-30 | Westfield, Stratford | Newham | 39,855 | 18 | 5 | Verify vs main 2025 PDF |
| 2025-05-02 | London Rd, Croydon | Croydon | 12,210 | 22 | 6 | Verify vs main 2025 PDF |
| 2025-05-02 | Bond St Stn | Westminster | 30,855 | 7 | 5 | Watchlist listed as 19,199 (anomaly) |
| 2025-05-06 | Mare St, Hackney | Hackney | 2,490 | 9 | 4 | Verify vs main 2025 PDF |
| 2025-05-06 | Shepherds Bush Green | H&F | 18,050 | 6 | 2 | Verify vs main 2025 PDF |
| 2025-05-08 | Powis St, Woolwich | Greenwich | 17,310 | 10 | 3 | Verify vs main 2025 PDF |
| 2025-05-08 | Station Lane, Hornchurch | Havering | 4,895 | 3 | 0 | New location for Havering; verify |
| 2025-05-10 | High Street, Ilford | Redbridge | 17,665 | 10 | 3 | Verify vs main 2025 PDF |
| 2025-05-10 | Barking | Barking and Dagenham | 15,001 | 10 | 6 | Verify vs main 2025 PDF |

---

## Source: live-facial-recognition-deployment-record-2026.pdf
Pages read: 1–5 | Records found: **95** (Jan–17 Apr 2026, partial year) | Operator: Metropolitan Police | Source type: official MPS deployment record

Watchlist: 16,834–18,800 (grown from ~16,000 in early 2025). Threshold still 0.64 throughout.

### January 2026 (21 deployments)

| Date | Location | Borough | Use Case | Faces | Alerts | Arrests | FA Rate | Notes |
|------|----------|---------|----------|-------|--------|---------|---------|-------|
| 06/01/26 | High St, Ilford | Redbridge | Crime Hotspot | 18,285 | 12 | 7 | 0% | |
| 06/01/26 | St Ann's, Harrow | Harrow | Crime Hotspot | 15,810 | 11 | 4 | 0% | |
| 08/01/26 | High St, Harlesden | Brent | Crime Hotspot | 5,940 | 2 | 1 | 0% | |
| 08/01/26 | King St, Hammersmith | H&F | Crime Hotspot | 20,955 | 8 | 3 | 0% | 1 true alert unconfirmed |
| 09/01/26 | North End, Croydon | Croydon | Crime Hotspot | 7,720 | 9 | 6 | 0.01% | 1 false alert confirmed |
| 13/01/26 | Bruce Grove, High Rd, Tottenham | Haringey | Crime Hotspot | 6,690 | 5 | 3 | 0% | |
| 13/01/26 | Victoria St, Victoria | Westminster | Crime Hotspot | 14,385 | 13 | 7 | 0% | |
| 15/01/26 | Edgware Road, J/W Penfold Pl | Westminster | Crime Hotspot | 5,055 | 9 | 6 | 0% | |
| 15/01/26 | Wembley Central Stn | Brent | Crime Hotspot | 11,230 | 3 | 0 | 0% | |
| 16/01/26 | North End, Croydon | Croydon | Crime Hotspot | 21,270 | 17 | 13 | 0% | |
| 20/01/26 | High Road, Kilburn | Brent | Crime Hotspot | 4,365 | 8 | 7 | 0% | |
| 20/01/26 | High Road, Wood Green | Haringey | Crime Hotspot | 21,660 | 14 | 9 | 0% | |
| 22/01/26 | North End, Croydon | Croydon | Crime Hotspot | 24,253 | 12 | 6 | 0% | |
| 23/01/26 | South St, Romford | Havering | Crime Hotspot | 14,520 | 12 | 5 | 0% | |
| 23/01/26 | Edmonton Green, Shopping Centre | Enfield | Crime Hotspot | 24,180 | 8 | 5 | 0% | |
| 27/01/26 | Station Parade, Barking | Barking & Dagenham | Crime Hotspot | 16,935 | 10 | 5 | 0.006% | 1 false alert confirmed |
| 27/01/26 | Hatton Gdn, Greville St | Islington | Crime Hotspot | 11,310 | 6 | 3 | 0% | |
| 28/01/26 | North End, Croydon | Croydon | Crime Hotspot | 20,801 | 14 | 7 | 0% | |
| 29/01/26 | Dagenham Heathway | Barking & Dagenham | Crime Hotspot | 10,305 | 1 | 0 | 0% | |
| 29/01/26 | Finsbury Pk Stn, J/W Seven Sisters Rd | Islington | Crime Hotspot | 9,885 | 15 | 9 | 0% | |
| 30/01/26 | North End, Croydon | Croydon | Crime Hotspot | 21,097 | 11 | 6 | 0% | |

### February 2026 (22 deployments including Haringey Event PSO)

| Date | Location | Borough | Use Case | Faces | Alerts | Arrests | FA Rate | Notes |
|------|----------|---------|----------|-------|--------|---------|---------|-------|
| 03/02/26 | High Street, Acton | Ealing | Crime Hotspot | 5,160 | 4 | 2 | 0% | |
| 03/02/26 | Rye Lane, Peckham | Southwark | Crime Hotspot | 8,367 | 9 | 5 | 0% | |
| 05/02/26 | Streatham High Road | Lambeth | Crime Hotspot | 7,215 | 7 | 3 | 0% | |
| 05/02/26 | East Ham, High St North, O/S Lidl | Newham | Crime Hotspot | 10,875 | 9 | 8 | 0% | |
| 06/02/26 | North End, Croydon | Croydon | Crime Hotspot | 18,604 | 11 | 8 | 0% | |
| 06/02/26 | Villiers Street, Westminster | Westminster | Crime Hotspot | 25,485 | 11 | 5 | 0% | 1 true alert unconfirmed |
| 10/02/26 | Dalston Kingsland Stn | Hackney | Crime Hotspot | 25,149 | 12 | 6 | 0% | |
| 10/02/26 | Walthamstow High Rd Town Sq | Waltham Forest | Crime Hotspot | 11,655 | 13 | 9 | 0% | |
| 11/02/26 | North End, Croydon | Croydon | Crime Hotspot | 32,962 | 11 | 9 | 0% | |
| 11/02/26 | Canning Town, Silvertown Way | Newham | Crime Hotspot | 9,345 | 5 | 4 | 0% | |
| 12/02/26 | Oxford Circus, J/W Argyll St | Westminster | Crime Hotspot | 41,000 | 9 | 2 | 0% | |
| 12/02/26 | Walworth Rd, J/W Wast St | Southwark | Crime Hotspot | 10,481 | 6 | 0 | 0% | |
| 17/02/26 | Shepherds Bush, Uxbridge Rd | H&F | Crime Hotspot | 22,260 | 9 | 3 | 0% | |
| 17/02/26 | Westfields, Stratford | Newham | Crime Hotspot | 42,870 | 11 | 5 | 0% | |
| 19/02/26 | Mare St, Hackney | Hackney | Crime Hotspot | 16,905 | 10 | 5 | 0% | |
| 20/02/26 | Green Street j/w Harold Rd, Newham | Newham | Crime Hotspot | 21,285 | 9 | 7 | 0% | |
| 20/02/26 | Bethnal Green, Op Jersey St | Tower Hamlets | Crime Hotspot | 10,200 | 13 | 5 | 0% | |
| 22/02/26 | Love Lane, Haringey | Haringey | **Event PSO** | 15,492 | 1 | 1 | 0% | **Tottenham Hotspur match** — Spurs stadium on High Rd |
| 22/02/26 | High Rd, Haringey | Haringey | **Event PSO** | 17,840 | 5 | 2 | 0% | Tottenham Hotspur match |
| 23/02/26 | Edgware Road, J/W Penfold Pl | Westminster | Crime Hotspot | 10,215 | 8 | 6 | 0% | 1 true alert unconfirmed |
| 23/02/26 | Ealing Broadway Stn | Ealing | Crime Hotspot | 17,325 | 7 | 1 | 0% | |
| 25/02/26 | Whitechapel Rd | Tower Hamlets | Crime Hotspot | 19,965 | 11 | 5 | 0% | |
| 25/02/26 | Hounslow High St | Hounslow | Crime Hotspot | 22,210 | 14 | 5 | 0% | |
| 27/02/26 | Brixton Road, Brixton | Lambeth | Crime Hotspot | 41,202 | 25 | 12 | 0% | 1 true alert unconfirmed — high volume |
| 27/02/26 | Tottenham Court Road | Camden | Crime Hotspot | 34,608 | 13 | 4 | 0% | 2 true alerts unconfirmed |
| 28/02/26 | North End, Croydon | Croydon | Crime Hotspot | 41,392 | 23 | 7 | 0% | 2 true alerts unconfirmed — high volume |

### March 2026 (22 deployments)

| Date | Location | Borough | Use Case | Faces | Alerts | Arrests | FA Rate | Notes |
|------|----------|---------|----------|-------|--------|---------|---------|-------|
| 02/03/26 | Lewisham High St, Gate Clock | Lewisham | Crime Hotspot | 18,014 | 19 | 7 | 0% | |
| 03/03/26 | King St, Hammersmith | H&F | Crime Hotspot | 17,661 | 13 | 7 | 0.005% | 1 false alert confirmed |
| 04/03/26 | Romford, South St | Havering | Crime Hotspot | 13,183 | 7 | 3 | 0% | |
| 04/03/26 | Edmonton Green o/s Lidl | Enfield | Crime Hotspot | 21,283 | 13 | 5 | 0% | |
| 05/03/26 | Richmond O/S Station | Richmond | Crime Hotspot | 12,226 | 3 | 0 | 0% | |
| 06/03/26 | North End, Croydon | Croydon | Crime Hotspot | 13,811 | 10 | 6 | 0% | |
| 06/03/26 | Kingston, Clarence St | Kingston | Crime Hotspot | 15,269 | 7 | 1 | 0% | |
| 09/03/26 | Catford, Rushey Green j/w Brownhill Rd | Lewisham | Crime Hotspot | 8,954 | 7 | 4 | 0% | |
| 09/03/26 | Marble Arch, j/w Oxford St | Westminster | Crime Hotspot | 22,462 | 8 | 6 | 0% | |
| 10/03/26 | Bromley High Street j/w Elmfield Road | Bromley | Crime Hotspot | 17,674 | 8 | 2 | 0% | |
| 10/03/26 | Clapham Junc, St John's Hill | Wandsworth | Crime Hotspot | 17,985 | 12 | 5 | 0% | 1 true alert unconfirmed |
| 11/03/26 | North End, Croydon | Croydon | Crime Hotspot | 17,231 | 14 | 6 | 0% | 1 true alert unconfirmed |
| 12/03/26 | Thornton Heath, High St/Brigstock Rd | Croydon | Crime Hotspot | 5,541 | 3 | 0 | 0% | 1 true alert unconfirmed |
| 12/03/26 | Bruce Grove, o/s Asda | Haringey | Crime Hotspot | 8,654 | 12 | 4 | 0% | |
| 17/03/26 | Morden, London Road | Merton | Crime Hotspot | 13,440 | 5 | 2 | 0% | |
| 17/03/26 | Broadway, Bexley | Bexley | Crime Hotspot | 4,882 | 7 | 0 | 0% | |
| 18/03/26 | North End, Croydon | Croydon | Crime Hotspot | 23,129 | 12 | 6 | 0% | |
| 18/03/26 | High Rd, Wood Green | Haringey | Crime Hotspot | 31,360 | 22 | 10 | 0.006% | 2 false alerts confirmed, 1 true alert unconfirmed |
| 23/03/26 | Victoria Street, Victoria | Westminster | Crime Hotspot | 18,962 | 10 | 5 | 0% | 1 true alert unconfirmed |
| 24/03/26 | Barking, Station Parade | Barking & Dagenham | Crime Hotspot | 16,154 | 7 | 4 | 0% | |
| 24/03/26 | Bond St Station, Oxford St | Westminster | Crime Hotspot | 24,408 | 7 | 4 | 0% | |
| 25/03/26 | North End, Croydon | Croydon | Crime Hotspot | 19,856 | 17 | 9 | 0% | |
| 25/03/26 | High St, Ilford | Redbridge | Crime Hotspot | 13,227 | 5 | 3 | 0% | |
| 26/03/26 | Tooting B'way, o/s Tube stn | Wandsworth | Crime Hotspot | 26,478 | 15 | 2 | 0% | |
| 27/03/26 | Powis St, Woolwich | Greenwich | Crime Hotspot | 9,980 | 13 | 6 | 0% | 1 true alert unconfirmed |
| 31/03/26 | Dagenham Heathway | Barking & Dagenham | Crime Hotspot | 12,620 | 7 | 2 | 0% | |
| 31/03/26 | Seven Sisters Rd | Haringey | Crime Hotspot | 15,805 | 18 | 8 | 0% | |

### April 2026 (30 deployments, to 17 Apr)

| Date | Location | Borough | Use Case | Faces | Alerts | Arrests | FA Rate | Notes |
|------|----------|---------|----------|-------|--------|---------|---------|-------|
| 01/04/26 | Whitechapel Rd jw Brady St | Tower Hamlets | Crime Hotspot | 21,647 | 15 | 4 | 0% | 1 true alert unconfirmed |
| 01/04/26 | Hatton Gdn, Jct Greville St | Islington | Crime Hotspot | 12,600 | 4 | 2 | 0% | |
| 02/04/26 | Green St, Upton Park | Newham | Crime Hotspot | 14,829 | 5 | 2 | 0% | |
| 02/04/26 | Angel | Islington | Crime Hotspot | 28,437 | 15 | 7 | 0% | |
| 07/04/26 | North Finchley, High Rd, Jct Percy Rd | Barnet | Crime Hotspot | 6,323 | 6 | 2 | 0% | |
| 07/04/26 | Piccadilly Circus | Westminster | Crime Hotspot | 45,804 | 7 | 3 | 0% | 1 true alert unconfirmed — watchlist 18,800 (anomaly: spike from ~17,800) |
| 08/04/26 | Hackney Mare St | Hackney | Crime Hotspot | 16,463 | 7 | 5 | 0% | |
| 08/04/26 | Paddington | Westminster | Crime Hotspot | 8,334 | 4 | 3 | 0% | |
| 09/04/26 | Harlesden High St | Brent | Crime Hotspot | 5,998 | 9 | 4 | 0.016% | **Highest FA rate in 2026 doc** — 1 false alert confirmed |
| 09/04/26 | Tottenham Court Rd | Camden | Crime Hotspot | 49,199 | 10 | 7 | 0% | |
| 10/04/26 | Portobello Rd j/w Talbot Rd | K&C | Crime Hotspot | 31,957 | 5 | 3 | 0% | |
| 10/04/26 | East Ham | Newham | Crime Hotspot | 22,162 | 13 | 9 | 0% | |
| 13/04/26 | Harrow on the Hill, o/s Tube stn | Harrow | Crime Hotspot | 17,719 | 12 | 5 | 0.005% | 1 false alert confirmed |
| 13/04/26 | Brompton Rd, Knightsbridge | K&C | Crime Hotspot | 11,830 | 1 | 0 | 0% | |
| 14/04/26 | Leyton, Lea Bridge Road | Waltham Forest | Crime Hotspot | 6,068 | 7 | 1 | 0% | |
| 14/04/26 | High St, Hounslow | Hounslow | Crime Hotspot | 21,103 | 7 | 5 | 0% | |
| 15/04/26 | Kings Cross Stn | Camden | Crime Hotspot | 26,343 | 8 | 7 | 0.004% | 1 false alert confirmed |
| 15/04/26 | Chrisp St, Poplar | Tower Hamlets | Crime Hotspot | 5,172 | 2 | 2 | 0% | |
| 16/04/26 | North End, Croydon | Croydon | Crime Hotspot | 12,510 | 18 | 9 | 0% | |
| 17/04/26 | Leicester Sq o/s Hippodrome | Westminster | Crime Hotspot | 35,508 | 5 | 1 | 0% | |
| 17/04/26 | Stratford Broadway | Newham | Crime Hotspot | 13,417 | 10 | 5 | 0% | |

**Document ends 17/04/26 — partial year record.**

**Gaps/uncertainties:**
- 22/02/26 Event PSO at Love Lane/High Rd, Haringey: likely Tottenham Hotspur FC match (Tottenham Hotspur Stadium is on the High Road, Haringey) — date confirmation recommended
- Piccadilly Circus 07/04/26 shows watchlist 18,800 — notably higher than surrounding entries (~17,800–17,900); possibly data entry variation or different watchlist config
- Harlesden High St 09/04/26 = 0.016% false alert rate, highest in 2026 document
- Angel (02/04/26) is Islington — first "Angel" area deployment in either record
- Portobello Rd (10/04/26) = first Kensington & Chelsea crime hotspot deployment in either record (K&C borderline — could be H&F territory; Portobello Rd is K&C)
- "Catford, Rushey Green" and "Thornton Heath" expand Croydon/Lewisham footprint
- North Finchley (07/04/26) = first Barnet deployment in either record
- No CNI PSO or second Event PSO category visible in this document beyond the Feb football match
- Harrow deployments new to 2026 (St Ann's Jan, Harrow on the Hill Apr) — expanding northwest

---

## Source: live-facial-recognition-deployment-record-2025.pdf
Pages read: 1–10 (p.11 blank) | Records found: **231** | Operator: Metropolitan Police | Vendor: NEC (implied, standard MPS kit) | Source type: official MPS deployment record

**Columns:** Date | Location | Borough | Use Case | Faces Scanned | Total Alerts | Arrests | False Alert Rate | Notes

All use case = "Crime Hotspot" unless noted. Threshold 0.64 throughout. Watchlist ~15,000–16,900 (grows over year).

### January 2025 (16 deployments)

| Date | Location | Borough | Use Case | Faces | Alerts | Arrests | FA Rate | Notes |
|------|----------|---------|----------|-------|--------|---------|---------|-------|
| 08/01/25 | High St North, East Ham | Newham | Crime Hotspot | 9,780 | 10 | 4 | 0% | |
| 08/01/25 | Green St, Newham | Newham | Crime Hotspot | 8,480 | 6 | 3 | 0% | |
| 10/01/25 | Powis St, Woolwich | Greenwich | Crime Hotspot | 15,480 | 14 | 5 | 0% | |
| 10/01/25 | Camberwell Green | Southwark | Crime Hotspot | 3,975 | 4 | 3 | 0% | |
| 14/01/25 | Rye Lane, Peckham | Southwark | Crime Hotspot | 10,245 | 12 | 4 | 0% | 1 true alert unconfirmed |
| 14/01/25 | Wembley Central | Brent | Crime Hotspot | 13,950 | 11 | 7 | 0% | |
| 16/01/25 | Streatham High Rd | Lambeth | Crime Hotspot | 3,890 | 2 | 2 | 0% | |
| 16/01/25 | Stratford B'way | Newham | Crime Hotspot | 25,335 | 24 | 11 | 0% | 1 true alert unconfirmed |
| 22/01/25 | Town Sq, Walthamstow | Waltham Forest | Crime Hotspot | 12,120 | 13 | 6 | 0.008% | 1 false alert confirmed |
| 22/01/25 | Walworth Rd | Southwark | Crime Hotspot | 5,200 | 3 | 1 | 0% | |
| 24/01/25 | Powis St, Woolwich | Greenwich | Crime Hotspot | 15,711 | 11 | 6 | 0% | |
| 24/01/25 | High St North, East Ham | Newham | Crime Hotspot | 17,265 | 13 | 4 | 0% | |
| 28/01/25 | Wembley Central | Brent | Crime Hotspot | 9,990 | 9 | 6 | 0% | |
| 28/01/25 | Kilburn High Rd | Brent | Crime Hotspot | 9,581 | 15 | 9 | 0% | |
| 30/01/25 | Stratford B'way | Newham | Crime Hotspot | 21,050 | 16 | 3 | 0% | 1 true alert unconfirmed |
| 30/01/25 | Leyton | Waltham Forest | Crime Hotspot | 5,645 | 5 | 0 | 0% | |

### February 2025 (16 deployments)

| Date | Location | Borough | Use Case | Faces | Alerts | Arrests | FA Rate | Notes |
|------|----------|---------|----------|-------|--------|---------|---------|-------|
| 04/02/25 | South St, Romford | Havering | Crime Hotspot | 13,110 | 16 | 5 | 0% | |
| 04/02/25 | Clapham Junction | Wandsworth | Crime Hotspot | 10,625 | 6 | 2 | 0% | |
| 06/02/25 | Dagenham Heathway | Barking & Dagenham | Crime Hotspot | 12,660 | 11 | 3 | 0.008% | 1 false alert confirmed |
| 06/02/25 | High St, Ilford | Redbridge | Crime Hotspot | 19,733 | 9 | 3 | 0% | |
| 11/02/25 | High St, Sutton | Sutton | Crime Hotspot | 14,430 | 7 | 2 | 0% | |
| 11/02/25 | Shepherds Bush Green | H&F | Crime Hotspot | 17,310 | 8 | 4 | 0% | |
| 13/02/25 | Barking | Barking & Dagenham | Crime Hotspot | 13,695 | 13 | 10 | 0% | |
| 13/02/25 | Oxford St | Westminster | Crime Hotspot | 29,025 | 12 | 6 | 0% | |
| 19/02/25 | Hammersmith Broadway | H&F | Crime Hotspot | 21,940 | 13 | 4 | 0% | |
| 19/02/25 | Clarence St, Kingston | Kingston | Crime Hotspot | 17,850 | 9 | 3 | 0% | |
| 21/02/25 | Westfield, Shepherds Bush | H&F | Crime Hotspot | 30,305 | 6 | 5 | 0% | |
| 21/02/25 | High St, Ilford | Redbridge | Crime Hotspot | 16,485 | 19 | 8 | 0% | |
| 25/02/25 | Oxford Circus | Westminster | Crime Hotspot | 32,160 | 14 | 5 | 0% | 2 true alerts unconfirmed |
| 25/02/25 | Tooting B'way | Wandsworth | Crime Hotspot | 16,380 | 9 | 3 | 0% | |
| 27/02/25 | South St, Romford | Havering | Crime Hotspot | 14,160 | 13 | 5 | 0% | |
| 27/02/25 | North End, Croydon | Croydon | Crime Hotspot | 24,365 | 20 | 8 | 0.004% | 1 false alert confirmed |

### March 2025 (16 deployments)

| Date | Location | Borough | Use Case | Faces | Alerts | Arrests | FA Rate | Notes |
|------|----------|---------|----------|-------|--------|---------|---------|-------|
| 05/03/25 | Deptford High St | Lewisham | Crime Hotspot | 8,440 | 6 | 3 | 0% | |
| 05/03/25 | West Croydon | Croydon | Crime Hotspot | 15,875 | 17 | 7 | 0% | |
| 07/03/25 | Wood Green | Haringey | Crime Hotspot | 15,315 | 13 | 7 | 0% | |
| 07/03/25 | High St, Hounslow | Hounslow | Crime Hotspot | 21,810 | 7 | 1 | 0% | |
| 11/03/25 | Dalston Kingsland | Hackney | Crime Hotspot | 13,210 | 12 | 5 | 0% | |
| 11/03/25 | Edmonton Green | Enfield | Crime Hotspot | 10,260 | 7 | 2 | 0% | |
| 13/03/25 | Lewisham High St | Lewisham | Crime Hotspot | 11,080 | 18 | 8 | 0% | |
| 13/03/25 | Ealing B'way | Ealing | Crime Hotspot | 19,320 | 10 | 4 | 0.005% | 1 false alert confirmed |
| 19/03/25 | Seven Sisters Rd | Haringey | Crime Hotspot | 7,695 | 10 | 5 | 0% | |
| 19/03/25 | High St North, East Ham | Newham | Crime Hotspot | 12,083 | 10 | 3 | 0% | |
| 22/03/25 | Stratford Westfield | Newham | Crime Hotspot | 32,835 | 13 | 9 | 0.003% | 1 false alert confirmed |
| 22/03/25 | North End, Croydon | Croydon | Crime Hotspot | 20,115 | 16 | 5 | 0% | 1 false alert confirmed |
| 25/03/25 | Deptford High Street | Lewisham | Crime Hotspot | 5,885 | 5 | 1 | 0% | |
| 25/03/25 | Wood Green | Haringey | Crime Hotspot | 13,380 | 11 | 7 | 0% | |
| 27/03/25 | Powis St, Woolwich | Greenwich | Crime Hotspot | 20,471 | 16 | 8 | 0% | |
| 27/03/25 | Dalston Kingsland | Hackney | Crime Hotspot | 14,580 | 7 | 7 | 0% | |

### April 2025 (18 deployments)

| Date | Location | Borough | Use Case | Faces | Alerts | Arrests | FA Rate | Notes |
|------|----------|---------|----------|-------|--------|---------|---------|-------|
| 01/04/25 | High St, Bromley | Bromley | Crime Hotspot | 11,835 | 8 | 3 | 0% | |
| 01/04/25 | High St, Camden | Camden | Crime Hotspot | 12,915 | 7 | 1 | 0% | |
| 03/04/25 | Stratford B'way | Newham | Crime Hotspot | 14,205 | 11 | 5 | 0% | |
| 03/04/25 | Kilburn High Rd | Brent | Crime Hotspot | 11,085 | 12 | 4 | 0% | |
| 09/04/25 | Stratford Westfield | Newham | Crime Hotspot | 32,920 | 16 | 3 | 0% | |
| 09/04/25 | Wembley Central | Brent | Crime Hotspot | 9,630 | 10 | 6 | 0% | |
| 11/04/25 | Walthamstow Central | Waltham Forest | Crime Hotspot | 19,240 | 20 | 7 | 0% | |
| 11/04/25 | Kings Cross | Camden | Crime Hotspot | 8,385 | 6 | 4 | 0% | |
| 15/04/25 | Walworth Rd | Southwark | Crime Hotspot | 12,120 | 8 | 2 | 0% | |
| 15/04/25 | Stratford B'way | Newham | Crime Hotspot | 13,285 | 12 | 4 | 0% | |
| 17/04/25 | Rye Lane, Peckham | Southwark | Crime Hotspot | 12,145 | 13 | 6 | 0% | 1 true alert unconfirmed |
| 17/04/25 | Green St, Newham | Newham | Crime Hotspot | 16,940 | 15 | 5 | 0% | |
| 22/04/25 | George St, Croydon | Croydon | Crime Hotspot | 8,030 | 9 | 3 | 0% | 3 true alerts unconfirmed |
| 22/04/25 | Walthamstow Central | Waltham Forest | Crime Hotspot | 17,755 | 18 | 10 | 0% | |
| 24/04/25 | Oxford Circus | Westminster | Crime Hotspot | 28,805 | 12 | 7 | 0% | 1 true alert unconfirmed |
| 24/04/25 | Wembley Central | Brent | Crime Hotspot | 11,445 | 4 | 2 | 0% | |
| 30/04/25 | Westfield, Stratford | Newham | Crime Hotspot | 39,855 | 18 | 5 | 0% | |
| 30/04/25 | Kilburn High Rd | Brent | Crime Hotspot | 8,970 | 9 | 5 | 0% | |

### May 2025 (20 deployments)

| Date | Location | Borough | Use Case | Faces | Alerts | Arrests | FA Rate | Notes |
|------|----------|---------|----------|-------|--------|---------|---------|-------|
| 02/05/25 | London Rd, Croydon | Croydon | Crime Hotspot | 12,210 | 23 | 6 | 0% | 1 true alert unconfirmed |
| 02/05/25 | Bond St Stn | Westminster | Crime Hotspot | 30,855 | 7 | 5 | 0% | |
| 06/05/25 | Mare St, Hackney | Hackney | Crime Hotspot | 2,490 | 9 | 4 | 0% | |
| 06/05/25 | Shepherds Bush Green | H&F | Crime Hotspot | 18,050 | 6 | 2 | 0% | |
| 08/05/25 | Powis St, Woolwich | Greenwich | Crime Hotspot | 17,310 | 10 | 3 | 0% | |
| 08/05/25 | Station Lane, Hornchurch | Havering | Crime Hotspot | 4,895 | 3 | 0 | 0% | |
| 10/05/25 | High Street, Ilford | Redbridge | Crime Hotspot | 17,665 | 10 | 3 | 0% | |
| 10/05/25 | Station Parade, Barking | Barking & Dagenham | Crime Hotspot | 15,001 | 10 | 6 | 0% | |
| 13/05/25 | Oxford Circus | Westminster | Crime Hotspot | 36,140 | 8 | 2 | 0% | |
| 13/05/25 | High St, Harlesden | Brent | Crime Hotspot | 8,430 | 8 | 4 | 0% | |
| 15/05/25 | High Street, Ilford | Redbridge | Crime Hotspot | 13,595 | 10 | 8 | 0% | |
| 15/05/25 | Station Parade, Barking | Barking & Dagenham | Crime Hotspot | 15,440 | 7 | 5 | 0% | |
| 21/05/25 | Dagenham Heathway | Barking & Dagenham | Crime Hotspot | 13,215 | 8 | 2 | 0% | |
| 21/05/25 | South St, Romford | Havering | Crime Hotspot | 16,890 | 11 | 4 | 0% | |
| 23/05/25 | Victoria St | Westminster | Crime Hotspot | 14,725 | 10 | 5 | 0% | |
| 23/05/25 | Dalston Kingsland | Hackney | Crime Hotspot | 13,200 | 15 | 10 | 0% | |
| 27/05/25 | Powis St, Woolwich | Greenwich | Crime Hotspot | 11,476 | 10 | 7 | 0.008% | 1 false alert confirmed |
| 27/05/25 | Lewisham High St | Lewisham | Crime Hotspot | 10,965 | 11 | 6 | 0% | |
| 29/05/25 | High St, Bexleyheath | Bexley | Crime Hotspot | 11,518 | 6 | 2 | 0% | |
| 29/05/25 | Edgware Rd | Westminster | Crime Hotspot | 8,560 | 6 | 6 | 0% | |

### June 2025 (18 deployments)

| Date | Location | Borough | Use Case | Faces | Alerts | Arrests | FA Rate | Notes |
|------|----------|---------|----------|-------|--------|---------|---------|-------|
| 04/06/25 | Green St, Newham | Newham | Crime Hotspot | 14,625 | 15 | 8 | 0% | |
| 04/06/25 | Tooting B'way | Wandsworth | Crime Hotspot | 14,985 | 16 | 4 | 0% | |
| 06/06/25 | Richmond High St | Richmond | Crime Hotspot | 13,065 | 9 | 3 | 0% | |
| 06/06/25 | Shoreditch High St | Hackney | Crime Hotspot | 9,915 | 1 | 1 | 0% | |
| 10/06/25 | Stratford B'way | Newham | Crime Hotspot | 15,315 | 10 | 7 | 0% | |
| 10/06/25 | Peckham Rye | Southwark | Crime Hotspot | 10,535 | 5 | 4 | 0% | |
| 12/06/25 | Tottenham Hale | Haringey | Crime Hotspot | 14,975 | 5 | 2 | 0.006% | 1 false alert confirmed |
| 12/06/25 | High St North, East Ham | Newham | Crime Hotspot | 17,430 | 7 | 4 | 0% | 1 true alert unconfirmed |
| 17/06/25 | Ealing B'way | Ealing | Crime Hotspot | 18,885 | 8 | 3 | 0% | |
| 17/06/25 | Bethnal Green Rd | Tower Hamlets | Crime Hotspot | 11,625 | 13 | 3 | 0% | 1 true alert unconfirmed |
| 19/06/25 | Walthamstow Central | Waltham Forest | Crime Hotspot | 15,950 | 12 | 8 | 0% | |
| 19/06/25 | Wood Green High Rd | Haringey | Crime Hotspot | 12,120 | 19 | 6 | 0% | |
| 24/06/25 | Poplar – Vesey Path | Tower Hamlets | Crime Hotspot | 6,780 | 7 | 2 | 0% | |
| 24/06/25 | Station Rd, Hayes | Hillingdon | Crime Hotspot | 8,282 | 4 | 1 | 0% | |
| 26/06/25 | Clarence St, Kingston | Kingston | Crime Hotspot | 22,560 | 11 | 5 | 0% | 1 true alert unconfirmed |
| 26/06/25 | Seven Sisters, Tottenham | Haringey | Crime Hotspot | 10,180 | 9 | 3 | 0% | 1 true alert unconfirmed |
| 01/07/25 | Kings Cross Station | Camden | Crime Hotspot | 9,960 | 0 | 0 | 0% | Zero alerts — no matches |
| 01/07/25 | Uxbridge Rd, Shepherds Bush | H&F | Crime Hotspot | 11,075 | 7 | 2 | 0% | |

### July 2025 (16 deployments)

| Date | Location | Borough | Use Case | Faces | Alerts | Arrests | FA Rate | Notes |
|------|----------|---------|----------|-------|--------|---------|---------|-------|
| 03/07/25 | Powis St, Woolwich | Greenwich | Crime Hotspot | 14,590 | 13 | 5 | 0% | |
| 03/07/25 | Oxford Circus | Westminster | Crime Hotspot | 32,555 | 9 | 6 | 0% | |
| 05/07/25 | Walthamstow Central | Waltham Forest | Crime Hotspot | 23,848 | 12 | 7 | 0% | 2 true alerts unconfirmed |
| 05/07/25 | Green St, Newham | Newham | Crime Hotspot | 21,930 | 7 | 3 | 0% | |
| 09/07/25 | Kilburn High Rd | Brent | Crime Hotspot | 13,635 | 11 | 4 | 0% | |
| 09/07/25 | Rye Lane, Peckham | Southwark | Crime Hotspot | 9,315 | 13 | 9 | 0% | 1 true alert unconfirmed |
| 11/07/25 | Station Parade, Barking | Barking & Dagenham | Crime Hotspot | 15,225 | 8 | 3 | 0% | |
| 11/07/25 | Coventry St, Westminster | Westminster | Crime Hotspot | 17,415 | 7 | 6 | 0% | |
| 15/07/25 | High St, Lewisham | Lewisham | Crime Hotspot | 12,615 | 12 | 8 | 0% | |
| 15/07/25 | King St, Hammersmith | H&F | Crime Hotspot | 16,285 | 12 | 7 | 0% | |
| 17/07/25 | Wembley Central | Brent | Crime Hotspot | 17,015 | 9 | 4 | 0% | |
| 17/07/25 | Leicester Sq | Westminster | Crime Hotspot | 32,690 | 7 | 4 | 0% | |
| 23/07/25 | Romford | Havering | Crime Hotspot | 29,930 | 11 | 3 | 0% | |
| 23/07/25 | Praed St, Paddington | Westminster | Crime Hotspot | 25,295 | 8 | 5 | 0% | |
| 25/07/25 | Camden | Camden | Crime Hotspot | 9,455 | 2 | 0 | 0% | |
| 25/07/25 | Piccadilly, Hard Rock | Westminster | Crime Hotspot | 7,490 | 4 | 4 | 0% | |
| 29/07/25 | Woolwich | Greenwich | Crime Hotspot | 21,080 | 11 | 6 | 0% | |
| 29/07/25 | Dagenham | Barking & Dagenham | Crime Hotspot | 9,455 | 5 | 3 | 0% | |
| 31/07/25 | London Bridge | Southwark | Crime Hotspot | 31,365 | 7 | 3 | 0% | 1 true alert unconfirmed |
| 31/07/25 | Ilford, High Rd | Redbridge | Crime Hotspot | 18,695 | 14 | 3 | 0% | |

### August 2025 (18 deployments including Notting Hill Carnival)

| Date | Location | Borough | Use Case | Faces | Alerts | Arrests | FA Rate | Notes |
|------|----------|---------|----------|-------|--------|---------|---------|-------|
| 05/08/25 | Shepherds Bush Green | H&F | Crime Hotspot | 19,605 | 6 | 2 | 0% | |
| 05/08/25 | Green Street, Newham | Newham | Crime Hotspot | 24,150 | 10 | 9 | 0% | |
| 07/08/25 | Oxford Circus | Westminster | Crime Hotspot | 31,640 | 7 | 5 | 0% | |
| 07/08/25 | Walworth Rd, Southwark | Southwark | Crime Hotspot | 13,785 | 7 | 4 | 0% | |
| 12/08/25 | Brixton Rd, Brixton | Lambeth | Crime Hotspot | 19,095 | 23 | 16 | 0% | High alert/arrest ratio |
| 12/08/25 | Bond St Stn | Westminster | Crime Hotspot | 33,780 | 5 | 1 | 0.002% | 1 false alert confirmed |
| 15/08/25 | Stratford, Westfields | Newham | Crime Hotspot | 31,774 | 17 | 9 | 0% | |
| 15/08/25 | Clarence St, Kingston | Kingston | Crime Hotspot | 26,460 | 9 | 3 | 0% | |
| 19/08/25 | Peckham Rye | Southwark | Crime Hotspot | 18,015 | 12 | 7 | 0% | |
| 19/08/25 | Victoria St | Westminster | Crime Hotspot | 14,505 | 6 | 4 | 0% | |
| 21/08/25 | Stratford B'way | Newham | Crime Hotspot | 18,270 | 9 | 1 | 0% | 1 true alert unconfirmed |
| 21/08/25 | Coventry St, Westminster | Westminster | Crime Hotspot | 25,050 | 12 | 4 | 0% | 1 true alert unconfirmed |
| 24/08/25 | Kilburn Lane | Brent | **Event PSO** | 46,848 | 33 | 23 | 0.002% | **Notting Hill Carnival Day 1** — 1 false alert confirmed |
| 24/08/25 | Paddington Stn | Westminster | **Event PSO** | 16,380 | 6 | 4 | 0% | Notting Hill Carnival Day 1 overflow |
| 25/08/25 | Kilburn Lane | Brent | **Event PSO** | 51,221 | 41 | 24 | 0% | **Notting Hill Carnival Day 2** — largest single-day face count in record |
| 25/08/25 | Paddington Stn | Westminster | **Event PSO** | 51,220 | 18 | 10 | 0.0009% | Notting Hill Carnival Day 2 |
| 27/08/25 | Tooting Broadway | Wandsworth | Crime Hotspot | 22,180 | 15 | 7 | 0% | |
| 27/08/25 | Hounslow High St | Hounslow | Crime Hotspot | 23,505 | 13 | 6 | 0% | |
| 29/08/25 | Ealing Broadway | Ealing | Crime Hotspot | 19,230 | 12 | 2 | 0% | |
| 29/08/25 | Walthamstow Central | Waltham Forest | Crime Hotspot | 23,610 | 14 | 10 | 0% | |

### September 2025 (18 deployments)

| Date | Location | Borough | Use Case | Faces | Alerts | Arrests | FA Rate | Notes |
|------|----------|---------|----------|-------|--------|---------|---------|-------|
| 02/09/25 | Walworth Rd | Southwark | Crime Hotspot | 19,515 | 8 | 5 | 0% | |
| 02/09/25 | Bond St Stn | Westminster | Crime Hotspot | 32,140 | 12 | 7 | 0% | 1 true alert unconfirmed |
| 04/09/25 | Edmonton Green | Enfield | Crime Hotspot | 16,125 | 12 | 6 | 0% | |
| 04/09/25 | Whitechapel | Tower Hamlets | Crime Hotspot | 16,900 | 15 | 7 | 0% | |
| 06/09/25 | North End, Croydon | Croydon | Crime Hotspot | 13,680 | 11 | 5 | 0% | 1 true alert unconfirmed |
| 09/09/25 | Finsbury Park | Islington | Crime Hotspot | 5,835 | 10 | 4 | 0% | 1 true alert unconfirmed |
| 09/09/25 | Dalston Kingsland | Hackney | Crime Hotspot | 13,425 | 13 | 9 | 0% | |
| 12/09/25 | High St, Lewisham | Lewisham | Crime Hotspot | 10,145 | 14 | 9 | 0% | |
| 12/09/25 | Brixton Rd, Brixton | Lambeth | Crime Hotspot | 35,280 | 32 | 14 | 0.002% | 1 false alert confirmed — high-volume deployment |
| 16/09/25 | Ilford High St | Redbridge | Crime Hotspot | 26,805 | 12 | 4 | 0.003% | 1 false alert confirmed |
| 16/09/25 | Bethnal Green Road | Tower Hamlets | Crime Hotspot | 9,150 | 7 | 3 | 0% | |
| 18/09/25 | Powis St, Woolwich | Greenwich | Crime Hotspot | 22,760 | 10 | 8 | 0% | |
| 18/09/25 | High Rd, Wood Green | Haringey | Crime Hotspot | 11,660 | 17 | 6 | 0% | 2 true alerts unconfirmed |
| 24/09/25 | Oxford Circus | Westminster | Crime Hotspot | 44,160 | 10 | 3 | 0% | |
| 24/09/25 | South St, Romford | Havering | Crime Hotspot | 13,870 | 8 | 1 | 0% | |
| 26/09/25 | Station Parade, Barking | Barking & Dagenham | Crime Hotspot | 18,525 | 10 | 5 | 0% | |
| 26/09/25 | Piccadilly Circus | Westminster | Crime Hotspot | 22,710 | 2 | 1 | 0% | |
| 30/09/25 | Edgware Rd | Westminster | Crime Hotspot | 7,575 | 11 | 5 | 0% | |
| 30/09/25 | Seven Sisters Rd | Haringey | Crime Hotspot | 8,460 | 6 | 1 | 0% | |

### October 2025 (22 deployments)

| Date | Location | Borough | Use Case | Faces | Alerts | Arrests | FA Rate | Notes |
|------|----------|---------|----------|-------|--------|---------|---------|-------|
| 01/10/25 | North End, Croydon | Croydon | Crime Hotspot | 23,521 | 18 | 9 | 0% | |
| 02/10/25 | Oxford Circus | Westminster | Crime Hotspot | 47,659 | 8 | 4 | 0% | |
| 02/10/25 | Stratford B'way | Newham | Crime Hotspot | 30,795 | 11 | 4 | 0% | |
| 07/10/25 | North End, Croydon | Croydon | Crime Hotspot | 15,036 | 20 | 8 | 0% | 1 true alert unconfirmed |
| 08/10/25 | Walworth Rd | Southwark | Crime Hotspot | 15,035 | 14 | 7 | 0% | |
| 08/10/25 | Piccadilly Circus | Westminster | Crime Hotspot | 28,150 | 10 | 4 | 0% | 1 true alert unconfirmed |
| 10/10/25 | Green St, Upton Park | Newham | Crime Hotspot | 21,750 | 4 | 2 | 0% | |
| 10/10/25 | Rye Lane, Peckham | Southwark | Crime Hotspot | 19,905 | 8 | 4 | 0% | |
| 14/10/25 | East Ham, High Rd North | Newham | Crime Hotspot | 20,385 | 9 | 7 | 0% | |
| 14/10/25 | Marble Arch | Westminster | Crime Hotspot | 18,780 | 10 | 4 | 0% | |
| 15/10/25 | North End, Croydon | Croydon | Crime Hotspot | 35,134 | 22 | 14 | 0% | High arrest rate |
| 16/10/25 | Brixton Road | Lambeth | Crime Hotspot | 27,840 | 24 | 13 | 0% | |
| 16/10/25 | Hatton Garden | Islington | Crime Hotspot | 13,190 | 4 | 4 | 0% | |
| 21/10/25 | Hammersmith Broadway | H&F | Crime Hotspot | 14,461 | 17 | 8 | 0% | 1 true alert unconfirmed |
| 21/10/25 | Harlesden | Brent | Crime Hotspot | 5,775 | 9 | 4 | 0% | |
| 24/10/25 | Tottenham Court Rd | Camden | Crime Hotspot | 23,190 | 10 | 8 | 0% | 1 true alert unconfirmed |
| 24/10/25 | Wembley Central | Brent | Crime Hotspot | 22,680 | 13 | 4 | 0% | |
| 28/10/25 | Walthamstow Central | Waltham Forest | Crime Hotspot | 18,700 | 3 | 1 | 0% | |
| 28/10/25 | Paddington Stn | Westminster | Crime Hotspot | 12,405 | 4 | 2 | 0% | |
| 29/10/25 | North End, Croydon | Croydon | Crime Hotspot | 9,205 | 13 | 6 | 0% | |
| 30/10/25 | Kilburn High Rd | Brent | Crime Hotspot | 6,770 | 9 | 5 | 0% | |
| 30/10/25 | Leicester Sq | Westminster | Crime Hotspot | 34,110 | 8 | 4 | 0% | 1 true alert unconfirmed |

### November 2025 (24 deployments)

| Date | Location | Borough | Use Case | Faces | Alerts | Arrests | FA Rate | Notes |
|------|----------|---------|----------|-------|--------|---------|---------|-------|
| 05/11/25 | Wood Green | Haringey | Crime Hotspot | 12,780 | 3 | 0 | 0% | |
| 05/11/25 | London Rd, Morden | Merton | Crime Hotspot | 11,895 | 7 | 1 | 0% | 1 true alert unconfirmed |
| 06/11/25 | North End, Croydon | Croydon | Crime Hotspot | 13,218 | 10 | 6 | 0% | |
| 07/11/25 | Edgware Rd | Westminster | Crime Hotspot | 14,580 | 6 | 5 | 0% | |
| 07/11/25 | Upton Park | Newham | Crime Hotspot | 18,455 | 10 | 6 | 0% | 1 true alert unconfirmed |
| 11/11/25 | Bruce Grove, Tottenham | Haringey | Crime Hotspot | 12,780 | 14 | 6 | 0% | 1 true alert unconfirmed |
| 11/11/25 | Tooting Broadway | Wandsworth | Crime Hotspot | 24,425 | 10 | 4 | 0% | 1 true alert unconfirmed |
| 13/11/25 | Sutton High St | Sutton | Crime Hotspot | 8,850 | 5 | 3 | 0% | |
| 13/11/25 | Southall | Ealing | Crime Hotspot | 13,050 | 4 | 1 | 0% | 1 true alert unconfirmed |
| 14/11/25 | North End, Croydon | Croydon | Crime Hotspot | 6,185 | 10 | 8 | 0% | |
| 18/11/25 | Edmonton Green | Enfield | Crime Hotspot | 18,075 | 14 | 6 | 0% | 1 true alert unconfirmed |
| 18/11/25 | Clarence St, Kingston | Kingston | Crime Hotspot | 17,225 | 8 | 4 | 0% | |
| 19/11/25 | North End, Croydon | Croydon | Crime Hotspot | 27,456 | 26 | 7 | 0% | 1 true alert unconfirmed |
| 20/11/25 | Piccadilly, Hard Rock | Westminster | Crime Hotspot | 14,805 | 3 | 0 | 0% | |
| 20/11/25 | Walthamstow | Waltham Forest | Crime Hotspot | 4,435 | 7 | 6 | 0% | |
| 21/11/25 | North End, Croydon | Croydon | Crime Hotspot | 17,242 | 13 | 7 | 0% | 1 true alert unconfirmed |
| 23/11/25 | Hornsey Road | Haringey | **Event PSO** | 8,435 | 1 | 0 | 0% | **Arsenal match (Emirates area)** |
| 23/11/25 | Holloway Road | Islington | **Event PSO** | 9,849 | 2 | 1 | 0% | Arsenal match support |
| 25/11/25 | Richmond | Richmond | Crime Hotspot | 17,585 | 8 | 3 | 0% | |
| 25/11/25 | High Street, Hounslow | Hounslow | Crime Hotspot | 19,465 | 7 | 2 | 0% | |
| 26/11/25 | North End, Croydon | Croydon | Crime Hotspot | 16,494 | 14 | 7 | 0% | 2 true alerts unconfirmed |
| 27/11/25 | T2 Heathrow Airport | Hillingdon | **CNI PSO** | 7,455 | 1 | 0 | 0% | **Critical National Infrastructure — first Heathrow deployment in record** |
| 28/11/25 | Westfield, White City | H&F | Crime Hotspot | 38,125 | 8 | 4 | 0% | |
| 28/11/25 | Westfield, Stratford | Newham | Crime Hotspot | 46,185 | 12 | 6 | 0% | |

### December 2025 (18 deployments)

| Date | Location | Borough | Use Case | Faces | Alerts | Arrests | FA Rate | Notes |
|------|----------|---------|----------|-------|--------|---------|---------|-------|
| 01/12/25 | Walthamstow Market | Waltham Forest | Crime Hotspot | 20,414 | 8 | 1 | 0% | |
| 01/12/25 | Tottenham Court Rd | Camden | Crime Hotspot | 33,520 | 5 | 3 | 0% | |
| 03/12/25 | Powis St, Woolwich | Greenwich | Crime Hotspot | 19,440 | 13 | 5 | 0% | 1 true alert unconfirmed |
| 03/12/25 | Upton Park | Newham | Crime Hotspot | 8,640 | 7 | 4 | 0% | 1 true alert unconfirmed |
| 04/12/25 | North End, Croydon | Croydon | Crime Hotspot | 16,611 | 10 | 3 | 0% | |
| 05/12/25 | Bond St Stn | Westminster | Crime Hotspot | 56,843 | 6 | 5 | 0% | 1 true alert unconfirmed — highest face count in record |
| 05/12/25 | Whitechapel | Tower Hamlets | Crime Hotspot | 11,690 | 12 | 2 | 0% | |
| 09/12/25 | Rye Lane, Peckham | Southwark | Crime Hotspot | 10,447 | 6 | 3 | 0% | |
| 09/12/25 | Covent Garden | Westminster | Crime Hotspot | 30,350 | 2 | 1 | 0% | |
| 10/12/25 | North End, Croydon | Croydon | Crime Hotspot | 23,842 | 14 | 6 | 0% | 1 true alert unconfirmed |
| 11/12/25 | Leicester Sq | Westminster | Crime Hotspot | 48,780 | 7 | 2 | 0% | |
| 11/12/25 | Mare St, Hackney | Hackney | Crime Hotspot | 12,055 | 13 | 11 | 0% | |
| 12/12/25 | Tottenham Court Rd | Camden | Crime Hotspot | 19,395 | 6 | 5 | 0% | |
| 15/12/25 | Leicester Sq | Westminster | Crime Hotspot | 42,096 | 5 | 2 | 0% | |
| 15/12/25 | South Bank | Lambeth | Crime Hotspot | 18,765 | 2 | 0 | 0% | |
| 17/12/25 | Brixton Rd | Lambeth | Crime Hotspot | 31,245 | 27 | 12 | 0% | 1 true alert unconfirmed |
| 17/12/25 | Oxford Circus | Westminster | Crime Hotspot | 55,495 | 11 | 7 | 0% | |
| 18/12/25 | North End, Croydon | Croydon | Crime Hotspot | 4 | — | — | — | Partial entry (1h 43m, 6282 faces) |
| 18/12/25 | North End, Croydon | Croydon | Crime Hotspot | 6,282 | 4 | 3 | 0% | |
| 19/12/25 | Dalston Junction | Hackney | Crime Hotspot | 15,465 | 13 | 10 | 0% | |
| 19/12/25 | Knightsbridge | Kensington & Chelsea | Crime Hotspot | 33,750 | 4 | 3 | 0% | 1 true alert unconfirmed |
| 23/12/25 | Lewisham High St | Lewisham | Crime Hotspot | 12,675 | 11 | 2 | 0% | |
| 23/12/25 | High St North, East Ham | Newham | Crime Hotspot | 15,105 | 9 | 7 | 0% | |

**Gaps/uncertainties:**
- Borough assignments are inferred from well-known London geography — should be verified against official ward data before JSON commit
- "Kilburn Lane" Carnival deployments are categorised here as Brent; actual boundary may straddle Brent/Kensington & Chelsea depending on exact position
- T2 Heathrow (CNI PSO 27/11/25) = first airport deployment in the full record; notable
- No vendor field in document — NEC assumed from MPS standard kit (confirm against policy doc)
- Watchlist sizes fluctuate slightly day to day (14,919–16,883); not anomalous, reflects ongoing additions/removals
- "Faces seen (estimate)" are operational estimates, not precise counts
- Bond St Stn 05/12/25 shows 56,843 faces — peak Christmas shopping; Oxford Circus 17/12/25 at 55,495 similarly elevated

---

## Source: The unchecked expansion of live facial recognition technology in London - Zoë Garbet.pdf

**Path:** Misc/Inbox to Process/
**Pages read:** 1–18 of 34 (remaining pages not yet extracted; cover govt consultation response guide + references)
**Type:** Political/investigative report — February 2026 — by Zoë Garbett, Green Party London Assembly Member

This is NOT a raw deployment data source. It is Garbett's analytical and advocacy report drawing on the same MPS deployment data used in her Excel. Contains key aggregate statistics, demographic analysis, and contextual data valuable for the ALHFRS project.

### Key data points extracted

**Deployment frequency (Table 1, p.9):**

| Year | Deployments | Frequency |
|------|-------------|-----------|
| 2020 | 3 | every 122 days |
| 2021 | 0 | n/a |
| 2022 | 6 | every 60.83 days |
| 2023 | 23 | every 15.86 days |
| 2024 | 180 | every 2.03 days |
| 2025 | 231 | every 1.58 days |

**Borough totals since 2020 (Table 2, p.14) — top boroughs:**

| Borough | Total deployments | Per 100k residents |
|---------|------------------|---------------------|
| Westminster | 75 | 36.72 |
| Croydon | 55 | 14.08 |
| Newham | 35 | 9.97 |
| Camden | 20 | 9.52 |
| Hammersmith and Fulham | 16 | 8.73 |
| Haringey | 20 | 7.56 |
| Southwark | 23 | 7.48 |
| Greenwich | 20 | 6.92 |
| Barking and Dagenham | 15 | 6.85 |
| Hackney | 13 | 5.02 |
| Lewisham | 15 | 4.99 |
| Havering | 12 | 4.58 |
| Wandsworth | 15 | 4.58 |
| Waltham Forest | 12 | 4.31 |
| Brent | 13 | 3.82 |
| Kingston | 6 | 3.57 |
| Redbridge | 11 | 3.54 |
| Hounslow | 9 | 3.12 |
| Tower Hamlets | 9 | 2.9 |
| Lambeth | 8 | 2.52 |
| Ealing | 9 | 2.45 |
| Sutton | 5 | 2.38 |
| Islington | 4 | 1.85 |
| Enfield | 5 | 1.52 |
| Kensington and Chelsea | 6 | 1.40 |
| Harrow | 3 | 1.15 |
| Richmond | 2 | 1.02 |
| Hillingdon | 3 | 0.98 |
| Merton | 2 | 0.93 |
| Bromley | 3 | 0.91 |
| Bexley | 2 | 0.81 |
| Barnet | 1 | 0.26 |

**Key 2025 aggregate statistics (p.12):**
- 1,130 arrests in 2025 from LFR deployments
- 925 Londoners stopped by LFR with no further action taken in 2025

**Croydon permanent camera (p.8, Jan 2026 MPS claim):**
- 100+ arrests in first 3 months of Croydon static camera pilot (Oct 2025 start)
- Since start of 2024, LFR deployments in Croydon led to 249 arrests, of which 193 charged or cautioned

**Demographic disproportion (p.15):**
- Since 2020: 263 deployments in wards with below-London-average White resident % vs 180 in above-average wards
- 2025 gap: 145 vs 86 (deployments in majority-non-White vs majority-White wards)

**Watchlist composition (p.13):**
- Average 105 under-18s on each watchlist (Liberty Investigates, Dec 2025)
- Children as young as 12 included

**MPS OIFR budget 2025/26:** £763,000 (despite MPS website claiming OIFR not in use)

**Notting Hill Carnival 2025:** LFR deployed on approach routes, not within event boundaries (BBC, Aug 2025)

**Gaps/uncertainties:** Pages 19–34 not read — contain further analysis and Government consultation response guide. No individual deployment records unique to this document. All deployment counts confirmed by this source match data extracted from PDFs above.

---

## Summary & Cross-Reference

### Files processed

| Source | Status | Records |
|--------|--------|---------|
| live-facial-recognition-deployment-record-2025.pdf | ✅ Complete | 231 (full year 2025) |
| live-facial-recognition-deployment-record-2026.pdf | ✅ Complete | 95 (Jan–Apr 17 2026) |
| Copy of Live Facial Recognition Deployments.xlsx | ✅ Complete | 254 (2020–partial 2025); 203 net new (2023+2024) |
| lfr-deployment-grid-2023-to-2024.pdf | ✅ Complete | 203 (2023+2024, confirms Excel) |
| lfr-deployment-grid-2020-2022.pdf | ✅ Complete | 9 (confirms existing JSON) |
| lfr-deployment-grid-2025-up-to-May20-.pdf | ✅ Complete | 66 (Jan–May 2025, subset of 2025 PDF) |
| Zoë Garbett report (Feb 2026) | ✅ Partial (p.1–18) | Context/analytics only |
| Inbox CSV (timeline data) | ⏭️ Skipped | Timeline events, not deployment records |

### Net new deployment records by source

| Period | Source | Count | Status vs JSON |
|--------|--------|-------|----------------|
| 2020–2022 | 2020-2022 PDF / Excel | 9 | Already in met-police-lfr.json (lfr-001 to ~lfr-005) |
| 2023 | Excel / 2023-2024 PDF | 23 | NET NEW — not in any JSON |
| 2024 | Excel / 2023-2024 PDF | 180 | NET NEW — not in any JSON |
| 2025 (full year) | 2025 PDF | 231 | NET NEW — not in any JSON |
| 2026 (Jan–Apr 17) | 2026 PDF | 95 | NET NEW — not in any JSON |
| **TOTAL NET NEW** | | **529** | |

### Cross-reference against existing deployments.json files

**met-police-lfr.json** (lfr-001 through lfr-008):
- lfr-001 to ~lfr-005: correspond to the 9 records in the 2020-2022 PDF (Stratford Feb 2020, Oxford Circus Feb-Feb 2020, Oxford Circus Jan/Jul/Jul/Jul 2022, Leicester Square Mar 2022, Piccadilly Jul 2022)
- lfr-008 = Croydon static camera (Oct 2025 permanent installation) — not a mobile deployment; confirmed by Garbett report (100+ arrests in first 3 months)
- lfr-006, lfr-007: likely correspond to remaining early 2023 deployments or other special cases — exact cross-reference needs verification against JSON file directly
- **ALL 529 net new records are NOT in the existing JSON**

**btp-lfr.json** (btp-001, btp-002):
- London Bridge and Waterloo (British Transport Police, Feb 2026) — NOT in MPS datasets; separate operator

**private-operators.json** (priv-001 through priv-005):
- Facewatch retail deployments — separate from all MPS data above

**retrospective-fr.json**: not checked (out of scope for this extraction — covers retrospective/CCTV matching, not live deployments)

### Data quality flags for JSON commit

1. **Borough inferences**: All 2025 and 2026 borough assignments are inferred (not from official data). The Garbett Excel provides ward codes for 2020-2025 records — use these for spatial data
2. **Date format**: 2020-2022 PDF uses DD/MM/YY; Garbett Excel had a MM/DD swap for the Stratford 2020 date (should be 2020-02-11, not 2020-11-02)
3. **Camden High Rd**: Excel shows Oct 12, faces 1,225 — PDF shows Dec 10, faces 12,225. Use PDF as authoritative
4. **Dalston date typo in 2023-2024 PDF**: Listed as "11/07/23" — correct date is 11/07/24 (watchlist and threshold confirm)
5. **Bond St Stn 02/05/25**: Watchlist shows 19,199 in 2025-up-to-May20 PDF — likely typo for 16,199; verify against main 2025 PDF
6. **Use case gaps**: Records prior to Sept 2024 use purpose references (1,2,3,4) rather than named use cases. All are "Crime Hotspot" (ref 1) unless specifically noted as Event PSO or CNI PSO
7. **Threshold progression for JSON**: threshold field should be 0.60 (2020–Jun 2024), 0.62 (Jul 11–Jul 24, 2024), 0.64 (Jul 25, 2024 onwards including all 2025 and 2026)

---


