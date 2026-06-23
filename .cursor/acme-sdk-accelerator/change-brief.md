# PR-ready change brief

## Request

Fix slice_along_axes so a scalar integer axes value works when one slice is supplied, matching the documented API.

## Plan

Normalize scalar axes with numbers.Integral before length validation in src/_skimage2/util/_slice_along_axes.py. Add regression tests in both skimage and skimage2 test suites.

## PM summary

slice_along_axes now accepts axes=1 (or any single integer) when exactly one slice tuple is provided, instead of raising TypeError: object of type 'int' has no len().

## Engineering notes

- Branch: `cursor/slice-along-axes-int-axes-98dd`
- Commit: `29b6b9ac7`
- AI disclosure: Cursor Agent assisted with this change; author remains responsible for review.

### Changed files

```text
src/_skimage2/util/_slice_along_axes.py      | 9 +++++++--
 tests/skimage/util/test_slice_along_axes.py  | 7 +++++++
 tests/skimage2/util/test_slice_along_axes.py | 7 +++++++
 3 files changed, 21 insertions(+), 2 deletions(-)
```

## QA notes

- Verify axes=1 with one slice crops along axis 1; axes=None default behavior unchanged.

## DevOps / CI notes

- Run the normal scikit-image CI gates before merge.

## Validation

- spin test -- tests/skimage/util/test_slice_along_axes.py tests/skimage2/util/test_slice_along_axes.py (20 passed)
- pre-commit run --files src/_skimage2/util/_slice_along_axes.py tests/skimage/util/test_slice_along_axes.py tests/skimage2/util/test_slice_along_axes.py (passed)

## Residual risk

- Low: only affects explicit scalar axes input; list/tuple axes paths unchanged.

## Local git status

```text
clean
```
