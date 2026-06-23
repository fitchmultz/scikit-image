# PR-ready change brief

## Request

Fix slice_along_axes so axes=1 with one slice works as documented (int axes currently crashes with 'object of type int has no len()').

## Plan

Normalize scalar int axes to a tuple before length/validation checks in src/_skimage2/util/_slice_along_axes.py. Add regression tests in skimage and skimage2 test suites.

## PM summary

slice_along_axes now accepts a single integer axes value when exactly one slice is provided, matching the docstring. No API change beyond fixing the documented behavior.

## Engineering notes

- Branch: `cursor/slice-along-axes-int-axes-240f`
- Commit: `97eb53a96`
- AI disclosure: Cursor Agent assisted with this change; author remains responsible for review.

### Changed files

```text
src/_skimage2/util/_slice_along_axes.py      | 3 +++
 tests/skimage/util/test_slice_along_axes.py  | 7 +++++++
 tests/skimage2/util/test_slice_along_axes.py | 7 +++++++
 3 files changed, 17 insertions(+)
```

## QA notes

- Verify axes=1 with one slice on 2D arrays; existing list/tuple axes behavior unchanged.

## DevOps / CI notes

- Run the normal scikit-image CI gates before merge.

## Validation

- spin test -- tests/skimage/util/test_slice_along_axes.py tests/skimage2/util/test_slice_along_axes.py (20 passed)
- pre-commit run --files src/_skimage2/util/_slice_along_axes.py tests/skimage/util/test_slice_along_axes.py tests/skimage2/util/test_slice_along_axes.py (passed)

## Residual risk

- Low: one-line normalization before existing validation; int with multiple slices still raises ValueError.

## Local git status

```text
clean
```
