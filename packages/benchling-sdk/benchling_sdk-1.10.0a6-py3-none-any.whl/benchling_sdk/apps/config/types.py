# Tuple instead of list so it's hashable and preserves order
from typing import Any, Dict, List, Tuple, Union

from benchling_sdk.models import (
    ArrayElementAppConfigItem,
    BooleanAppConfigItem,
    DateAppConfigItem,
    DatetimeAppConfigItem,
    EntitySchemaAppConfigItem,
    FieldAppConfigItem,
    FloatAppConfigItem,
    GenericApiIdentifiedAppConfigItem,
    IntegerAppConfigItem,
    JsonAppConfigItem,
    SecureTextAppConfigItem,
    TextAppConfigItem,
)

# Tuple for an ordered collection that's hashable
ConfigItemPath = Tuple[str, ...]

# Everything from AppConfigItem except UnknownType
ConfigurationReference = Union[
    ArrayElementAppConfigItem,
    DateAppConfigItem,
    DatetimeAppConfigItem,
    JsonAppConfigItem,
    EntitySchemaAppConfigItem,
    FieldAppConfigItem,
    BooleanAppConfigItem,
    IntegerAppConfigItem,
    FloatAppConfigItem,
    GenericApiIdentifiedAppConfigItem,
    SecureTextAppConfigItem,
    TextAppConfigItem,
]

JsonType = Union[Dict[str, Any], List[Any], str, int, float, bool]
