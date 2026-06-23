# PR-ready change brief

## Request

Fix slice_along_axes to accept integer axes with one slice.

## Plan

Normalize scalar integer axes to a one-item list, preserve existing validation, and add mirrored regression tests in skimage/skimage2 suites.

## PM summary

slice_along_axes now accepts int-like axes values for single-slice input and has mirrored regression tests in both util test suites.

## Engineering notes

- Branch: `cursor/fix-slice-int-axis-3ea2`
- Commit: `c641f46e2`
- AI disclosure: Cursor Agent assisted with this change; author remains responsible for review.

### Changed files

```text
.cursor/acme-sdk-accelerator/change-brief.html | 66 ++++++++++++++++++++++++++
 .cursor/acme-sdk-accelerator/change-brief.md   | 52 ++++++++++++++++++++
 src/_skimage2/util/_slice_along_axes.py        |  9 +++-
 tests/skimage/util/test_slice_along_axes.py    |  7 +++
 tests/skimage2/util/test_slice_along_axes.py   |  7 +++
 5 files changed, 139 insertions(+), 2 deletions(-)
```

## QA notes

- Regression covered by direct scalar-axis tests in both mirrored util suites.
- Modified-subpackage test gate passed with expected optional dependency skips.

## DevOps / CI notes

- No workflow or dependency changes; standard CI gates should remain unchanged.

## Validation

- CC=gcc CXX=g++ spin install (pass)
- spin test -- tests/skimage/util/test_slice_along_axes.py tests/skimage2/util/test_slice_along_axes.py (20 passed)
- pre-commit run --files src/\_skimage2/util/\_slice_along_axes.py tests/skimage/util/test_slice_along_axes.py tests/skimage2/util/test_slice_along_axes.py .cursor/acme-sdk-accelerator/change-brief.md .cursor/acme-sdk-accelerator/change-brief.html (pass)
- spin test --test-modified --base-ref main (870 passed, 4 skipped optional deps)

## Residual risk

- Low residual risk: scalar-axis normalization is localized and keeps existing range/uniqueness checks.

## Local git status

```text
clean
```
