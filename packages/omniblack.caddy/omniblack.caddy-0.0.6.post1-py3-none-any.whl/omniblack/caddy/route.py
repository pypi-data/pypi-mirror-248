from __future__ import annotations

from collections.abc import Sequence, Mapping
from operator import attrgetter
from re import Pattern, compile
from typing import (
    Annotated,
    Any,
    ClassVar,
    Iterable,
    Literal,
    NoReturn,
    Optional,
    Union,
)

from pydantic import (
    BaseModel,
    Field,
    ConfigDict,
    model_serializer,
)

handlers = Literal[
    'acme_server',
    'authentication',
    'encode',
    'error',
    'file_server',
    'headers',
    'map',
    'metrics',
    'push',
    'request_body',
    'reverse_proxy',
    'rewrite',
    'static_response',
    'subroute',
    'templates',
    'vars',
]


def empty_to_None(value):
    if isinstance(value, BaseModel):
        return empty_to_None(value.model_dump())
    elif isinstance(value, Sequence) and not isinstance(value, str):
        value = (
            empty_to_None(value)
            for value in value
        )

        value = [
            value
            for value in value
            if value is not None
        ]

        if value:
            return value
    elif isinstance(value, Mapping):
        value = (
            (key, empty_to_None(value))
            for key, value in value.items()
        )

        value = {
            key: value
            for key, value in value
            if value is not None
        }

        if value:
            return value
    else:
        return value


class CaddyBase(BaseModel):
    @model_serializer(mode='wrap')
    def ser_model(self, next):
        return empty_to_None(next(self))


upper_pattern = compile('([A-Z])')


class Handler(CaddyBase):
    name: ClassVar[handlers]
    sub_classes: ClassVar[list] = []

    def __init_subclass__(cls, **kwargs):
        name = cls.__name__.removesuffix('Handler')
        name = name[0].lower() + name[1:]
        snake_case = upper_pattern.sub(r'_\1', name).lower()
        cls.name = snake_case
        Handler.sub_classes.append(cls)

    @model_serializer(mode='wrap')
    def ser_handler(self, next):
        data = next(self)
        cls = self.__class__

        data['handler'] = cls.name

        return data


class EncodeHandler(Handler):
    encodings: list[Literal['gzip', 'ztsd']] = Field(default_factory=list)


class FileServerHandler(Handler):
    root: str = None
    hide: list[str] = Field(default_factory=list)
    index_names: list[str] = Field(default_factory=list)
    browse: dict | bool = None
    canonical_uris: bool = None
    status_code: int = None
    pass_thru: bool = None
    precompressed: dict = None
    precompressed_order: list[str] = Field(default_factory=list)


class ReplaceHeader(CaddyBase):
    search: str | Pattern = None
    replace: str = None


class HeaderDict(dict):
    def add(self, key, value):
        self.setdefault(key, [])
        self[key].append(value)

    def add_seq(self, key, seq):
        self.setdefault(key, [])
        self[key].extend(seq)

    def replace(self, key, value):
        self[key] = [value]

    def replace_seq(self, key, seq):
        self[key] = seq


Headers = Annotated[
    HeaderDict[str, list[str]],
    Field(default_factory=HeaderDict),
]

ReplaceHeaders = Annotated[
    HeaderDict[str, list[ReplaceHeader]],
    Field(default_factory=HeaderDict),
]


class CaddyHeader(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    add: Headers
    set: Headers
    replace: ReplaceHeaders
    delete: list[str] = Field(default_factory=list)


class Require(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    status_code: list[int] = Field(default_factory=list)
    headers: Headers


class ResponseHeader(CaddyHeader):
    require: Require = Field(default_factory=Require)
    deferred: bool = None


class HeadersHandler(Handler):
    request: CaddyHeader = Field(default_factory=CaddyHeader)
    response: ResponseHeader = Field(default_factory=ResponseHeader)


class ReverseProxyHeaders(BaseModel):
    request: CaddyHeader = Field(default_factory=CaddyHeader)
    response: ResponseHeader = Field(default_factory=ResponseHeader)


class Upstream(BaseModel):
    dial: str = ''
    max_requests: int = None


class ReverseProxyHandler(Handler):
    upstreams: list[Upstream] = Field(default_factory=list)
    headers: ReverseProxyHeaders = Field(default_factory=ReverseProxyHeaders)
    flush_interval: int = None
    buffer_requests: bool = None
    buffer_responses: bool = None
    max_buffer_size: int = None


class SubrouteHandler(Handler):
    routes: list[Route] = Field(default_factory=list)
    errors: dict[str, list[Route]] = Field(default_factory=dict)


class StaticResponseHandler(Handler):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    statue_code: int = None
    headers: Headers
    body: str = None
    close: bool = None
    abort: bool = None


class VarsHandler(Handler):
    vars: dict = Field(default_factory=dict)

    @model_serializer(mode='wrap')
    def ser_vars(self, next):
        data = next(self)

        vars = data.pop('vars')
        if empty_to_None(vars) is None:
            return None

        vars['handler'] = 'vars'
        return vars


class UriSubstring(BaseModel):
    find: str
    replace: str
    limit: int = 0


class UriPathRegexp(BaseModel):
    find: Pattern | str
    replace: str


class RewriteHandler(Handler):
    method: str = None
    uri: str = None
    strip_path_prefix: str = None
    strip_path_suffix: str = None
    uri_substring: list[UriSubstring] = Field(default_factory=list)
    path_regexp: list[UriPathRegexp] = Field(default_factory=list)


def no_and() -> NoReturn:
    raise TypeError(
        "MatcherList cannot be AND'ed.",
    )


class Matcher(BaseModel):
    name: ClassVar[str]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __init_subclass__(cls, **kwargs):
        name = cls.__name__.removesuffix('Matcher').lower()
        cls.name = name

    def __or__(self, other: Matcher | MatcherList | MatcherSet):
        if isinstance(other, Matcher):
            return MatcherList(MatcherSet(self), MatcherSet(other))
        elif isinstance(other, MatcherSet):
            return MatcherList(other, MatcherSet(self))
        elif isinstance(other, MatcherList):
            return MatcherList(self, *other)
        else:
            return NotImplemented

    __ror__ = __or__

    def __and__(self, other: Matcher | MatcherSet):
        if isinstance(other, Matcher):
            return MatcherSet(self, other)
        elif isinstance(other, MatcherSet):
            return MatcherSet(self, *other)
        elif isinstance(other, MatcherList):
            no_and()
        else:
            return NotImplemented

    __rand__ = __and__


class MatcherTuple(Matcher):
    values: list[Matcher | str] = Field(default_factory=list)

    def __init__(self, *values):
        super().__init__(values=values)

    def __repr__(self):
        cls = self.__class__
        args = ', '.join(
            repr(item)
            for item in self.values
        )
        return f'{cls.__name__}({args})'

    def __rich_repr__(self):
        yield from self.values

    @model_serializer
    def ser_matcher_tuple(self):
        values = []

        for value in self.values:
            if isinstance(value, BaseModel):
                values.append(value.model_dump())
            elif value is not None:
                values.append(value)

        values = empty_to_None(values)

        cls = self.__class__

        if not getattr(cls, 'matcher_container', None):
            return {
                cls.name: values,
            }
        else:
            return values


class HostMatcher(MatcherTuple):
    def __add__(self, other: HostMatcher):
        if isinstance(other, HostMatcher):
            return HostMatcher(*self, *other)
        else:
            return NotImplemented

    def __iadd__(self, other: HostMatcher):
        if isinstance(other, HostMatcher):
            self.values.extend(other.values)
            return self
        else:
            return NotImplemented


class PathMatcher(MatcherTuple):
    def __add__(self, other: PathMatcher):
        if isinstance(other, PathMatcher):
            return PathMatcher(*self, *other)
        else:
            return NotImplemented

    def __iadd__(self, other: PathMatcher):
        if isinstance(other, PathMatcher):
            self.values.extend(other.values)
            return self
        else:
            return NotImplemented


class DictMatcher(Matcher):
    values: dict[str, Any] = Field(default_factory=dict)

    def __getitem__(self, key):
        return self.values[key]

    def __setitem__(self, key, value):
        self.values[key] = value

    def __delitem__(self, key):
        del self.values[key]

    def __iter__(self):
        return iter(self.values)

    def keys(self):
        return self.keys()

    def values(self):
        return self.values()

    def items(self):
        return self.items()

    def get(self, key, default=None):
        return self.values(key, default)


class VarsMatcher(DictMatcher):
    def __add__(self, other: VarsMatcher):
        cls = self.__class__
        if isinstance(other, VarsMatcher):
            return cls(self.copy().update(other))
        else:
            return NotImplemented

    def __iadd__(self, other: VarsMatcher):
        if isinstance(other, VarsMatcher):
            self.values |= other.values


get_name = attrgetter('name')


class MatcherSet(MatcherTuple):
    """Caddy will AND the matchers in the set."""
    matcher_container: ClassVar = True

    def __and__(self, other: MatcherSet | Matcher) -> MatcherSet:
        cls = self.__class__
        if isinstance(other, MatcherSet):
            return cls(*self.values, *other)
        elif isinstance(other, MatcherList):
            no_and()
        elif isinstance(other, Matcher):
            return cls(*self.values, other)
        else:
            return NotImplemented

    def __iand__(self, other: MatcherSet | Matcher):
        if isinstance(other, MatcherSet):
            self.values.extend(other.values)
            return self
        elif isinstance(other, MatcherList):
            no_and()
        elif isinstance(other, Matcher):
            self.values.append(other)
            return self
        else:
            return NotImplemented

    __rand__ = __and__

    def __or__(self, other: any_matcher) -> MatcherList:
        cls = self.__class__
        if isinstance(other, MatcherList):
            other_cls = other.__class__
            return other_cls(self, *other)
        elif isinstance(other, Matcher):
            return MatcherList(self, cls(other))
        elif isinstance(other, MatcherSet):
            return MatcherList(self, other)
        else:
            return NotImplemented

    __ror__ = __or__


args_type = Iterable[Matcher | MatcherSet]


class MatcherList(MatcherTuple):
    """Caddy will OR the matchers in the list."""
    matcher_container: ClassVar = True

    @classmethod
    def _coerce(cls, args: args_type) -> Iterable[MatcherSet]:
        for arg in args:
            yield MatcherSet(arg)

    def __or__(self, other: any_matcher) -> MatcherList:
        cls = self.__class__
        if isinstance(other, MatcherList):
            return cls((*self, *other))
        elif isinstance(other, Matcher):
            return cls((*self, MatcherSet(other)))
        elif isinstance((other, MatcherSet)):
            return cls(*self, other)
        else:
            return NotImplemented

    def __iand__(self, other: any_matcher) -> MatcherList:
        if isinstance(other, MatcherList):
            self.values.extend(other.values)
        elif isinstance(other, Matcher):
            self.values.append(MatcherSet(other))
        elif isinstance(other, MatcherSet):
            self.values.append(other)
        else:
            return NotImplemented

        return self

    __ror__ = __or__

    def __and__(self, other) -> NoReturn:
        if isinstance(other, (MatcherList, MatcherSet, Matcher)):
            no_and()
        else:
            return NotImplemented

    __rand__ = __and__


any_matcher = Matcher | MatcherSet | MatcherList


all_handlers = Union[tuple(Handler.sub_classes)]


class Route(CaddyBase):
    match: MatcherList = Field(default_factory=MatcherList)
    handle: list[all_handlers] = Field(default_factory=list)
    group: Optional[str] = None
    terminal: bool = None


class Site(BaseModel):
    name: str
    hostname: str
    port: int
    local_hostname: str
    extra_routes: Optional[list[dict]] = Field(default_factory=list)

    @model_serializer
    def ser_site(self):
        headers = HeadersHandler()
        add_standard_headers(headers)

        handlers = [
            EncodeHandler(encodings=('zstd', 'gzip')),
            headers,
            ReverseProxyHandler([f'{self.local_hostname}:{self.port}']),
        ]

        route = Route(
            match=MatcherList(HostMatcher(self.hostname)),
            handle=handlers,
            terminal=True,
            group=self.hostname,
        )

        if self.extra_routes:
            all_routes = SubrouteHandler()
            all_routes.routes += self.extra_routes
            all_routes.routes.append(route)
            route = Route(
                match=MatcherList(HostMatcher(self.hostname)),
                handle=[all_routes],
                terminal=True,
            )

        return route.model_dump()


def add_standard_headers(headers):
    headers.response.delete += ('server', 'X-Powered-By')
    headers.response.deferred = True
    set_headers = headers.response.set
    set_headers.replace('referrer-policy', 'no-referrer')
    set_headers.replace('strict-transport-security', 'max-age=31536000;')
    set_headers.replace('x-content-type-options', 'nosniff')
    set_headers.replace('x-frame-options', 'DENY')
    set_headers.replace('x-permitted-cross-domain-policies', 'none')
    add_headers = headers.response.add

    """
        "A man is not dead while his name is still spoken."
            - Going Postal, Chapter 4 prologue
    """
    add_headers.add('x-clacks-overhead', 'GNU Terry Pratchett')
    add_headers.add('x-clacks-overhead', 'GNU Eddie Patterson')
    add_headers.add('x-clacks-overhead', 'GNU Katelyn Barnes')
