# PR-ready change brief

## Request

Fix slice_along_axes so axes=1 with one slice works (docstring says int is allowed)

## Plan

Normalize explicit int axes to a one-element list in src/_skimage2/util/_slice_along_axes.py; add regression tests in skimage and skimage2 test suites.

## PM summary

slice_along_axes now accepts a single integer axes value when one slice is supplied, matching the documented API. Previously this raised TypeError: object of type 'int' has no len().

## Engineering notes

- Branch: `cursor/fix-slice-along-axes-int-5807`
- Commit: `a233c4aae`
- AI disclosure: Cursor Agent assisted with this change; author remains responsible for review.

### Changed files

```text
src/_skimage2/util/_slice_along_axes.py      | 7 +++++--
 tests/skimage/util/test_slice_along_axes.py  | 7 +++++++
 tests/skimage2/util/test_slice_along_axes.py | 7 +++++++
 3 files changed, 19 insertions(+), 2 deletions(-)
```

## QA notes

- Regression test covers axes=1 with a single 2D slice.

## DevOps / CI notes

- Run the normal scikit-image CI gates before merge.

## Validation

- spin test -- tests/skimage/util/test_slice_along_axes.py tests/skimage2/util/test_slice_along_axes.py (20 passed)
- pre-commit run --files <changed files> (passed)

## Residual risk

- Residual risk: numpy scalar integer types (np.int64) are not normalized; docstring documents Python int only.

## Local git status

```text
clean
```
