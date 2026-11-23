# Research Protocol v1.0 — Indonesia Labour Justice Observatory

**Research Question:** *"What Do Indonesian Court Decisions Tell Us About Workers' Access to Justice?"*  
**Research Director:** Cecep Mustafa, Ph.D.  
**Pilot Period:** 2021–2026 (Target: 100–500 records, subject to lawful access and coverage).

## 1. Units of Analysis
- **Primary Unit:** One Industrial Relations Court (*Pengadilan Hubungan Industrial* / PHI) or Supreme Court cassation (*Kasasi PHI*) judgment (`record_id`).
- **Secondary Unit:** One legal claim or statutory issue within a judgment.

## 2. Controlled Vocabularies
- `court_level`: `PHI_First_Instance`, `MA_Cassation`, `Unknown`
- `dispute_type`: `Rights dispute`, `Interest dispute`, `Termination dispute`, `Inter-union dispute`, `Unknown`
- `judgment_outcome`: `Granted`, `Partly granted`, `Rejected`, `Dismissed on procedural grounds`, `Other`, `Unknown`
- `execution_status`: `Confirmed executed`, `Confirmed partially executed`, `Confirmed not executed`, `Unknown`, `Not observable`

## 3. 10-Stage Pipeline Architecture
1. **Source Discovery** -> 2. **Collection** -> 3. **Document Extraction** -> 4. **Normalization** -> 5. **Deduplication** -> 6. **Validation** -> 7. **Privacy Review** -> 8. **Analysis** -> 9. **Publication Review** -> 10. **Publication (Human-Gated)**.

Every stage emits an execution log, input/output counts, error report, validation report, provenance record, and completion status, and is restartable and idempotent.
