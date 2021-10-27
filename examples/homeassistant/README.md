# What

![](https://community-home-assistant-assets.s3.dualstack.us-west-2.amazonaws.com/original/3X/0/b/0bad2a8e1b4494b8c7ae209a103c8cf142c7543f.jpeg)

# Setup

This was tested and works with Home Assistant 0.96.

You need to clone this folder to '{config path}/custom_components'.
The commands below should create the correct hierarchy while not downloading the whole code, yet allowing you to upgrade.

```
# Modify the following line to replace the path after "cd" to match your folder structure
cd home-assistant/config/custom_components
git clone --depth=1 https://github.com/Fusion/pywhistle.git --no-checkout
cd pywhistle
git checkout master -- examples/homeassistant
cd ..
ln -s pywhistle/examples/homeassistant whistle
```

Note that the organization suggested below for your yaml files may not match your own. In that case, I trust that you will know which files to modify.

Add the device tracker to 'configuration.yaml':

```
device_tracker:
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
  - platform: template
    sensors:
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
      charlie_distance:
        friendly_name: "Distance"
        icon_template: mdi:map-marker-distance
        value_template: '{{ state_attr("device_tracker.whistle_charlie", "activity_distance") | round(1) }}'
        unit_of_measurement: 'miles'
      charlie_calories:
        friendly_name: "Calories"
        icon_template: mdi:run
        value_template: '{{ state_attr("device_tracker.whistle_charlie", "activity_calories") | round(1) }}'
        unit_of_measurement: 'calories'
      charlie_battery_days_left:
        friendly_name: "Battery Days Left"
        icon_template: mdi:calendar-clock
        value_template: '{{ state_attr("device_tracker.whistle_charlie", "battery_days_left") }}'
        unit_of_measurement: 'days'
      charlie_battery_24h_wifi_usage:
        friendly_name: "Battery WiFi Usage"
        icon_template: mdi:wifi
        value_template: '{{ state_attr("device_tracker.whistle_charlie", "24h_battery_wifi_usage") }}'
        unit_of_measurement: '%'
      charlie_battery_24h_cell_usage:
        friendly_name: "Battery Cellular Usage"
        icon_template: mdi:cellphone-basic
        value_template: '{{ state_attr("device_tracker.whistle_charlie", "24h_battery_cellular_usage") }}'
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
                  - sensor.charlie_distance
                  - sensor.charlie_calories
                  - sensor.charlie_battery_24h_wifi_usage
                  - sensor.charlie_battery_24h_cell_usage
                  - sensor.charlie_battery_days_left

```
