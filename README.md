# Home Assistant Community Add-on: ElOverBlik-helper

El overblik-helper is a Home-assistant(hassio) addon to ingest hourly energy uasge from the [El overblik](https://github.com/JonasPed/homeassistant-eloverblik) custom component into influx as a timeseries.

you should be able to run this locally (docker or python) as well if you don't want to use the add-on.

in the app folder there is a local.json file when not running as a hassio addon the script should automatically use that file instead (please keep in mind that some keys might be missing in it so you might have to add them yourself when you set up your env)

feel free to open a issue if you need help with running this either as a add-on or locally.

## About

Everything about this is probably wrong but it works on my machine.

## License

MIT License

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.