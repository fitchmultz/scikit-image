# PR-ready change brief

## Request

Fix slice_along_axes to accept integer axes with one slice.

## Plan

Normalize scalar integer axes to a one-item list, preserve existing validation, and add mirrored regression tests in skimage/skimage2 suites.

## PM summary

slice_along_axes now accepts int-like axes values for single-slice input and has regression coverage in both test modules.

## Engineering notes

- Branch: `cursor/fix-slice-int-axis-3ea2`
- Commit: `0802e942b`
- AI disclosure: Cursor Agent assisted with this change; author remains responsible for review.

### Changed files

```text
src/_skimage2/util/_slice_along_axes.py      | 9 +++++++--
 tests/skimage/util/test_slice_along_axes.py  | 7 +++++++
 tests/skimage2/util/test_slice_along_axes.py | 7 +++++++
 3 files changed, 21 insertions(+), 2 deletions(-)
```

## QA notes

- Verify changed behavior and any edge cases named in the tests.

## DevOps / CI notes

- Run the normal scikit-image CI gates before merge.

## Validation

- Pre-test snapshot commit; focused spin test and pre-commit checks run in follow-up commits.

## Residual risk

- Low risk: normalization only touches scalar axes handling and still enforces length/range checks.

## Local git status

```text
M src/_skimage2/util/_slice_along_axes.py
 M tests/skimage/util/test_slice_along_axes.py
 M tests/skimage2/util/test_slice_along_axes.py
```
