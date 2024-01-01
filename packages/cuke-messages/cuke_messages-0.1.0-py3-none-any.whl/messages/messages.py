from enum import Enum
from typing import List, Optional, Union

from pydantic import BaseModel, ConfigDict, Field

# mypy: disable-error-code="typeddict-unknown-key, typeddict-item"


class ContentEncoding(Enum):
    identity = "IDENTITY"
    base64 = "BASE64"


class MediaType(Enum):
    text_x_cucumber_gherkin_plain = "text/x.cucumber.gherkin+plain"
    text_x_cucumber_gherkin_markdown = "text/x.cucumber.gherkin+markdown"


class Source(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
        use_enum_values=True,
    )
    uri: str = Field(
        ...,
        description="*\n The [URI](https://en.wikipedia.org/wiki/Uniform_Resource_Identifier)\n"
        " of the source, typically a file path relative to the root directory",
    )
    data: str = Field(..., description="The contents of the file")
    media_type: Union["MediaType", str] = Field(
        ...,
        alias="mediaType",
        description="The media type of the file. Can be used to specify custom types, such as\n"
        " text/x.cucumber.gherkin+plain",
    )


class Location(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    line: int
    column: Optional[int] = None


class Comment(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    location: Optional["Location"] = Field(..., description="The location of the comment")
    text: str = Field(..., description="The text of the comment")


class DocString(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    location: Optional["Location"]
    media_type: Optional[str] = Field(None, alias="mediaType")
    content: str
    delimiter: str


class KeywordType(Enum):
    unknown = "Unknown"
    context = "Context"
    action = "Action"
    outcome = "Outcome"
    conjunction = "Conjunction"


class TableCell(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    location: Optional["Location"] = Field(..., description="The location of the cell")
    value: str = Field(..., description="The value of the cell")


class TableRow(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    location: Optional["Location"] = Field(..., description="The location of the first cell in the row")
    cells: List["TableCell"] = Field(..., description="Cells in the row")
    id: str


class Tag(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    location: Optional["Location"] = Field(..., description="Location of the tag")
    name: str = Field(..., description="The name of the tag (including the leading `@`)")
    id: str = Field(..., description="Unique ID to be able to reference the Tag from PickleTag")


class JavaMethod(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    class_name: str = Field(..., alias="className")
    method_name: str = Field(..., alias="methodName")
    method_parameter_types: List[str] = Field(..., alias="methodParameterTypes")


class JavaStackTraceElement(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    class_name: str = Field(..., alias="className")
    file_name: str = Field(..., alias="fileName")
    method_name: str = Field(..., alias="methodName")


class Git(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    remote: str
    revision: str
    branch: Optional[str] = None
    tag: Optional[str] = None


class Product(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    name: str = Field(..., description="The product name")
    version: Optional[str] = Field(None, description="The product version")


class PickleDocString(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    media_type: Optional[str] = Field(None, alias="mediaType")
    content: str


class Type(Enum):
    unknown = "Unknown"
    context = "Context"
    action = "Action"
    outcome = "Outcome"


class PickleTableCell(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    value: str


class PickleTableRow(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    cells: List["PickleTableCell"] = Field(..., min_length=1)


class PickleTag(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    name: str
    ast_node_id: str = Field(..., alias="astNodeId", description="Points to the AST node this was created from")


class ExpressionType(Enum):
    cucumber_expression = "CUCUMBER_EXPRESSION"
    regular_expression = "REGULAR_EXPRESSION"


class StepDefinitionPattern(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    source: str
    type: Union["ExpressionType", str]


class Group(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    children: List["Group"]
    start: Optional[int] = None
    value: Optional[str] = None


class StepMatchArgument(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    group: "Group" = Field(
        ...,
        description="*\n Represents the outermost capture group of an argument. This message closely matches the\n "
        "`Group` class in the `cucumber-expressions` library.",
    )
    parameter_type_name: Optional[str] = Field(None, alias="parameterTypeName")


class StepMatchArgumentsList(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    step_match_arguments: List["StepMatchArgument"] = Field(..., alias="stepMatchArguments")


class TestStep(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    hook_id: Optional[str] = Field(None, alias="hookId", description="Pointer to the `Hook` (if derived from a Hook)")
    id: str
    pickle_step_id: Optional[str] = Field(
        None, alias="pickleStepId", description="Pointer to the `PickleStep` (if derived from a `PickleStep`)"
    )
    step_definition_ids: Optional[List[str]] = Field(
        None,
        alias="stepDefinitionIds",
        description="Pointer to all the matching `StepDefinition`s (if derived from a `PickleStep`)",
    )
    step_match_arguments_lists: Optional[List["StepMatchArgumentsList"]] = Field(
        None,
        alias="stepMatchArgumentsLists",
        description="A list of list of StepMatchArgument (if derived from a `PickleStep`).\n "
        "Each element represents a matching step definition. A size of 0 means `UNDEFINED`,\n "
        "and a size of 2+ means `AMBIGUOUS`",
    )


class Timestamp(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    seconds: int = Field(
        ...,
        description="Represents seconds of UTC time since Unix epoch\n "
        "1970-01-01T00:00:00Z. Must be from 0001-01-01T00:00:00Z to\n 9999-12-31T23:59:59Z inclusive.",
    )
    nanos: int = Field(
        ...,
        description="Non-negative fractions of a second at nanosecond resolution. Negative\n "
        "second values with fractions must still have non-negative nanos values\n "
        "that count forward in time. Must be from 0 to 999,999,999\n inclusive.",
    )


class TestCaseStarted(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    attempt: int = Field(
        ...,
        description="*\n The first attempt should have value 0, and for each retry the value\n should increase by 1.",
    )
    id: str = Field(
        ...,
        description="*\n Because a `TestCase` can be run multiple times (in case of a retry),\n "
        "we use this field to group messages relating to the same attempt.",
    )
    test_case_id: str = Field(..., alias="testCaseId")
    worker_id: Optional[str] = Field(
        None,
        alias="workerId",
        description="An identifier for the worker process running this test case, "
        "if test cases are being run in parallel. The identifier will be unique per worker, "
        "but no particular format is defined - it could be an index, uuid, machine name etc - "
        "and as such should be assumed that it's not human readable.",
    )
    timestamp: "Timestamp"


class ExceptionMessage(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    type: str = Field(
        ...,
        description="The type of the exception that caused this result. "
        'E.g. "Error" or "org.opentest4j.AssertionFailedError"',
    )
    message: Optional[str] = Field(
        None, description='The message of exception that caused this result. E.g. expected: "a" but was: "b"'
    )


class TestRunStarted(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    timestamp: "Timestamp"


class Status(Enum):
    unknown = "UNKNOWN"
    passed = "PASSED"
    skipped = "SKIPPED"
    pending = "PENDING"
    undefined = "UNDEFINED"
    ambiguous = "AMBIGUOUS"
    failed = "FAILED"


class Duration(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    seconds: int
    nanos: int = Field(
        ...,
        description="Non-negative fractions of a second at nanosecond resolution. Negative\n "
        "second values with fractions must still have non-negative nanos values\n "
        "that count forward in time. Must be from 0 to 999,999,999\n inclusive.",
    )


class TestStepStarted(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    test_case_started_id: str = Field(..., alias="testCaseStartedId")
    test_step_id: str = Field(..., alias="testStepId")
    timestamp: "Timestamp"


class UndefinedParameterType(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    expression: str
    name: str


class Attachment(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
        use_enum_values=True,
    )
    body: str = Field(
        ...,
        description="*\n The body of the attachment. If `contentEncoding` is `IDENTITY`, the attachment\n is simply "
        "the string. If it's `BASE64`, the string should be Base64 decoded to\n obtain the attachment.",
    )
    content_encoding: "ContentEncoding" = Field(
        ...,
        alias="contentEncoding",
        description='*\n Whether to interpret `body` "as-is" (IDENTITY) or if it needs to be Base64-decoded (BASE64).'
        "\n\n Content encoding is *not* determined by the media type, but rather by the type\n of the "
        "object being attached:\n\n - string: IDENTITY\n - byte array: BASE64\n - stream: BASE64",
    )
    file_name: Optional[str] = Field(
        None,
        alias="fileName",
        description="*\n Suggested file name of the attachment. (Provided by the user as an argument to `attach`)",
    )
    media_type: str = Field(
        ...,
        alias="mediaType",
        description="*\n The media type of the data. This can be any valid\n "
        "[IANA Media Type](https://www.iana.org/assignments/media-types/media-types.xhtml)\n"
        " as well as Cucumber-specific media types such as `text/x.cucumber.gherkin+plain`\n "
        "and `text/x.cucumber.stacktrace+plain`",
    )
    source: Optional["Source"] = None
    test_case_started_id: Optional[str] = Field(None, alias="testCaseStartedId")
    test_step_id: Optional[str] = Field(None, alias="testStepId")
    url: Optional[str] = Field(
        None,
        description="*\n A URL where the attachment can be retrieved. This field should not be set by Cucumber.\n "
        "It should be set by a program that reads a message stream and does the following for\n "
        "each Attachment message:\n\n "
        "- Writes the body (after base64 decoding if necessary) to a new file.\n "
        "- Sets `body` and `contentEncoding` to `null`\n "
        "- Writes out the new attachment message\n\n "
        "This will result in a smaller message stream, which can improve performance and\n "
        "reduce bandwidth of message consumers. "
        "It also makes it easier to process and download attachments\n separately from reports.",
    )


class DataTable(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    location: Optional["Location"]
    rows: List["TableRow"]


class Examples(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    location: Optional["Location"] = Field(..., description="The location of the `Examples` keyword")
    tags: List["Tag"]
    keyword: str
    name: str
    description: str
    table_header: Optional["TableRow"] = Field(None, alias="tableHeader")
    table_body: List["TableRow"] = Field(..., alias="tableBody")
    id: str


class Step(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    location: Optional["Location"] = Field(..., description="The location of the steps' `keyword`")
    keyword: str = Field(..., description="The actual keyword as it appeared in the source.")
    keyword_type: Optional["KeywordType"] = Field(
        None,
        alias="keywordType",
        description="The test phase signalled by the keyword: Context definition (Given), Action performance (When), "
        "Outcome assertion (Then). Other keywords signal Continuation (And and But) from a prior keyword. "
        "Please note that all translations which a dialect maps to multiple keywords (`*` is in this "
        "category for all dialects), map to 'Unknown'.",
    )
    text: str
    doc_string: Optional["DocString"] = Field(None, alias="docString")
    data_table: Optional["DataTable"] = Field(None, alias="dataTable")
    id: str = Field(..., description="Unique ID to be able to reference the Step from PickleStep")


class SourceReference(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    uri: Optional[str] = None
    java_method: Optional["JavaMethod"] = Field(None, alias="javaMethod")
    java_stack_trace_element: Optional["JavaStackTraceElement"] = Field(None, alias="javaStackTraceElement")
    location: Optional["Location"] = None


class Ci(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    name: str = Field(..., description='Name of the CI product, e.g. "Jenkins", "CircleCI" etc.')
    url: Optional[str] = Field(None, description="Link to the build")
    build_number: Optional[str] = Field(
        None,
        alias="buildNumber",
        description="The build number. Some CI servers use non-numeric build numbers, which is why this is a string",
    )
    git: Optional["Git"] = None


class ParameterType(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    name: str = Field(..., description="The name is unique, so we don't need an id.")
    regular_expressions: List[str] = Field(..., alias="regularExpressions", min_length=1)
    prefer_for_regular_expression_match: bool = Field(..., alias="preferForRegularExpressionMatch")
    use_for_snippets: bool = Field(..., alias="useForSnippets")
    id: str
    source_reference: Optional["SourceReference"] = Field(None, alias="sourceReference")


class ParseError(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    source: "SourceReference"
    message: str


class PickleTable(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    rows: List["PickleTableRow"]


class StepDefinition(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    id: str
    pattern: "StepDefinitionPattern"
    source_reference: "SourceReference" = Field(..., alias="sourceReference")


class TestCase(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    id: str
    pickle_id: str = Field(..., alias="pickleId", description="The ID of the `Pickle` this `TestCase` is derived from.")
    test_steps: List["TestStep"] = Field(..., alias="testSteps")


class TestCaseFinished(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    test_case_started_id: str = Field(..., alias="testCaseStartedId")
    timestamp: "Timestamp"
    will_be_retried: bool = Field(..., alias="willBeRetried")


class TestRunFinished(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    message: Optional[str] = Field(
        None,
        description="An informative message about the test run. Typically additional information about failure, "
        "but not necessarily.",
    )
    success: bool = Field(
        ...,
        description="A test run is successful if all steps are either passed or skipped, all before/after hooks passed "
        "and no other exceptions where thrown.",
    )
    timestamp: "Timestamp" = Field(..., description="Timestamp when the TestRun is finished")
    exception: Optional["ExceptionMessage"] = Field(
        None,
        description="Any exception thrown during the test run, if any. Does not include exceptions thrown while "
        "executing steps.",
    )


class TestStepResult(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    duration: "Duration"
    message: Optional[str] = Field(
        None,
        description="An arbitrary bit of information that explains this result. "
        "This can be a stack trace of anything else.",
    )
    status: "Status"
    exception: Optional["ExceptionMessage"] = Field(
        None, description="Exception thrown while executing this step, if any."
    )


class Background(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    location: Optional["Location"] = Field(..., description="The location of the `Background` keyword")
    keyword: str
    name: str
    description: str
    steps: List["Step"]
    id: str


class Scenario(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    location: Optional["Location"] = Field(..., description="The location of the `Scenario` keyword")
    tags: List["Tag"]
    keyword: str
    name: str
    description: str
    steps: List["Step"]
    examples: List["Examples"]
    id: str


class Hook(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    id: str
    name: Optional[str] = None
    source_reference: "SourceReference" = Field(..., alias="sourceReference")
    tag_expression: Optional[str] = Field(None, alias="tagExpression")


class Meta(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    protocol_version: str = Field(
        ..., alias="protocolVersion", description="*\n The [SEMVER](https://semver.org/) version number of the protocol"
    )
    implementation: "Product" = Field(..., description="SpecFlow, Cucumber-JVM, Cucumber.js, Cucumber-Ruby, Behat etc.")
    runtime: "Product" = Field(..., description="Java, Ruby, Node.js etc")
    os: "Product" = Field(..., description="Windows, Linux, MacOS etc")
    cpu: "Product" = Field(..., description="386, arm, amd64 etc")
    ci: Optional["Ci"] = None


class PickleStepArgument(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    doc_string: Optional["PickleDocString"] = Field(None, alias="docString")
    data_table: Optional["PickleTable"] = Field(None, alias="dataTable")


class TestStepFinished(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    test_case_started_id: str = Field(..., alias="testCaseStartedId")
    test_step_id: str = Field(..., alias="testStepId")
    test_step_result: "TestStepResult" = Field(..., alias="testStepResult")
    timestamp: "Timestamp"


class RuleChild(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    background: Optional["Background"] = None
    scenario: Optional["Scenario"] = None


class PickleStep(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    argument: Optional["PickleStepArgument"] = None
    ast_node_ids: List[str] = Field(
        ...,
        alias="astNodeIds",
        description="References the IDs of the source of the step. For Gherkin, this can be\n the ID of a Step, and "
        "possibly also the ID of a TableRow",
    )
    id: str = Field(..., description="A unique ID for the PickleStep")
    type: Optional["Type"] = Field(
        None,
        description="The context in which the step was specified: context (Given), action (When) or outcome (Then).\n\n"
        "Note that the keywords `But` and `And` inherit their meaning from prior steps and the `*` "
        "'keyword' doesn't have specific meaning (hence Unknown)",
    )
    text: str


class Rule(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    location: Optional["Location"] = Field(..., description="The location of the `Rule` keyword")
    tags: List["Tag"] = Field(..., description="All the tags placed above the `Rule` keyword")
    keyword: str
    name: str
    description: str
    children: List["RuleChild"]
    id: str


class Pickle(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    id: str = Field(..., description="*\n A unique id for the pickle")
    uri: str = Field(..., description="The uri of the source file")
    name: str = Field(..., description="The name of the pickle")
    language: str = Field(..., description="The language of the pickle")
    steps: List["PickleStep"] = Field(..., description="One or more steps")
    tags: List["PickleTag"] = Field(
        ...,
        description="*\n One or more tags. If this pickle is constructed from a Gherkin document,\n It includes "
        "inherited tags from the `Feature` as well.",
    )
    ast_node_ids: List[str] = Field(
        ...,
        alias="astNodeIds",
        description="*\n Points to the AST node locations of the pickle. The last one represents the unique\n "
        "id of the pickle. A pickle constructed from `Examples` will have the first\n id originating "
        "from the `Scenario` AST node, and the second from the `TableRow` AST node.",
        min_length=1,
    )


class FeatureChild(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    rule: Optional["Rule"] = None
    background: Optional["Background"] = None
    scenario: Optional["Scenario"] = None


class Feature(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    location: Optional["Location"] = Field(..., description="The location of the `Feature` keyword")
    tags: List["Tag"] = Field(..., description="All the tags placed above the `Feature` keyword")
    language: str = Field(
        ...,
        description="The [ISO 639-1](https://en.wikipedia.org/wiki/ISO_639-1) language code of the Gherkin document",
    )
    keyword: Optional[str] = Field(
        None, description="The text of the `Feature` keyword (in the language specified by `language`)"
    )
    name: str = Field(..., description="The name of the feature (the text following the `keyword`)")
    description: str = Field(
        ..., description="The line(s) underneath the line with the `keyword` that are used as description"
    )
    children: List["FeatureChild"] = Field(..., description="Zero or more children")


class GherkinDocument(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    uri: Optional[str] = Field(
        None,
        description="*\n The [URI](https://en.wikipedia.org/wiki/Uniform_Resource_Identifier)\n of the source, "
        "typically a file path relative to the root directory",
    )
    feature: Optional["Feature"] = None
    comments: List["Comment"] = Field(..., description="All the comments in the Gherkin document")


class Envelope(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    attachment: Optional["Attachment"] = None
    gherkin_document: Optional["GherkinDocument"] = Field(None, alias="gherkinDocument")
    hook: Optional["Hook"] = None
    meta: Optional["Meta"] = None
    parameter_type: Optional["ParameterType"] = Field(None, alias="parameterType")
    parse_error: Optional["ParseError"] = Field(None, alias="parseError")
    pickle: Optional["Pickle"] = None
    source: Optional["Source"] = None
    step_definition: Optional["StepDefinition"] = Field(None, alias="stepDefinition")
    test_case: Optional["TestCase"] = Field(None, alias="testCase")
    test_case_finished: Optional["TestCaseFinished"] = Field(None, alias="testCaseFinished")
    test_case_started: Optional["TestCaseStarted"] = Field(None, alias="testCaseStarted")
    test_run_finished: Optional["TestRunFinished"] = Field(None, alias="testRunFinished")
    test_run_started: Optional["TestRunStarted"] = Field(None, alias="testRunStarted")
    test_step_finished: Optional["TestStepFinished"] = Field(None, alias="testStepFinished")
    test_step_started: Optional["TestStepStarted"] = Field(None, alias="testStepStarted")
    undefined_parameter_type: Optional["UndefinedParameterType"] = Field(None, alias="undefinedParameterType")


Group.model_rebuild()  # type: ignore[attr-defined]
