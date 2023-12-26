# dimtim-utils

Python utils for Dim-Tim projects

### Changelog

__v0.1.8__ _\[25.12.2023\]_

* add `utils.proxy.DictProxy` class

-------------------------------------------------------------------------------

__v0.1.7__ _\[21.12.2023\]_

* optimize command runner
* add `utils.importing.load_file_as_module(str, str?, bool?)`

-------------------------------------------------------------------------------

__v0.1.6__ _\[14.12.2023\]_

* minor fixes

-------------------------------------------------------------------------------

__v0.1.5__ _\[14.12.2023\]_

* add `utils.importing.import_string(str)` method
* add `PydanticV2` compatibility to json serializer

-------------------------------------------------------------------------------

__v0.1.4__ _\[13.09.2023\]_

* update requirements
* add `tzdata` as dependency

-------------------------------------------------------------------------------

__v0.1.3__ _\[24.03.2023\]_

* `utils.timezone` package fixes
* deprecation of `pytz` library in favor of `zoneinfo`

-------------------------------------------------------------------------------

__v0.1.2__ _\[06.10.2022\]_

* some fixes and update requirements

-------------------------------------------------------------------------------

__v0.1.1__ _\[15.06.2022\]_

* fixed `helpers.management.cron_command.CronCommand` cron tasks setup

-------------------------------------------------------------------------------

__v0.1.0__ _\[14.06.2022\]_

* added `helpers.management.runner.CommandRunner` class
* added `dtrun` console command

-------------------------------------------------------------------------------

__v0.0.18__ _\[07.06.2022\]_

* fix `utils.json.JsonEncoder` set and frozenset serialization

-------------------------------------------------------------------------------

__v0.0.17__ _\[26.05.2022\]_

* fix `utils.json.JsonEncoder` datetime serialization
* update requirements

-------------------------------------------------------------------------------

__v0.0.16__ _\[31.01.2022\]_

* fix `utils.terminal.show_progress(int, int, str?, IOBase?)` function

-------------------------------------------------------------------------------

__v0.0.15__ _\[31.01.2022\]_

* added `utils.terminal.show_progress(int, int, str?, IOBase?)` function

-------------------------------------------------------------------------------

__v0.0.14__ _\[23.01.2022\]_

* fix `helpers.management` import without installed __python-crontab__ library

-------------------------------------------------------------------------------

__v0.0.13__ _\[22.01.2022\]_

* added `out` argument to `utils.debug.timeit(str?, Logger?)` to specify logger output
* small fix in importing module
* added `utils.text.to_kebab_case(str)` function
* added some tests

-------------------------------------------------------------------------------

__v0.0.12__ _\[17.01.2022\]_

* small json serializer fixes

-------------------------------------------------------------------------------

__v0.0.11__ _\[17.01.2022\]_

* small fixes

-------------------------------------------------------------------------------

__v0.0.10__ _\[17.01.2022\]_

* small fixes

-------------------------------------------------------------------------------

__v0.0.9__ _\[17.01.2022\]_

* added `utils.decorators.freezeargs()` decorator

-------------------------------------------------------------------------------

__v0.0.8__ _\[10.12.2021\]_

* update `utils.debug.timeit(str?)` function

-------------------------------------------------------------------------------

__v0.0.7__ _\[10.12.2021\]_

* added `utils.text.inline(str)` function
