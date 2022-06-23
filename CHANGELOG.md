# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [4.5.0] - 2022-06-23
### Added
 - CTkScrollbar (vertical, horizontal)

## [4.4.0] - 2022-06-14
### Changed
 - Changed custom dropdown menu to normal tkinter.Menu because of multiple platform specific bugs

## [4.3.0] - 2022-06-1
### Added
 - Added CTkComboBox
 - Small fixes for new dropdown menu

## [4.2.0] - 2022-05-30
### Added
 - CTkOptionMenu with custom dropdown menu
 - Support for clicking on labels of CTkCheckBox, CTkRadioButton, CTkSwitch

## [4.1.0] - 2022-05-24
### Added
 - Configure width and height for frame, button, label, progressbar, slider, entry

## [4.0.0] - 2022-05-22
### Added
 - This changelog file
 - Adopted semantic versioning
 - Added HighDPI scaling to all widgets and geometry managers (place, pack, grid)
 - Restructured CTkSettings and renamed a few manager classes
 - Orientation attribute for slider and progressbar

### Removed
 - A few unnecessary tests
