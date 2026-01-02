Development on `/develop` branch.
- merge external pull requests into `/develop`
- implement features, fix bugs on `/develop`
- update changelog in `CHANGELOG.md`
- test on all platforms for new graphical features

When ready: Bump version using `tbump`:
```
tbump 5.2.3
```

Create pull request to merge `/develop` into `/master` branch on Github.
- approval by owner (Tom), merge to `/master`


Publish new version to PyPI (Tom):
```
python -m pip install --upgrade build
rm -r dist
python -m build
python -m twine upload dist/*
```
Finally: Update documentation for new features.
- upload to website by Tom
