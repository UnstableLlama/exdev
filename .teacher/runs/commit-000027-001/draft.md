# 5498926b60c23e4dfc689f5fe2adff29436cb2ed


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/5498926b60c23e4dfc689f5fe2adff29436cb2ed) · [Evidence ledger](draft.json)

Adds disk-cache docstrings without changing caching behavior, but inaccurately describes cache location, naming and accepted arguments.

- [Document persistent evaluation caching](#runtime)

## Problem

The disk-cache decorator and selective clearing helper lacked docstrings. [source; call_249cf257554f424dbfda1daa7dbec3c1]

## Reasoning

The change documents evaluation-result caching, cache-name collisions, output serialization and clearing by arguments, without changing the implementation. [source; call_249cf257554f424dbfda1daa7dbec3c1]

## Impact

Cache lookup, writes and deletion retain their existing behavior; the new documentation does not precisely describe the actual path, namespace or argument-serialization requirements. [source; call_249cf257554f424dbfda1daa7dbec3c1, call_e40188926cdc4a0cb9498db533bfcb86]

<a id="runtime"></a>

## Document persistent evaluation caching

Both lookup and clearing open the shelf selected by the explicit filename argument. They construct the same key from separately JSON-serialized positional and keyword arguments, with sorted dictionary keys. A hit returns the stored result; a miss calls the wrapped function and stores its output. Clearing deletes only the matching entry. [source; call_e40188926cdc4a0cb9498db533bfcb86]

disk_lru_cache_name creates __disk_lru_cache__ beside the absolute sys.argv[0] path and appends filename + '.lru'. Function identity is not included. In compare_q.py, get_test_data explicitly uses the different cache name 'get_dataset'; main selectively clears 'test_ppl' using the same specification arguments passed to the cached function. [source; call_e40188926cdc4a0cb9498db533bfcb86, call_6c23015cb774460596cf7598cbc8c251]

The earlier runtime entry describes JSON-keyed persistence beside the launching script and notes that no eviction is implemented. Inspection of the unchanged implementation confirms that this patch adds neither eviction nor capacity limits. [source; call_f6782c813a704489a68ecfb4e882631c, call_e40188926cdc4a0cb9498db533bfcb86, call_249cf257554f424dbfda1daa7dbec3c1]

A bounded standard-library transcription produced identical keys for dictionaries with reversed insertion order, resolved a synthetic launcher path to /tmp/launcher/__disk_lru_cache__/get_dataset.lru, and rejected an object with a string representation as not JSON serializable. [execution; call_a65a1f3445124906a194d8c09d52f715]

## Authoring-time findings — pending review

### cache-docstring-contract (suspected; defect)

The added documentation substitutes module directory, function name and string representation for the implementation's launcher directory, explicit cache filename and JSON serialization.

Trigger: A caller relies on the docstring when the launcher and decorated module are in different directories, the cache filename differs from the function name, or an argument is printable but not JSON serializable.

Expected: Documentation should identify sys.argv[0]-relative storage, the explicit filename namespace and JSON-serializable arguments; clearing must use that same namespace.

Actual: The docstrings describe module-relative storage and function-name identification, and state a string-representation requirement. The unchanged implementation instead uses sys.argv[0], filename and json.dumps. Existing get_test_data already uses a cache name different from its function name.

Locations: 5498926b60c23e4dfc689f5fe2adff29436cb2ed:exllamav3/util/file.py — disk_lru_cache, 5498926b60c23e4dfc689f5fe2adff29436cb2ed:exllamav3/util/file.py — disk_lru_cache_clear

Source evidence: call_249cf257554f424dbfda1daa7dbec3c1, call_e40188926cdc4a0cb9498db533bfcb86, call_6c23015cb774460596cf7598cbc8c251

source_inspection: Whole-parent literal search found uses in four evaluation files. Inspected compare_q.py demonstrates the explicit-name mismatch and a direct clearing call from main. This is a documentation-contract observation, not evidence of failures across all evaluation workflows. [call_f20bf542f2ca47c3b03aab84c691f40d, call_6c23015cb774460596cf7598cbc8c251]. Limits: Other evaluation call sites were located but not individually inspected; dynamic use is not ruled out.

scalar_transcription: Modeled the inspected JSON serialization and path expressions with standard-library Python. [call_e40188926cdc4a0cb9498db533bfcb86, call_a65a1f3445124906a194d8c09d52f715]. Limits: Did not execute the decorator or open a shelf.

## Uncertainty and limits

No evaluation workflow or shelve filesystem operation was executed. The standard-library check models only path construction and JSON key serialization.
