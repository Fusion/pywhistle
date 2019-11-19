# What

![](https://community-home-assistant-assets.s3.dualstack.us-west-2.amazonaws.com/original/3X/0/b/0bad2a8e1b4494b8c7ae209a103c8cf142c7543f.jpeg)

# Setup

This was tested and works with Home Assistant 0.96.

You need to clone this folder to '{config path}/custom_components'.
The commands below should create the correct hierarchy while not downloading the whole code, yet allowing you to upgrade.

```
git clone --depth=1 git@github.com:Fusion/pywhistle.git --no-checkout
cd pywhistle
git checkout master -- examples/homeassistant
ln -s $(pwd)/examples/homeassistant ../whistle
```

Note that the organization suggested below for your yaml files may not match your own. In that case, I trust that you will know which files to modify.

Add the device tracker to 'configuration.yaml':

```
device_tracker:
  ...
  - platform: whistle
    username: !secret whistle_username
    password: !secret whistle_password
    monitored_variables:
      - WHISTLE
```

Provide the correct credentials in 'secrets.yaml':

```
whistle_username: {your email address}
whistle_password: {your password}
```

Declare the following template in 'configuration.yaml', in order to retrieve the tracker's attributes.
You will have to replace 'whistle_charlie' with your tracker's name as found in the 'states' tab:

```
sensor:
  ...
      charlie_goal_minutes:
        friendly_name: "Activity Goal"
        icon_template: mdi:trophy-outline
        value_template: '{{ state_attr("device_tracker.whistle_charlie", "activity_goal") }}'
        unit_of_measurement: "minutes"
      charlie_goal_streak:
        friendly_name: "Activity Streak"
        icon_template: mdi:chart-timeline
        value_template: '{{ state_attr("device_tracker.whistle_charlie", "activity_streak") }}'
        unit_of_measurement: "days"
      charlie_active_minutes:
        friendly_name: "Active For"
        icon_template: mdi:dog-side
        value_template: '{{ state_attr("device_tracker.whistle_charlie", "activity_minutes_active") }}'
        unit_of_measurement: "minutes"
      charlie_rest_minutes:
        friendly_name: "Rest For"
        icon_template: mdi:sleep
        value_template: '{{ state_attr("device_tracker.whistle_charlie", "activity_minutes_rest") }}'
        unit_of_measurement: "minutes"
      charlie_battery_level:
        friendly_name: "Battery Level"
        icon_template: mdi:battery
        value_template: '{{ state_attr("device_tracker.whistle_charlie", "battery_level") }}'
        unit_of_measurement: '%'
```

Then, use these templates in 'ui-lovelace.yaml' -- 
I am using the 'fold-entity-row' custom card, but you do not have to:

```
views:
  ...
    ...
      ...
        ...
          ...
            ...
              - type: custom:fold-entity-row
                head: device_tracker.whistle_charlie
                items:
                  - sensor.charlie_battery_level
                  - sensor.charlie_goal_minutes
                  - sensor.charlie_goal_streak
                  - sensor.charlie_active_minutes
                  - sensor.charlie_rest_minutes

```
