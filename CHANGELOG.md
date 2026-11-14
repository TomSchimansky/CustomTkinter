# Changelog
All notable changes to this project will be documented in this file!

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

ToDo:
 - cursor configuring
 - overwrite winfo methods
 - set icon (self.call("wm", "iconphoto", self._w, tkinter.PhotoImage(file="test_images/CustomTkinter_logo_single.png")))
 - add option to change label position for checkbox, switch, radiobutton #628

## [Unreleased]
### Added
 - Drawing method "image_shapes": antialiased shapes from small PNG images, works with every Tk 8.6 and 9 build without extra dependencies
 - Two-finger touchpad scrolling for CTkScrollableFrame with Tk 9 on Windows and macOS (<TouchpadScroll> event)

### Changed
 - "image_shapes" is the default drawing method on Linux, it's faster than "font_shapes" and doesn't need Xft
 - "font_shapes" switches to "image_shapes" if Tk can't use the CustomTkinter_shapes_font

### Fixed
 - Mouse wheel scrolling on Linux with Tk 9 for CTkScrollableFrame, CTkScrollbar and CTkSlider (Tk 9 sends <MouseWheel> instead of <Button-4>/<Button-5>)

## [6.0.0] - 2026-01-21
### Added
 - Showroom App, immediately available with the library installation
 - Gold theme
 - set(), index(), len() methods for those widgets that were suitable to use them
 - Attribute to CTkSegmentedButton to make it vertically instead of horizontally
 - Attribute to CTkTabview to configure the font for its CTkSegmentedButton
 - Possibility to add a border to CTkLabel
 - Mouse Wheel detection to CTkSlider and improved it on CTkScrollbar

### Changed
 - CTkButton triggers the command when the Mouse Button is released
 - CTkEntry and CTkTextbox lose focus when you click somewhere else
 - Clicking the Dropdown button again closes the menu for CTkComboBox and CTkOptionMenu
 - Improved/fixed configure() and cget() methods for all widgets
 - Improved Tab renaming for CTkTabview
 - Improved drag behavior for CTkScrollbar
 - Properly managed borders for CTkScrollableFrame
 - Fixed a bug that prevented setting a custom Icon for CTkToplevel
 - Fixed many bugs related to missing invocations or wrong names
 - Widgets on CTkScrollableFrame get scrolled properly when the mouse is over them and the mouse wheel is used

## [5.2.0] - 2022-05-02
### Added
 - Mostly bug fixes

## [5.1.0] - 2022-05-02
### Added
 - Added CTkScrollableFrame

### Changed
 - Changed license to MIT

## [5.0.0] - 2022-11-13
### Added
 - Added CTkTextbox with automatic x and y scrollbars, corner_radius, border_width, border_spacing
 - Added CTkSegmentedButton
 - Added CTkTabview
 - Added .cget() method to all widgets and windows
 - Added .bind() and .focus() methods to almost all widgets
 - Added 'anchor' option to CTkButton to position image and text inside the button
 - Added 'anchor' option to CTkOptionMenu and 'justify' option to CTkComboBox
 - Added CTkFont class
 - Added CTkImage class to replace PIL.ImageTk.PhotoImage, supports scaling and two images for appearance mode, supports configuring
 - Added missing configure options for multiple widgets

### Changed
 - Changed value for transparent colors (same as background) from None to 'transparent'
 - Changed 'text_font' attribute to 'font' in all widgets, changed 'dropdown_text_font' to 'dropdown_font'
 - Changed 'dropdown_color' attribute to 'dropdown_fg_color' for combobox, optionmenu
 - Changed 'orient' attribute of CTkProgressBar and CTkSlider to 'orientation'
 - Width and height attributes of CTkCheckBox, CTkRadioButton, CTkSwitch now describe the outer dimensions of the whole widget. The button/switch size is described by separate attributes like checkbox_width, checkbox_height
 - font attribute must be tuple or CTkFont now, all size values are measured in pixel now
 - Changed dictionary key 'window_bg_color' to 'window' in theme files
 - CTkInputDialog attributes completely changed
 - CTkScrollbar attributes scrollbar_color, scrollbar_hover_color changed to button_color, button_hover_color

### Removed
 - Removed setter and getter functions like set_text in CTkButton
 - Removed bg and background attribute from CTk and CTkToplevel, always use fg_color
 - Removed Settings class and moved settings to widget and window classes
 - removed customtkinter.set_spacing_scaling(), now set_widget_scaling() is used for spacing too

## [4.6.0] - 2022-09-17
### Added
 - CTkProgressBar indeterminate mode, automatic progress loop with .start() and .stop()

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
