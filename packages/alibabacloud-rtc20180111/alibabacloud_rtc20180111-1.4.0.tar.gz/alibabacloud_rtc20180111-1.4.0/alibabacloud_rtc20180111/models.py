# -*- coding: utf-8 -*-
# This file is auto-generated, don't edit it. Thanks.
from Tea.model import TeaModel
from typing import List, Dict


class AddRecordTemplateRequestBackgrounds(TeaModel):
    def __init__(
        self,
        display: int = None,
        height: float = None,
        url: str = None,
        width: float = None,
        x: float = None,
        y: float = None,
        zorder: int = None,
    ):
        self.display = display
        self.height = height
        self.url = url
        self.width = width
        self.x = x
        self.y = y
        self.zorder = zorder

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.display is not None:
            result['Display'] = self.display
        if self.height is not None:
            result['Height'] = self.height
        if self.url is not None:
            result['Url'] = self.url
        if self.width is not None:
            result['Width'] = self.width
        if self.x is not None:
            result['X'] = self.x
        if self.y is not None:
            result['Y'] = self.y
        if self.zorder is not None:
            result['ZOrder'] = self.zorder
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Display') is not None:
            self.display = m.get('Display')
        if m.get('Height') is not None:
            self.height = m.get('Height')
        if m.get('Url') is not None:
            self.url = m.get('Url')
        if m.get('Width') is not None:
            self.width = m.get('Width')
        if m.get('X') is not None:
            self.x = m.get('X')
        if m.get('Y') is not None:
            self.y = m.get('Y')
        if m.get('ZOrder') is not None:
            self.zorder = m.get('ZOrder')
        return self


class AddRecordTemplateRequestClockWidgets(TeaModel):
    def __init__(
        self,
        font_color: int = None,
        font_size: int = None,
        font_type: int = None,
        x: float = None,
        y: float = None,
        zorder: int = None,
    ):
        self.font_color = font_color
        self.font_size = font_size
        self.font_type = font_type
        self.x = x
        self.y = y
        self.zorder = zorder

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.font_color is not None:
            result['FontColor'] = self.font_color
        if self.font_size is not None:
            result['FontSize'] = self.font_size
        if self.font_type is not None:
            result['FontType'] = self.font_type
        if self.x is not None:
            result['X'] = self.x
        if self.y is not None:
            result['Y'] = self.y
        if self.zorder is not None:
            result['ZOrder'] = self.zorder
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('FontColor') is not None:
            self.font_color = m.get('FontColor')
        if m.get('FontSize') is not None:
            self.font_size = m.get('FontSize')
        if m.get('FontType') is not None:
            self.font_type = m.get('FontType')
        if m.get('X') is not None:
            self.x = m.get('X')
        if m.get('Y') is not None:
            self.y = m.get('Y')
        if m.get('ZOrder') is not None:
            self.zorder = m.get('ZOrder')
        return self


class AddRecordTemplateRequestWatermarks(TeaModel):
    def __init__(
        self,
        alpha: float = None,
        display: int = None,
        height: float = None,
        url: str = None,
        width: float = None,
        x: float = None,
        y: float = None,
        zorder: int = None,
    ):
        self.alpha = alpha
        self.display = display
        self.height = height
        self.url = url
        self.width = width
        self.x = x
        self.y = y
        self.zorder = zorder

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.alpha is not None:
            result['Alpha'] = self.alpha
        if self.display is not None:
            result['Display'] = self.display
        if self.height is not None:
            result['Height'] = self.height
        if self.url is not None:
            result['Url'] = self.url
        if self.width is not None:
            result['Width'] = self.width
        if self.x is not None:
            result['X'] = self.x
        if self.y is not None:
            result['Y'] = self.y
        if self.zorder is not None:
            result['ZOrder'] = self.zorder
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Alpha') is not None:
            self.alpha = m.get('Alpha')
        if m.get('Display') is not None:
            self.display = m.get('Display')
        if m.get('Height') is not None:
            self.height = m.get('Height')
        if m.get('Url') is not None:
            self.url = m.get('Url')
        if m.get('Width') is not None:
            self.width = m.get('Width')
        if m.get('X') is not None:
            self.x = m.get('X')
        if m.get('Y') is not None:
            self.y = m.get('Y')
        if m.get('ZOrder') is not None:
            self.zorder = m.get('ZOrder')
        return self


class AddRecordTemplateRequest(TeaModel):
    def __init__(
        self,
        app_id: str = None,
        background_color: int = None,
        backgrounds: List[AddRecordTemplateRequestBackgrounds] = None,
        clock_widgets: List[AddRecordTemplateRequestClockWidgets] = None,
        delay_stop_time: int = None,
        enable_m3u_8date_time: bool = None,
        file_split_interval: int = None,
        formats: List[str] = None,
        http_callback_url: str = None,
        layout_ids: List[int] = None,
        media_encode: int = None,
        mns_queue: str = None,
        name: str = None,
        oss_bucket: str = None,
        oss_endpoint: str = None,
        oss_file_prefix: str = None,
        owner_id: int = None,
        task_profile: str = None,
        watermarks: List[AddRecordTemplateRequestWatermarks] = None,
    ):
        self.app_id = app_id
        self.background_color = background_color
        self.backgrounds = backgrounds
        self.clock_widgets = clock_widgets
        self.delay_stop_time = delay_stop_time
        self.enable_m3u_8date_time = enable_m3u_8date_time
        self.file_split_interval = file_split_interval
        self.formats = formats
        self.http_callback_url = http_callback_url
        self.layout_ids = layout_ids
        self.media_encode = media_encode
        self.mns_queue = mns_queue
        self.name = name
        self.oss_bucket = oss_bucket
        self.oss_endpoint = oss_endpoint
        self.oss_file_prefix = oss_file_prefix
        self.owner_id = owner_id
        self.task_profile = task_profile
        self.watermarks = watermarks

    def validate(self):
        if self.backgrounds:
            for k in self.backgrounds:
                if k:
                    k.validate()
        if self.clock_widgets:
            for k in self.clock_widgets:
                if k:
                    k.validate()
        if self.watermarks:
            for k in self.watermarks:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.app_id is not None:
            result['AppId'] = self.app_id
        if self.background_color is not None:
            result['BackgroundColor'] = self.background_color
        result['Backgrounds'] = []
        if self.backgrounds is not None:
            for k in self.backgrounds:
                result['Backgrounds'].append(k.to_map() if k else None)
        result['ClockWidgets'] = []
        if self.clock_widgets is not None:
            for k in self.clock_widgets:
                result['ClockWidgets'].append(k.to_map() if k else None)
        if self.delay_stop_time is not None:
            result['DelayStopTime'] = self.delay_stop_time
        if self.enable_m3u_8date_time is not None:
            result['EnableM3u8DateTime'] = self.enable_m3u_8date_time
        if self.file_split_interval is not None:
            result['FileSplitInterval'] = self.file_split_interval
        if self.formats is not None:
            result['Formats'] = self.formats
        if self.http_callback_url is not None:
            result['HttpCallbackUrl'] = self.http_callback_url
        if self.layout_ids is not None:
            result['LayoutIds'] = self.layout_ids
        if self.media_encode is not None:
            result['MediaEncode'] = self.media_encode
        if self.mns_queue is not None:
            result['MnsQueue'] = self.mns_queue
        if self.name is not None:
            result['Name'] = self.name
        if self.oss_bucket is not None:
            result['OssBucket'] = self.oss_bucket
        if self.oss_endpoint is not None:
            result['OssEndpoint'] = self.oss_endpoint
        if self.oss_file_prefix is not None:
            result['OssFilePrefix'] = self.oss_file_prefix
        if self.owner_id is not None:
            result['OwnerId'] = self.owner_id
        if self.task_profile is not None:
            result['TaskProfile'] = self.task_profile
        result['Watermarks'] = []
        if self.watermarks is not None:
            for k in self.watermarks:
                result['Watermarks'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('AppId') is not None:
            self.app_id = m.get('AppId')
        if m.get('BackgroundColor') is not None:
            self.background_color = m.get('BackgroundColor')
        self.backgrounds = []
        if m.get('Backgrounds') is not None:
            for k in m.get('Backgrounds'):
                temp_model = AddRecordTemplateRequestBackgrounds()
                self.backgrounds.append(temp_model.from_map(k))
        self.clock_widgets = []
        if m.get('ClockWidgets') is not None:
            for k in m.get('ClockWidgets'):
                temp_model = AddRecordTemplateRequestClockWidgets()
                self.clock_widgets.append(temp_model.from_map(k))
        if m.get('DelayStopTime') is not None:
            self.delay_stop_time = m.get('DelayStopTime')
        if m.get('EnableM3u8DateTime') is not None:
            self.enable_m3u_8date_time = m.get('EnableM3u8DateTime')
        if m.get('FileSplitInterval') is not None:
            self.file_split_interval = m.get('FileSplitInterval')
        if m.get('Formats') is not None:
            self.formats = m.get('Formats')
        if m.get('HttpCallbackUrl') is not None:
            self.http_callback_url = m.get('HttpCallbackUrl')
        if m.get('LayoutIds') is not None:
            self.layout_ids = m.get('LayoutIds')
        if m.get('MediaEncode') is not None:
            self.media_encode = m.get('MediaEncode')
        if m.get('MnsQueue') is not None:
            self.mns_queue = m.get('MnsQueue')
        if m.get('Name') is not None:
            self.name = m.get('Name')
        if m.get('OssBucket') is not None:
            self.oss_bucket = m.get('OssBucket')
        if m.get('OssEndpoint') is not None:
            self.oss_endpoint = m.get('OssEndpoint')
        if m.get('OssFilePrefix') is not None:
            self.oss_file_prefix = m.get('OssFilePrefix')
        if m.get('OwnerId') is not None:
            self.owner_id = m.get('OwnerId')
        if m.get('TaskProfile') is not None:
            self.task_profile = m.get('TaskProfile')
        self.watermarks = []
        if m.get('Watermarks') is not None:
            for k in m.get('Watermarks'):
                temp_model = AddRecordTemplateRequestWatermarks()
                self.watermarks.append(temp_model.from_map(k))
        return self


class AddRecordTemplateResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
        template_id: str = None,
    ):
        self.request_id = request_id
        self.template_id = template_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.template_id is not None:
            result['TemplateId'] = self.template_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('TemplateId') is not None:
            self.template_id = m.get('TemplateId')
        return self


class AddRecordTemplateResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: AddRecordTemplateResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.status_code, 'status_code')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = AddRecordTemplateResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class CreateAutoLiveStreamRuleRequest(TeaModel):
    def __init__(
        self,
        app_id: str = None,
        call_back: str = None,
        channel_id_prefixes: List[str] = None,
        channel_ids: List[str] = None,
        media_encode: int = None,
        owner_id: int = None,
        play_domain: str = None,
        rule_name: str = None,
    ):
        self.app_id = app_id
        self.call_back = call_back
        self.channel_id_prefixes = channel_id_prefixes
        self.channel_ids = channel_ids
        self.media_encode = media_encode
        self.owner_id = owner_id
        self.play_domain = play_domain
        self.rule_name = rule_name

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.app_id is not None:
            result['AppId'] = self.app_id
        if self.call_back is not None:
            result['CallBack'] = self.call_back
        if self.channel_id_prefixes is not None:
            result['ChannelIdPrefixes'] = self.channel_id_prefixes
        if self.channel_ids is not None:
            result['ChannelIds'] = self.channel_ids
        if self.media_encode is not None:
            result['MediaEncode'] = self.media_encode
        if self.owner_id is not None:
            result['OwnerId'] = self.owner_id
        if self.play_domain is not None:
            result['PlayDomain'] = self.play_domain
        if self.rule_name is not None:
            result['RuleName'] = self.rule_name
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('AppId') is not None:
            self.app_id = m.get('AppId')
        if m.get('CallBack') is not None:
            self.call_back = m.get('CallBack')
        if m.get('ChannelIdPrefixes') is not None:
            self.channel_id_prefixes = m.get('ChannelIdPrefixes')
        if m.get('ChannelIds') is not None:
            self.channel_ids = m.get('ChannelIds')
        if m.get('MediaEncode') is not None:
            self.media_encode = m.get('MediaEncode')
        if m.get('OwnerId') is not None:
            self.owner_id = m.get('OwnerId')
        if m.get('PlayDomain') is not None:
            self.play_domain = m.get('PlayDomain')
        if m.get('RuleName') is not None:
            self.rule_name = m.get('RuleName')
        return self


class CreateAutoLiveStreamRuleResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
        rule_id: int = None,
    ):
        self.request_id = request_id
        self.rule_id = rule_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.rule_id is not None:
            result['RuleId'] = self.rule_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('RuleId') is not None:
            self.rule_id = m.get('RuleId')
        return self


class CreateAutoLiveStreamRuleResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: CreateAutoLiveStreamRuleResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.status_code, 'status_code')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = CreateAutoLiveStreamRuleResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class CreateEventSubscribeRequest(TeaModel):
    def __init__(
        self,
        app_id: str = None,
        callback_url: str = None,
        channel_id: str = None,
        client_token: str = None,
        events: List[str] = None,
        need_callback_auth: bool = None,
        owner_id: int = None,
        role: int = None,
        users: List[str] = None,
    ):
        self.app_id = app_id
        self.callback_url = callback_url
        self.channel_id = channel_id
        self.client_token = client_token
        self.events = events
        self.need_callback_auth = need_callback_auth
        self.owner_id = owner_id
        self.role = role
        self.users = users

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.app_id is not None:
            result['AppId'] = self.app_id
        if self.callback_url is not None:
            result['CallbackUrl'] = self.callback_url
        if self.channel_id is not None:
            result['ChannelId'] = self.channel_id
        if self.client_token is not None:
            result['ClientToken'] = self.client_token
        if self.events is not None:
            result['Events'] = self.events
        if self.need_callback_auth is not None:
            result['NeedCallbackAuth'] = self.need_callback_auth
        if self.owner_id is not None:
            result['OwnerId'] = self.owner_id
        if self.role is not None:
            result['Role'] = self.role
        if self.users is not None:
            result['Users'] = self.users
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('AppId') is not None:
            self.app_id = m.get('AppId')
        if m.get('CallbackUrl') is not None:
            self.callback_url = m.get('CallbackUrl')
        if m.get('ChannelId') is not None:
            self.channel_id = m.get('ChannelId')
        if m.get('ClientToken') is not None:
            self.client_token = m.get('ClientToken')
        if m.get('Events') is not None:
            self.events = m.get('Events')
        if m.get('NeedCallbackAuth') is not None:
            self.need_callback_auth = m.get('NeedCallbackAuth')
        if m.get('OwnerId') is not None:
            self.owner_id = m.get('OwnerId')
        if m.get('Role') is not None:
            self.role = m.get('Role')
        if m.get('Users') is not None:
            self.users = m.get('Users')
        return self


class CreateEventSubscribeResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
        subscribe_id: str = None,
    ):
        self.request_id = request_id
        self.subscribe_id = subscribe_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.subscribe_id is not None:
            result['SubscribeId'] = self.subscribe_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('SubscribeId') is not None:
            self.subscribe_id = m.get('SubscribeId')
        return self


class CreateEventSubscribeResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: CreateEventSubscribeResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.status_code, 'status_code')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = CreateEventSubscribeResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class CreateMPULayoutRequestPanes(TeaModel):
    def __init__(
        self,
        height: float = None,
        major_pane: int = None,
        pane_id: int = None,
        width: float = None,
        x: float = None,
        y: float = None,
        zorder: int = None,
    ):
        self.height = height
        self.major_pane = major_pane
        self.pane_id = pane_id
        self.width = width
        self.x = x
        self.y = y
        self.zorder = zorder

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.height is not None:
            result['Height'] = self.height
        if self.major_pane is not None:
            result['MajorPane'] = self.major_pane
        if self.pane_id is not None:
            result['PaneId'] = self.pane_id
        if self.width is not None:
            result['Width'] = self.width
        if self.x is not None:
            result['X'] = self.x
        if self.y is not None:
            result['Y'] = self.y
        if self.zorder is not None:
            result['ZOrder'] = self.zorder
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Height') is not None:
            self.height = m.get('Height')
        if m.get('MajorPane') is not None:
            self.major_pane = m.get('MajorPane')
        if m.get('PaneId') is not None:
            self.pane_id = m.get('PaneId')
        if m.get('Width') is not None:
            self.width = m.get('Width')
        if m.get('X') is not None:
            self.x = m.get('X')
        if m.get('Y') is not None:
            self.y = m.get('Y')
        if m.get('ZOrder') is not None:
            self.zorder = m.get('ZOrder')
        return self


class CreateMPULayoutRequest(TeaModel):
    def __init__(
        self,
        app_id: str = None,
        audio_mix_count: int = None,
        name: str = None,
        owner_id: int = None,
        panes: List[CreateMPULayoutRequestPanes] = None,
    ):
        self.app_id = app_id
        self.audio_mix_count = audio_mix_count
        self.name = name
        self.owner_id = owner_id
        self.panes = panes

    def validate(self):
        if self.panes:
            for k in self.panes:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.app_id is not None:
            result['AppId'] = self.app_id
        if self.audio_mix_count is not None:
            result['AudioMixCount'] = self.audio_mix_count
        if self.name is not None:
            result['Name'] = self.name
        if self.owner_id is not None:
            result['OwnerId'] = self.owner_id
        result['Panes'] = []
        if self.panes is not None:
            for k in self.panes:
                result['Panes'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('AppId') is not None:
            self.app_id = m.get('AppId')
        if m.get('AudioMixCount') is not None:
            self.audio_mix_count = m.get('AudioMixCount')
        if m.get('Name') is not None:
            self.name = m.get('Name')
        if m.get('OwnerId') is not None:
            self.owner_id = m.get('OwnerId')
        self.panes = []
        if m.get('Panes') is not None:
            for k in m.get('Panes'):
                temp_model = CreateMPULayoutRequestPanes()
                self.panes.append(temp_model.from_map(k))
        return self


class CreateMPULayoutResponseBody(TeaModel):
    def __init__(
        self,
        layout_id: int = None,
        request_id: str = None,
    ):
        self.layout_id = layout_id
        self.request_id = request_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.layout_id is not None:
            result['LayoutId'] = self.layout_id
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('LayoutId') is not None:
            self.layout_id = m.get('LayoutId')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        return self


class CreateMPULayoutResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: CreateMPULayoutResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.status_code, 'status_code')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = CreateMPULayoutResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DeleteAutoLiveStreamRuleRequest(TeaModel):
    def __init__(
        self,
        app_id: str = None,
        owner_id: int = None,
        rule_id: int = None,
    ):
        self.app_id = app_id
        self.owner_id = owner_id
        self.rule_id = rule_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.app_id is not None:
            result['AppId'] = self.app_id
        if self.owner_id is not None:
            result['OwnerId'] = self.owner_id
        if self.rule_id is not None:
            result['RuleId'] = self.rule_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('AppId') is not None:
            self.app_id = m.get('AppId')
        if m.get('OwnerId') is not None:
            self.owner_id = m.get('OwnerId')
        if m.get('RuleId') is not None:
            self.rule_id = m.get('RuleId')
        return self


class DeleteAutoLiveStreamRuleResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
    ):
        self.request_id = request_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        return self


class DeleteAutoLiveStreamRuleResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: DeleteAutoLiveStreamRuleResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.status_code, 'status_code')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = DeleteAutoLiveStreamRuleResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DeleteChannelRequest(TeaModel):
    def __init__(
        self,
        app_id: str = None,
        channel_id: str = None,
        owner_id: int = None,
    ):
        self.app_id = app_id
        self.channel_id = channel_id
        self.owner_id = owner_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.app_id is not None:
            result['AppId'] = self.app_id
        if self.channel_id is not None:
            result['ChannelId'] = self.channel_id
        if self.owner_id is not None:
            result['OwnerId'] = self.owner_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('AppId') is not None:
            self.app_id = m.get('AppId')
        if m.get('ChannelId') is not None:
            self.channel_id = m.get('ChannelId')
        if m.get('OwnerId') is not None:
            self.owner_id = m.get('OwnerId')
        return self


class DeleteChannelResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
    ):
        self.request_id = request_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        return self


class DeleteChannelResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: DeleteChannelResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.status_code, 'status_code')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = DeleteChannelResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DeleteEventSubscribeRequest(TeaModel):
    def __init__(
        self,
        app_id: str = None,
        owner_id: int = None,
        subscribe_id: str = None,
    ):
        self.app_id = app_id
        self.owner_id = owner_id
        self.subscribe_id = subscribe_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.app_id is not None:
            result['AppId'] = self.app_id
        if self.owner_id is not None:
            result['OwnerId'] = self.owner_id
        if self.subscribe_id is not None:
            result['SubscribeId'] = self.subscribe_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('AppId') is not None:
            self.app_id = m.get('AppId')
        if m.get('OwnerId') is not None:
            self.owner_id = m.get('OwnerId')
        if m.get('SubscribeId') is not None:
            self.subscribe_id = m.get('SubscribeId')
        return self


class DeleteEventSubscribeResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
    ):
        self.request_id = request_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        return self


class DeleteEventSubscribeResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: DeleteEventSubscribeResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.status_code, 'status_code')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = DeleteEventSubscribeResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DeleteMPULayoutRequest(TeaModel):
    def __init__(
        self,
        app_id: str = None,
        layout_id: int = None,
        owner_id: int = None,
    ):
        self.app_id = app_id
        self.layout_id = layout_id
        self.owner_id = owner_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.app_id is not None:
            result['AppId'] = self.app_id
        if self.layout_id is not None:
            result['LayoutId'] = self.layout_id
        if self.owner_id is not None:
            result['OwnerId'] = self.owner_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('AppId') is not None:
            self.app_id = m.get('AppId')
        if m.get('LayoutId') is not None:
            self.layout_id = m.get('LayoutId')
        if m.get('OwnerId') is not None:
            self.owner_id = m.get('OwnerId')
        return self


class DeleteMPULayoutResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
    ):
        self.request_id = request_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        return self


class DeleteMPULayoutResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: DeleteMPULayoutResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.status_code, 'status_code')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = DeleteMPULayoutResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DeleteRecordTemplateRequest(TeaModel):
    def __init__(
        self,
        app_id: str = None,
        owner_id: int = None,
        template_id: str = None,
    ):
        self.app_id = app_id
        # 1
        self.owner_id = owner_id
        self.template_id = template_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.app_id is not None:
            result['AppId'] = self.app_id
        if self.owner_id is not None:
            result['OwnerId'] = self.owner_id
        if self.template_id is not None:
            result['TemplateId'] = self.template_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('AppId') is not None:
            self.app_id = m.get('AppId')
        if m.get('OwnerId') is not None:
            self.owner_id = m.get('OwnerId')
        if m.get('TemplateId') is not None:
            self.template_id = m.get('TemplateId')
        return self


class DeleteRecordTemplateResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
    ):
        self.request_id = request_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        return self


class DeleteRecordTemplateResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: DeleteRecordTemplateResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.status_code, 'status_code')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = DeleteRecordTemplateResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DescribeAppKeyRequest(TeaModel):
    def __init__(
        self,
        app_id: str = None,
        owner_id: int = None,
    ):
        self.app_id = app_id
        self.owner_id = owner_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.app_id is not None:
            result['AppId'] = self.app_id
        if self.owner_id is not None:
            result['OwnerId'] = self.owner_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('AppId') is not None:
            self.app_id = m.get('AppId')
        if m.get('OwnerId') is not None:
            self.owner_id = m.get('OwnerId')
        return self


class DescribeAppKeyResponseBody(TeaModel):
    def __init__(
        self,
        app_key: str = None,
        request_id: str = None,
    ):
        # AppKey。
        self.app_key = app_key
        self.request_id = request_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.app_key is not None:
            result['AppKey'] = self.app_key
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('AppKey') is not None:
            self.app_key = m.get('AppKey')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        return self


class DescribeAppKeyResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: DescribeAppKeyResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.status_code, 'status_code')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = DescribeAppKeyResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DescribeAppsRequest(TeaModel):
    def __init__(
        self,
        app_id: str = None,
        order: str = None,
        owner_id: int = None,
        page_num: int = None,
        page_size: int = None,
        status: str = None,
    ):
        self.app_id = app_id
        self.order = order
        self.owner_id = owner_id
        self.page_num = page_num
        self.page_size = page_size
        self.status = status

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.app_id is not None:
            result['AppId'] = self.app_id
        if self.order is not None:
            result['Order'] = self.order
        if self.owner_id is not None:
            result['OwnerId'] = self.owner_id
        if self.page_num is not None:
            result['PageNum'] = self.page_num
        if self.page_size is not None:
            result['PageSize'] = self.page_size
        if self.status is not None:
            result['Status'] = self.status
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('AppId') is not None:
            self.app_id = m.get('AppId')
        if m.get('Order') is not None:
            self.order = m.get('Order')
        if m.get('OwnerId') is not None:
            self.owner_id = m.get('OwnerId')
        if m.get('PageNum') is not None:
            self.page_num = m.get('PageNum')
        if m.get('PageSize') is not None:
            self.page_size = m.get('PageSize')
        if m.get('Status') is not None:
            self.status = m.get('Status')
        return self


class DescribeAppsResponseBodyAppListAppServiceAreas(TeaModel):
    def __init__(
        self,
        service_area: List[str] = None,
    ):
        self.service_area = service_area

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.service_area is not None:
            result['ServiceArea'] = self.service_area
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ServiceArea') is not None:
            self.service_area = m.get('ServiceArea')
        return self


class DescribeAppsResponseBodyAppListApp(TeaModel):
    def __init__(
        self,
        app_id: str = None,
        app_name: str = None,
        app_type: str = None,
        bill_type: str = None,
        create_time: str = None,
        region: str = None,
        service_areas: DescribeAppsResponseBodyAppListAppServiceAreas = None,
        status: int = None,
    ):
        self.app_id = app_id
        self.app_name = app_name
        self.app_type = app_type
        self.bill_type = bill_type
        self.create_time = create_time
        self.region = region
        self.service_areas = service_areas
        self.status = status

    def validate(self):
        if self.service_areas:
            self.service_areas.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.app_id is not None:
            result['AppId'] = self.app_id
        if self.app_name is not None:
            result['AppName'] = self.app_name
        if self.app_type is not None:
            result['AppType'] = self.app_type
        if self.bill_type is not None:
            result['BillType'] = self.bill_type
        if self.create_time is not None:
            result['CreateTime'] = self.create_time
        if self.region is not None:
            result['Region'] = self.region
        if self.service_areas is not None:
            result['ServiceAreas'] = self.service_areas.to_map()
        if self.status is not None:
            result['Status'] = self.status
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('AppId') is not None:
            self.app_id = m.get('AppId')
        if m.get('AppName') is not None:
            self.app_name = m.get('AppName')
        if m.get('AppType') is not None:
            self.app_type = m.get('AppType')
        if m.get('BillType') is not None:
            self.bill_type = m.get('BillType')
        if m.get('CreateTime') is not None:
            self.create_time = m.get('CreateTime')
        if m.get('Region') is not None:
            self.region = m.get('Region')
        if m.get('ServiceAreas') is not None:
            temp_model = DescribeAppsResponseBodyAppListAppServiceAreas()
            self.service_areas = temp_model.from_map(m['ServiceAreas'])
        if m.get('Status') is not None:
            self.status = m.get('Status')
        return self


class DescribeAppsResponseBodyAppList(TeaModel):
    def __init__(
        self,
        app: List[DescribeAppsResponseBodyAppListApp] = None,
    ):
        self.app = app

    def validate(self):
        if self.app:
            for k in self.app:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        result['App'] = []
        if self.app is not None:
            for k in self.app:
                result['App'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.app = []
        if m.get('App') is not None:
            for k in m.get('App'):
                temp_model = DescribeAppsResponseBodyAppListApp()
                self.app.append(temp_model.from_map(k))
        return self


class DescribeAppsResponseBody(TeaModel):
    def __init__(
        self,
        app_list: DescribeAppsResponseBodyAppList = None,
        request_id: str = None,
        total_num: int = None,
        total_page: int = None,
    ):
        self.app_list = app_list
        self.request_id = request_id
        self.total_num = total_num
        self.total_page = total_page

    def validate(self):
        if self.app_list:
            self.app_list.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.app_list is not None:
            result['AppList'] = self.app_list.to_map()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.total_num is not None:
            result['TotalNum'] = self.total_num
        if self.total_page is not None:
            result['TotalPage'] = self.total_page
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('AppList') is not None:
            temp_model = DescribeAppsResponseBodyAppList()
            self.app_list = temp_model.from_map(m['AppList'])
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('TotalNum') is not None:
            self.total_num = m.get('TotalNum')
        if m.get('TotalPage') is not None:
            self.total_page = m.get('TotalPage')
        return self


class DescribeAppsResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: DescribeAppsResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.status_code, 'status_code')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = DescribeAppsResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DescribeAutoLiveStreamRuleRequest(TeaModel):
    def __init__(
        self,
        app_id: str = None,
        owner_id: int = None,
    ):
        self.app_id = app_id
        self.owner_id = owner_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.app_id is not None:
            result['AppId'] = self.app_id
        if self.owner_id is not None:
            result['OwnerId'] = self.owner_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('AppId') is not None:
            self.app_id = m.get('AppId')
        if m.get('OwnerId') is not None:
            self.owner_id = m.get('OwnerId')
        return self


class DescribeAutoLiveStreamRuleResponseBodyRules(TeaModel):
    def __init__(
        self,
        call_back: str = None,
        channel_id_prefixes: List[str] = None,
        channel_ids: List[str] = None,
        create_time: str = None,
        media_encode: int = None,
        play_domain: str = None,
        rule_id: int = None,
        rule_name: str = None,
        status: str = None,
    ):
        self.call_back = call_back
        self.channel_id_prefixes = channel_id_prefixes
        self.channel_ids = channel_ids
        self.create_time = create_time
        self.media_encode = media_encode
        self.play_domain = play_domain
        self.rule_id = rule_id
        self.rule_name = rule_name
        self.status = status

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.call_back is not None:
            result['CallBack'] = self.call_back
        if self.channel_id_prefixes is not None:
            result['ChannelIdPrefixes'] = self.channel_id_prefixes
        if self.channel_ids is not None:
            result['ChannelIds'] = self.channel_ids
        if self.create_time is not None:
            result['CreateTime'] = self.create_time
        if self.media_encode is not None:
            result['MediaEncode'] = self.media_encode
        if self.play_domain is not None:
            result['PlayDomain'] = self.play_domain
        if self.rule_id is not None:
            result['RuleId'] = self.rule_id
        if self.rule_name is not None:
            result['RuleName'] = self.rule_name
        if self.status is not None:
            result['Status'] = self.status
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('CallBack') is not None:
            self.call_back = m.get('CallBack')
        if m.get('ChannelIdPrefixes') is not None:
            self.channel_id_prefixes = m.get('ChannelIdPrefixes')
        if m.get('ChannelIds') is not None:
            self.channel_ids = m.get('ChannelIds')
        if m.get('CreateTime') is not None:
            self.create_time = m.get('CreateTime')
        if m.get('MediaEncode') is not None:
            self.media_encode = m.get('MediaEncode')
        if m.get('PlayDomain') is not None:
            self.play_domain = m.get('PlayDomain')
        if m.get('RuleId') is not None:
            self.rule_id = m.get('RuleId')
        if m.get('RuleName') is not None:
            self.rule_name = m.get('RuleName')
        if m.get('Status') is not None:
            self.status = m.get('Status')
        return self


class DescribeAutoLiveStreamRuleResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
        rules: List[DescribeAutoLiveStreamRuleResponseBodyRules] = None,
    ):
        self.request_id = request_id
        self.rules = rules

    def validate(self):
        if self.rules:
            for k in self.rules:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        result['Rules'] = []
        if self.rules is not None:
            for k in self.rules:
                result['Rules'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        self.rules = []
        if m.get('Rules') is not None:
            for k in m.get('Rules'):
                temp_model = DescribeAutoLiveStreamRuleResponseBodyRules()
                self.rules.append(temp_model.from_map(k))
        return self


class DescribeAutoLiveStreamRuleResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: DescribeAutoLiveStreamRuleResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.status_code, 'status_code')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = DescribeAutoLiveStreamRuleResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DescribeCallListRequest(TeaModel):
    def __init__(
        self,
        app_id: str = None,
        call_status: str = None,
        channel_id: str = None,
        end_ts: int = None,
        order_by: str = None,
        page_no: int = None,
        page_size: int = None,
        query_mode: str = None,
        start_ts: int = None,
        user_id: str = None,
    ):
        # APP ID。
        self.app_id = app_id
        self.call_status = call_status
        self.channel_id = channel_id
        self.end_ts = end_ts
        self.order_by = order_by
        self.page_no = page_no
        self.page_size = page_size
        self.query_mode = query_mode
        self.start_ts = start_ts
        self.user_id = user_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.app_id is not None:
            result['AppId'] = self.app_id
        if self.call_status is not None:
            result['CallStatus'] = self.call_status
        if self.channel_id is not None:
            result['ChannelId'] = self.channel_id
        if self.end_ts is not None:
            result['EndTs'] = self.end_ts
        if self.order_by is not None:
            result['OrderBy'] = self.order_by
        if self.page_no is not None:
            result['PageNo'] = self.page_no
        if self.page_size is not None:
            result['PageSize'] = self.page_size
        if self.query_mode is not None:
            result['QueryMode'] = self.query_mode
        if self.start_ts is not None:
            result['StartTs'] = self.start_ts
        if self.user_id is not None:
            result['UserId'] = self.user_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('AppId') is not None:
            self.app_id = m.get('AppId')
        if m.get('CallStatus') is not None:
            self.call_status = m.get('CallStatus')
        if m.get('ChannelId') is not None:
            self.channel_id = m.get('ChannelId')
        if m.get('EndTs') is not None:
            self.end_ts = m.get('EndTs')
        if m.get('OrderBy') is not None:
            self.order_by = m.get('OrderBy')
        if m.get('PageNo') is not None:
            self.page_no = m.get('PageNo')
        if m.get('PageSize') is not None:
            self.page_size = m.get('PageSize')
        if m.get('QueryMode') is not None:
            self.query_mode = m.get('QueryMode')
        if m.get('StartTs') is not None:
            self.start_ts = m.get('StartTs')
        if m.get('UserId') is not None:
            self.user_id = m.get('UserId')
        return self


class DescribeCallListResponseBodyCallList(TeaModel):
    def __init__(
        self,
        app_id: str = None,
        bad_exp_user_cnt: int = None,
        call_status: str = None,
        channel_id: str = None,
        created_ts: int = None,
        destroyed_ts: int = None,
        duration: int = None,
        user_cnt: int = None,
    ):
        # App ID。
        self.app_id = app_id
        self.bad_exp_user_cnt = bad_exp_user_cnt
        self.call_status = call_status
        self.channel_id = channel_id
        self.created_ts = created_ts
        self.destroyed_ts = destroyed_ts
        self.duration = duration
        self.user_cnt = user_cnt

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.app_id is not None:
            result['AppId'] = self.app_id
        if self.bad_exp_user_cnt is not None:
            result['BadExpUserCnt'] = self.bad_exp_user_cnt
        if self.call_status is not None:
            result['CallStatus'] = self.call_status
        if self.channel_id is not None:
            result['ChannelId'] = self.channel_id
        if self.created_ts is not None:
            result['CreatedTs'] = self.created_ts
        if self.destroyed_ts is not None:
            result['DestroyedTs'] = self.destroyed_ts
        if self.duration is not None:
            result['Duration'] = self.duration
        if self.user_cnt is not None:
            result['UserCnt'] = self.user_cnt
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('AppId') is not None:
            self.app_id = m.get('AppId')
        if m.get('BadExpUserCnt') is not None:
            self.bad_exp_user_cnt = m.get('BadExpUserCnt')
        if m.get('CallStatus') is not None:
            self.call_status = m.get('CallStatus')
        if m.get('ChannelId') is not None:
            self.channel_id = m.get('ChannelId')
        if m.get('CreatedTs') is not None:
            self.created_ts = m.get('CreatedTs')
        if m.get('DestroyedTs') is not None:
            self.destroyed_ts = m.get('DestroyedTs')
        if m.get('Duration') is not None:
            self.duration = m.get('Duration')
        if m.get('UserCnt') is not None:
            self.user_cnt = m.get('UserCnt')
        return self


class DescribeCallListResponseBody(TeaModel):
    def __init__(
        self,
        call_list: List[DescribeCallListResponseBodyCallList] = None,
        page_no: int = None,
        page_size: int = None,
        request_id: str = None,
        total_cnt: int = None,
    ):
        self.call_list = call_list
        self.page_no = page_no
        self.page_size = page_size
        self.request_id = request_id
        self.total_cnt = total_cnt

    def validate(self):
        if self.call_list:
            for k in self.call_list:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        result['CallList'] = []
        if self.call_list is not None:
            for k in self.call_list:
                result['CallList'].append(k.to_map() if k else None)
        if self.page_no is not None:
            result['PageNo'] = self.page_no
        if self.page_size is not None:
            result['PageSize'] = self.page_size
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.total_cnt is not None:
            result['TotalCnt'] = self.total_cnt
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.call_list = []
        if m.get('CallList') is not None:
            for k in m.get('CallList'):
                temp_model = DescribeCallListResponseBodyCallList()
                self.call_list.append(temp_model.from_map(k))
        if m.get('PageNo') is not None:
            self.page_no = m.get('PageNo')
        if m.get('PageSize') is not None:
            self.page_size = m.get('PageSize')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('TotalCnt') is not None:
            self.total_cnt = m.get('TotalCnt')
        return self


class DescribeCallListResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: DescribeCallListResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.status_code, 'status_code')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = DescribeCallListResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DescribeChannelParticipantsRequest(TeaModel):
    def __init__(
        self,
        app_id: str = None,
        channel_id: str = None,
        order: str = None,
        owner_id: int = None,
        page_num: int = None,
        page_size: int = None,
    ):
        self.app_id = app_id
        self.channel_id = channel_id
        self.order = order
        self.owner_id = owner_id
        self.page_num = page_num
        self.page_size = page_size

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.app_id is not None:
            result['AppId'] = self.app_id
        if self.channel_id is not None:
            result['ChannelId'] = self.channel_id
        if self.order is not None:
            result['Order'] = self.order
        if self.owner_id is not None:
            result['OwnerId'] = self.owner_id
        if self.page_num is not None:
            result['PageNum'] = self.page_num
        if self.page_size is not None:
            result['PageSize'] = self.page_size
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('AppId') is not None:
            self.app_id = m.get('AppId')
        if m.get('ChannelId') is not None:
            self.channel_id = m.get('ChannelId')
        if m.get('Order') is not None:
            self.order = m.get('Order')
        if m.get('OwnerId') is not None:
            self.owner_id = m.get('OwnerId')
        if m.get('PageNum') is not None:
            self.page_num = m.get('PageNum')
        if m.get('PageSize') is not None:
            self.page_size = m.get('PageSize')
        return self


class DescribeChannelParticipantsResponseBodyUserList(TeaModel):
    def __init__(
        self,
        user: List[str] = None,
    ):
        self.user = user

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.user is not None:
            result['User'] = self.user
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('User') is not None:
            self.user = m.get('User')
        return self


class DescribeChannelParticipantsResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
        timestamp: int = None,
        total_num: int = None,
        total_page: int = None,
        user_list: DescribeChannelParticipantsResponseBodyUserList = None,
    ):
        self.request_id = request_id
        self.timestamp = timestamp
        self.total_num = total_num
        self.total_page = total_page
        self.user_list = user_list

    def validate(self):
        if self.user_list:
            self.user_list.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.timestamp is not None:
            result['Timestamp'] = self.timestamp
        if self.total_num is not None:
            result['TotalNum'] = self.total_num
        if self.total_page is not None:
            result['TotalPage'] = self.total_page
        if self.user_list is not None:
            result['UserList'] = self.user_list.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Timestamp') is not None:
            self.timestamp = m.get('Timestamp')
        if m.get('TotalNum') is not None:
            self.total_num = m.get('TotalNum')
        if m.get('TotalPage') is not None:
            self.total_page = m.get('TotalPage')
        if m.get('UserList') is not None:
            temp_model = DescribeChannelParticipantsResponseBodyUserList()
            self.user_list = temp_model.from_map(m['UserList'])
        return self


class DescribeChannelParticipantsResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: DescribeChannelParticipantsResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.status_code, 'status_code')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = DescribeChannelParticipantsResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DescribeChannelUsersRequest(TeaModel):
    def __init__(
        self,
        app_id: str = None,
        channel_id: str = None,
        owner_id: int = None,
    ):
        self.app_id = app_id
        self.channel_id = channel_id
        self.owner_id = owner_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.app_id is not None:
            result['AppId'] = self.app_id
        if self.channel_id is not None:
            result['ChannelId'] = self.channel_id
        if self.owner_id is not None:
            result['OwnerId'] = self.owner_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('AppId') is not None:
            self.app_id = m.get('AppId')
        if m.get('ChannelId') is not None:
            self.channel_id = m.get('ChannelId')
        if m.get('OwnerId') is not None:
            self.owner_id = m.get('OwnerId')
        return self


class DescribeChannelUsersResponseBody(TeaModel):
    def __init__(
        self,
        channel_profile: int = None,
        comm_total_num: int = None,
        interactive_user_list: List[str] = None,
        interactive_user_num: int = None,
        is_channel_exist: bool = None,
        live_user_list: List[str] = None,
        live_user_num: int = None,
        request_id: str = None,
        timestamp: int = None,
        user_list: List[str] = None,
    ):
        self.channel_profile = channel_profile
        self.comm_total_num = comm_total_num
        self.interactive_user_list = interactive_user_list
        self.interactive_user_num = interactive_user_num
        self.is_channel_exist = is_channel_exist
        self.live_user_list = live_user_list
        self.live_user_num = live_user_num
        self.request_id = request_id
        self.timestamp = timestamp
        self.user_list = user_list

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.channel_profile is not None:
            result['ChannelProfile'] = self.channel_profile
        if self.comm_total_num is not None:
            result['CommTotalNum'] = self.comm_total_num
        if self.interactive_user_list is not None:
            result['InteractiveUserList'] = self.interactive_user_list
        if self.interactive_user_num is not None:
            result['InteractiveUserNum'] = self.interactive_user_num
        if self.is_channel_exist is not None:
            result['IsChannelExist'] = self.is_channel_exist
        if self.live_user_list is not None:
            result['LiveUserList'] = self.live_user_list
        if self.live_user_num is not None:
            result['LiveUserNum'] = self.live_user_num
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.timestamp is not None:
            result['Timestamp'] = self.timestamp
        if self.user_list is not None:
            result['UserList'] = self.user_list
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ChannelProfile') is not None:
            self.channel_profile = m.get('ChannelProfile')
        if m.get('CommTotalNum') is not None:
            self.comm_total_num = m.get('CommTotalNum')
        if m.get('InteractiveUserList') is not None:
            self.interactive_user_list = m.get('InteractiveUserList')
        if m.get('InteractiveUserNum') is not None:
            self.interactive_user_num = m.get('InteractiveUserNum')
        if m.get('IsChannelExist') is not None:
            self.is_channel_exist = m.get('IsChannelExist')
        if m.get('LiveUserList') is not None:
            self.live_user_list = m.get('LiveUserList')
        if m.get('LiveUserNum') is not None:
            self.live_user_num = m.get('LiveUserNum')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Timestamp') is not None:
            self.timestamp = m.get('Timestamp')
        if m.get('UserList') is not None:
            self.user_list = m.get('UserList')
        return self


class DescribeChannelUsersResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: DescribeChannelUsersResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.status_code, 'status_code')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = DescribeChannelUsersResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DescribeMPULayoutInfoListRequest(TeaModel):
    def __init__(
        self,
        app_id: str = None,
        layout_id: int = None,
        name: str = None,
        owner_id: int = None,
        page_num: int = None,
        page_size: int = None,
    ):
        self.app_id = app_id
        self.layout_id = layout_id
        self.name = name
        self.owner_id = owner_id
        self.page_num = page_num
        self.page_size = page_size

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.app_id is not None:
            result['AppId'] = self.app_id
        if self.layout_id is not None:
            result['LayoutId'] = self.layout_id
        if self.name is not None:
            result['Name'] = self.name
        if self.owner_id is not None:
            result['OwnerId'] = self.owner_id
        if self.page_num is not None:
            result['PageNum'] = self.page_num
        if self.page_size is not None:
            result['PageSize'] = self.page_size
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('AppId') is not None:
            self.app_id = m.get('AppId')
        if m.get('LayoutId') is not None:
            self.layout_id = m.get('LayoutId')
        if m.get('Name') is not None:
            self.name = m.get('Name')
        if m.get('OwnerId') is not None:
            self.owner_id = m.get('OwnerId')
        if m.get('PageNum') is not None:
            self.page_num = m.get('PageNum')
        if m.get('PageSize') is not None:
            self.page_size = m.get('PageSize')
        return self


class DescribeMPULayoutInfoListResponseBodyLayoutsLayoutPanesPanes(TeaModel):
    def __init__(
        self,
        height: float = None,
        major_pane: int = None,
        pane_id: int = None,
        width: float = None,
        x: float = None,
        y: float = None,
        zorder: int = None,
    ):
        self.height = height
        self.major_pane = major_pane
        self.pane_id = pane_id
        self.width = width
        self.x = x
        self.y = y
        self.zorder = zorder

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.height is not None:
            result['Height'] = self.height
        if self.major_pane is not None:
            result['MajorPane'] = self.major_pane
        if self.pane_id is not None:
            result['PaneId'] = self.pane_id
        if self.width is not None:
            result['Width'] = self.width
        if self.x is not None:
            result['X'] = self.x
        if self.y is not None:
            result['Y'] = self.y
        if self.zorder is not None:
            result['ZOrder'] = self.zorder
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Height') is not None:
            self.height = m.get('Height')
        if m.get('MajorPane') is not None:
            self.major_pane = m.get('MajorPane')
        if m.get('PaneId') is not None:
            self.pane_id = m.get('PaneId')
        if m.get('Width') is not None:
            self.width = m.get('Width')
        if m.get('X') is not None:
            self.x = m.get('X')
        if m.get('Y') is not None:
            self.y = m.get('Y')
        if m.get('ZOrder') is not None:
            self.zorder = m.get('ZOrder')
        return self


class DescribeMPULayoutInfoListResponseBodyLayoutsLayoutPanes(TeaModel):
    def __init__(
        self,
        panes: List[DescribeMPULayoutInfoListResponseBodyLayoutsLayoutPanesPanes] = None,
    ):
        self.panes = panes

    def validate(self):
        if self.panes:
            for k in self.panes:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        result['Panes'] = []
        if self.panes is not None:
            for k in self.panes:
                result['Panes'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.panes = []
        if m.get('Panes') is not None:
            for k in m.get('Panes'):
                temp_model = DescribeMPULayoutInfoListResponseBodyLayoutsLayoutPanesPanes()
                self.panes.append(temp_model.from_map(k))
        return self


class DescribeMPULayoutInfoListResponseBodyLayoutsLayout(TeaModel):
    def __init__(
        self,
        audio_mix_count: int = None,
        layout_id: int = None,
        name: str = None,
        panes: DescribeMPULayoutInfoListResponseBodyLayoutsLayoutPanes = None,
    ):
        self.audio_mix_count = audio_mix_count
        self.layout_id = layout_id
        self.name = name
        self.panes = panes

    def validate(self):
        if self.panes:
            self.panes.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.audio_mix_count is not None:
            result['AudioMixCount'] = self.audio_mix_count
        if self.layout_id is not None:
            result['LayoutId'] = self.layout_id
        if self.name is not None:
            result['Name'] = self.name
        if self.panes is not None:
            result['Panes'] = self.panes.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('AudioMixCount') is not None:
            self.audio_mix_count = m.get('AudioMixCount')
        if m.get('LayoutId') is not None:
            self.layout_id = m.get('LayoutId')
        if m.get('Name') is not None:
            self.name = m.get('Name')
        if m.get('Panes') is not None:
            temp_model = DescribeMPULayoutInfoListResponseBodyLayoutsLayoutPanes()
            self.panes = temp_model.from_map(m['Panes'])
        return self


class DescribeMPULayoutInfoListResponseBodyLayouts(TeaModel):
    def __init__(
        self,
        layout: List[DescribeMPULayoutInfoListResponseBodyLayoutsLayout] = None,
    ):
        self.layout = layout

    def validate(self):
        if self.layout:
            for k in self.layout:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        result['Layout'] = []
        if self.layout is not None:
            for k in self.layout:
                result['Layout'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.layout = []
        if m.get('Layout') is not None:
            for k in m.get('Layout'):
                temp_model = DescribeMPULayoutInfoListResponseBodyLayoutsLayout()
                self.layout.append(temp_model.from_map(k))
        return self


class DescribeMPULayoutInfoListResponseBody(TeaModel):
    def __init__(
        self,
        layouts: DescribeMPULayoutInfoListResponseBodyLayouts = None,
        request_id: str = None,
        total_num: int = None,
        total_page: int = None,
    ):
        self.layouts = layouts
        self.request_id = request_id
        self.total_num = total_num
        self.total_page = total_page

    def validate(self):
        if self.layouts:
            self.layouts.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.layouts is not None:
            result['Layouts'] = self.layouts.to_map()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.total_num is not None:
            result['TotalNum'] = self.total_num
        if self.total_page is not None:
            result['TotalPage'] = self.total_page
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Layouts') is not None:
            temp_model = DescribeMPULayoutInfoListResponseBodyLayouts()
            self.layouts = temp_model.from_map(m['Layouts'])
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('TotalNum') is not None:
            self.total_num = m.get('TotalNum')
        if m.get('TotalPage') is not None:
            self.total_page = m.get('TotalPage')
        return self


class DescribeMPULayoutInfoListResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: DescribeMPULayoutInfoListResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.status_code, 'status_code')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = DescribeMPULayoutInfoListResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DescribeRecordFilesRequest(TeaModel):
    def __init__(
        self,
        app_id: str = None,
        channel_id: str = None,
        end_time: str = None,
        owner_id: int = None,
        page_num: int = None,
        page_size: int = None,
        start_time: str = None,
        task_ids: List[str] = None,
    ):
        self.app_id = app_id
        self.channel_id = channel_id
        self.end_time = end_time
        self.owner_id = owner_id
        self.page_num = page_num
        self.page_size = page_size
        self.start_time = start_time
        self.task_ids = task_ids

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.app_id is not None:
            result['AppId'] = self.app_id
        if self.channel_id is not None:
            result['ChannelId'] = self.channel_id
        if self.end_time is not None:
            result['EndTime'] = self.end_time
        if self.owner_id is not None:
            result['OwnerId'] = self.owner_id
        if self.page_num is not None:
            result['PageNum'] = self.page_num
        if self.page_size is not None:
            result['PageSize'] = self.page_size
        if self.start_time is not None:
            result['StartTime'] = self.start_time
        if self.task_ids is not None:
            result['TaskIds'] = self.task_ids
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('AppId') is not None:
            self.app_id = m.get('AppId')
        if m.get('ChannelId') is not None:
            self.channel_id = m.get('ChannelId')
        if m.get('EndTime') is not None:
            self.end_time = m.get('EndTime')
        if m.get('OwnerId') is not None:
            self.owner_id = m.get('OwnerId')
        if m.get('PageNum') is not None:
            self.page_num = m.get('PageNum')
        if m.get('PageSize') is not None:
            self.page_size = m.get('PageSize')
        if m.get('StartTime') is not None:
            self.start_time = m.get('StartTime')
        if m.get('TaskIds') is not None:
            self.task_ids = m.get('TaskIds')
        return self


class DescribeRecordFilesResponseBodyRecordFiles(TeaModel):
    def __init__(
        self,
        app_id: str = None,
        channel_id: str = None,
        create_time: str = None,
        duration: float = None,
        start_time: str = None,
        stop_time: str = None,
        task_id: str = None,
        url: str = None,
    ):
        self.app_id = app_id
        self.channel_id = channel_id
        self.create_time = create_time
        self.duration = duration
        self.start_time = start_time
        self.stop_time = stop_time
        self.task_id = task_id
        self.url = url

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.app_id is not None:
            result['AppId'] = self.app_id
        if self.channel_id is not None:
            result['ChannelId'] = self.channel_id
        if self.create_time is not None:
            result['CreateTime'] = self.create_time
        if self.duration is not None:
            result['Duration'] = self.duration
        if self.start_time is not None:
            result['StartTime'] = self.start_time
        if self.stop_time is not None:
            result['StopTime'] = self.stop_time
        if self.task_id is not None:
            result['TaskId'] = self.task_id
        if self.url is not None:
            result['Url'] = self.url
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('AppId') is not None:
            self.app_id = m.get('AppId')
        if m.get('ChannelId') is not None:
            self.channel_id = m.get('ChannelId')
        if m.get('CreateTime') is not None:
            self.create_time = m.get('CreateTime')
        if m.get('Duration') is not None:
            self.duration = m.get('Duration')
        if m.get('StartTime') is not None:
            self.start_time = m.get('StartTime')
        if m.get('StopTime') is not None:
            self.stop_time = m.get('StopTime')
        if m.get('TaskId') is not None:
            self.task_id = m.get('TaskId')
        if m.get('Url') is not None:
            self.url = m.get('Url')
        return self


class DescribeRecordFilesResponseBody(TeaModel):
    def __init__(
        self,
        record_files: List[DescribeRecordFilesResponseBodyRecordFiles] = None,
        request_id: str = None,
        total_num: int = None,
        total_page: int = None,
    ):
        self.record_files = record_files
        self.request_id = request_id
        self.total_num = total_num
        self.total_page = total_page

    def validate(self):
        if self.record_files:
            for k in self.record_files:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        result['RecordFiles'] = []
        if self.record_files is not None:
            for k in self.record_files:
                result['RecordFiles'].append(k.to_map() if k else None)
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.total_num is not None:
            result['TotalNum'] = self.total_num
        if self.total_page is not None:
            result['TotalPage'] = self.total_page
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.record_files = []
        if m.get('RecordFiles') is not None:
            for k in m.get('RecordFiles'):
                temp_model = DescribeRecordFilesResponseBodyRecordFiles()
                self.record_files.append(temp_model.from_map(k))
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('TotalNum') is not None:
            self.total_num = m.get('TotalNum')
        if m.get('TotalPage') is not None:
            self.total_page = m.get('TotalPage')
        return self


class DescribeRecordFilesResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: DescribeRecordFilesResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.status_code, 'status_code')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = DescribeRecordFilesResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DescribeRecordTemplatesRequest(TeaModel):
    def __init__(
        self,
        app_id: str = None,
        owner_id: int = None,
        page_num: int = None,
        page_size: int = None,
        template_ids: List[str] = None,
    ):
        self.app_id = app_id
        # 1
        self.owner_id = owner_id
        self.page_num = page_num
        self.page_size = page_size
        self.template_ids = template_ids

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.app_id is not None:
            result['AppId'] = self.app_id
        if self.owner_id is not None:
            result['OwnerId'] = self.owner_id
        if self.page_num is not None:
            result['PageNum'] = self.page_num
        if self.page_size is not None:
            result['PageSize'] = self.page_size
        if self.template_ids is not None:
            result['TemplateIds'] = self.template_ids
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('AppId') is not None:
            self.app_id = m.get('AppId')
        if m.get('OwnerId') is not None:
            self.owner_id = m.get('OwnerId')
        if m.get('PageNum') is not None:
            self.page_num = m.get('PageNum')
        if m.get('PageSize') is not None:
            self.page_size = m.get('PageSize')
        if m.get('TemplateIds') is not None:
            self.template_ids = m.get('TemplateIds')
        return self


class DescribeRecordTemplatesResponseBodyTemplatesBackgrounds(TeaModel):
    def __init__(
        self,
        display: int = None,
        height: float = None,
        url: str = None,
        width: float = None,
        x: float = None,
        y: float = None,
        zorder: int = None,
    ):
        self.display = display
        self.height = height
        self.url = url
        self.width = width
        self.x = x
        self.y = y
        self.zorder = zorder

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.display is not None:
            result['Display'] = self.display
        if self.height is not None:
            result['Height'] = self.height
        if self.url is not None:
            result['Url'] = self.url
        if self.width is not None:
            result['Width'] = self.width
        if self.x is not None:
            result['X'] = self.x
        if self.y is not None:
            result['Y'] = self.y
        if self.zorder is not None:
            result['ZOrder'] = self.zorder
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Display') is not None:
            self.display = m.get('Display')
        if m.get('Height') is not None:
            self.height = m.get('Height')
        if m.get('Url') is not None:
            self.url = m.get('Url')
        if m.get('Width') is not None:
            self.width = m.get('Width')
        if m.get('X') is not None:
            self.x = m.get('X')
        if m.get('Y') is not None:
            self.y = m.get('Y')
        if m.get('ZOrder') is not None:
            self.zorder = m.get('ZOrder')
        return self


class DescribeRecordTemplatesResponseBodyTemplatesClockWidgets(TeaModel):
    def __init__(
        self,
        font_color: int = None,
        font_size: int = None,
        font_type: int = None,
        x: float = None,
        y: float = None,
        zorder: int = None,
    ):
        self.font_color = font_color
        self.font_size = font_size
        self.font_type = font_type
        self.x = x
        self.y = y
        self.zorder = zorder

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.font_color is not None:
            result['FontColor'] = self.font_color
        if self.font_size is not None:
            result['FontSize'] = self.font_size
        if self.font_type is not None:
            result['FontType'] = self.font_type
        if self.x is not None:
            result['X'] = self.x
        if self.y is not None:
            result['Y'] = self.y
        if self.zorder is not None:
            result['ZOrder'] = self.zorder
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('FontColor') is not None:
            self.font_color = m.get('FontColor')
        if m.get('FontSize') is not None:
            self.font_size = m.get('FontSize')
        if m.get('FontType') is not None:
            self.font_type = m.get('FontType')
        if m.get('X') is not None:
            self.x = m.get('X')
        if m.get('Y') is not None:
            self.y = m.get('Y')
        if m.get('ZOrder') is not None:
            self.zorder = m.get('ZOrder')
        return self


class DescribeRecordTemplatesResponseBodyTemplatesWatermarks(TeaModel):
    def __init__(
        self,
        alpha: float = None,
        display: int = None,
        height: float = None,
        url: str = None,
        width: float = None,
        x: float = None,
        y: float = None,
        zorder: int = None,
    ):
        self.alpha = alpha
        self.display = display
        self.height = height
        self.url = url
        self.width = width
        self.x = x
        self.y = y
        self.zorder = zorder

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.alpha is not None:
            result['Alpha'] = self.alpha
        if self.display is not None:
            result['Display'] = self.display
        if self.height is not None:
            result['Height'] = self.height
        if self.url is not None:
            result['Url'] = self.url
        if self.width is not None:
            result['Width'] = self.width
        if self.x is not None:
            result['X'] = self.x
        if self.y is not None:
            result['Y'] = self.y
        if self.zorder is not None:
            result['ZOrder'] = self.zorder
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Alpha') is not None:
            self.alpha = m.get('Alpha')
        if m.get('Display') is not None:
            self.display = m.get('Display')
        if m.get('Height') is not None:
            self.height = m.get('Height')
        if m.get('Url') is not None:
            self.url = m.get('Url')
        if m.get('Width') is not None:
            self.width = m.get('Width')
        if m.get('X') is not None:
            self.x = m.get('X')
        if m.get('Y') is not None:
            self.y = m.get('Y')
        if m.get('ZOrder') is not None:
            self.zorder = m.get('ZOrder')
        return self


class DescribeRecordTemplatesResponseBodyTemplates(TeaModel):
    def __init__(
        self,
        background_color: int = None,
        backgrounds: List[DescribeRecordTemplatesResponseBodyTemplatesBackgrounds] = None,
        clock_widgets: List[DescribeRecordTemplatesResponseBodyTemplatesClockWidgets] = None,
        create_time: str = None,
        delay_stop_time: int = None,
        enable_m3u_8date_time: bool = None,
        file_split_interval: int = None,
        formats: List[str] = None,
        http_callback_url: str = None,
        layout_ids: List[int] = None,
        media_encode: int = None,
        mns_queue: str = None,
        name: str = None,
        oss_bucket: str = None,
        oss_file_prefix: str = None,
        task_profile: str = None,
        template_id: str = None,
        watermarks: List[DescribeRecordTemplatesResponseBodyTemplatesWatermarks] = None,
    ):
        self.background_color = background_color
        self.backgrounds = backgrounds
        self.clock_widgets = clock_widgets
        self.create_time = create_time
        self.delay_stop_time = delay_stop_time
        self.enable_m3u_8date_time = enable_m3u_8date_time
        self.file_split_interval = file_split_interval
        self.formats = formats
        self.http_callback_url = http_callback_url
        self.layout_ids = layout_ids
        self.media_encode = media_encode
        self.mns_queue = mns_queue
        self.name = name
        self.oss_bucket = oss_bucket
        self.oss_file_prefix = oss_file_prefix
        self.task_profile = task_profile
        self.template_id = template_id
        self.watermarks = watermarks

    def validate(self):
        if self.backgrounds:
            for k in self.backgrounds:
                if k:
                    k.validate()
        if self.clock_widgets:
            for k in self.clock_widgets:
                if k:
                    k.validate()
        if self.watermarks:
            for k in self.watermarks:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.background_color is not None:
            result['BackgroundColor'] = self.background_color
        result['Backgrounds'] = []
        if self.backgrounds is not None:
            for k in self.backgrounds:
                result['Backgrounds'].append(k.to_map() if k else None)
        result['ClockWidgets'] = []
        if self.clock_widgets is not None:
            for k in self.clock_widgets:
                result['ClockWidgets'].append(k.to_map() if k else None)
        if self.create_time is not None:
            result['CreateTime'] = self.create_time
        if self.delay_stop_time is not None:
            result['DelayStopTime'] = self.delay_stop_time
        if self.enable_m3u_8date_time is not None:
            result['EnableM3u8DateTime'] = self.enable_m3u_8date_time
        if self.file_split_interval is not None:
            result['FileSplitInterval'] = self.file_split_interval
        if self.formats is not None:
            result['Formats'] = self.formats
        if self.http_callback_url is not None:
            result['HttpCallbackUrl'] = self.http_callback_url
        if self.layout_ids is not None:
            result['LayoutIds'] = self.layout_ids
        if self.media_encode is not None:
            result['MediaEncode'] = self.media_encode
        if self.mns_queue is not None:
            result['MnsQueue'] = self.mns_queue
        if self.name is not None:
            result['Name'] = self.name
        if self.oss_bucket is not None:
            result['OssBucket'] = self.oss_bucket
        if self.oss_file_prefix is not None:
            result['OssFilePrefix'] = self.oss_file_prefix
        if self.task_profile is not None:
            result['TaskProfile'] = self.task_profile
        if self.template_id is not None:
            result['TemplateId'] = self.template_id
        result['Watermarks'] = []
        if self.watermarks is not None:
            for k in self.watermarks:
                result['Watermarks'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('BackgroundColor') is not None:
            self.background_color = m.get('BackgroundColor')
        self.backgrounds = []
        if m.get('Backgrounds') is not None:
            for k in m.get('Backgrounds'):
                temp_model = DescribeRecordTemplatesResponseBodyTemplatesBackgrounds()
                self.backgrounds.append(temp_model.from_map(k))
        self.clock_widgets = []
        if m.get('ClockWidgets') is not None:
            for k in m.get('ClockWidgets'):
                temp_model = DescribeRecordTemplatesResponseBodyTemplatesClockWidgets()
                self.clock_widgets.append(temp_model.from_map(k))
        if m.get('CreateTime') is not None:
            self.create_time = m.get('CreateTime')
        if m.get('DelayStopTime') is not None:
            self.delay_stop_time = m.get('DelayStopTime')
        if m.get('EnableM3u8DateTime') is not None:
            self.enable_m3u_8date_time = m.get('EnableM3u8DateTime')
        if m.get('FileSplitInterval') is not None:
            self.file_split_interval = m.get('FileSplitInterval')
        if m.get('Formats') is not None:
            self.formats = m.get('Formats')
        if m.get('HttpCallbackUrl') is not None:
            self.http_callback_url = m.get('HttpCallbackUrl')
        if m.get('LayoutIds') is not None:
            self.layout_ids = m.get('LayoutIds')
        if m.get('MediaEncode') is not None:
            self.media_encode = m.get('MediaEncode')
        if m.get('MnsQueue') is not None:
            self.mns_queue = m.get('MnsQueue')
        if m.get('Name') is not None:
            self.name = m.get('Name')
        if m.get('OssBucket') is not None:
            self.oss_bucket = m.get('OssBucket')
        if m.get('OssFilePrefix') is not None:
            self.oss_file_prefix = m.get('OssFilePrefix')
        if m.get('TaskProfile') is not None:
            self.task_profile = m.get('TaskProfile')
        if m.get('TemplateId') is not None:
            self.template_id = m.get('TemplateId')
        self.watermarks = []
        if m.get('Watermarks') is not None:
            for k in m.get('Watermarks'):
                temp_model = DescribeRecordTemplatesResponseBodyTemplatesWatermarks()
                self.watermarks.append(temp_model.from_map(k))
        return self


class DescribeRecordTemplatesResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
        templates: List[DescribeRecordTemplatesResponseBodyTemplates] = None,
        total_num: int = None,
        total_page: int = None,
    ):
        self.request_id = request_id
        self.templates = templates
        self.total_num = total_num
        self.total_page = total_page

    def validate(self):
        if self.templates:
            for k in self.templates:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        result['Templates'] = []
        if self.templates is not None:
            for k in self.templates:
                result['Templates'].append(k.to_map() if k else None)
        if self.total_num is not None:
            result['TotalNum'] = self.total_num
        if self.total_page is not None:
            result['TotalPage'] = self.total_page
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        self.templates = []
        if m.get('Templates') is not None:
            for k in m.get('Templates'):
                temp_model = DescribeRecordTemplatesResponseBodyTemplates()
                self.templates.append(temp_model.from_map(k))
        if m.get('TotalNum') is not None:
            self.total_num = m.get('TotalNum')
        if m.get('TotalPage') is not None:
            self.total_page = m.get('TotalPage')
        return self


class DescribeRecordTemplatesResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: DescribeRecordTemplatesResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.status_code, 'status_code')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = DescribeRecordTemplatesResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DescribeRtcChannelListRequest(TeaModel):
    def __init__(
        self,
        app_id: str = None,
        channel_id: str = None,
        owner_id: int = None,
        page_no: int = None,
        page_size: int = None,
        service_area: str = None,
        sort_type: str = None,
        time_point: str = None,
        user_id: str = None,
    ):
        self.app_id = app_id
        self.channel_id = channel_id
        self.owner_id = owner_id
        self.page_no = page_no
        self.page_size = page_size
        self.service_area = service_area
        self.sort_type = sort_type
        self.time_point = time_point
        self.user_id = user_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.app_id is not None:
            result['AppId'] = self.app_id
        if self.channel_id is not None:
            result['ChannelId'] = self.channel_id
        if self.owner_id is not None:
            result['OwnerId'] = self.owner_id
        if self.page_no is not None:
            result['PageNo'] = self.page_no
        if self.page_size is not None:
            result['PageSize'] = self.page_size
        if self.service_area is not None:
            result['ServiceArea'] = self.service_area
        if self.sort_type is not None:
            result['SortType'] = self.sort_type
        if self.time_point is not None:
            result['TimePoint'] = self.time_point
        if self.user_id is not None:
            result['UserId'] = self.user_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('AppId') is not None:
            self.app_id = m.get('AppId')
        if m.get('ChannelId') is not None:
            self.channel_id = m.get('ChannelId')
        if m.get('OwnerId') is not None:
            self.owner_id = m.get('OwnerId')
        if m.get('PageNo') is not None:
            self.page_no = m.get('PageNo')
        if m.get('PageSize') is not None:
            self.page_size = m.get('PageSize')
        if m.get('ServiceArea') is not None:
            self.service_area = m.get('ServiceArea')
        if m.get('SortType') is not None:
            self.sort_type = m.get('SortType')
        if m.get('TimePoint') is not None:
            self.time_point = m.get('TimePoint')
        if m.get('UserId') is not None:
            self.user_id = m.get('UserId')
        return self


class DescribeRtcChannelListResponseBodyChannelListChannelListCallArea(TeaModel):
    def __init__(
        self,
        call_area: List[str] = None,
    ):
        self.call_area = call_area

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.call_area is not None:
            result['CallArea'] = self.call_area
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('CallArea') is not None:
            self.call_area = m.get('CallArea')
        return self


class DescribeRtcChannelListResponseBodyChannelListChannelList(TeaModel):
    def __init__(
        self,
        call_area: DescribeRtcChannelListResponseBodyChannelListChannelListCallArea = None,
        channel_id: str = None,
        end_time: str = None,
        start_time: str = None,
        total_user_cnt: int = None,
    ):
        self.call_area = call_area
        self.channel_id = channel_id
        self.end_time = end_time
        self.start_time = start_time
        self.total_user_cnt = total_user_cnt

    def validate(self):
        if self.call_area:
            self.call_area.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.call_area is not None:
            result['CallArea'] = self.call_area.to_map()
        if self.channel_id is not None:
            result['ChannelId'] = self.channel_id
        if self.end_time is not None:
            result['EndTime'] = self.end_time
        if self.start_time is not None:
            result['StartTime'] = self.start_time
        if self.total_user_cnt is not None:
            result['TotalUserCnt'] = self.total_user_cnt
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('CallArea') is not None:
            temp_model = DescribeRtcChannelListResponseBodyChannelListChannelListCallArea()
            self.call_area = temp_model.from_map(m['CallArea'])
        if m.get('ChannelId') is not None:
            self.channel_id = m.get('ChannelId')
        if m.get('EndTime') is not None:
            self.end_time = m.get('EndTime')
        if m.get('StartTime') is not None:
            self.start_time = m.get('StartTime')
        if m.get('TotalUserCnt') is not None:
            self.total_user_cnt = m.get('TotalUserCnt')
        return self


class DescribeRtcChannelListResponseBodyChannelList(TeaModel):
    def __init__(
        self,
        channel_list: List[DescribeRtcChannelListResponseBodyChannelListChannelList] = None,
    ):
        self.channel_list = channel_list

    def validate(self):
        if self.channel_list:
            for k in self.channel_list:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        result['ChannelList'] = []
        if self.channel_list is not None:
            for k in self.channel_list:
                result['ChannelList'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.channel_list = []
        if m.get('ChannelList') is not None:
            for k in m.get('ChannelList'):
                temp_model = DescribeRtcChannelListResponseBodyChannelListChannelList()
                self.channel_list.append(temp_model.from_map(k))
        return self


class DescribeRtcChannelListResponseBody(TeaModel):
    def __init__(
        self,
        channel_list: DescribeRtcChannelListResponseBodyChannelList = None,
        page_no: int = None,
        page_size: int = None,
        request_id: str = None,
        total_cnt: int = None,
    ):
        self.channel_list = channel_list
        self.page_no = page_no
        self.page_size = page_size
        self.request_id = request_id
        self.total_cnt = total_cnt

    def validate(self):
        if self.channel_list:
            self.channel_list.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.channel_list is not None:
            result['ChannelList'] = self.channel_list.to_map()
        if self.page_no is not None:
            result['PageNo'] = self.page_no
        if self.page_size is not None:
            result['PageSize'] = self.page_size
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.total_cnt is not None:
            result['TotalCnt'] = self.total_cnt
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ChannelList') is not None:
            temp_model = DescribeRtcChannelListResponseBodyChannelList()
            self.channel_list = temp_model.from_map(m['ChannelList'])
        if m.get('PageNo') is not None:
            self.page_no = m.get('PageNo')
        if m.get('PageSize') is not None:
            self.page_size = m.get('PageSize')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('TotalCnt') is not None:
            self.total_cnt = m.get('TotalCnt')
        return self


class DescribeRtcChannelListResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: DescribeRtcChannelListResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.status_code, 'status_code')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = DescribeRtcChannelListResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DescribeRtcChannelMetricRequest(TeaModel):
    def __init__(
        self,
        app_id: str = None,
        channel_id: str = None,
        owner_id: int = None,
        time_point: str = None,
    ):
        self.app_id = app_id
        self.channel_id = channel_id
        self.owner_id = owner_id
        self.time_point = time_point

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.app_id is not None:
            result['AppId'] = self.app_id
        if self.channel_id is not None:
            result['ChannelId'] = self.channel_id
        if self.owner_id is not None:
            result['OwnerId'] = self.owner_id
        if self.time_point is not None:
            result['TimePoint'] = self.time_point
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('AppId') is not None:
            self.app_id = m.get('AppId')
        if m.get('ChannelId') is not None:
            self.channel_id = m.get('ChannelId')
        if m.get('OwnerId') is not None:
            self.owner_id = m.get('OwnerId')
        if m.get('TimePoint') is not None:
            self.time_point = m.get('TimePoint')
        return self


class DescribeRtcChannelMetricResponseBodyChannelMetricInfoChannelMetric(TeaModel):
    def __init__(
        self,
        channel_id: str = None,
        end_time: str = None,
        pub_user_count: int = None,
        start_time: str = None,
        sub_user_count: int = None,
        user_count: int = None,
    ):
        self.channel_id = channel_id
        self.end_time = end_time
        self.pub_user_count = pub_user_count
        self.start_time = start_time
        self.sub_user_count = sub_user_count
        self.user_count = user_count

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.channel_id is not None:
            result['ChannelId'] = self.channel_id
        if self.end_time is not None:
            result['EndTime'] = self.end_time
        if self.pub_user_count is not None:
            result['PubUserCount'] = self.pub_user_count
        if self.start_time is not None:
            result['StartTime'] = self.start_time
        if self.sub_user_count is not None:
            result['SubUserCount'] = self.sub_user_count
        if self.user_count is not None:
            result['UserCount'] = self.user_count
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ChannelId') is not None:
            self.channel_id = m.get('ChannelId')
        if m.get('EndTime') is not None:
            self.end_time = m.get('EndTime')
        if m.get('PubUserCount') is not None:
            self.pub_user_count = m.get('PubUserCount')
        if m.get('StartTime') is not None:
            self.start_time = m.get('StartTime')
        if m.get('SubUserCount') is not None:
            self.sub_user_count = m.get('SubUserCount')
        if m.get('UserCount') is not None:
            self.user_count = m.get('UserCount')
        return self


class DescribeRtcChannelMetricResponseBodyChannelMetricInfoDurationPubDuration(TeaModel):
    def __init__(
        self,
        audio: int = None,
        content: int = None,
        video_1080: int = None,
        video_360: int = None,
        video_720: int = None,
    ):
        self.audio = audio
        self.content = content
        self.video_1080 = video_1080
        self.video_360 = video_360
        self.video_720 = video_720

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.audio is not None:
            result['Audio'] = self.audio
        if self.content is not None:
            result['Content'] = self.content
        if self.video_1080 is not None:
            result['Video1080'] = self.video_1080
        if self.video_360 is not None:
            result['Video360'] = self.video_360
        if self.video_720 is not None:
            result['Video720'] = self.video_720
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Audio') is not None:
            self.audio = m.get('Audio')
        if m.get('Content') is not None:
            self.content = m.get('Content')
        if m.get('Video1080') is not None:
            self.video_1080 = m.get('Video1080')
        if m.get('Video360') is not None:
            self.video_360 = m.get('Video360')
        if m.get('Video720') is not None:
            self.video_720 = m.get('Video720')
        return self


class DescribeRtcChannelMetricResponseBodyChannelMetricInfoDurationSubDuration(TeaModel):
    def __init__(
        self,
        audio: int = None,
        content: int = None,
        video_1080: int = None,
        video_360: int = None,
        video_720: int = None,
    ):
        self.audio = audio
        self.content = content
        self.video_1080 = video_1080
        self.video_360 = video_360
        self.video_720 = video_720

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.audio is not None:
            result['Audio'] = self.audio
        if self.content is not None:
            result['Content'] = self.content
        if self.video_1080 is not None:
            result['Video1080'] = self.video_1080
        if self.video_360 is not None:
            result['Video360'] = self.video_360
        if self.video_720 is not None:
            result['Video720'] = self.video_720
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Audio') is not None:
            self.audio = m.get('Audio')
        if m.get('Content') is not None:
            self.content = m.get('Content')
        if m.get('Video1080') is not None:
            self.video_1080 = m.get('Video1080')
        if m.get('Video360') is not None:
            self.video_360 = m.get('Video360')
        if m.get('Video720') is not None:
            self.video_720 = m.get('Video720')
        return self


class DescribeRtcChannelMetricResponseBodyChannelMetricInfoDuration(TeaModel):
    def __init__(
        self,
        pub_duration: DescribeRtcChannelMetricResponseBodyChannelMetricInfoDurationPubDuration = None,
        sub_duration: DescribeRtcChannelMetricResponseBodyChannelMetricInfoDurationSubDuration = None,
    ):
        self.pub_duration = pub_duration
        self.sub_duration = sub_duration

    def validate(self):
        if self.pub_duration:
            self.pub_duration.validate()
        if self.sub_duration:
            self.sub_duration.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.pub_duration is not None:
            result['PubDuration'] = self.pub_duration.to_map()
        if self.sub_duration is not None:
            result['SubDuration'] = self.sub_duration.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('PubDuration') is not None:
            temp_model = DescribeRtcChannelMetricResponseBodyChannelMetricInfoDurationPubDuration()
            self.pub_duration = temp_model.from_map(m['PubDuration'])
        if m.get('SubDuration') is not None:
            temp_model = DescribeRtcChannelMetricResponseBodyChannelMetricInfoDurationSubDuration()
            self.sub_duration = temp_model.from_map(m['SubDuration'])
        return self


class DescribeRtcChannelMetricResponseBodyChannelMetricInfo(TeaModel):
    def __init__(
        self,
        channel_metric: DescribeRtcChannelMetricResponseBodyChannelMetricInfoChannelMetric = None,
        duration: DescribeRtcChannelMetricResponseBodyChannelMetricInfoDuration = None,
    ):
        self.channel_metric = channel_metric
        self.duration = duration

    def validate(self):
        if self.channel_metric:
            self.channel_metric.validate()
        if self.duration:
            self.duration.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.channel_metric is not None:
            result['ChannelMetric'] = self.channel_metric.to_map()
        if self.duration is not None:
            result['Duration'] = self.duration.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ChannelMetric') is not None:
            temp_model = DescribeRtcChannelMetricResponseBodyChannelMetricInfoChannelMetric()
            self.channel_metric = temp_model.from_map(m['ChannelMetric'])
        if m.get('Duration') is not None:
            temp_model = DescribeRtcChannelMetricResponseBodyChannelMetricInfoDuration()
            self.duration = temp_model.from_map(m['Duration'])
        return self


class DescribeRtcChannelMetricResponseBody(TeaModel):
    def __init__(
        self,
        channel_metric_info: DescribeRtcChannelMetricResponseBodyChannelMetricInfo = None,
        request_id: str = None,
    ):
        self.channel_metric_info = channel_metric_info
        self.request_id = request_id

    def validate(self):
        if self.channel_metric_info:
            self.channel_metric_info.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.channel_metric_info is not None:
            result['ChannelMetricInfo'] = self.channel_metric_info.to_map()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ChannelMetricInfo') is not None:
            temp_model = DescribeRtcChannelMetricResponseBodyChannelMetricInfo()
            self.channel_metric_info = temp_model.from_map(m['ChannelMetricInfo'])
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        return self


class DescribeRtcChannelMetricResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: DescribeRtcChannelMetricResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.status_code, 'status_code')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = DescribeRtcChannelMetricResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DescribeRtcDurationDataRequest(TeaModel):
    def __init__(
        self,
        app_id: str = None,
        end_time: str = None,
        interval: str = None,
        owner_id: int = None,
        service_area: str = None,
        start_time: str = None,
    ):
        self.app_id = app_id
        self.end_time = end_time
        self.interval = interval
        self.owner_id = owner_id
        self.service_area = service_area
        self.start_time = start_time

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.app_id is not None:
            result['AppId'] = self.app_id
        if self.end_time is not None:
            result['EndTime'] = self.end_time
        if self.interval is not None:
            result['Interval'] = self.interval
        if self.owner_id is not None:
            result['OwnerId'] = self.owner_id
        if self.service_area is not None:
            result['ServiceArea'] = self.service_area
        if self.start_time is not None:
            result['StartTime'] = self.start_time
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('AppId') is not None:
            self.app_id = m.get('AppId')
        if m.get('EndTime') is not None:
            self.end_time = m.get('EndTime')
        if m.get('Interval') is not None:
            self.interval = m.get('Interval')
        if m.get('OwnerId') is not None:
            self.owner_id = m.get('OwnerId')
        if m.get('ServiceArea') is not None:
            self.service_area = m.get('ServiceArea')
        if m.get('StartTime') is not None:
            self.start_time = m.get('StartTime')
        return self


class DescribeRtcDurationDataResponseBodyDurationDataPerIntervalDurationModule(TeaModel):
    def __init__(
        self,
        audio_duration: int = None,
        content_duration: int = None,
        time_stamp: str = None,
        total_duration: int = None,
        v_1080duration: int = None,
        v_360duration: int = None,
        v_720duration: int = None,
    ):
        self.audio_duration = audio_duration
        self.content_duration = content_duration
        self.time_stamp = time_stamp
        self.total_duration = total_duration
        self.v_1080duration = v_1080duration
        self.v_360duration = v_360duration
        self.v_720duration = v_720duration

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.audio_duration is not None:
            result['AudioDuration'] = self.audio_duration
        if self.content_duration is not None:
            result['ContentDuration'] = self.content_duration
        if self.time_stamp is not None:
            result['TimeStamp'] = self.time_stamp
        if self.total_duration is not None:
            result['TotalDuration'] = self.total_duration
        if self.v_1080duration is not None:
            result['V1080Duration'] = self.v_1080duration
        if self.v_360duration is not None:
            result['V360Duration'] = self.v_360duration
        if self.v_720duration is not None:
            result['V720Duration'] = self.v_720duration
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('AudioDuration') is not None:
            self.audio_duration = m.get('AudioDuration')
        if m.get('ContentDuration') is not None:
            self.content_duration = m.get('ContentDuration')
        if m.get('TimeStamp') is not None:
            self.time_stamp = m.get('TimeStamp')
        if m.get('TotalDuration') is not None:
            self.total_duration = m.get('TotalDuration')
        if m.get('V1080Duration') is not None:
            self.v_1080duration = m.get('V1080Duration')
        if m.get('V360Duration') is not None:
            self.v_360duration = m.get('V360Duration')
        if m.get('V720Duration') is not None:
            self.v_720duration = m.get('V720Duration')
        return self


class DescribeRtcDurationDataResponseBodyDurationDataPerInterval(TeaModel):
    def __init__(
        self,
        duration_module: List[DescribeRtcDurationDataResponseBodyDurationDataPerIntervalDurationModule] = None,
    ):
        self.duration_module = duration_module

    def validate(self):
        if self.duration_module:
            for k in self.duration_module:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        result['DurationModule'] = []
        if self.duration_module is not None:
            for k in self.duration_module:
                result['DurationModule'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.duration_module = []
        if m.get('DurationModule') is not None:
            for k in m.get('DurationModule'):
                temp_model = DescribeRtcDurationDataResponseBodyDurationDataPerIntervalDurationModule()
                self.duration_module.append(temp_model.from_map(k))
        return self


class DescribeRtcDurationDataResponseBody(TeaModel):
    def __init__(
        self,
        duration_data_per_interval: DescribeRtcDurationDataResponseBodyDurationDataPerInterval = None,
        request_id: str = None,
    ):
        self.duration_data_per_interval = duration_data_per_interval
        self.request_id = request_id

    def validate(self):
        if self.duration_data_per_interval:
            self.duration_data_per_interval.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.duration_data_per_interval is not None:
            result['DurationDataPerInterval'] = self.duration_data_per_interval.to_map()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('DurationDataPerInterval') is not None:
            temp_model = DescribeRtcDurationDataResponseBodyDurationDataPerInterval()
            self.duration_data_per_interval = temp_model.from_map(m['DurationDataPerInterval'])
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        return self


class DescribeRtcDurationDataResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: DescribeRtcDurationDataResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.status_code, 'status_code')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = DescribeRtcDurationDataResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DescribeRtcPeakChannelCntDataRequest(TeaModel):
    def __init__(
        self,
        app_id: str = None,
        end_time: str = None,
        interval: str = None,
        owner_id: int = None,
        service_area: str = None,
        start_time: str = None,
    ):
        self.app_id = app_id
        self.end_time = end_time
        self.interval = interval
        self.owner_id = owner_id
        self.service_area = service_area
        self.start_time = start_time

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.app_id is not None:
            result['AppId'] = self.app_id
        if self.end_time is not None:
            result['EndTime'] = self.end_time
        if self.interval is not None:
            result['Interval'] = self.interval
        if self.owner_id is not None:
            result['OwnerId'] = self.owner_id
        if self.service_area is not None:
            result['ServiceArea'] = self.service_area
        if self.start_time is not None:
            result['StartTime'] = self.start_time
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('AppId') is not None:
            self.app_id = m.get('AppId')
        if m.get('EndTime') is not None:
            self.end_time = m.get('EndTime')
        if m.get('Interval') is not None:
            self.interval = m.get('Interval')
        if m.get('OwnerId') is not None:
            self.owner_id = m.get('OwnerId')
        if m.get('ServiceArea') is not None:
            self.service_area = m.get('ServiceArea')
        if m.get('StartTime') is not None:
            self.start_time = m.get('StartTime')
        return self


class DescribeRtcPeakChannelCntDataResponseBodyPeakChannelCntDataPerIntervalPeakChannelCntModule(TeaModel):
    def __init__(
        self,
        active_channel_peak: int = None,
        active_channel_peak_time: str = None,
        time_stamp: str = None,
    ):
        self.active_channel_peak = active_channel_peak
        self.active_channel_peak_time = active_channel_peak_time
        self.time_stamp = time_stamp

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.active_channel_peak is not None:
            result['ActiveChannelPeak'] = self.active_channel_peak
        if self.active_channel_peak_time is not None:
            result['ActiveChannelPeakTime'] = self.active_channel_peak_time
        if self.time_stamp is not None:
            result['TimeStamp'] = self.time_stamp
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ActiveChannelPeak') is not None:
            self.active_channel_peak = m.get('ActiveChannelPeak')
        if m.get('ActiveChannelPeakTime') is not None:
            self.active_channel_peak_time = m.get('ActiveChannelPeakTime')
        if m.get('TimeStamp') is not None:
            self.time_stamp = m.get('TimeStamp')
        return self


class DescribeRtcPeakChannelCntDataResponseBodyPeakChannelCntDataPerInterval(TeaModel):
    def __init__(
        self,
        peak_channel_cnt_module: List[DescribeRtcPeakChannelCntDataResponseBodyPeakChannelCntDataPerIntervalPeakChannelCntModule] = None,
    ):
        self.peak_channel_cnt_module = peak_channel_cnt_module

    def validate(self):
        if self.peak_channel_cnt_module:
            for k in self.peak_channel_cnt_module:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        result['PeakChannelCntModule'] = []
        if self.peak_channel_cnt_module is not None:
            for k in self.peak_channel_cnt_module:
                result['PeakChannelCntModule'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.peak_channel_cnt_module = []
        if m.get('PeakChannelCntModule') is not None:
            for k in m.get('PeakChannelCntModule'):
                temp_model = DescribeRtcPeakChannelCntDataResponseBodyPeakChannelCntDataPerIntervalPeakChannelCntModule()
                self.peak_channel_cnt_module.append(temp_model.from_map(k))
        return self


class DescribeRtcPeakChannelCntDataResponseBody(TeaModel):
    def __init__(
        self,
        peak_channel_cnt_data_per_interval: DescribeRtcPeakChannelCntDataResponseBodyPeakChannelCntDataPerInterval = None,
        request_id: str = None,
    ):
        self.peak_channel_cnt_data_per_interval = peak_channel_cnt_data_per_interval
        self.request_id = request_id

    def validate(self):
        if self.peak_channel_cnt_data_per_interval:
            self.peak_channel_cnt_data_per_interval.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.peak_channel_cnt_data_per_interval is not None:
            result['PeakChannelCntDataPerInterval'] = self.peak_channel_cnt_data_per_interval.to_map()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('PeakChannelCntDataPerInterval') is not None:
            temp_model = DescribeRtcPeakChannelCntDataResponseBodyPeakChannelCntDataPerInterval()
            self.peak_channel_cnt_data_per_interval = temp_model.from_map(m['PeakChannelCntDataPerInterval'])
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        return self


class DescribeRtcPeakChannelCntDataResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: DescribeRtcPeakChannelCntDataResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.status_code, 'status_code')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = DescribeRtcPeakChannelCntDataResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DescribeRtcUserCntDataRequest(TeaModel):
    def __init__(
        self,
        app_id: str = None,
        end_time: str = None,
        interval: str = None,
        owner_id: int = None,
        service_area: str = None,
        start_time: str = None,
    ):
        self.app_id = app_id
        self.end_time = end_time
        self.interval = interval
        self.owner_id = owner_id
        self.service_area = service_area
        self.start_time = start_time

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.app_id is not None:
            result['AppId'] = self.app_id
        if self.end_time is not None:
            result['EndTime'] = self.end_time
        if self.interval is not None:
            result['Interval'] = self.interval
        if self.owner_id is not None:
            result['OwnerId'] = self.owner_id
        if self.service_area is not None:
            result['ServiceArea'] = self.service_area
        if self.start_time is not None:
            result['StartTime'] = self.start_time
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('AppId') is not None:
            self.app_id = m.get('AppId')
        if m.get('EndTime') is not None:
            self.end_time = m.get('EndTime')
        if m.get('Interval') is not None:
            self.interval = m.get('Interval')
        if m.get('OwnerId') is not None:
            self.owner_id = m.get('OwnerId')
        if m.get('ServiceArea') is not None:
            self.service_area = m.get('ServiceArea')
        if m.get('StartTime') is not None:
            self.start_time = m.get('StartTime')
        return self


class DescribeRtcUserCntDataResponseBodyUserCntDataPerIntervalUserCntModule(TeaModel):
    def __init__(
        self,
        active_user_cnt: int = None,
        time_stamp: str = None,
    ):
        self.active_user_cnt = active_user_cnt
        self.time_stamp = time_stamp

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.active_user_cnt is not None:
            result['ActiveUserCnt'] = self.active_user_cnt
        if self.time_stamp is not None:
            result['TimeStamp'] = self.time_stamp
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ActiveUserCnt') is not None:
            self.active_user_cnt = m.get('ActiveUserCnt')
        if m.get('TimeStamp') is not None:
            self.time_stamp = m.get('TimeStamp')
        return self


class DescribeRtcUserCntDataResponseBodyUserCntDataPerInterval(TeaModel):
    def __init__(
        self,
        user_cnt_module: List[DescribeRtcUserCntDataResponseBodyUserCntDataPerIntervalUserCntModule] = None,
    ):
        self.user_cnt_module = user_cnt_module

    def validate(self):
        if self.user_cnt_module:
            for k in self.user_cnt_module:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        result['UserCntModule'] = []
        if self.user_cnt_module is not None:
            for k in self.user_cnt_module:
                result['UserCntModule'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.user_cnt_module = []
        if m.get('UserCntModule') is not None:
            for k in m.get('UserCntModule'):
                temp_model = DescribeRtcUserCntDataResponseBodyUserCntDataPerIntervalUserCntModule()
                self.user_cnt_module.append(temp_model.from_map(k))
        return self


class DescribeRtcUserCntDataResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
        user_cnt_data_per_interval: DescribeRtcUserCntDataResponseBodyUserCntDataPerInterval = None,
    ):
        self.request_id = request_id
        self.user_cnt_data_per_interval = user_cnt_data_per_interval

    def validate(self):
        if self.user_cnt_data_per_interval:
            self.user_cnt_data_per_interval.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.user_cnt_data_per_interval is not None:
            result['UserCntDataPerInterval'] = self.user_cnt_data_per_interval.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('UserCntDataPerInterval') is not None:
            temp_model = DescribeRtcUserCntDataResponseBodyUserCntDataPerInterval()
            self.user_cnt_data_per_interval = temp_model.from_map(m['UserCntDataPerInterval'])
        return self


class DescribeRtcUserCntDataResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: DescribeRtcUserCntDataResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.status_code, 'status_code')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = DescribeRtcUserCntDataResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DescribeUserInfoInChannelRequest(TeaModel):
    def __init__(
        self,
        app_id: str = None,
        channel_id: str = None,
        owner_id: int = None,
        user_id: str = None,
    ):
        self.app_id = app_id
        self.channel_id = channel_id
        self.owner_id = owner_id
        self.user_id = user_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.app_id is not None:
            result['AppId'] = self.app_id
        if self.channel_id is not None:
            result['ChannelId'] = self.channel_id
        if self.owner_id is not None:
            result['OwnerId'] = self.owner_id
        if self.user_id is not None:
            result['UserId'] = self.user_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('AppId') is not None:
            self.app_id = m.get('AppId')
        if m.get('ChannelId') is not None:
            self.channel_id = m.get('ChannelId')
        if m.get('OwnerId') is not None:
            self.owner_id = m.get('OwnerId')
        if m.get('UserId') is not None:
            self.user_id = m.get('UserId')
        return self


class DescribeUserInfoInChannelResponseBodyProperty(TeaModel):
    def __init__(
        self,
        join: int = None,
        role: int = None,
        session: str = None,
    ):
        self.join = join
        self.role = role
        self.session = session

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.join is not None:
            result['Join'] = self.join
        if self.role is not None:
            result['Role'] = self.role
        if self.session is not None:
            result['Session'] = self.session
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Join') is not None:
            self.join = m.get('Join')
        if m.get('Role') is not None:
            self.role = m.get('Role')
        if m.get('Session') is not None:
            self.session = m.get('Session')
        return self


class DescribeUserInfoInChannelResponseBody(TeaModel):
    def __init__(
        self,
        is_channel_exist: bool = None,
        is_in_channel: bool = None,
        property: List[DescribeUserInfoInChannelResponseBodyProperty] = None,
        request_id: str = None,
        timestamp: int = None,
    ):
        self.is_channel_exist = is_channel_exist
        self.is_in_channel = is_in_channel
        self.property = property
        self.request_id = request_id
        self.timestamp = timestamp

    def validate(self):
        if self.property:
            for k in self.property:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.is_channel_exist is not None:
            result['IsChannelExist'] = self.is_channel_exist
        if self.is_in_channel is not None:
            result['IsInChannel'] = self.is_in_channel
        result['Property'] = []
        if self.property is not None:
            for k in self.property:
                result['Property'].append(k.to_map() if k else None)
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.timestamp is not None:
            result['Timestamp'] = self.timestamp
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('IsChannelExist') is not None:
            self.is_channel_exist = m.get('IsChannelExist')
        if m.get('IsInChannel') is not None:
            self.is_in_channel = m.get('IsInChannel')
        self.property = []
        if m.get('Property') is not None:
            for k in m.get('Property'):
                temp_model = DescribeUserInfoInChannelResponseBodyProperty()
                self.property.append(temp_model.from_map(k))
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Timestamp') is not None:
            self.timestamp = m.get('Timestamp')
        return self


class DescribeUserInfoInChannelResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: DescribeUserInfoInChannelResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.status_code, 'status_code')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = DescribeUserInfoInChannelResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DisableAutoLiveStreamRuleRequest(TeaModel):
    def __init__(
        self,
        app_id: str = None,
        owner_id: int = None,
        rule_id: int = None,
    ):
        self.app_id = app_id
        self.owner_id = owner_id
        self.rule_id = rule_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.app_id is not None:
            result['AppId'] = self.app_id
        if self.owner_id is not None:
            result['OwnerId'] = self.owner_id
        if self.rule_id is not None:
            result['RuleId'] = self.rule_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('AppId') is not None:
            self.app_id = m.get('AppId')
        if m.get('OwnerId') is not None:
            self.owner_id = m.get('OwnerId')
        if m.get('RuleId') is not None:
            self.rule_id = m.get('RuleId')
        return self


class DisableAutoLiveStreamRuleResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
    ):
        self.request_id = request_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        return self


class DisableAutoLiveStreamRuleResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: DisableAutoLiveStreamRuleResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.status_code, 'status_code')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = DisableAutoLiveStreamRuleResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class EnableAutoLiveStreamRuleRequest(TeaModel):
    def __init__(
        self,
        app_id: str = None,
        owner_id: int = None,
        rule_id: int = None,
    ):
        self.app_id = app_id
        self.owner_id = owner_id
        self.rule_id = rule_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.app_id is not None:
            result['AppId'] = self.app_id
        if self.owner_id is not None:
            result['OwnerId'] = self.owner_id
        if self.rule_id is not None:
            result['RuleId'] = self.rule_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('AppId') is not None:
            self.app_id = m.get('AppId')
        if m.get('OwnerId') is not None:
            self.owner_id = m.get('OwnerId')
        if m.get('RuleId') is not None:
            self.rule_id = m.get('RuleId')
        return self


class EnableAutoLiveStreamRuleResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
    ):
        self.request_id = request_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        return self


class EnableAutoLiveStreamRuleResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: EnableAutoLiveStreamRuleResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.status_code, 'status_code')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = EnableAutoLiveStreamRuleResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class GetMPUTaskStatusRequest(TeaModel):
    def __init__(
        self,
        app_id: str = None,
        owner_id: int = None,
        task_id: str = None,
    ):
        self.app_id = app_id
        self.owner_id = owner_id
        self.task_id = task_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.app_id is not None:
            result['AppId'] = self.app_id
        if self.owner_id is not None:
            result['OwnerId'] = self.owner_id
        if self.task_id is not None:
            result['TaskId'] = self.task_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('AppId') is not None:
            self.app_id = m.get('AppId')
        if m.get('OwnerId') is not None:
            self.owner_id = m.get('OwnerId')
        if m.get('TaskId') is not None:
            self.task_id = m.get('TaskId')
        return self


class GetMPUTaskStatusResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
        status: int = None,
    ):
        self.request_id = request_id
        self.status = status

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.status is not None:
            result['Status'] = self.status
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Status') is not None:
            self.status = m.get('Status')
        return self


class GetMPUTaskStatusResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: GetMPUTaskStatusResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.status_code, 'status_code')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = GetMPUTaskStatusResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class ModifyAppRequest(TeaModel):
    def __init__(
        self,
        app_id: str = None,
        app_name: str = None,
        owner_id: int = None,
    ):
        self.app_id = app_id
        self.app_name = app_name
        self.owner_id = owner_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.app_id is not None:
            result['AppId'] = self.app_id
        if self.app_name is not None:
            result['AppName'] = self.app_name
        if self.owner_id is not None:
            result['OwnerId'] = self.owner_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('AppId') is not None:
            self.app_id = m.get('AppId')
        if m.get('AppName') is not None:
            self.app_name = m.get('AppName')
        if m.get('OwnerId') is not None:
            self.owner_id = m.get('OwnerId')
        return self


class ModifyAppResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
    ):
        self.request_id = request_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        return self


class ModifyAppResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: ModifyAppResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.status_code, 'status_code')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = ModifyAppResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class ModifyMPULayoutRequestPanes(TeaModel):
    def __init__(
        self,
        height: float = None,
        major_pane: int = None,
        pane_id: int = None,
        width: float = None,
        x: float = None,
        y: float = None,
        zorder: int = None,
    ):
        self.height = height
        self.major_pane = major_pane
        self.pane_id = pane_id
        self.width = width
        self.x = x
        self.y = y
        self.zorder = zorder

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.height is not None:
            result['Height'] = self.height
        if self.major_pane is not None:
            result['MajorPane'] = self.major_pane
        if self.pane_id is not None:
            result['PaneId'] = self.pane_id
        if self.width is not None:
            result['Width'] = self.width
        if self.x is not None:
            result['X'] = self.x
        if self.y is not None:
            result['Y'] = self.y
        if self.zorder is not None:
            result['ZOrder'] = self.zorder
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Height') is not None:
            self.height = m.get('Height')
        if m.get('MajorPane') is not None:
            self.major_pane = m.get('MajorPane')
        if m.get('PaneId') is not None:
            self.pane_id = m.get('PaneId')
        if m.get('Width') is not None:
            self.width = m.get('Width')
        if m.get('X') is not None:
            self.x = m.get('X')
        if m.get('Y') is not None:
            self.y = m.get('Y')
        if m.get('ZOrder') is not None:
            self.zorder = m.get('ZOrder')
        return self


class ModifyMPULayoutRequest(TeaModel):
    def __init__(
        self,
        app_id: str = None,
        audio_mix_count: int = None,
        layout_id: int = None,
        name: str = None,
        owner_id: int = None,
        panes: List[ModifyMPULayoutRequestPanes] = None,
    ):
        self.app_id = app_id
        self.audio_mix_count = audio_mix_count
        self.layout_id = layout_id
        self.name = name
        self.owner_id = owner_id
        self.panes = panes

    def validate(self):
        if self.panes:
            for k in self.panes:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.app_id is not None:
            result['AppId'] = self.app_id
        if self.audio_mix_count is not None:
            result['AudioMixCount'] = self.audio_mix_count
        if self.layout_id is not None:
            result['LayoutId'] = self.layout_id
        if self.name is not None:
            result['Name'] = self.name
        if self.owner_id is not None:
            result['OwnerId'] = self.owner_id
        result['Panes'] = []
        if self.panes is not None:
            for k in self.panes:
                result['Panes'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('AppId') is not None:
            self.app_id = m.get('AppId')
        if m.get('AudioMixCount') is not None:
            self.audio_mix_count = m.get('AudioMixCount')
        if m.get('LayoutId') is not None:
            self.layout_id = m.get('LayoutId')
        if m.get('Name') is not None:
            self.name = m.get('Name')
        if m.get('OwnerId') is not None:
            self.owner_id = m.get('OwnerId')
        self.panes = []
        if m.get('Panes') is not None:
            for k in m.get('Panes'):
                temp_model = ModifyMPULayoutRequestPanes()
                self.panes.append(temp_model.from_map(k))
        return self


class ModifyMPULayoutResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
    ):
        self.request_id = request_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        return self


class ModifyMPULayoutResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: ModifyMPULayoutResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.status_code, 'status_code')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = ModifyMPULayoutResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class RemoveTerminalsRequest(TeaModel):
    def __init__(
        self,
        app_id: str = None,
        channel_id: str = None,
        owner_id: int = None,
        terminal_ids: List[str] = None,
    ):
        self.app_id = app_id
        self.channel_id = channel_id
        self.owner_id = owner_id
        self.terminal_ids = terminal_ids

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.app_id is not None:
            result['AppId'] = self.app_id
        if self.channel_id is not None:
            result['ChannelId'] = self.channel_id
        if self.owner_id is not None:
            result['OwnerId'] = self.owner_id
        if self.terminal_ids is not None:
            result['TerminalIds'] = self.terminal_ids
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('AppId') is not None:
            self.app_id = m.get('AppId')
        if m.get('ChannelId') is not None:
            self.channel_id = m.get('ChannelId')
        if m.get('OwnerId') is not None:
            self.owner_id = m.get('OwnerId')
        if m.get('TerminalIds') is not None:
            self.terminal_ids = m.get('TerminalIds')
        return self


class RemoveTerminalsResponseBodyTerminalsTerminal(TeaModel):
    def __init__(
        self,
        code: int = None,
        id: str = None,
        message: str = None,
    ):
        self.code = code
        self.id = id
        self.message = message

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.code is not None:
            result['Code'] = self.code
        if self.id is not None:
            result['Id'] = self.id
        if self.message is not None:
            result['Message'] = self.message
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Code') is not None:
            self.code = m.get('Code')
        if m.get('Id') is not None:
            self.id = m.get('Id')
        if m.get('Message') is not None:
            self.message = m.get('Message')
        return self


class RemoveTerminalsResponseBodyTerminals(TeaModel):
    def __init__(
        self,
        terminal: List[RemoveTerminalsResponseBodyTerminalsTerminal] = None,
    ):
        self.terminal = terminal

    def validate(self):
        if self.terminal:
            for k in self.terminal:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        result['Terminal'] = []
        if self.terminal is not None:
            for k in self.terminal:
                result['Terminal'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.terminal = []
        if m.get('Terminal') is not None:
            for k in m.get('Terminal'):
                temp_model = RemoveTerminalsResponseBodyTerminalsTerminal()
                self.terminal.append(temp_model.from_map(k))
        return self


class RemoveTerminalsResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
        terminals: RemoveTerminalsResponseBodyTerminals = None,
    ):
        self.request_id = request_id
        self.terminals = terminals

    def validate(self):
        if self.terminals:
            self.terminals.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.terminals is not None:
            result['Terminals'] = self.terminals.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Terminals') is not None:
            temp_model = RemoveTerminalsResponseBodyTerminals()
            self.terminals = temp_model.from_map(m['Terminals'])
        return self


class RemoveTerminalsResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: RemoveTerminalsResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.status_code, 'status_code')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = RemoveTerminalsResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class StartMPUTaskRequestBackgrounds(TeaModel):
    def __init__(
        self,
        display: int = None,
        height: float = None,
        url: str = None,
        width: float = None,
        x: float = None,
        y: float = None,
        zorder: int = None,
    ):
        self.display = display
        self.height = height
        self.url = url
        self.width = width
        self.x = x
        self.y = y
        self.zorder = zorder

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.display is not None:
            result['Display'] = self.display
        if self.height is not None:
            result['Height'] = self.height
        if self.url is not None:
            result['Url'] = self.url
        if self.width is not None:
            result['Width'] = self.width
        if self.x is not None:
            result['X'] = self.x
        if self.y is not None:
            result['Y'] = self.y
        if self.zorder is not None:
            result['ZOrder'] = self.zorder
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Display') is not None:
            self.display = m.get('Display')
        if m.get('Height') is not None:
            self.height = m.get('Height')
        if m.get('Url') is not None:
            self.url = m.get('Url')
        if m.get('Width') is not None:
            self.width = m.get('Width')
        if m.get('X') is not None:
            self.x = m.get('X')
        if m.get('Y') is not None:
            self.y = m.get('Y')
        if m.get('ZOrder') is not None:
            self.zorder = m.get('ZOrder')
        return self


class StartMPUTaskRequestClockWidgets(TeaModel):
    def __init__(
        self,
        alpha: float = None,
        border_color: int = None,
        border_width: int = None,
        box: bool = None,
        box_border_width: int = None,
        box_color: int = None,
        font_color: int = None,
        font_size: int = None,
        font_type: int = None,
        x: float = None,
        y: float = None,
        zorder: int = None,
    ):
        self.alpha = alpha
        self.border_color = border_color
        self.border_width = border_width
        self.box = box
        self.box_border_width = box_border_width
        self.box_color = box_color
        self.font_color = font_color
        self.font_size = font_size
        self.font_type = font_type
        self.x = x
        self.y = y
        self.zorder = zorder

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.alpha is not None:
            result['Alpha'] = self.alpha
        if self.border_color is not None:
            result['BorderColor'] = self.border_color
        if self.border_width is not None:
            result['BorderWidth'] = self.border_width
        if self.box is not None:
            result['Box'] = self.box
        if self.box_border_width is not None:
            result['BoxBorderWidth'] = self.box_border_width
        if self.box_color is not None:
            result['BoxColor'] = self.box_color
        if self.font_color is not None:
            result['FontColor'] = self.font_color
        if self.font_size is not None:
            result['FontSize'] = self.font_size
        if self.font_type is not None:
            result['FontType'] = self.font_type
        if self.x is not None:
            result['X'] = self.x
        if self.y is not None:
            result['Y'] = self.y
        if self.zorder is not None:
            result['ZOrder'] = self.zorder
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Alpha') is not None:
            self.alpha = m.get('Alpha')
        if m.get('BorderColor') is not None:
            self.border_color = m.get('BorderColor')
        if m.get('BorderWidth') is not None:
            self.border_width = m.get('BorderWidth')
        if m.get('Box') is not None:
            self.box = m.get('Box')
        if m.get('BoxBorderWidth') is not None:
            self.box_border_width = m.get('BoxBorderWidth')
        if m.get('BoxColor') is not None:
            self.box_color = m.get('BoxColor')
        if m.get('FontColor') is not None:
            self.font_color = m.get('FontColor')
        if m.get('FontSize') is not None:
            self.font_size = m.get('FontSize')
        if m.get('FontType') is not None:
            self.font_type = m.get('FontType')
        if m.get('X') is not None:
            self.x = m.get('X')
        if m.get('Y') is not None:
            self.y = m.get('Y')
        if m.get('ZOrder') is not None:
            self.zorder = m.get('ZOrder')
        return self


class StartMPUTaskRequestEnhancedParam(TeaModel):
    def __init__(
        self,
        enable_portrait_segmentation: bool = None,
    ):
        self.enable_portrait_segmentation = enable_portrait_segmentation

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.enable_portrait_segmentation is not None:
            result['EnablePortraitSegmentation'] = self.enable_portrait_segmentation
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('EnablePortraitSegmentation') is not None:
            self.enable_portrait_segmentation = m.get('EnablePortraitSegmentation')
        return self


class StartMPUTaskRequestUserPanesImages(TeaModel):
    def __init__(
        self,
        display: int = None,
        height: float = None,
        url: str = None,
        width: float = None,
        x: float = None,
        y: float = None,
        zorder: int = None,
    ):
        self.display = display
        self.height = height
        self.url = url
        self.width = width
        self.x = x
        self.y = y
        self.zorder = zorder

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.display is not None:
            result['Display'] = self.display
        if self.height is not None:
            result['Height'] = self.height
        if self.url is not None:
            result['Url'] = self.url
        if self.width is not None:
            result['Width'] = self.width
        if self.x is not None:
            result['X'] = self.x
        if self.y is not None:
            result['Y'] = self.y
        if self.zorder is not None:
            result['ZOrder'] = self.zorder
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Display') is not None:
            self.display = m.get('Display')
        if m.get('Height') is not None:
            self.height = m.get('Height')
        if m.get('Url') is not None:
            self.url = m.get('Url')
        if m.get('Width') is not None:
            self.width = m.get('Width')
        if m.get('X') is not None:
            self.x = m.get('X')
        if m.get('Y') is not None:
            self.y = m.get('Y')
        if m.get('ZOrder') is not None:
            self.zorder = m.get('ZOrder')
        return self


class StartMPUTaskRequestUserPanesTexts(TeaModel):
    def __init__(
        self,
        alpha: float = None,
        border_color: int = None,
        border_width: int = None,
        box: bool = None,
        box_border_width: int = None,
        box_color: int = None,
        font_color: int = None,
        font_size: int = None,
        font_type: int = None,
        text: str = None,
        x: float = None,
        y: float = None,
        zorder: int = None,
    ):
        self.alpha = alpha
        self.border_color = border_color
        self.border_width = border_width
        self.box = box
        self.box_border_width = box_border_width
        self.box_color = box_color
        self.font_color = font_color
        self.font_size = font_size
        self.font_type = font_type
        self.text = text
        self.x = x
        self.y = y
        self.zorder = zorder

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.alpha is not None:
            result['Alpha'] = self.alpha
        if self.border_color is not None:
            result['BorderColor'] = self.border_color
        if self.border_width is not None:
            result['BorderWidth'] = self.border_width
        if self.box is not None:
            result['Box'] = self.box
        if self.box_border_width is not None:
            result['BoxBorderWidth'] = self.box_border_width
        if self.box_color is not None:
            result['BoxColor'] = self.box_color
        if self.font_color is not None:
            result['FontColor'] = self.font_color
        if self.font_size is not None:
            result['FontSize'] = self.font_size
        if self.font_type is not None:
            result['FontType'] = self.font_type
        if self.text is not None:
            result['Text'] = self.text
        if self.x is not None:
            result['X'] = self.x
        if self.y is not None:
            result['Y'] = self.y
        if self.zorder is not None:
            result['ZOrder'] = self.zorder
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Alpha') is not None:
            self.alpha = m.get('Alpha')
        if m.get('BorderColor') is not None:
            self.border_color = m.get('BorderColor')
        if m.get('BorderWidth') is not None:
            self.border_width = m.get('BorderWidth')
        if m.get('Box') is not None:
            self.box = m.get('Box')
        if m.get('BoxBorderWidth') is not None:
            self.box_border_width = m.get('BoxBorderWidth')
        if m.get('BoxColor') is not None:
            self.box_color = m.get('BoxColor')
        if m.get('FontColor') is not None:
            self.font_color = m.get('FontColor')
        if m.get('FontSize') is not None:
            self.font_size = m.get('FontSize')
        if m.get('FontType') is not None:
            self.font_type = m.get('FontType')
        if m.get('Text') is not None:
            self.text = m.get('Text')
        if m.get('X') is not None:
            self.x = m.get('X')
        if m.get('Y') is not None:
            self.y = m.get('Y')
        if m.get('ZOrder') is not None:
            self.zorder = m.get('ZOrder')
        return self


class StartMPUTaskRequestUserPanes(TeaModel):
    def __init__(
        self,
        images: List[StartMPUTaskRequestUserPanesImages] = None,
        pane_id: int = None,
        segment_type: int = None,
        source_type: str = None,
        texts: List[StartMPUTaskRequestUserPanesTexts] = None,
        user_id: str = None,
    ):
        self.images = images
        self.pane_id = pane_id
        self.segment_type = segment_type
        self.source_type = source_type
        self.texts = texts
        self.user_id = user_id

    def validate(self):
        if self.images:
            for k in self.images:
                if k:
                    k.validate()
        if self.texts:
            for k in self.texts:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        result['Images'] = []
        if self.images is not None:
            for k in self.images:
                result['Images'].append(k.to_map() if k else None)
        if self.pane_id is not None:
            result['PaneId'] = self.pane_id
        if self.segment_type is not None:
            result['SegmentType'] = self.segment_type
        if self.source_type is not None:
            result['SourceType'] = self.source_type
        result['Texts'] = []
        if self.texts is not None:
            for k in self.texts:
                result['Texts'].append(k.to_map() if k else None)
        if self.user_id is not None:
            result['UserId'] = self.user_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.images = []
        if m.get('Images') is not None:
            for k in m.get('Images'):
                temp_model = StartMPUTaskRequestUserPanesImages()
                self.images.append(temp_model.from_map(k))
        if m.get('PaneId') is not None:
            self.pane_id = m.get('PaneId')
        if m.get('SegmentType') is not None:
            self.segment_type = m.get('SegmentType')
        if m.get('SourceType') is not None:
            self.source_type = m.get('SourceType')
        self.texts = []
        if m.get('Texts') is not None:
            for k in m.get('Texts'):
                temp_model = StartMPUTaskRequestUserPanesTexts()
                self.texts.append(temp_model.from_map(k))
        if m.get('UserId') is not None:
            self.user_id = m.get('UserId')
        return self


class StartMPUTaskRequestWatermarks(TeaModel):
    def __init__(
        self,
        alpha: float = None,
        display: int = None,
        height: float = None,
        url: str = None,
        width: float = None,
        x: float = None,
        y: float = None,
        zorder: int = None,
    ):
        self.alpha = alpha
        self.display = display
        self.height = height
        self.url = url
        self.width = width
        self.x = x
        self.y = y
        self.zorder = zorder

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.alpha is not None:
            result['Alpha'] = self.alpha
        if self.display is not None:
            result['Display'] = self.display
        if self.height is not None:
            result['Height'] = self.height
        if self.url is not None:
            result['Url'] = self.url
        if self.width is not None:
            result['Width'] = self.width
        if self.x is not None:
            result['X'] = self.x
        if self.y is not None:
            result['Y'] = self.y
        if self.zorder is not None:
            result['ZOrder'] = self.zorder
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Alpha') is not None:
            self.alpha = m.get('Alpha')
        if m.get('Display') is not None:
            self.display = m.get('Display')
        if m.get('Height') is not None:
            self.height = m.get('Height')
        if m.get('Url') is not None:
            self.url = m.get('Url')
        if m.get('Width') is not None:
            self.width = m.get('Width')
        if m.get('X') is not None:
            self.x = m.get('X')
        if m.get('Y') is not None:
            self.y = m.get('Y')
        if m.get('ZOrder') is not None:
            self.zorder = m.get('ZOrder')
        return self


class StartMPUTaskRequest(TeaModel):
    def __init__(
        self,
        app_id: str = None,
        background_color: int = None,
        backgrounds: List[StartMPUTaskRequestBackgrounds] = None,
        channel_id: str = None,
        clock_widgets: List[StartMPUTaskRequestClockWidgets] = None,
        crop_mode: int = None,
        enhanced_param: StartMPUTaskRequestEnhancedParam = None,
        layout_ids: List[int] = None,
        media_encode: int = None,
        mix_mode: int = None,
        owner_id: int = None,
        payload_type: int = None,
        report_vad: int = None,
        rtp_ext_info: int = None,
        source_type: str = None,
        stream_type: int = None,
        stream_url: str = None,
        sub_spec_audio_users: List[str] = None,
        sub_spec_camera_users: List[str] = None,
        sub_spec_share_screen_users: List[str] = None,
        sub_spec_users: List[str] = None,
        task_id: str = None,
        task_type: int = None,
        time_stamp_ref: int = None,
        unsub_spec_audio_users: List[str] = None,
        unsub_spec_camera_users: List[str] = None,
        unsub_spec_share_screen_users: List[str] = None,
        user_panes: List[StartMPUTaskRequestUserPanes] = None,
        vad_interval: int = None,
        watermarks: List[StartMPUTaskRequestWatermarks] = None,
    ):
        self.app_id = app_id
        self.background_color = background_color
        self.backgrounds = backgrounds
        self.channel_id = channel_id
        self.clock_widgets = clock_widgets
        self.crop_mode = crop_mode
        self.enhanced_param = enhanced_param
        self.layout_ids = layout_ids
        self.media_encode = media_encode
        self.mix_mode = mix_mode
        self.owner_id = owner_id
        self.payload_type = payload_type
        self.report_vad = report_vad
        self.rtp_ext_info = rtp_ext_info
        self.source_type = source_type
        self.stream_type = stream_type
        self.stream_url = stream_url
        self.sub_spec_audio_users = sub_spec_audio_users
        self.sub_spec_camera_users = sub_spec_camera_users
        self.sub_spec_share_screen_users = sub_spec_share_screen_users
        self.sub_spec_users = sub_spec_users
        self.task_id = task_id
        self.task_type = task_type
        self.time_stamp_ref = time_stamp_ref
        self.unsub_spec_audio_users = unsub_spec_audio_users
        self.unsub_spec_camera_users = unsub_spec_camera_users
        self.unsub_spec_share_screen_users = unsub_spec_share_screen_users
        self.user_panes = user_panes
        self.vad_interval = vad_interval
        self.watermarks = watermarks

    def validate(self):
        if self.backgrounds:
            for k in self.backgrounds:
                if k:
                    k.validate()
        if self.clock_widgets:
            for k in self.clock_widgets:
                if k:
                    k.validate()
        if self.enhanced_param:
            self.enhanced_param.validate()
        if self.user_panes:
            for k in self.user_panes:
                if k:
                    k.validate()
        if self.watermarks:
            for k in self.watermarks:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.app_id is not None:
            result['AppId'] = self.app_id
        if self.background_color is not None:
            result['BackgroundColor'] = self.background_color
        result['Backgrounds'] = []
        if self.backgrounds is not None:
            for k in self.backgrounds:
                result['Backgrounds'].append(k.to_map() if k else None)
        if self.channel_id is not None:
            result['ChannelId'] = self.channel_id
        result['ClockWidgets'] = []
        if self.clock_widgets is not None:
            for k in self.clock_widgets:
                result['ClockWidgets'].append(k.to_map() if k else None)
        if self.crop_mode is not None:
            result['CropMode'] = self.crop_mode
        if self.enhanced_param is not None:
            result['EnhancedParam'] = self.enhanced_param.to_map()
        if self.layout_ids is not None:
            result['LayoutIds'] = self.layout_ids
        if self.media_encode is not None:
            result['MediaEncode'] = self.media_encode
        if self.mix_mode is not None:
            result['MixMode'] = self.mix_mode
        if self.owner_id is not None:
            result['OwnerId'] = self.owner_id
        if self.payload_type is not None:
            result['PayloadType'] = self.payload_type
        if self.report_vad is not None:
            result['ReportVad'] = self.report_vad
        if self.rtp_ext_info is not None:
            result['RtpExtInfo'] = self.rtp_ext_info
        if self.source_type is not None:
            result['SourceType'] = self.source_type
        if self.stream_type is not None:
            result['StreamType'] = self.stream_type
        if self.stream_url is not None:
            result['StreamURL'] = self.stream_url
        if self.sub_spec_audio_users is not None:
            result['SubSpecAudioUsers'] = self.sub_spec_audio_users
        if self.sub_spec_camera_users is not None:
            result['SubSpecCameraUsers'] = self.sub_spec_camera_users
        if self.sub_spec_share_screen_users is not None:
            result['SubSpecShareScreenUsers'] = self.sub_spec_share_screen_users
        if self.sub_spec_users is not None:
            result['SubSpecUsers'] = self.sub_spec_users
        if self.task_id is not None:
            result['TaskId'] = self.task_id
        if self.task_type is not None:
            result['TaskType'] = self.task_type
        if self.time_stamp_ref is not None:
            result['TimeStampRef'] = self.time_stamp_ref
        if self.unsub_spec_audio_users is not None:
            result['UnsubSpecAudioUsers'] = self.unsub_spec_audio_users
        if self.unsub_spec_camera_users is not None:
            result['UnsubSpecCameraUsers'] = self.unsub_spec_camera_users
        if self.unsub_spec_share_screen_users is not None:
            result['UnsubSpecShareScreenUsers'] = self.unsub_spec_share_screen_users
        result['UserPanes'] = []
        if self.user_panes is not None:
            for k in self.user_panes:
                result['UserPanes'].append(k.to_map() if k else None)
        if self.vad_interval is not None:
            result['VadInterval'] = self.vad_interval
        result['Watermarks'] = []
        if self.watermarks is not None:
            for k in self.watermarks:
                result['Watermarks'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('AppId') is not None:
            self.app_id = m.get('AppId')
        if m.get('BackgroundColor') is not None:
            self.background_color = m.get('BackgroundColor')
        self.backgrounds = []
        if m.get('Backgrounds') is not None:
            for k in m.get('Backgrounds'):
                temp_model = StartMPUTaskRequestBackgrounds()
                self.backgrounds.append(temp_model.from_map(k))
        if m.get('ChannelId') is not None:
            self.channel_id = m.get('ChannelId')
        self.clock_widgets = []
        if m.get('ClockWidgets') is not None:
            for k in m.get('ClockWidgets'):
                temp_model = StartMPUTaskRequestClockWidgets()
                self.clock_widgets.append(temp_model.from_map(k))
        if m.get('CropMode') is not None:
            self.crop_mode = m.get('CropMode')
        if m.get('EnhancedParam') is not None:
            temp_model = StartMPUTaskRequestEnhancedParam()
            self.enhanced_param = temp_model.from_map(m['EnhancedParam'])
        if m.get('LayoutIds') is not None:
            self.layout_ids = m.get('LayoutIds')
        if m.get('MediaEncode') is not None:
            self.media_encode = m.get('MediaEncode')
        if m.get('MixMode') is not None:
            self.mix_mode = m.get('MixMode')
        if m.get('OwnerId') is not None:
            self.owner_id = m.get('OwnerId')
        if m.get('PayloadType') is not None:
            self.payload_type = m.get('PayloadType')
        if m.get('ReportVad') is not None:
            self.report_vad = m.get('ReportVad')
        if m.get('RtpExtInfo') is not None:
            self.rtp_ext_info = m.get('RtpExtInfo')
        if m.get('SourceType') is not None:
            self.source_type = m.get('SourceType')
        if m.get('StreamType') is not None:
            self.stream_type = m.get('StreamType')
        if m.get('StreamURL') is not None:
            self.stream_url = m.get('StreamURL')
        if m.get('SubSpecAudioUsers') is not None:
            self.sub_spec_audio_users = m.get('SubSpecAudioUsers')
        if m.get('SubSpecCameraUsers') is not None:
            self.sub_spec_camera_users = m.get('SubSpecCameraUsers')
        if m.get('SubSpecShareScreenUsers') is not None:
            self.sub_spec_share_screen_users = m.get('SubSpecShareScreenUsers')
        if m.get('SubSpecUsers') is not None:
            self.sub_spec_users = m.get('SubSpecUsers')
        if m.get('TaskId') is not None:
            self.task_id = m.get('TaskId')
        if m.get('TaskType') is not None:
            self.task_type = m.get('TaskType')
        if m.get('TimeStampRef') is not None:
            self.time_stamp_ref = m.get('TimeStampRef')
        if m.get('UnsubSpecAudioUsers') is not None:
            self.unsub_spec_audio_users = m.get('UnsubSpecAudioUsers')
        if m.get('UnsubSpecCameraUsers') is not None:
            self.unsub_spec_camera_users = m.get('UnsubSpecCameraUsers')
        if m.get('UnsubSpecShareScreenUsers') is not None:
            self.unsub_spec_share_screen_users = m.get('UnsubSpecShareScreenUsers')
        self.user_panes = []
        if m.get('UserPanes') is not None:
            for k in m.get('UserPanes'):
                temp_model = StartMPUTaskRequestUserPanes()
                self.user_panes.append(temp_model.from_map(k))
        if m.get('VadInterval') is not None:
            self.vad_interval = m.get('VadInterval')
        self.watermarks = []
        if m.get('Watermarks') is not None:
            for k in m.get('Watermarks'):
                temp_model = StartMPUTaskRequestWatermarks()
                self.watermarks.append(temp_model.from_map(k))
        return self


class StartMPUTaskResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
    ):
        self.request_id = request_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        return self


class StartMPUTaskResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: StartMPUTaskResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.status_code, 'status_code')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = StartMPUTaskResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class StartRecordTaskRequestUserPanesImages(TeaModel):
    def __init__(
        self,
        display: int = None,
        height: float = None,
        url: str = None,
        width: float = None,
        x: float = None,
        y: float = None,
        zorder: int = None,
    ):
        self.display = display
        self.height = height
        self.url = url
        self.width = width
        self.x = x
        self.y = y
        self.zorder = zorder

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.display is not None:
            result['Display'] = self.display
        if self.height is not None:
            result['Height'] = self.height
        if self.url is not None:
            result['Url'] = self.url
        if self.width is not None:
            result['Width'] = self.width
        if self.x is not None:
            result['X'] = self.x
        if self.y is not None:
            result['Y'] = self.y
        if self.zorder is not None:
            result['ZOrder'] = self.zorder
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Display') is not None:
            self.display = m.get('Display')
        if m.get('Height') is not None:
            self.height = m.get('Height')
        if m.get('Url') is not None:
            self.url = m.get('Url')
        if m.get('Width') is not None:
            self.width = m.get('Width')
        if m.get('X') is not None:
            self.x = m.get('X')
        if m.get('Y') is not None:
            self.y = m.get('Y')
        if m.get('ZOrder') is not None:
            self.zorder = m.get('ZOrder')
        return self


class StartRecordTaskRequestUserPanesTexts(TeaModel):
    def __init__(
        self,
        font_color: int = None,
        font_size: int = None,
        font_type: int = None,
        text: str = None,
        x: float = None,
        y: float = None,
        zorder: int = None,
    ):
        self.font_color = font_color
        self.font_size = font_size
        self.font_type = font_type
        self.text = text
        self.x = x
        self.y = y
        self.zorder = zorder

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.font_color is not None:
            result['FontColor'] = self.font_color
        if self.font_size is not None:
            result['FontSize'] = self.font_size
        if self.font_type is not None:
            result['FontType'] = self.font_type
        if self.text is not None:
            result['Text'] = self.text
        if self.x is not None:
            result['X'] = self.x
        if self.y is not None:
            result['Y'] = self.y
        if self.zorder is not None:
            result['ZOrder'] = self.zorder
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('FontColor') is not None:
            self.font_color = m.get('FontColor')
        if m.get('FontSize') is not None:
            self.font_size = m.get('FontSize')
        if m.get('FontType') is not None:
            self.font_type = m.get('FontType')
        if m.get('Text') is not None:
            self.text = m.get('Text')
        if m.get('X') is not None:
            self.x = m.get('X')
        if m.get('Y') is not None:
            self.y = m.get('Y')
        if m.get('ZOrder') is not None:
            self.zorder = m.get('ZOrder')
        return self


class StartRecordTaskRequestUserPanes(TeaModel):
    def __init__(
        self,
        images: List[StartRecordTaskRequestUserPanesImages] = None,
        pane_id: int = None,
        source_type: str = None,
        texts: List[StartRecordTaskRequestUserPanesTexts] = None,
        user_id: str = None,
    ):
        self.images = images
        self.pane_id = pane_id
        self.source_type = source_type
        self.texts = texts
        self.user_id = user_id

    def validate(self):
        if self.images:
            for k in self.images:
                if k:
                    k.validate()
        if self.texts:
            for k in self.texts:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        result['Images'] = []
        if self.images is not None:
            for k in self.images:
                result['Images'].append(k.to_map() if k else None)
        if self.pane_id is not None:
            result['PaneId'] = self.pane_id
        if self.source_type is not None:
            result['SourceType'] = self.source_type
        result['Texts'] = []
        if self.texts is not None:
            for k in self.texts:
                result['Texts'].append(k.to_map() if k else None)
        if self.user_id is not None:
            result['UserId'] = self.user_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.images = []
        if m.get('Images') is not None:
            for k in m.get('Images'):
                temp_model = StartRecordTaskRequestUserPanesImages()
                self.images.append(temp_model.from_map(k))
        if m.get('PaneId') is not None:
            self.pane_id = m.get('PaneId')
        if m.get('SourceType') is not None:
            self.source_type = m.get('SourceType')
        self.texts = []
        if m.get('Texts') is not None:
            for k in m.get('Texts'):
                temp_model = StartRecordTaskRequestUserPanesTexts()
                self.texts.append(temp_model.from_map(k))
        if m.get('UserId') is not None:
            self.user_id = m.get('UserId')
        return self


class StartRecordTaskRequest(TeaModel):
    def __init__(
        self,
        app_id: str = None,
        channel_id: str = None,
        crop_mode: int = None,
        layout_ids: List[int] = None,
        media_encode: int = None,
        mix_mode: int = None,
        owner_id: int = None,
        source_type: str = None,
        stream_type: int = None,
        sub_spec_audio_users: List[str] = None,
        sub_spec_camera_users: List[str] = None,
        sub_spec_share_screen_users: List[str] = None,
        sub_spec_users: List[str] = None,
        task_id: str = None,
        task_profile: str = None,
        template_id: str = None,
        unsub_spec_audio_users: List[str] = None,
        unsub_spec_camera_users: List[str] = None,
        unsub_spec_share_screen_users: List[str] = None,
        user_panes: List[StartRecordTaskRequestUserPanes] = None,
    ):
        self.app_id = app_id
        self.channel_id = channel_id
        self.crop_mode = crop_mode
        self.layout_ids = layout_ids
        self.media_encode = media_encode
        self.mix_mode = mix_mode
        self.owner_id = owner_id
        self.source_type = source_type
        self.stream_type = stream_type
        self.sub_spec_audio_users = sub_spec_audio_users
        self.sub_spec_camera_users = sub_spec_camera_users
        self.sub_spec_share_screen_users = sub_spec_share_screen_users
        self.sub_spec_users = sub_spec_users
        self.task_id = task_id
        self.task_profile = task_profile
        self.template_id = template_id
        self.unsub_spec_audio_users = unsub_spec_audio_users
        self.unsub_spec_camera_users = unsub_spec_camera_users
        self.unsub_spec_share_screen_users = unsub_spec_share_screen_users
        self.user_panes = user_panes

    def validate(self):
        if self.user_panes:
            for k in self.user_panes:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.app_id is not None:
            result['AppId'] = self.app_id
        if self.channel_id is not None:
            result['ChannelId'] = self.channel_id
        if self.crop_mode is not None:
            result['CropMode'] = self.crop_mode
        if self.layout_ids is not None:
            result['LayoutIds'] = self.layout_ids
        if self.media_encode is not None:
            result['MediaEncode'] = self.media_encode
        if self.mix_mode is not None:
            result['MixMode'] = self.mix_mode
        if self.owner_id is not None:
            result['OwnerId'] = self.owner_id
        if self.source_type is not None:
            result['SourceType'] = self.source_type
        if self.stream_type is not None:
            result['StreamType'] = self.stream_type
        if self.sub_spec_audio_users is not None:
            result['SubSpecAudioUsers'] = self.sub_spec_audio_users
        if self.sub_spec_camera_users is not None:
            result['SubSpecCameraUsers'] = self.sub_spec_camera_users
        if self.sub_spec_share_screen_users is not None:
            result['SubSpecShareScreenUsers'] = self.sub_spec_share_screen_users
        if self.sub_spec_users is not None:
            result['SubSpecUsers'] = self.sub_spec_users
        if self.task_id is not None:
            result['TaskId'] = self.task_id
        if self.task_profile is not None:
            result['TaskProfile'] = self.task_profile
        if self.template_id is not None:
            result['TemplateId'] = self.template_id
        if self.unsub_spec_audio_users is not None:
            result['UnsubSpecAudioUsers'] = self.unsub_spec_audio_users
        if self.unsub_spec_camera_users is not None:
            result['UnsubSpecCameraUsers'] = self.unsub_spec_camera_users
        if self.unsub_spec_share_screen_users is not None:
            result['UnsubSpecShareScreenUsers'] = self.unsub_spec_share_screen_users
        result['UserPanes'] = []
        if self.user_panes is not None:
            for k in self.user_panes:
                result['UserPanes'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('AppId') is not None:
            self.app_id = m.get('AppId')
        if m.get('ChannelId') is not None:
            self.channel_id = m.get('ChannelId')
        if m.get('CropMode') is not None:
            self.crop_mode = m.get('CropMode')
        if m.get('LayoutIds') is not None:
            self.layout_ids = m.get('LayoutIds')
        if m.get('MediaEncode') is not None:
            self.media_encode = m.get('MediaEncode')
        if m.get('MixMode') is not None:
            self.mix_mode = m.get('MixMode')
        if m.get('OwnerId') is not None:
            self.owner_id = m.get('OwnerId')
        if m.get('SourceType') is not None:
            self.source_type = m.get('SourceType')
        if m.get('StreamType') is not None:
            self.stream_type = m.get('StreamType')
        if m.get('SubSpecAudioUsers') is not None:
            self.sub_spec_audio_users = m.get('SubSpecAudioUsers')
        if m.get('SubSpecCameraUsers') is not None:
            self.sub_spec_camera_users = m.get('SubSpecCameraUsers')
        if m.get('SubSpecShareScreenUsers') is not None:
            self.sub_spec_share_screen_users = m.get('SubSpecShareScreenUsers')
        if m.get('SubSpecUsers') is not None:
            self.sub_spec_users = m.get('SubSpecUsers')
        if m.get('TaskId') is not None:
            self.task_id = m.get('TaskId')
        if m.get('TaskProfile') is not None:
            self.task_profile = m.get('TaskProfile')
        if m.get('TemplateId') is not None:
            self.template_id = m.get('TemplateId')
        if m.get('UnsubSpecAudioUsers') is not None:
            self.unsub_spec_audio_users = m.get('UnsubSpecAudioUsers')
        if m.get('UnsubSpecCameraUsers') is not None:
            self.unsub_spec_camera_users = m.get('UnsubSpecCameraUsers')
        if m.get('UnsubSpecShareScreenUsers') is not None:
            self.unsub_spec_share_screen_users = m.get('UnsubSpecShareScreenUsers')
        self.user_panes = []
        if m.get('UserPanes') is not None:
            for k in m.get('UserPanes'):
                temp_model = StartRecordTaskRequestUserPanes()
                self.user_panes.append(temp_model.from_map(k))
        return self


class StartRecordTaskResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
    ):
        self.request_id = request_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        return self


class StartRecordTaskResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: StartRecordTaskResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.status_code, 'status_code')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = StartRecordTaskResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class StopMPUTaskRequest(TeaModel):
    def __init__(
        self,
        app_id: str = None,
        owner_id: int = None,
        task_id: str = None,
    ):
        self.app_id = app_id
        self.owner_id = owner_id
        self.task_id = task_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.app_id is not None:
            result['AppId'] = self.app_id
        if self.owner_id is not None:
            result['OwnerId'] = self.owner_id
        if self.task_id is not None:
            result['TaskId'] = self.task_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('AppId') is not None:
            self.app_id = m.get('AppId')
        if m.get('OwnerId') is not None:
            self.owner_id = m.get('OwnerId')
        if m.get('TaskId') is not None:
            self.task_id = m.get('TaskId')
        return self


class StopMPUTaskResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
    ):
        self.request_id = request_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        return self


class StopMPUTaskResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: StopMPUTaskResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.status_code, 'status_code')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = StopMPUTaskResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class StopRecordTaskRequest(TeaModel):
    def __init__(
        self,
        app_id: str = None,
        owner_id: int = None,
        task_id: str = None,
    ):
        self.app_id = app_id
        self.owner_id = owner_id
        self.task_id = task_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.app_id is not None:
            result['AppId'] = self.app_id
        if self.owner_id is not None:
            result['OwnerId'] = self.owner_id
        if self.task_id is not None:
            result['TaskId'] = self.task_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('AppId') is not None:
            self.app_id = m.get('AppId')
        if m.get('OwnerId') is not None:
            self.owner_id = m.get('OwnerId')
        if m.get('TaskId') is not None:
            self.task_id = m.get('TaskId')
        return self


class StopRecordTaskResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
    ):
        self.request_id = request_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        return self


class StopRecordTaskResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: StopRecordTaskResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.status_code, 'status_code')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = StopRecordTaskResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class UpdateAutoLiveStreamRuleRequest(TeaModel):
    def __init__(
        self,
        app_id: str = None,
        call_back: str = None,
        channel_id_prefixes: List[str] = None,
        channel_ids: List[str] = None,
        media_encode: int = None,
        owner_id: int = None,
        play_domain: str = None,
        rule_id: int = None,
        rule_name: str = None,
    ):
        self.app_id = app_id
        self.call_back = call_back
        self.channel_id_prefixes = channel_id_prefixes
        self.channel_ids = channel_ids
        self.media_encode = media_encode
        self.owner_id = owner_id
        self.play_domain = play_domain
        self.rule_id = rule_id
        self.rule_name = rule_name

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.app_id is not None:
            result['AppId'] = self.app_id
        if self.call_back is not None:
            result['CallBack'] = self.call_back
        if self.channel_id_prefixes is not None:
            result['ChannelIdPrefixes'] = self.channel_id_prefixes
        if self.channel_ids is not None:
            result['ChannelIds'] = self.channel_ids
        if self.media_encode is not None:
            result['MediaEncode'] = self.media_encode
        if self.owner_id is not None:
            result['OwnerId'] = self.owner_id
        if self.play_domain is not None:
            result['PlayDomain'] = self.play_domain
        if self.rule_id is not None:
            result['RuleId'] = self.rule_id
        if self.rule_name is not None:
            result['RuleName'] = self.rule_name
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('AppId') is not None:
            self.app_id = m.get('AppId')
        if m.get('CallBack') is not None:
            self.call_back = m.get('CallBack')
        if m.get('ChannelIdPrefixes') is not None:
            self.channel_id_prefixes = m.get('ChannelIdPrefixes')
        if m.get('ChannelIds') is not None:
            self.channel_ids = m.get('ChannelIds')
        if m.get('MediaEncode') is not None:
            self.media_encode = m.get('MediaEncode')
        if m.get('OwnerId') is not None:
            self.owner_id = m.get('OwnerId')
        if m.get('PlayDomain') is not None:
            self.play_domain = m.get('PlayDomain')
        if m.get('RuleId') is not None:
            self.rule_id = m.get('RuleId')
        if m.get('RuleName') is not None:
            self.rule_name = m.get('RuleName')
        return self


class UpdateAutoLiveStreamRuleResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
    ):
        self.request_id = request_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        return self


class UpdateAutoLiveStreamRuleResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: UpdateAutoLiveStreamRuleResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.status_code, 'status_code')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = UpdateAutoLiveStreamRuleResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class UpdateMPUTaskRequestBackgrounds(TeaModel):
    def __init__(
        self,
        display: int = None,
        height: float = None,
        url: str = None,
        width: float = None,
        x: float = None,
        y: float = None,
        zorder: int = None,
    ):
        self.display = display
        self.height = height
        self.url = url
        self.width = width
        self.x = x
        self.y = y
        self.zorder = zorder

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.display is not None:
            result['Display'] = self.display
        if self.height is not None:
            result['Height'] = self.height
        if self.url is not None:
            result['Url'] = self.url
        if self.width is not None:
            result['Width'] = self.width
        if self.x is not None:
            result['X'] = self.x
        if self.y is not None:
            result['Y'] = self.y
        if self.zorder is not None:
            result['ZOrder'] = self.zorder
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Display') is not None:
            self.display = m.get('Display')
        if m.get('Height') is not None:
            self.height = m.get('Height')
        if m.get('Url') is not None:
            self.url = m.get('Url')
        if m.get('Width') is not None:
            self.width = m.get('Width')
        if m.get('X') is not None:
            self.x = m.get('X')
        if m.get('Y') is not None:
            self.y = m.get('Y')
        if m.get('ZOrder') is not None:
            self.zorder = m.get('ZOrder')
        return self


class UpdateMPUTaskRequestClockWidgets(TeaModel):
    def __init__(
        self,
        alpha: float = None,
        border_color: int = None,
        border_width: int = None,
        box: bool = None,
        box_border_width: int = None,
        box_color: int = None,
        font_color: int = None,
        font_size: int = None,
        font_type: int = None,
        x: float = None,
        y: float = None,
        zorder: int = None,
    ):
        self.alpha = alpha
        self.border_color = border_color
        self.border_width = border_width
        self.box = box
        self.box_border_width = box_border_width
        self.box_color = box_color
        self.font_color = font_color
        self.font_size = font_size
        self.font_type = font_type
        self.x = x
        self.y = y
        self.zorder = zorder

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.alpha is not None:
            result['Alpha'] = self.alpha
        if self.border_color is not None:
            result['BorderColor'] = self.border_color
        if self.border_width is not None:
            result['BorderWidth'] = self.border_width
        if self.box is not None:
            result['Box'] = self.box
        if self.box_border_width is not None:
            result['BoxBorderWidth'] = self.box_border_width
        if self.box_color is not None:
            result['BoxColor'] = self.box_color
        if self.font_color is not None:
            result['FontColor'] = self.font_color
        if self.font_size is not None:
            result['FontSize'] = self.font_size
        if self.font_type is not None:
            result['FontType'] = self.font_type
        if self.x is not None:
            result['X'] = self.x
        if self.y is not None:
            result['Y'] = self.y
        if self.zorder is not None:
            result['ZOrder'] = self.zorder
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Alpha') is not None:
            self.alpha = m.get('Alpha')
        if m.get('BorderColor') is not None:
            self.border_color = m.get('BorderColor')
        if m.get('BorderWidth') is not None:
            self.border_width = m.get('BorderWidth')
        if m.get('Box') is not None:
            self.box = m.get('Box')
        if m.get('BoxBorderWidth') is not None:
            self.box_border_width = m.get('BoxBorderWidth')
        if m.get('BoxColor') is not None:
            self.box_color = m.get('BoxColor')
        if m.get('FontColor') is not None:
            self.font_color = m.get('FontColor')
        if m.get('FontSize') is not None:
            self.font_size = m.get('FontSize')
        if m.get('FontType') is not None:
            self.font_type = m.get('FontType')
        if m.get('X') is not None:
            self.x = m.get('X')
        if m.get('Y') is not None:
            self.y = m.get('Y')
        if m.get('ZOrder') is not None:
            self.zorder = m.get('ZOrder')
        return self


class UpdateMPUTaskRequestUserPanesImages(TeaModel):
    def __init__(
        self,
        display: int = None,
        height: float = None,
        url: str = None,
        width: float = None,
        x: float = None,
        y: float = None,
        zorder: int = None,
    ):
        self.display = display
        self.height = height
        self.url = url
        self.width = width
        self.x = x
        self.y = y
        self.zorder = zorder

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.display is not None:
            result['Display'] = self.display
        if self.height is not None:
            result['Height'] = self.height
        if self.url is not None:
            result['Url'] = self.url
        if self.width is not None:
            result['Width'] = self.width
        if self.x is not None:
            result['X'] = self.x
        if self.y is not None:
            result['Y'] = self.y
        if self.zorder is not None:
            result['ZOrder'] = self.zorder
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Display') is not None:
            self.display = m.get('Display')
        if m.get('Height') is not None:
            self.height = m.get('Height')
        if m.get('Url') is not None:
            self.url = m.get('Url')
        if m.get('Width') is not None:
            self.width = m.get('Width')
        if m.get('X') is not None:
            self.x = m.get('X')
        if m.get('Y') is not None:
            self.y = m.get('Y')
        if m.get('ZOrder') is not None:
            self.zorder = m.get('ZOrder')
        return self


class UpdateMPUTaskRequestUserPanesTexts(TeaModel):
    def __init__(
        self,
        alpha: float = None,
        border_color: int = None,
        border_width: int = None,
        box: bool = None,
        box_border_width: int = None,
        box_color: int = None,
        font_color: int = None,
        font_size: int = None,
        font_type: int = None,
        text: str = None,
        x: float = None,
        y: float = None,
        zorder: int = None,
    ):
        self.alpha = alpha
        self.border_color = border_color
        self.border_width = border_width
        self.box = box
        self.box_border_width = box_border_width
        self.box_color = box_color
        self.font_color = font_color
        self.font_size = font_size
        self.font_type = font_type
        self.text = text
        self.x = x
        self.y = y
        self.zorder = zorder

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.alpha is not None:
            result['Alpha'] = self.alpha
        if self.border_color is not None:
            result['BorderColor'] = self.border_color
        if self.border_width is not None:
            result['BorderWidth'] = self.border_width
        if self.box is not None:
            result['Box'] = self.box
        if self.box_border_width is not None:
            result['BoxBorderWidth'] = self.box_border_width
        if self.box_color is not None:
            result['BoxColor'] = self.box_color
        if self.font_color is not None:
            result['FontColor'] = self.font_color
        if self.font_size is not None:
            result['FontSize'] = self.font_size
        if self.font_type is not None:
            result['FontType'] = self.font_type
        if self.text is not None:
            result['Text'] = self.text
        if self.x is not None:
            result['X'] = self.x
        if self.y is not None:
            result['Y'] = self.y
        if self.zorder is not None:
            result['ZOrder'] = self.zorder
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Alpha') is not None:
            self.alpha = m.get('Alpha')
        if m.get('BorderColor') is not None:
            self.border_color = m.get('BorderColor')
        if m.get('BorderWidth') is not None:
            self.border_width = m.get('BorderWidth')
        if m.get('Box') is not None:
            self.box = m.get('Box')
        if m.get('BoxBorderWidth') is not None:
            self.box_border_width = m.get('BoxBorderWidth')
        if m.get('BoxColor') is not None:
            self.box_color = m.get('BoxColor')
        if m.get('FontColor') is not None:
            self.font_color = m.get('FontColor')
        if m.get('FontSize') is not None:
            self.font_size = m.get('FontSize')
        if m.get('FontType') is not None:
            self.font_type = m.get('FontType')
        if m.get('Text') is not None:
            self.text = m.get('Text')
        if m.get('X') is not None:
            self.x = m.get('X')
        if m.get('Y') is not None:
            self.y = m.get('Y')
        if m.get('ZOrder') is not None:
            self.zorder = m.get('ZOrder')
        return self


class UpdateMPUTaskRequestUserPanes(TeaModel):
    def __init__(
        self,
        images: List[UpdateMPUTaskRequestUserPanesImages] = None,
        pane_id: int = None,
        segment_type: int = None,
        source_type: str = None,
        texts: List[UpdateMPUTaskRequestUserPanesTexts] = None,
        user_id: str = None,
    ):
        self.images = images
        self.pane_id = pane_id
        self.segment_type = segment_type
        self.source_type = source_type
        self.texts = texts
        self.user_id = user_id

    def validate(self):
        if self.images:
            for k in self.images:
                if k:
                    k.validate()
        if self.texts:
            for k in self.texts:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        result['Images'] = []
        if self.images is not None:
            for k in self.images:
                result['Images'].append(k.to_map() if k else None)
        if self.pane_id is not None:
            result['PaneId'] = self.pane_id
        if self.segment_type is not None:
            result['SegmentType'] = self.segment_type
        if self.source_type is not None:
            result['SourceType'] = self.source_type
        result['Texts'] = []
        if self.texts is not None:
            for k in self.texts:
                result['Texts'].append(k.to_map() if k else None)
        if self.user_id is not None:
            result['UserId'] = self.user_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.images = []
        if m.get('Images') is not None:
            for k in m.get('Images'):
                temp_model = UpdateMPUTaskRequestUserPanesImages()
                self.images.append(temp_model.from_map(k))
        if m.get('PaneId') is not None:
            self.pane_id = m.get('PaneId')
        if m.get('SegmentType') is not None:
            self.segment_type = m.get('SegmentType')
        if m.get('SourceType') is not None:
            self.source_type = m.get('SourceType')
        self.texts = []
        if m.get('Texts') is not None:
            for k in m.get('Texts'):
                temp_model = UpdateMPUTaskRequestUserPanesTexts()
                self.texts.append(temp_model.from_map(k))
        if m.get('UserId') is not None:
            self.user_id = m.get('UserId')
        return self


class UpdateMPUTaskRequestWatermarks(TeaModel):
    def __init__(
        self,
        alpha: float = None,
        display: int = None,
        height: float = None,
        url: str = None,
        width: float = None,
        x: float = None,
        y: float = None,
        zorder: int = None,
    ):
        self.alpha = alpha
        self.display = display
        self.height = height
        self.url = url
        self.width = width
        self.x = x
        self.y = y
        self.zorder = zorder

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.alpha is not None:
            result['Alpha'] = self.alpha
        if self.display is not None:
            result['Display'] = self.display
        if self.height is not None:
            result['Height'] = self.height
        if self.url is not None:
            result['Url'] = self.url
        if self.width is not None:
            result['Width'] = self.width
        if self.x is not None:
            result['X'] = self.x
        if self.y is not None:
            result['Y'] = self.y
        if self.zorder is not None:
            result['ZOrder'] = self.zorder
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Alpha') is not None:
            self.alpha = m.get('Alpha')
        if m.get('Display') is not None:
            self.display = m.get('Display')
        if m.get('Height') is not None:
            self.height = m.get('Height')
        if m.get('Url') is not None:
            self.url = m.get('Url')
        if m.get('Width') is not None:
            self.width = m.get('Width')
        if m.get('X') is not None:
            self.x = m.get('X')
        if m.get('Y') is not None:
            self.y = m.get('Y')
        if m.get('ZOrder') is not None:
            self.zorder = m.get('ZOrder')
        return self


class UpdateMPUTaskRequest(TeaModel):
    def __init__(
        self,
        app_id: str = None,
        background_color: int = None,
        backgrounds: List[UpdateMPUTaskRequestBackgrounds] = None,
        clock_widgets: List[UpdateMPUTaskRequestClockWidgets] = None,
        crop_mode: int = None,
        layout_ids: List[int] = None,
        media_encode: int = None,
        mix_mode: int = None,
        owner_id: int = None,
        source_type: str = None,
        stream_type: int = None,
        sub_spec_audio_users: List[str] = None,
        sub_spec_camera_users: List[str] = None,
        sub_spec_share_screen_users: List[str] = None,
        sub_spec_users: List[str] = None,
        task_id: str = None,
        unsub_spec_audio_users: List[str] = None,
        unsub_spec_camera_users: List[str] = None,
        unsub_spec_share_screen_users: List[str] = None,
        user_panes: List[UpdateMPUTaskRequestUserPanes] = None,
        watermarks: List[UpdateMPUTaskRequestWatermarks] = None,
    ):
        self.app_id = app_id
        self.background_color = background_color
        self.backgrounds = backgrounds
        self.clock_widgets = clock_widgets
        self.crop_mode = crop_mode
        self.layout_ids = layout_ids
        self.media_encode = media_encode
        self.mix_mode = mix_mode
        self.owner_id = owner_id
        self.source_type = source_type
        self.stream_type = stream_type
        self.sub_spec_audio_users = sub_spec_audio_users
        self.sub_spec_camera_users = sub_spec_camera_users
        self.sub_spec_share_screen_users = sub_spec_share_screen_users
        self.sub_spec_users = sub_spec_users
        self.task_id = task_id
        self.unsub_spec_audio_users = unsub_spec_audio_users
        self.unsub_spec_camera_users = unsub_spec_camera_users
        self.unsub_spec_share_screen_users = unsub_spec_share_screen_users
        self.user_panes = user_panes
        self.watermarks = watermarks

    def validate(self):
        if self.backgrounds:
            for k in self.backgrounds:
                if k:
                    k.validate()
        if self.clock_widgets:
            for k in self.clock_widgets:
                if k:
                    k.validate()
        if self.user_panes:
            for k in self.user_panes:
                if k:
                    k.validate()
        if self.watermarks:
            for k in self.watermarks:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.app_id is not None:
            result['AppId'] = self.app_id
        if self.background_color is not None:
            result['BackgroundColor'] = self.background_color
        result['Backgrounds'] = []
        if self.backgrounds is not None:
            for k in self.backgrounds:
                result['Backgrounds'].append(k.to_map() if k else None)
        result['ClockWidgets'] = []
        if self.clock_widgets is not None:
            for k in self.clock_widgets:
                result['ClockWidgets'].append(k.to_map() if k else None)
        if self.crop_mode is not None:
            result['CropMode'] = self.crop_mode
        if self.layout_ids is not None:
            result['LayoutIds'] = self.layout_ids
        if self.media_encode is not None:
            result['MediaEncode'] = self.media_encode
        if self.mix_mode is not None:
            result['MixMode'] = self.mix_mode
        if self.owner_id is not None:
            result['OwnerId'] = self.owner_id
        if self.source_type is not None:
            result['SourceType'] = self.source_type
        if self.stream_type is not None:
            result['StreamType'] = self.stream_type
        if self.sub_spec_audio_users is not None:
            result['SubSpecAudioUsers'] = self.sub_spec_audio_users
        if self.sub_spec_camera_users is not None:
            result['SubSpecCameraUsers'] = self.sub_spec_camera_users
        if self.sub_spec_share_screen_users is not None:
            result['SubSpecShareScreenUsers'] = self.sub_spec_share_screen_users
        if self.sub_spec_users is not None:
            result['SubSpecUsers'] = self.sub_spec_users
        if self.task_id is not None:
            result['TaskId'] = self.task_id
        if self.unsub_spec_audio_users is not None:
            result['UnsubSpecAudioUsers'] = self.unsub_spec_audio_users
        if self.unsub_spec_camera_users is not None:
            result['UnsubSpecCameraUsers'] = self.unsub_spec_camera_users
        if self.unsub_spec_share_screen_users is not None:
            result['UnsubSpecShareScreenUsers'] = self.unsub_spec_share_screen_users
        result['UserPanes'] = []
        if self.user_panes is not None:
            for k in self.user_panes:
                result['UserPanes'].append(k.to_map() if k else None)
        result['Watermarks'] = []
        if self.watermarks is not None:
            for k in self.watermarks:
                result['Watermarks'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('AppId') is not None:
            self.app_id = m.get('AppId')
        if m.get('BackgroundColor') is not None:
            self.background_color = m.get('BackgroundColor')
        self.backgrounds = []
        if m.get('Backgrounds') is not None:
            for k in m.get('Backgrounds'):
                temp_model = UpdateMPUTaskRequestBackgrounds()
                self.backgrounds.append(temp_model.from_map(k))
        self.clock_widgets = []
        if m.get('ClockWidgets') is not None:
            for k in m.get('ClockWidgets'):
                temp_model = UpdateMPUTaskRequestClockWidgets()
                self.clock_widgets.append(temp_model.from_map(k))
        if m.get('CropMode') is not None:
            self.crop_mode = m.get('CropMode')
        if m.get('LayoutIds') is not None:
            self.layout_ids = m.get('LayoutIds')
        if m.get('MediaEncode') is not None:
            self.media_encode = m.get('MediaEncode')
        if m.get('MixMode') is not None:
            self.mix_mode = m.get('MixMode')
        if m.get('OwnerId') is not None:
            self.owner_id = m.get('OwnerId')
        if m.get('SourceType') is not None:
            self.source_type = m.get('SourceType')
        if m.get('StreamType') is not None:
            self.stream_type = m.get('StreamType')
        if m.get('SubSpecAudioUsers') is not None:
            self.sub_spec_audio_users = m.get('SubSpecAudioUsers')
        if m.get('SubSpecCameraUsers') is not None:
            self.sub_spec_camera_users = m.get('SubSpecCameraUsers')
        if m.get('SubSpecShareScreenUsers') is not None:
            self.sub_spec_share_screen_users = m.get('SubSpecShareScreenUsers')
        if m.get('SubSpecUsers') is not None:
            self.sub_spec_users = m.get('SubSpecUsers')
        if m.get('TaskId') is not None:
            self.task_id = m.get('TaskId')
        if m.get('UnsubSpecAudioUsers') is not None:
            self.unsub_spec_audio_users = m.get('UnsubSpecAudioUsers')
        if m.get('UnsubSpecCameraUsers') is not None:
            self.unsub_spec_camera_users = m.get('UnsubSpecCameraUsers')
        if m.get('UnsubSpecShareScreenUsers') is not None:
            self.unsub_spec_share_screen_users = m.get('UnsubSpecShareScreenUsers')
        self.user_panes = []
        if m.get('UserPanes') is not None:
            for k in m.get('UserPanes'):
                temp_model = UpdateMPUTaskRequestUserPanes()
                self.user_panes.append(temp_model.from_map(k))
        self.watermarks = []
        if m.get('Watermarks') is not None:
            for k in m.get('Watermarks'):
                temp_model = UpdateMPUTaskRequestWatermarks()
                self.watermarks.append(temp_model.from_map(k))
        return self


class UpdateMPUTaskResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
    ):
        self.request_id = request_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        return self


class UpdateMPUTaskResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: UpdateMPUTaskResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.status_code, 'status_code')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = UpdateMPUTaskResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class UpdateRecordTaskRequestUserPanesImages(TeaModel):
    def __init__(
        self,
        display: int = None,
        height: float = None,
        url: str = None,
        width: float = None,
        x: float = None,
        y: float = None,
        zorder: int = None,
    ):
        self.display = display
        self.height = height
        self.url = url
        self.width = width
        self.x = x
        self.y = y
        self.zorder = zorder

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.display is not None:
            result['Display'] = self.display
        if self.height is not None:
            result['Height'] = self.height
        if self.url is not None:
            result['Url'] = self.url
        if self.width is not None:
            result['Width'] = self.width
        if self.x is not None:
            result['X'] = self.x
        if self.y is not None:
            result['Y'] = self.y
        if self.zorder is not None:
            result['ZOrder'] = self.zorder
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Display') is not None:
            self.display = m.get('Display')
        if m.get('Height') is not None:
            self.height = m.get('Height')
        if m.get('Url') is not None:
            self.url = m.get('Url')
        if m.get('Width') is not None:
            self.width = m.get('Width')
        if m.get('X') is not None:
            self.x = m.get('X')
        if m.get('Y') is not None:
            self.y = m.get('Y')
        if m.get('ZOrder') is not None:
            self.zorder = m.get('ZOrder')
        return self


class UpdateRecordTaskRequestUserPanesTexts(TeaModel):
    def __init__(
        self,
        font_color: int = None,
        font_size: int = None,
        font_type: int = None,
        text: str = None,
        x: float = None,
        y: float = None,
        zorder: int = None,
    ):
        self.font_color = font_color
        self.font_size = font_size
        self.font_type = font_type
        self.text = text
        self.x = x
        self.y = y
        self.zorder = zorder

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.font_color is not None:
            result['FontColor'] = self.font_color
        if self.font_size is not None:
            result['FontSize'] = self.font_size
        if self.font_type is not None:
            result['FontType'] = self.font_type
        if self.text is not None:
            result['Text'] = self.text
        if self.x is not None:
            result['X'] = self.x
        if self.y is not None:
            result['Y'] = self.y
        if self.zorder is not None:
            result['ZOrder'] = self.zorder
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('FontColor') is not None:
            self.font_color = m.get('FontColor')
        if m.get('FontSize') is not None:
            self.font_size = m.get('FontSize')
        if m.get('FontType') is not None:
            self.font_type = m.get('FontType')
        if m.get('Text') is not None:
            self.text = m.get('Text')
        if m.get('X') is not None:
            self.x = m.get('X')
        if m.get('Y') is not None:
            self.y = m.get('Y')
        if m.get('ZOrder') is not None:
            self.zorder = m.get('ZOrder')
        return self


class UpdateRecordTaskRequestUserPanes(TeaModel):
    def __init__(
        self,
        images: List[UpdateRecordTaskRequestUserPanesImages] = None,
        pane_id: int = None,
        source_type: str = None,
        texts: List[UpdateRecordTaskRequestUserPanesTexts] = None,
        user_id: str = None,
    ):
        self.images = images
        self.pane_id = pane_id
        self.source_type = source_type
        self.texts = texts
        self.user_id = user_id

    def validate(self):
        if self.images:
            for k in self.images:
                if k:
                    k.validate()
        if self.texts:
            for k in self.texts:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        result['Images'] = []
        if self.images is not None:
            for k in self.images:
                result['Images'].append(k.to_map() if k else None)
        if self.pane_id is not None:
            result['PaneId'] = self.pane_id
        if self.source_type is not None:
            result['SourceType'] = self.source_type
        result['Texts'] = []
        if self.texts is not None:
            for k in self.texts:
                result['Texts'].append(k.to_map() if k else None)
        if self.user_id is not None:
            result['UserId'] = self.user_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.images = []
        if m.get('Images') is not None:
            for k in m.get('Images'):
                temp_model = UpdateRecordTaskRequestUserPanesImages()
                self.images.append(temp_model.from_map(k))
        if m.get('PaneId') is not None:
            self.pane_id = m.get('PaneId')
        if m.get('SourceType') is not None:
            self.source_type = m.get('SourceType')
        self.texts = []
        if m.get('Texts') is not None:
            for k in m.get('Texts'):
                temp_model = UpdateRecordTaskRequestUserPanesTexts()
                self.texts.append(temp_model.from_map(k))
        if m.get('UserId') is not None:
            self.user_id = m.get('UserId')
        return self


class UpdateRecordTaskRequest(TeaModel):
    def __init__(
        self,
        app_id: str = None,
        channel_id: str = None,
        crop_mode: int = None,
        layout_ids: List[int] = None,
        media_encode: int = None,
        owner_id: int = None,
        sub_spec_audio_users: List[str] = None,
        sub_spec_camera_users: List[str] = None,
        sub_spec_share_screen_users: List[str] = None,
        sub_spec_users: List[str] = None,
        task_id: str = None,
        task_profile: str = None,
        template_id: str = None,
        unsub_spec_audio_users: List[str] = None,
        unsub_spec_camera_users: List[str] = None,
        unsub_spec_share_screen_users: List[str] = None,
        user_panes: List[UpdateRecordTaskRequestUserPanes] = None,
    ):
        self.app_id = app_id
        self.channel_id = channel_id
        self.crop_mode = crop_mode
        self.layout_ids = layout_ids
        self.media_encode = media_encode
        self.owner_id = owner_id
        self.sub_spec_audio_users = sub_spec_audio_users
        self.sub_spec_camera_users = sub_spec_camera_users
        self.sub_spec_share_screen_users = sub_spec_share_screen_users
        self.sub_spec_users = sub_spec_users
        self.task_id = task_id
        self.task_profile = task_profile
        self.template_id = template_id
        self.unsub_spec_audio_users = unsub_spec_audio_users
        self.unsub_spec_camera_users = unsub_spec_camera_users
        self.unsub_spec_share_screen_users = unsub_spec_share_screen_users
        self.user_panes = user_panes

    def validate(self):
        if self.user_panes:
            for k in self.user_panes:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.app_id is not None:
            result['AppId'] = self.app_id
        if self.channel_id is not None:
            result['ChannelId'] = self.channel_id
        if self.crop_mode is not None:
            result['CropMode'] = self.crop_mode
        if self.layout_ids is not None:
            result['LayoutIds'] = self.layout_ids
        if self.media_encode is not None:
            result['MediaEncode'] = self.media_encode
        if self.owner_id is not None:
            result['OwnerId'] = self.owner_id
        if self.sub_spec_audio_users is not None:
            result['SubSpecAudioUsers'] = self.sub_spec_audio_users
        if self.sub_spec_camera_users is not None:
            result['SubSpecCameraUsers'] = self.sub_spec_camera_users
        if self.sub_spec_share_screen_users is not None:
            result['SubSpecShareScreenUsers'] = self.sub_spec_share_screen_users
        if self.sub_spec_users is not None:
            result['SubSpecUsers'] = self.sub_spec_users
        if self.task_id is not None:
            result['TaskId'] = self.task_id
        if self.task_profile is not None:
            result['TaskProfile'] = self.task_profile
        if self.template_id is not None:
            result['TemplateId'] = self.template_id
        if self.unsub_spec_audio_users is not None:
            result['UnsubSpecAudioUsers'] = self.unsub_spec_audio_users
        if self.unsub_spec_camera_users is not None:
            result['UnsubSpecCameraUsers'] = self.unsub_spec_camera_users
        if self.unsub_spec_share_screen_users is not None:
            result['UnsubSpecShareScreenUsers'] = self.unsub_spec_share_screen_users
        result['UserPanes'] = []
        if self.user_panes is not None:
            for k in self.user_panes:
                result['UserPanes'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('AppId') is not None:
            self.app_id = m.get('AppId')
        if m.get('ChannelId') is not None:
            self.channel_id = m.get('ChannelId')
        if m.get('CropMode') is not None:
            self.crop_mode = m.get('CropMode')
        if m.get('LayoutIds') is not None:
            self.layout_ids = m.get('LayoutIds')
        if m.get('MediaEncode') is not None:
            self.media_encode = m.get('MediaEncode')
        if m.get('OwnerId') is not None:
            self.owner_id = m.get('OwnerId')
        if m.get('SubSpecAudioUsers') is not None:
            self.sub_spec_audio_users = m.get('SubSpecAudioUsers')
        if m.get('SubSpecCameraUsers') is not None:
            self.sub_spec_camera_users = m.get('SubSpecCameraUsers')
        if m.get('SubSpecShareScreenUsers') is not None:
            self.sub_spec_share_screen_users = m.get('SubSpecShareScreenUsers')
        if m.get('SubSpecUsers') is not None:
            self.sub_spec_users = m.get('SubSpecUsers')
        if m.get('TaskId') is not None:
            self.task_id = m.get('TaskId')
        if m.get('TaskProfile') is not None:
            self.task_profile = m.get('TaskProfile')
        if m.get('TemplateId') is not None:
            self.template_id = m.get('TemplateId')
        if m.get('UnsubSpecAudioUsers') is not None:
            self.unsub_spec_audio_users = m.get('UnsubSpecAudioUsers')
        if m.get('UnsubSpecCameraUsers') is not None:
            self.unsub_spec_camera_users = m.get('UnsubSpecCameraUsers')
        if m.get('UnsubSpecShareScreenUsers') is not None:
            self.unsub_spec_share_screen_users = m.get('UnsubSpecShareScreenUsers')
        self.user_panes = []
        if m.get('UserPanes') is not None:
            for k in m.get('UserPanes'):
                temp_model = UpdateRecordTaskRequestUserPanes()
                self.user_panes.append(temp_model.from_map(k))
        return self


class UpdateRecordTaskResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
    ):
        self.request_id = request_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        return self


class UpdateRecordTaskResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: UpdateRecordTaskResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.status_code, 'status_code')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = UpdateRecordTaskResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class UpdateRecordTemplateRequestBackgrounds(TeaModel):
    def __init__(
        self,
        display: int = None,
        height: float = None,
        url: str = None,
        width: float = None,
        x: float = None,
        y: float = None,
        zorder: int = None,
    ):
        self.display = display
        self.height = height
        self.url = url
        self.width = width
        self.x = x
        self.y = y
        self.zorder = zorder

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.display is not None:
            result['Display'] = self.display
        if self.height is not None:
            result['Height'] = self.height
        if self.url is not None:
            result['Url'] = self.url
        if self.width is not None:
            result['Width'] = self.width
        if self.x is not None:
            result['X'] = self.x
        if self.y is not None:
            result['Y'] = self.y
        if self.zorder is not None:
            result['ZOrder'] = self.zorder
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Display') is not None:
            self.display = m.get('Display')
        if m.get('Height') is not None:
            self.height = m.get('Height')
        if m.get('Url') is not None:
            self.url = m.get('Url')
        if m.get('Width') is not None:
            self.width = m.get('Width')
        if m.get('X') is not None:
            self.x = m.get('X')
        if m.get('Y') is not None:
            self.y = m.get('Y')
        if m.get('ZOrder') is not None:
            self.zorder = m.get('ZOrder')
        return self


class UpdateRecordTemplateRequestClockWidgets(TeaModel):
    def __init__(
        self,
        font_color: int = None,
        font_size: int = None,
        font_type: int = None,
        x: float = None,
        y: float = None,
        zorder: int = None,
    ):
        self.font_color = font_color
        self.font_size = font_size
        self.font_type = font_type
        self.x = x
        self.y = y
        self.zorder = zorder

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.font_color is not None:
            result['FontColor'] = self.font_color
        if self.font_size is not None:
            result['FontSize'] = self.font_size
        if self.font_type is not None:
            result['FontType'] = self.font_type
        if self.x is not None:
            result['X'] = self.x
        if self.y is not None:
            result['Y'] = self.y
        if self.zorder is not None:
            result['ZOrder'] = self.zorder
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('FontColor') is not None:
            self.font_color = m.get('FontColor')
        if m.get('FontSize') is not None:
            self.font_size = m.get('FontSize')
        if m.get('FontType') is not None:
            self.font_type = m.get('FontType')
        if m.get('X') is not None:
            self.x = m.get('X')
        if m.get('Y') is not None:
            self.y = m.get('Y')
        if m.get('ZOrder') is not None:
            self.zorder = m.get('ZOrder')
        return self


class UpdateRecordTemplateRequestWatermarks(TeaModel):
    def __init__(
        self,
        alpha: float = None,
        display: int = None,
        height: float = None,
        url: str = None,
        width: float = None,
        x: float = None,
        y: float = None,
        zorder: int = None,
    ):
        self.alpha = alpha
        self.display = display
        self.height = height
        self.url = url
        self.width = width
        self.x = x
        self.y = y
        self.zorder = zorder

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.alpha is not None:
            result['Alpha'] = self.alpha
        if self.display is not None:
            result['Display'] = self.display
        if self.height is not None:
            result['Height'] = self.height
        if self.url is not None:
            result['Url'] = self.url
        if self.width is not None:
            result['Width'] = self.width
        if self.x is not None:
            result['X'] = self.x
        if self.y is not None:
            result['Y'] = self.y
        if self.zorder is not None:
            result['ZOrder'] = self.zorder
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Alpha') is not None:
            self.alpha = m.get('Alpha')
        if m.get('Display') is not None:
            self.display = m.get('Display')
        if m.get('Height') is not None:
            self.height = m.get('Height')
        if m.get('Url') is not None:
            self.url = m.get('Url')
        if m.get('Width') is not None:
            self.width = m.get('Width')
        if m.get('X') is not None:
            self.x = m.get('X')
        if m.get('Y') is not None:
            self.y = m.get('Y')
        if m.get('ZOrder') is not None:
            self.zorder = m.get('ZOrder')
        return self


class UpdateRecordTemplateRequest(TeaModel):
    def __init__(
        self,
        app_id: str = None,
        background_color: int = None,
        backgrounds: List[UpdateRecordTemplateRequestBackgrounds] = None,
        clock_widgets: List[UpdateRecordTemplateRequestClockWidgets] = None,
        delay_stop_time: int = None,
        enable_m3u_8date_time: bool = None,
        file_split_interval: int = None,
        formats: List[str] = None,
        http_callback_url: str = None,
        layout_ids: List[int] = None,
        media_encode: int = None,
        mns_queue: str = None,
        name: str = None,
        oss_bucket: str = None,
        oss_endpoint: str = None,
        oss_file_prefix: str = None,
        owner_id: int = None,
        task_profile: str = None,
        template_id: str = None,
        watermarks: List[UpdateRecordTemplateRequestWatermarks] = None,
    ):
        self.app_id = app_id
        self.background_color = background_color
        self.backgrounds = backgrounds
        self.clock_widgets = clock_widgets
        self.delay_stop_time = delay_stop_time
        self.enable_m3u_8date_time = enable_m3u_8date_time
        self.file_split_interval = file_split_interval
        self.formats = formats
        self.http_callback_url = http_callback_url
        self.layout_ids = layout_ids
        self.media_encode = media_encode
        self.mns_queue = mns_queue
        self.name = name
        self.oss_bucket = oss_bucket
        self.oss_endpoint = oss_endpoint
        self.oss_file_prefix = oss_file_prefix
        self.owner_id = owner_id
        self.task_profile = task_profile
        self.template_id = template_id
        self.watermarks = watermarks

    def validate(self):
        if self.backgrounds:
            for k in self.backgrounds:
                if k:
                    k.validate()
        if self.clock_widgets:
            for k in self.clock_widgets:
                if k:
                    k.validate()
        if self.watermarks:
            for k in self.watermarks:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.app_id is not None:
            result['AppId'] = self.app_id
        if self.background_color is not None:
            result['BackgroundColor'] = self.background_color
        result['Backgrounds'] = []
        if self.backgrounds is not None:
            for k in self.backgrounds:
                result['Backgrounds'].append(k.to_map() if k else None)
        result['ClockWidgets'] = []
        if self.clock_widgets is not None:
            for k in self.clock_widgets:
                result['ClockWidgets'].append(k.to_map() if k else None)
        if self.delay_stop_time is not None:
            result['DelayStopTime'] = self.delay_stop_time
        if self.enable_m3u_8date_time is not None:
            result['EnableM3u8DateTime'] = self.enable_m3u_8date_time
        if self.file_split_interval is not None:
            result['FileSplitInterval'] = self.file_split_interval
        if self.formats is not None:
            result['Formats'] = self.formats
        if self.http_callback_url is not None:
            result['HttpCallbackUrl'] = self.http_callback_url
        if self.layout_ids is not None:
            result['LayoutIds'] = self.layout_ids
        if self.media_encode is not None:
            result['MediaEncode'] = self.media_encode
        if self.mns_queue is not None:
            result['MnsQueue'] = self.mns_queue
        if self.name is not None:
            result['Name'] = self.name
        if self.oss_bucket is not None:
            result['OssBucket'] = self.oss_bucket
        if self.oss_endpoint is not None:
            result['OssEndpoint'] = self.oss_endpoint
        if self.oss_file_prefix is not None:
            result['OssFilePrefix'] = self.oss_file_prefix
        if self.owner_id is not None:
            result['OwnerId'] = self.owner_id
        if self.task_profile is not None:
            result['TaskProfile'] = self.task_profile
        if self.template_id is not None:
            result['TemplateId'] = self.template_id
        result['Watermarks'] = []
        if self.watermarks is not None:
            for k in self.watermarks:
                result['Watermarks'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('AppId') is not None:
            self.app_id = m.get('AppId')
        if m.get('BackgroundColor') is not None:
            self.background_color = m.get('BackgroundColor')
        self.backgrounds = []
        if m.get('Backgrounds') is not None:
            for k in m.get('Backgrounds'):
                temp_model = UpdateRecordTemplateRequestBackgrounds()
                self.backgrounds.append(temp_model.from_map(k))
        self.clock_widgets = []
        if m.get('ClockWidgets') is not None:
            for k in m.get('ClockWidgets'):
                temp_model = UpdateRecordTemplateRequestClockWidgets()
                self.clock_widgets.append(temp_model.from_map(k))
        if m.get('DelayStopTime') is not None:
            self.delay_stop_time = m.get('DelayStopTime')
        if m.get('EnableM3u8DateTime') is not None:
            self.enable_m3u_8date_time = m.get('EnableM3u8DateTime')
        if m.get('FileSplitInterval') is not None:
            self.file_split_interval = m.get('FileSplitInterval')
        if m.get('Formats') is not None:
            self.formats = m.get('Formats')
        if m.get('HttpCallbackUrl') is not None:
            self.http_callback_url = m.get('HttpCallbackUrl')
        if m.get('LayoutIds') is not None:
            self.layout_ids = m.get('LayoutIds')
        if m.get('MediaEncode') is not None:
            self.media_encode = m.get('MediaEncode')
        if m.get('MnsQueue') is not None:
            self.mns_queue = m.get('MnsQueue')
        if m.get('Name') is not None:
            self.name = m.get('Name')
        if m.get('OssBucket') is not None:
            self.oss_bucket = m.get('OssBucket')
        if m.get('OssEndpoint') is not None:
            self.oss_endpoint = m.get('OssEndpoint')
        if m.get('OssFilePrefix') is not None:
            self.oss_file_prefix = m.get('OssFilePrefix')
        if m.get('OwnerId') is not None:
            self.owner_id = m.get('OwnerId')
        if m.get('TaskProfile') is not None:
            self.task_profile = m.get('TaskProfile')
        if m.get('TemplateId') is not None:
            self.template_id = m.get('TemplateId')
        self.watermarks = []
        if m.get('Watermarks') is not None:
            for k in m.get('Watermarks'):
                temp_model = UpdateRecordTemplateRequestWatermarks()
                self.watermarks.append(temp_model.from_map(k))
        return self


class UpdateRecordTemplateResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
        template_id: str = None,
    ):
        self.request_id = request_id
        self.template_id = template_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.template_id is not None:
            result['TemplateId'] = self.template_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('TemplateId') is not None:
            self.template_id = m.get('TemplateId')
        return self


class UpdateRecordTemplateResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: UpdateRecordTemplateResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.status_code, 'status_code')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = UpdateRecordTemplateResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


