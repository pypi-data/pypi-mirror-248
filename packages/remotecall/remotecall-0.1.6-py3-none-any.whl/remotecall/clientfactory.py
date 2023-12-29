import typing
from typing import Optional
from typing import Any

"""
Example:
    {
        "endpoints": [
            {
                "name": "foo",
                "documentation": "Foo.\n\nTest docstring.",
                "parameters": [
                    {
                        "name": "a",
                        "annotation": "int"
                    },
                    {
                        "name": "b",
                        "annotation": "str",
                        "default": "foo"
                    }
                ],
                "return_annotation": "bool"
            }
        ],
        "address": {
            "hostname": "127.0.0.1",
            "port": 8000
        }
    }
"""


class ClientFactory:
    def __init__(self, definition: dict, class_name: Optional[str] = None):
        self._definition = definition
        self._client_class_name = class_name or "Client"

    def generate(self):
        address = self._definition.get("address", {})
        host = address.get("host", "localhost")
        port = address.get("port", 8000)

        c = Class(name=self._client_class_name)
        c.doc = self._definition.get("documentation", "")
        c.methods.append(self.generate_init_method((host, port)))

        endpoints = self._definition.get("endpoints", [])
        for endpoint in endpoints:
            name = endpoint.get("name")
            doc = endpoint.get("documentation")
            return_annotation = endpoint.get("return_annotation")

            m = Method(name=name, return_annotation=return_annotation, doc=doc)
            c.methods.append(m)
            for parameter in endpoint.get("parameters", []):
                p = Parameter(
                    parameter["name"], parameter["annotation"], parameter.get("default", None)
                )
                m.parameters.append(p)

        lines = ["from __future__ import annotations\n"]
        lines.append("import typing")
        lines.append("from typing import Optional\n")
        lines.append("from remotecall import BaseClient\n\n")
        lines.append(str(c))

        return "\n".join(lines)

    @classmethod
    def generate_init_method(cls, server_address):
        return (
            f"    def __init__(self, server_address={server_address}):\n"
            f"        super().__init__(server_address=server_address)\n"
        )


class Parameter:
    def __init__(self, name: str, annotation: str, default: Any):
        self.name = name
        self.annotation = annotation
        self.default = default

    def __str__(self):
        lines = [f"{self.name}: {self.annotation}"]

        if self.default is not None:
            lines.append(f" = {self.default}")

        return "".join(lines)


class Method:
    def __init__(self, name: str, return_annotation: str, doc: str = None):
        self.name = name
        self.return_annotation = return_annotation
        self.parameters = []
        self.indent = "    "
        self.doc = indent_doc(doc, self.indent * 2)

    def __str__(self):
        lines = [f"{self.indent}def {self.name}(self"]

        # Signature
        for parameter in self.parameters:
            lines.append(f", {parameter}")
        lines.append(")")

        # Return type
        if self.return_annotation:
            lines.append(f" -> {self.return_annotation}")

        lines.append(":\n")

        # Docstring
        if self.doc:
            lines.append(self.indent * 2)
            lines.append(f'"""{self.doc}\n')
            lines.append(self.indent * 2)
            lines.append('"""\n')

        # Method body
        lines.append(self.indent * 2)
        lines.append(f'return self.call("{self.name}"')

        for parameter in self.parameters:
            lines.append(f", {parameter.name}={parameter.name}")

        lines.append(")\n")

        return "".join(lines)


class Class:
    def __init__(self, name: str):
        self.name = name.capitalize()
        self.methods = []
        self.indent = ""
        self.doc = None

    def __str__(self):
        lines = [f"class {self.name}(BaseClient):"]

        if self.doc:
            lines.append(f'    """{self.doc}')
            lines.append('    """')

        for method in self.methods:
            lines.append(str(method))

        return "\n".join(lines)


def indent_doc(doc: str, indent: str) -> str:
    if not doc:
        return doc

    lines = doc.split("\n")
    for i, line in enumerate(lines[1:], 1):
        lines[i] = indent + line
    return "\n".join(lines)
