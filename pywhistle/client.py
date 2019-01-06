from aiohttp import ClientSession, client_exceptions

WHISTLE_CONST = {
        "proto": "https",
        "remote_host": "app.whistle.com",
        "endpoint": "api"
}


class Client:


    """
    Returns a string: URL(host, endpoint, resource)
    """
    def url(self, config, resource) -> str:
        return "%s://%s/%s/%s" % (config["proto"], config["remote_host"], config["endpoint"], resource)


    """
    Returns default headers as understood by the Whistle API
    Not invoked when retrieving a token.
    """
    def headers(self, config, token):
        return {
            "Host": config['remote_host'],
            "Content-Type": "application/json",
            "Connection": "keep-alive",
            "Accept": "application/vnd.whistle.com.v4+json",
            "Accept-Language": "en-us",
            "Accept-Encoding": "br, gzip, deflate",
            "User-Agent": "Winston/2.5.3 (iPhone; iOS 12.0.1; Build:1276; Scale/2.0)",
            "Authorization": "Bearer %s" % token
    }


    """
    Performs AIO request. Covers all verbs.
    Returns json payload.
    Raises exception if received http error code.
    """
    async def request(
            self,
            config,
            method: str,
            resource: str,
            headers: dict = None,
            data: dict = None
            ) -> dict:
        if not headers:
            headers = {}
        async with self._websession.request(
                method,
                self.url(config, resource),
                headers=headers,
                data=data) as r:
            r.raise_for_status()
            return await r.json()


    """
    Helper to retrieve a single resource, such as '/pet'
    """
    async def get_resource(self, config, token, resource):
        return await self.request(
                config,
                method='get',
                resource=resource,
                headers=self.headers(config, token)
                )


    """
    Attempts login with credentials provided in init()
    Returns authorization token for future requests.
    """
    async def login(self, config) -> str:
        return (await self.request(
                config,
                method='post',
                resource='login',
                data={
                    "email": self._username,
                    "password": self._password
                }))['auth_token']


    """
    Returns:
        pets: array of
            id, gender, name,
            profile_photo_url_sizes: dict of size(wxh):url,
            profile/breed, dob, address, etc.
    """
    async def get_pets(self):
        return await self.get_resource(self._config, self._token, 'pets')


    """
    Returns:
        owners: array of
            id, first_name, last_name, current_user, searchable, email,
            profile_photo_url_sizes': dict of size (wxh): url
    """
    async def get_owners(self, pet_id):
        return await self.get_resource(self._config, self._token, "pets/%s/owners" % pet_id)


    """
    Returns:
        array of
            address, name,
            id,
            latitude, longitude, radius_meters,
            shape,
            outline: array of lat/long if shape == polygon,
            per_ids: array of pet ids,
            wifi network information
    """
    async def get_places(self):
        return await self.get_resource(self._config, self._token, "places")


    """
    Returns:
        stats: dict of
            average_minutes_active, average_minutes_rest, average_calories, average_distance, current_streak, longest_streak, most_active_day
    """
    async def get_stats(self, pet_id):
        return await self.get_resource(self._config, self._token, "pets/%s/stats" % pet_id)


    """
    Returns:
        timeline_items: array of
            type ('inside'),
            data: dict of
                place: array of
                    id, name
                start_time, end_time
            - or -
            type('outside'),
            data: dict of
                static_map_url: a google map url,
                origin, destination
    """
    async def get_timeline(self, pet_id):
        return await self.get_resource(self._config, self._token, "pets/%s/timelines/location" % pet_id)


    """
    Returns:
        dailies: array of
            activity_goal, minutes_active, minutes_rest,
            calories, distance,
            day_number, excluded, timestamp, updated_at
    """
    async def get_dailies(self, pet_id):
        return await self.get_resource(self._config, self._token, "pets/%s/dailies" % pet_id)


    """
    Returns:
        daily: dict of
            activities_goal, etc,
            bar_chart_18min: array of values
    """
    async def get_dailies_day(self, pet_id, day_id):
        return await self.get_resource(self._config, self._token, "pets/%s/dailies/%s" % (pet_id, day_id))


    """
    This one is lots of fun. Gamification for the win!

    Returns:
        achievements: array of
            id, earned_achievement_id, actionable, type,
            title, short_name,
            background_color, strike_color,
            badge_images: dict of size (wxh): url,
            template_type, template_properties: dict of
                header, footer, body, description (full text),
                earned, earned_timestamp,
                type_properties: dict of
                    progressive_type, unit, goal_value, current_value, decimal_places
    """
    async def get_achievements(self, pet_id):
        return await self.get_resource(self._config, self._token, "pets/%s/achievements" % pet_id)


    async def async_init(self, whistle_const = WHISTLE_CONST) -> None:
        self._config = whistle_const
        if self._token is None:
            self._token = await self.login(self._config)


    def __init__(
            self,
            email: str,
            password: str,
            websession: ClientSession
            ) -> None:
        self._config = None
        self._token = None
        self._username = email
        self._password = password
        self._websession = websession
