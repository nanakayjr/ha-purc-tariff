# Changelog

All notable changes to this integration are documented in this file.

## [1.1.0] - 2026-08-08

### Added

- 💧 Optional **water tariff** tracking (GHS/m³), sourced from the PURC [Water Tariff Reckoner](https://www.purcghapp.com/Water.aspx). Opt in during setup by selecting "Also track water tariffs" and choosing your water customer category.
- 🔘 **Force Update** button entity to trigger an immediate refresh from the PURC website on demand, instead of waiting for the daily automatic refresh.
- 🕒 **Last Updated** sensor showing the timestamp of the last successful tariff fetch.
- 💾 Tariff values are now cached to disk and restored immediately on Home Assistant restart, instead of showing `unknown` until the first refresh completes.
- 🔁 Sensor values are now re-announced every minute (without any extra requests to the PURC website) so entities never look stale between daily refreshes.

### Changed

- All numeric sensor values are now rounded to 2 decimal places (previously 5).
- The coordinator now uses Home Assistant's `TimestampDataUpdateCoordinator`, which is required for the new "Last Updated" sensor and fixes a potential `AttributeError` on `last_update_success_time` used by diagnostics.

## [1.0.0] - Initial release

- Automatic tariff discovery from the PURC Electricity Tariff Reckoner.
- Support for Residential and Non-Residential/SLT customer categories.
- Lifeline, regular, and high consumption tariff sensors, levy percentage, and service charge sensors.
- Daily automatic refresh with graceful fallback to last known values.
- Built-in diagnostics support.
