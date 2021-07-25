![PyPI - Downloads](https://img.shields.io/pypi/dd/pywhistle)

This is a very basic library to query Whistle.app's API for Whistle 3 devices. It is also compatible with all new devices.

The API is not published, so it may break eventually (although compatibility has not broken in several years)

In the `examples/homeassistant` folder you will find a custom component to integrate this information in your dashboard.

Available information for each pet, including dailies:

- Activity goal, in minutes
- Activity streak
- Activity, in minutes
- Rest time, in minutes
- Distance walked
- Calories
- Battery level
- Battery wifi usage
- Battery cell usage
- Battery days left

To use the library itself in your project:

```
pip install pywhistle
```

You can specify it in `requirements.txt` as well:

```
pywhistle==0.0.4
```



