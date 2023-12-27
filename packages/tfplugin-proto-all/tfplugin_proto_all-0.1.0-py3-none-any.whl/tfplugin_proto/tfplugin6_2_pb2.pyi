from typing import Any
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class StringKind(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__: list[str] = []
    PLAIN: _ClassVar[StringKind]
    MARKDOWN: _ClassVar[StringKind]
PLAIN: StringKind
MARKDOWN: StringKind

class DynamicValue(_message.Message):
    __slots__ = ["msgpack", "json"]
    MSGPACK_FIELD_NUMBER: _ClassVar[int]
    JSON_FIELD_NUMBER: _ClassVar[int]
    msgpack: bytes
    json: bytes
    def __init__(self, msgpack: _Optional[bytes] = ..., json: _Optional[bytes] = ...) -> None: ...

class Diagnostic(_message.Message):
    __slots__ = ["severity", "summary", "detail", "attribute"]
    class Severity(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__: list[str] = []
        INVALID: _ClassVar[Diagnostic.Severity]
        ERROR: _ClassVar[Diagnostic.Severity]
        WARNING: _ClassVar[Diagnostic.Severity]
    INVALID: Diagnostic.Severity
    ERROR: Diagnostic.Severity
    WARNING: Diagnostic.Severity
    SEVERITY_FIELD_NUMBER: _ClassVar[int]
    SUMMARY_FIELD_NUMBER: _ClassVar[int]
    DETAIL_FIELD_NUMBER: _ClassVar[int]
    ATTRIBUTE_FIELD_NUMBER: _ClassVar[int]
    severity: Diagnostic.Severity
    summary: str
    detail: str
    attribute: AttributePath
    def __init__(self, severity: _Optional[_Union[Diagnostic.Severity, str]] = ..., summary: _Optional[str] = ..., detail: _Optional[str] = ..., attribute: _Optional[_Union[AttributePath, _Mapping[Any, Any]]] = ...) -> None: ...

class AttributePath(_message.Message):
    __slots__ = ["steps"]
    class Step(_message.Message):
        __slots__ = ["attribute_name", "element_key_string", "element_key_int"]
        ATTRIBUTE_NAME_FIELD_NUMBER: _ClassVar[int]
        ELEMENT_KEY_STRING_FIELD_NUMBER: _ClassVar[int]
        ELEMENT_KEY_INT_FIELD_NUMBER: _ClassVar[int]
        attribute_name: str
        element_key_string: str
        element_key_int: int
        def __init__(self, attribute_name: _Optional[str] = ..., element_key_string: _Optional[str] = ..., element_key_int: _Optional[int] = ...) -> None: ...
    STEPS_FIELD_NUMBER: _ClassVar[int]
    steps: _containers.RepeatedCompositeFieldContainer[AttributePath.Step]
    def __init__(self, steps: _Optional[_Iterable[_Union[AttributePath.Step, _Mapping[Any, Any]]]] = ...) -> None: ...

class StopProvider(_message.Message):
    __slots__: list[str] = []
    class Request(_message.Message):
        __slots__: list[str] = []
        def __init__(self) -> None: ...
    class Response(_message.Message):
        __slots__ = ["Error"]
        ERROR_FIELD_NUMBER: _ClassVar[int]
        Error: str
        def __init__(self, Error: _Optional[str] = ...) -> None: ...
    def __init__(self) -> None: ...

class RawState(_message.Message):
    __slots__ = ["json", "flatmap"]
    class FlatmapEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    JSON_FIELD_NUMBER: _ClassVar[int]
    FLATMAP_FIELD_NUMBER: _ClassVar[int]
    json: bytes
    flatmap: _containers.ScalarMap[str, str]
    def __init__(self, json: _Optional[bytes] = ..., flatmap: _Optional[_Mapping[str, str]] = ...) -> None: ...

class Schema(_message.Message):
    __slots__ = ["version", "block"]
    class Block(_message.Message):
        __slots__ = ["version", "attributes", "block_types", "description", "description_kind", "deprecated"]
        VERSION_FIELD_NUMBER: _ClassVar[int]
        ATTRIBUTES_FIELD_NUMBER: _ClassVar[int]
        BLOCK_TYPES_FIELD_NUMBER: _ClassVar[int]
        DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
        DESCRIPTION_KIND_FIELD_NUMBER: _ClassVar[int]
        DEPRECATED_FIELD_NUMBER: _ClassVar[int]
        version: int
        attributes: _containers.RepeatedCompositeFieldContainer[Schema.Attribute]
        block_types: _containers.RepeatedCompositeFieldContainer[Schema.NestedBlock]
        description: str
        description_kind: StringKind
        deprecated: bool
        def __init__(self, version: _Optional[int] = ..., attributes: _Optional[_Iterable[_Union[Schema.Attribute, _Mapping[Any, Any]]]] = ..., block_types: _Optional[_Iterable[_Union[Schema.NestedBlock, _Mapping[Any, Any]]]] = ..., description: _Optional[str] = ..., description_kind: _Optional[_Union[StringKind, str]] = ..., deprecated: bool = ...) -> None: ...
    class Attribute(_message.Message):
        __slots__ = ["name", "type", "nested_type", "description", "required", "optional", "computed", "sensitive", "description_kind", "deprecated"]
        NAME_FIELD_NUMBER: _ClassVar[int]
        TYPE_FIELD_NUMBER: _ClassVar[int]
        NESTED_TYPE_FIELD_NUMBER: _ClassVar[int]
        DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
        REQUIRED_FIELD_NUMBER: _ClassVar[int]
        OPTIONAL_FIELD_NUMBER: _ClassVar[int]
        COMPUTED_FIELD_NUMBER: _ClassVar[int]
        SENSITIVE_FIELD_NUMBER: _ClassVar[int]
        DESCRIPTION_KIND_FIELD_NUMBER: _ClassVar[int]
        DEPRECATED_FIELD_NUMBER: _ClassVar[int]
        name: str
        type: bytes
        nested_type: Schema.Object
        description: str
        required: bool
        optional: bool
        computed: bool
        sensitive: bool
        description_kind: StringKind
        deprecated: bool
        def __init__(self, name: _Optional[str] = ..., type: _Optional[bytes] = ..., nested_type: _Optional[_Union[Schema.Object, _Mapping[Any, Any]]] = ..., description: _Optional[str] = ..., required: bool = ..., optional: bool = ..., computed: bool = ..., sensitive: bool = ..., description_kind: _Optional[_Union[StringKind, str]] = ..., deprecated: bool = ...) -> None: ...
    class NestedBlock(_message.Message):
        __slots__ = ["type_name", "block", "nesting", "min_items", "max_items"]
        class NestingMode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
            __slots__: list[str] = []
            INVALID: _ClassVar[Schema.NestedBlock.NestingMode]
            SINGLE: _ClassVar[Schema.NestedBlock.NestingMode]
            LIST: _ClassVar[Schema.NestedBlock.NestingMode]
            SET: _ClassVar[Schema.NestedBlock.NestingMode]
            MAP: _ClassVar[Schema.NestedBlock.NestingMode]
            GROUP: _ClassVar[Schema.NestedBlock.NestingMode]
        INVALID: Schema.NestedBlock.NestingMode
        SINGLE: Schema.NestedBlock.NestingMode
        LIST: Schema.NestedBlock.NestingMode
        SET: Schema.NestedBlock.NestingMode
        MAP: Schema.NestedBlock.NestingMode
        GROUP: Schema.NestedBlock.NestingMode
        TYPE_NAME_FIELD_NUMBER: _ClassVar[int]
        BLOCK_FIELD_NUMBER: _ClassVar[int]
        NESTING_FIELD_NUMBER: _ClassVar[int]
        MIN_ITEMS_FIELD_NUMBER: _ClassVar[int]
        MAX_ITEMS_FIELD_NUMBER: _ClassVar[int]
        type_name: str
        block: Schema.Block
        nesting: Schema.NestedBlock.NestingMode
        min_items: int
        max_items: int
        def __init__(self, type_name: _Optional[str] = ..., block: _Optional[_Union[Schema.Block, _Mapping[Any, Any]]] = ..., nesting: _Optional[_Union[Schema.NestedBlock.NestingMode, str]] = ..., min_items: _Optional[int] = ..., max_items: _Optional[int] = ...) -> None: ...
    class Object(_message.Message):
        __slots__ = ["attributes", "nesting", "min_items", "max_items"]
        class NestingMode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
            __slots__: list[str] = []
            INVALID: _ClassVar[Schema.Object.NestingMode]
            SINGLE: _ClassVar[Schema.Object.NestingMode]
            LIST: _ClassVar[Schema.Object.NestingMode]
            SET: _ClassVar[Schema.Object.NestingMode]
            MAP: _ClassVar[Schema.Object.NestingMode]
        INVALID: Schema.Object.NestingMode
        SINGLE: Schema.Object.NestingMode
        LIST: Schema.Object.NestingMode
        SET: Schema.Object.NestingMode
        MAP: Schema.Object.NestingMode
        ATTRIBUTES_FIELD_NUMBER: _ClassVar[int]
        NESTING_FIELD_NUMBER: _ClassVar[int]
        MIN_ITEMS_FIELD_NUMBER: _ClassVar[int]
        MAX_ITEMS_FIELD_NUMBER: _ClassVar[int]
        attributes: _containers.RepeatedCompositeFieldContainer[Schema.Attribute]
        nesting: Schema.Object.NestingMode
        min_items: int
        max_items: int
        def __init__(self, attributes: _Optional[_Iterable[_Union[Schema.Attribute, _Mapping[Any, Any]]]] = ..., nesting: _Optional[_Union[Schema.Object.NestingMode, str]] = ..., min_items: _Optional[int] = ..., max_items: _Optional[int] = ...) -> None: ...
    VERSION_FIELD_NUMBER: _ClassVar[int]
    BLOCK_FIELD_NUMBER: _ClassVar[int]
    version: int
    block: Schema.Block
    def __init__(self, version: _Optional[int] = ..., block: _Optional[_Union[Schema.Block, _Mapping[Any, Any]]] = ...) -> None: ...

class GetProviderSchema(_message.Message):
    __slots__: list[str] = []
    class Request(_message.Message):
        __slots__: list[str] = []
        def __init__(self) -> None: ...
    class Response(_message.Message):
        __slots__ = ["provider", "resource_schemas", "data_source_schemas", "diagnostics", "provider_meta"]
        class ResourceSchemasEntry(_message.Message):
            __slots__ = ["key", "value"]
            KEY_FIELD_NUMBER: _ClassVar[int]
            VALUE_FIELD_NUMBER: _ClassVar[int]
            key: str
            value: Schema
            def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[Schema, _Mapping[Any, Any]]] = ...) -> None: ...
        class DataSourceSchemasEntry(_message.Message):
            __slots__ = ["key", "value"]
            KEY_FIELD_NUMBER: _ClassVar[int]
            VALUE_FIELD_NUMBER: _ClassVar[int]
            key: str
            value: Schema
            def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[Schema, _Mapping[Any, Any]]] = ...) -> None: ...
        PROVIDER_FIELD_NUMBER: _ClassVar[int]
        RESOURCE_SCHEMAS_FIELD_NUMBER: _ClassVar[int]
        DATA_SOURCE_SCHEMAS_FIELD_NUMBER: _ClassVar[int]
        DIAGNOSTICS_FIELD_NUMBER: _ClassVar[int]
        PROVIDER_META_FIELD_NUMBER: _ClassVar[int]
        provider: Schema
        resource_schemas: _containers.MessageMap[str, Schema]
        data_source_schemas: _containers.MessageMap[str, Schema]
        diagnostics: _containers.RepeatedCompositeFieldContainer[Diagnostic]
        provider_meta: Schema
        def __init__(self, provider: _Optional[_Union[Schema, _Mapping[Any, Any]]] = ..., resource_schemas: _Optional[_Mapping[str, Schema]] = ..., data_source_schemas: _Optional[_Mapping[str, Schema]] = ..., diagnostics: _Optional[_Iterable[_Union[Diagnostic, _Mapping[Any, Any]]]] = ..., provider_meta: _Optional[_Union[Schema, _Mapping[Any, Any]]] = ...) -> None: ...
    def __init__(self) -> None: ...

class ValidateProviderConfig(_message.Message):
    __slots__: list[str] = []
    class Request(_message.Message):
        __slots__ = ["config"]
        CONFIG_FIELD_NUMBER: _ClassVar[int]
        config: DynamicValue
        def __init__(self, config: _Optional[_Union[DynamicValue, _Mapping[Any, Any]]] = ...) -> None: ...
    class Response(_message.Message):
        __slots__ = ["diagnostics"]
        DIAGNOSTICS_FIELD_NUMBER: _ClassVar[int]
        diagnostics: _containers.RepeatedCompositeFieldContainer[Diagnostic]
        def __init__(self, diagnostics: _Optional[_Iterable[_Union[Diagnostic, _Mapping[Any, Any]]]] = ...) -> None: ...
    def __init__(self) -> None: ...

class UpgradeResourceState(_message.Message):
    __slots__: list[str] = []
    class Request(_message.Message):
        __slots__ = ["type_name", "version", "raw_state"]
        TYPE_NAME_FIELD_NUMBER: _ClassVar[int]
        VERSION_FIELD_NUMBER: _ClassVar[int]
        RAW_STATE_FIELD_NUMBER: _ClassVar[int]
        type_name: str
        version: int
        raw_state: RawState
        def __init__(self, type_name: _Optional[str] = ..., version: _Optional[int] = ..., raw_state: _Optional[_Union[RawState, _Mapping[Any, Any]]] = ...) -> None: ...
    class Response(_message.Message):
        __slots__ = ["upgraded_state", "diagnostics"]
        UPGRADED_STATE_FIELD_NUMBER: _ClassVar[int]
        DIAGNOSTICS_FIELD_NUMBER: _ClassVar[int]
        upgraded_state: DynamicValue
        diagnostics: _containers.RepeatedCompositeFieldContainer[Diagnostic]
        def __init__(self, upgraded_state: _Optional[_Union[DynamicValue, _Mapping[Any, Any]]] = ..., diagnostics: _Optional[_Iterable[_Union[Diagnostic, _Mapping[Any, Any]]]] = ...) -> None: ...
    def __init__(self) -> None: ...

class ValidateResourceConfig(_message.Message):
    __slots__: list[str] = []
    class Request(_message.Message):
        __slots__ = ["type_name", "config"]
        TYPE_NAME_FIELD_NUMBER: _ClassVar[int]
        CONFIG_FIELD_NUMBER: _ClassVar[int]
        type_name: str
        config: DynamicValue
        def __init__(self, type_name: _Optional[str] = ..., config: _Optional[_Union[DynamicValue, _Mapping[Any, Any]]] = ...) -> None: ...
    class Response(_message.Message):
        __slots__ = ["diagnostics"]
        DIAGNOSTICS_FIELD_NUMBER: _ClassVar[int]
        diagnostics: _containers.RepeatedCompositeFieldContainer[Diagnostic]
        def __init__(self, diagnostics: _Optional[_Iterable[_Union[Diagnostic, _Mapping[Any, Any]]]] = ...) -> None: ...
    def __init__(self) -> None: ...

class ValidateDataResourceConfig(_message.Message):
    __slots__: list[str] = []
    class Request(_message.Message):
        __slots__ = ["type_name", "config"]
        TYPE_NAME_FIELD_NUMBER: _ClassVar[int]
        CONFIG_FIELD_NUMBER: _ClassVar[int]
        type_name: str
        config: DynamicValue
        def __init__(self, type_name: _Optional[str] = ..., config: _Optional[_Union[DynamicValue, _Mapping[Any, Any]]] = ...) -> None: ...
    class Response(_message.Message):
        __slots__ = ["diagnostics"]
        DIAGNOSTICS_FIELD_NUMBER: _ClassVar[int]
        diagnostics: _containers.RepeatedCompositeFieldContainer[Diagnostic]
        def __init__(self, diagnostics: _Optional[_Iterable[_Union[Diagnostic, _Mapping[Any, Any]]]] = ...) -> None: ...
    def __init__(self) -> None: ...

class ConfigureProvider(_message.Message):
    __slots__: list[str] = []
    class Request(_message.Message):
        __slots__ = ["terraform_version", "config"]
        TERRAFORM_VERSION_FIELD_NUMBER: _ClassVar[int]
        CONFIG_FIELD_NUMBER: _ClassVar[int]
        terraform_version: str
        config: DynamicValue
        def __init__(self, terraform_version: _Optional[str] = ..., config: _Optional[_Union[DynamicValue, _Mapping[Any, Any]]] = ...) -> None: ...
    class Response(_message.Message):
        __slots__ = ["diagnostics"]
        DIAGNOSTICS_FIELD_NUMBER: _ClassVar[int]
        diagnostics: _containers.RepeatedCompositeFieldContainer[Diagnostic]
        def __init__(self, diagnostics: _Optional[_Iterable[_Union[Diagnostic, _Mapping[Any, Any]]]] = ...) -> None: ...
    def __init__(self) -> None: ...

class ReadResource(_message.Message):
    __slots__: list[str] = []
    class Request(_message.Message):
        __slots__ = ["type_name", "current_state", "private", "provider_meta"]
        TYPE_NAME_FIELD_NUMBER: _ClassVar[int]
        CURRENT_STATE_FIELD_NUMBER: _ClassVar[int]
        PRIVATE_FIELD_NUMBER: _ClassVar[int]
        PROVIDER_META_FIELD_NUMBER: _ClassVar[int]
        type_name: str
        current_state: DynamicValue
        private: bytes
        provider_meta: DynamicValue
        def __init__(self, type_name: _Optional[str] = ..., current_state: _Optional[_Union[DynamicValue, _Mapping[Any, Any]]] = ..., private: _Optional[bytes] = ..., provider_meta: _Optional[_Union[DynamicValue, _Mapping[Any, Any]]] = ...) -> None: ...
    class Response(_message.Message):
        __slots__ = ["new_state", "diagnostics", "private"]
        NEW_STATE_FIELD_NUMBER: _ClassVar[int]
        DIAGNOSTICS_FIELD_NUMBER: _ClassVar[int]
        PRIVATE_FIELD_NUMBER: _ClassVar[int]
        new_state: DynamicValue
        diagnostics: _containers.RepeatedCompositeFieldContainer[Diagnostic]
        private: bytes
        def __init__(self, new_state: _Optional[_Union[DynamicValue, _Mapping[Any, Any]]] = ..., diagnostics: _Optional[_Iterable[_Union[Diagnostic, _Mapping[Any, Any]]]] = ..., private: _Optional[bytes] = ...) -> None: ...
    def __init__(self) -> None: ...

class PlanResourceChange(_message.Message):
    __slots__: list[str] = []
    class Request(_message.Message):
        __slots__ = ["type_name", "prior_state", "proposed_new_state", "config", "prior_private", "provider_meta"]
        TYPE_NAME_FIELD_NUMBER: _ClassVar[int]
        PRIOR_STATE_FIELD_NUMBER: _ClassVar[int]
        PROPOSED_NEW_STATE_FIELD_NUMBER: _ClassVar[int]
        CONFIG_FIELD_NUMBER: _ClassVar[int]
        PRIOR_PRIVATE_FIELD_NUMBER: _ClassVar[int]
        PROVIDER_META_FIELD_NUMBER: _ClassVar[int]
        type_name: str
        prior_state: DynamicValue
        proposed_new_state: DynamicValue
        config: DynamicValue
        prior_private: bytes
        provider_meta: DynamicValue
        def __init__(self, type_name: _Optional[str] = ..., prior_state: _Optional[_Union[DynamicValue, _Mapping[Any, Any]]] = ..., proposed_new_state: _Optional[_Union[DynamicValue, _Mapping[Any, Any]]] = ..., config: _Optional[_Union[DynamicValue, _Mapping[Any, Any]]] = ..., prior_private: _Optional[bytes] = ..., provider_meta: _Optional[_Union[DynamicValue, _Mapping[Any, Any]]] = ...) -> None: ...
    class Response(_message.Message):
        __slots__ = ["planned_state", "requires_replace", "planned_private", "diagnostics", "legacy_type_system"]
        PLANNED_STATE_FIELD_NUMBER: _ClassVar[int]
        REQUIRES_REPLACE_FIELD_NUMBER: _ClassVar[int]
        PLANNED_PRIVATE_FIELD_NUMBER: _ClassVar[int]
        DIAGNOSTICS_FIELD_NUMBER: _ClassVar[int]
        LEGACY_TYPE_SYSTEM_FIELD_NUMBER: _ClassVar[int]
        planned_state: DynamicValue
        requires_replace: _containers.RepeatedCompositeFieldContainer[AttributePath]
        planned_private: bytes
        diagnostics: _containers.RepeatedCompositeFieldContainer[Diagnostic]
        legacy_type_system: bool
        def __init__(self, planned_state: _Optional[_Union[DynamicValue, _Mapping[Any, Any]]] = ..., requires_replace: _Optional[_Iterable[_Union[AttributePath, _Mapping[Any, Any]]]] = ..., planned_private: _Optional[bytes] = ..., diagnostics: _Optional[_Iterable[_Union[Diagnostic, _Mapping[Any, Any]]]] = ..., legacy_type_system: bool = ...) -> None: ...
    def __init__(self) -> None: ...

class ApplyResourceChange(_message.Message):
    __slots__: list[str] = []
    class Request(_message.Message):
        __slots__ = ["type_name", "prior_state", "planned_state", "config", "planned_private", "provider_meta"]
        TYPE_NAME_FIELD_NUMBER: _ClassVar[int]
        PRIOR_STATE_FIELD_NUMBER: _ClassVar[int]
        PLANNED_STATE_FIELD_NUMBER: _ClassVar[int]
        CONFIG_FIELD_NUMBER: _ClassVar[int]
        PLANNED_PRIVATE_FIELD_NUMBER: _ClassVar[int]
        PROVIDER_META_FIELD_NUMBER: _ClassVar[int]
        type_name: str
        prior_state: DynamicValue
        planned_state: DynamicValue
        config: DynamicValue
        planned_private: bytes
        provider_meta: DynamicValue
        def __init__(self, type_name: _Optional[str] = ..., prior_state: _Optional[_Union[DynamicValue, _Mapping[Any, Any]]] = ..., planned_state: _Optional[_Union[DynamicValue, _Mapping[Any, Any]]] = ..., config: _Optional[_Union[DynamicValue, _Mapping[Any, Any]]] = ..., planned_private: _Optional[bytes] = ..., provider_meta: _Optional[_Union[DynamicValue, _Mapping[Any, Any]]] = ...) -> None: ...
    class Response(_message.Message):
        __slots__ = ["new_state", "private", "diagnostics", "legacy_type_system"]
        NEW_STATE_FIELD_NUMBER: _ClassVar[int]
        PRIVATE_FIELD_NUMBER: _ClassVar[int]
        DIAGNOSTICS_FIELD_NUMBER: _ClassVar[int]
        LEGACY_TYPE_SYSTEM_FIELD_NUMBER: _ClassVar[int]
        new_state: DynamicValue
        private: bytes
        diagnostics: _containers.RepeatedCompositeFieldContainer[Diagnostic]
        legacy_type_system: bool
        def __init__(self, new_state: _Optional[_Union[DynamicValue, _Mapping[Any, Any]]] = ..., private: _Optional[bytes] = ..., diagnostics: _Optional[_Iterable[_Union[Diagnostic, _Mapping[Any, Any]]]] = ..., legacy_type_system: bool = ...) -> None: ...
    def __init__(self) -> None: ...

class ImportResourceState(_message.Message):
    __slots__: list[str] = []
    class Request(_message.Message):
        __slots__ = ["type_name", "id"]
        TYPE_NAME_FIELD_NUMBER: _ClassVar[int]
        ID_FIELD_NUMBER: _ClassVar[int]
        type_name: str
        id: str
        def __init__(self, type_name: _Optional[str] = ..., id: _Optional[str] = ...) -> None: ...
    class ImportedResource(_message.Message):
        __slots__ = ["type_name", "state", "private"]
        TYPE_NAME_FIELD_NUMBER: _ClassVar[int]
        STATE_FIELD_NUMBER: _ClassVar[int]
        PRIVATE_FIELD_NUMBER: _ClassVar[int]
        type_name: str
        state: DynamicValue
        private: bytes
        def __init__(self, type_name: _Optional[str] = ..., state: _Optional[_Union[DynamicValue, _Mapping[Any, Any]]] = ..., private: _Optional[bytes] = ...) -> None: ...
    class Response(_message.Message):
        __slots__ = ["imported_resources", "diagnostics"]
        IMPORTED_RESOURCES_FIELD_NUMBER: _ClassVar[int]
        DIAGNOSTICS_FIELD_NUMBER: _ClassVar[int]
        imported_resources: _containers.RepeatedCompositeFieldContainer[ImportResourceState.ImportedResource]
        diagnostics: _containers.RepeatedCompositeFieldContainer[Diagnostic]
        def __init__(self, imported_resources: _Optional[_Iterable[_Union[ImportResourceState.ImportedResource, _Mapping[Any, Any]]]] = ..., diagnostics: _Optional[_Iterable[_Union[Diagnostic, _Mapping[Any, Any]]]] = ...) -> None: ...
    def __init__(self) -> None: ...

class ReadDataSource(_message.Message):
    __slots__: list[str] = []
    class Request(_message.Message):
        __slots__ = ["type_name", "config", "provider_meta"]
        TYPE_NAME_FIELD_NUMBER: _ClassVar[int]
        CONFIG_FIELD_NUMBER: _ClassVar[int]
        PROVIDER_META_FIELD_NUMBER: _ClassVar[int]
        type_name: str
        config: DynamicValue
        provider_meta: DynamicValue
        def __init__(self, type_name: _Optional[str] = ..., config: _Optional[_Union[DynamicValue, _Mapping[Any, Any]]] = ..., provider_meta: _Optional[_Union[DynamicValue, _Mapping[Any, Any]]] = ...) -> None: ...
    class Response(_message.Message):
        __slots__ = ["state", "diagnostics"]
        STATE_FIELD_NUMBER: _ClassVar[int]
        DIAGNOSTICS_FIELD_NUMBER: _ClassVar[int]
        state: DynamicValue
        diagnostics: _containers.RepeatedCompositeFieldContainer[Diagnostic]
        def __init__(self, state: _Optional[_Union[DynamicValue, _Mapping[Any, Any]]] = ..., diagnostics: _Optional[_Iterable[_Union[Diagnostic, _Mapping[Any, Any]]]] = ...) -> None: ...
    def __init__(self) -> None: ...
