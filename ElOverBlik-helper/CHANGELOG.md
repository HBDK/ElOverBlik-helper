# Changelog

OBS: Version 0.10 and 0.11 are not compatible with prior measurements so you have to insert data into a new series or drop existing data. (old data can be re inserted using the bulk loader)

## 0.10

- [Cast Value to float](https://github.com/HBDK/ElOverBlik-helper/issues/5): this will probably break existing data

## 0.11

- [Configurable measurement name](https://github.com/HBDK/ElOverBlik-helper/issues/7)
- Ingest time changed from timestamp to datetime
- Values are now inserted at the end of the hour instead of the middle
- [Errors during insert are now handled and will be reported if webhooks are enabled](https://github.com/HBDK/ElOverBlik-helper/issues/8)
- Added Bulk loader

## 0.12

added atributes:

- Week Number
- Year
- day of week
- Week and year
- Month and year

## 0.13

- add icon and fix description.
- fix addon url

## 0.14

- add support for multiple sets of measurements
