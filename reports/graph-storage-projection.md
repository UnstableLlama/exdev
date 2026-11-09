# Graph storage decision

Measured before the migration through position 159. The detailed [per-commit curve and sampled components](graph-storage-projection.json) preserve the measurements and model assumptions.

| Measured interval | Commits | Mean stored/logical components per commit | Duplicate SQLite snapshot JSON |
|---|---:|---:|---:|
| 1–25 | 25 | 3.87 MiB | 0.82 MiB |
| 26–50 | 25 | 3.98 MiB | 0.85 MiB |
| 51–100 | 50 | 4.30 MiB | 0.92 MiB |
| 101–159 | 59 | 4.90 MiB | 1.07 MiB |

The mean column sums compressed graph JSON, compressed backend database, logs and uncompressed SQLite snapshot payload; it excludes occurrence rows and SQLite page/index overhead. Those are included in the full projection using measured page allocation. This distinction avoids presenting logical JSON size as total disk usage.

The full-history model linearly interpolates per-commit sizes between the four measured validation snapshots at positions 1, 755, 1509 and 2264. Compressed database sizes were measured by compression, not estimated from node counts. Occurrence overhead is calibrated against the live SQLite page allocation.

| Projected component | GiB |
|---|---:|
| Duplicate SQLite snapshot JSON | 10.44 |
| Symbol occurrences and associated index allocation | 3.72 |
| Compressed graph JSON | 1.05 |
| Compressed backend databases | 13.09 |
| Raw logs and binding evidence | 18.87 |
| Total before change | **47.17** |
| Total without duplicate SQLite snapshot JSON | **36.73** |

This supports the review's approximately 50 GB estimate. The projection is a sizing model, not measured full-history storage. A ±30% sensitivity scenario puts the reduced store around 25.7–47.7 GiB; it is not a statistical confidence interval. Source mirrors, preliminary validation caches, temporary indexing space and the migration backup are outside that total. Some small timeline/index overhead is also excluded. About 294 GiB was free at measurement time.

## Decision and verification

Schema v2 replaces `commits.snapshot` with a relative `snapshot_path` pointing to the existing compressed graph. The canonical fingerprint remains in SQLite and is checked on reads and resumed imports. Source snapshots and their reproduction data are retained; this is not a change to event semantics.

The walk was temporarily stopped at 165 completed commits. Every archive was checked against its original timeline value before migration. A SQLite backup was retained; the schema update was transactional, followed by compaction and integrity checks. The active timeline shrank from **230,064,128 to 62,570,496 bytes** (about 73%). See [migration evidence](timeline-storage-migration.json).

The independent source/database audit passed for all 165 migrated commits, and the indexer verified/reused the complete prefix. The walk can now continue with the reduced storage layout. Raw logs remain the next largest optional compression target; no log evidence was discarded in this change.
