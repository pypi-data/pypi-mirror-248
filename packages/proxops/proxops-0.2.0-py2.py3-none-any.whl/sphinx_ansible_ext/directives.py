from docutils import nodes
from docutils.core import publish_string
from docutils.parsers.rst import Directive

TABLE_HEADER = r"""
  <table class="colwidths-auto ansible-option-table docutils align-default" style="width: 100%">
    <thead>
      <tr class="row-odd">
        <th class="head"><p>Parameter</p></th>
        <th class="head"><p>Comments</p></th>
      </tr>
    </thead>
    <tbody>
"""

TABLE_TR = r"""
    <tr class="row-{row}">
      <td>
        <div class="ansible-option-cell">
          <div class="ansibleOptionAnchor" id="parameter-{param}"></div>
          <p class="ansible-option-title">
            <strong>{param}</strong>
          </p>
          <a class="ansibleOptionLink" href="#parameter-{param}" title="Permalink to this option"></a>
          <p class="ansible-option-type-line">
            {required}
          </p>
          </p>
        </div>
      </td>
      <td>
        <div class="ansible-option-cell">"""

TABLE_P_NOT_REQUIRED = """
            <span class="ansible-option-type">{type}</span>"""

TABLE_P_REQUIRED = """
            <span class="ansible-option-type">{type}</span>
            /
            <span class="ansible-option-required">required</span>"""

TABLE_TR_END = r"""
        </div>
      </td>
    </tr>"""


class AnsibleVarDesc(Directive):
    optional_arguments = 0
    required_arguments = 0
    final_argument_whitespace = False
    has_content = True

    def run(self) -> list[nodes.Node]:
        self.assert_has_content()

        content = self._parse_input(self.content)
        content = self._render(content)

        div_node = nodes.inline("", classes=["custom-table"])
        div_node += nodes.raw("", content, format="html")

        # For the weirdest possible reasons, if we don't apply
        # an extra node, then our raw html is displayed under
        # the footer... wtf.
        div_node += nodes.table()
        return [div_node]

    @staticmethod
    def _parse_input(lines):
        output = []
        item = {}
        state = 0
        for line in lines:
            if line.strip() == "":
                continue
            if not line.startswith(" "):
                # push item, and start a new one
                state = 0
                output += [item]
                item = {}

            line = line.strip()
            if state == 0:
                # param name
                item["param"] = line.strip()
                state = 1
            elif state == 1:
                # param type
                line = line.strip()
                if line.endswith("/ required"):
                    item["type"] = line.split("/")[0].strip()
                    item["required"] = True
                else:
                    item["type"] = line
                state = 2
            elif state == 2:
                # description
                item.setdefault("content", [])
                item["content"] += [line.strip()]
        output += [item]
        output = [x for x in output if x]
        return output

    def _render(self, content):
        output = TABLE_HEADER

        # For each parameter
        i = 1
        for item in content:
            i += 1
            param = item["param"]
            type = item["type"]
            row = "even" if i % 2 == 0 else "odd"

            if item.get("required"):
                required = TABLE_P_REQUIRED.format(type=type)
            else:
                required = TABLE_P_NOT_REQUIRED.format(type=type)

            output += TABLE_TR.format(param=param, type=type, row=row, required=required)
            for line in item["content"]:
                line = publish_string(line, writer_name="html")
                line = line.decode("utf-8").strip("\n")
                output += f"""<p>{line}</p>"""
            output += TABLE_TR_END
        return output


def setup_directives(app):
    # Add directives
    app.add_directive("ansible-var-desc", AnsibleVarDesc)
