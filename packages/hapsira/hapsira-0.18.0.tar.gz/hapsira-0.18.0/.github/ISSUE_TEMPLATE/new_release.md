---
name: New release
about: Checklist for new release (development only)
title: Release X.Y.Z checklist
labels: development
assignees: astrojuanlu
---

## Preparing the release

* [ ] Rerun all notebooks (pay special attention to new features)
* [ ] Review documentation, optionally improving the user guide or adding new notebooks showcasing new functionality
* [ ] Write the changelog and list of contributors
  - Commits since last release branch https://github.com/hapsira/hapsira/compare/X.Y.Z...main
  - Issues closed in this milestone https://github.com/hapsira/hapsira/milestone/N?closed=1 (note that there might be issues without milestone!)
  - Pull requests merged since last branching https://github.com/hapsira/hapsira/pulls?q=is%3Apr+is%3Amerged+merged%3A%3E%3D2019-02-09+sort%3Aupdated-asc
  - List of contributors: `git shortlog --summary --email ${BRANCHING_COMMIT}..`

## Before the beta release

* [ ] New branch
* [ ] Bump version **to X.Yb1** in:
  - `README.md`
  - `__init__.py`
* [ ] Check all the badges in `README` point to the appropriate git **branch** (manually replace `main` by new branch)
* [ ] Check that docs badges and URLs point to appropriate **tag** (manually replace `latest` by new tag)
* [ ] `git commit -m 'Bump to next beta version'`
* [ ] Generate sdist and bdist_wheel with `python -m build`
* [ ] `twine upload dist/* --repository-url https://test.pypi.org/legacy/`
* [ ] Tag
* [ ] Bump main to next development version

## Beta release

* [ ] Push branch to GitHub **and tags**
* [ ] Check on Test PyPI that the badges will work
* [ ] Upload sdist and bdist_wheel to PyPI - *this step cannot be undone if the release is removed!* `twine upload dist/*`
* [ ] Check Read the Docs

## Before final release

* [ ] Backport any bugs to release branch
* [ ] Update release date in changelog of release branch
* [ ] Bump version **to X.Y.Z** in:
  - `README.md`
  - `__init__.py`
* [ ] Check that docs badges and URLs point to appropriate **tag** (replace `vX.Yb1` by `vX.Y.Z`)
* [ ] Push commit to release branch and wait for CI to be green
* [ ] Generate sdist and bdist_wheel running `python -m build`
* [ ] `twine upload dist/* --repository-url https://test.pypi.org/legacy/`
* [ ] Tag

## Final release

* [ ] Push tag to GitHub
* [ ] Upload sdist and bdist_wheel to PyPI - *this step cannot be undone if the release is removed!* `twine upload dist/*`
* [ ] Check Read the Docs
* [ ] Create GitHub release
* [ ] Add Zenodo badge to GitHub release
* [ ] Send announcement email with subject "ANN: hapsira X.Y.Z released 🚀"
* [ ] Cherry pick release date to main
* [ ] Close milestone
