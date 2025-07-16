tests:
{% for test in tests %}
  {{ test.id }}:
    input: "{{ test.prompt }}"
    output: "{{ test.answer }}"
    reference_trajectory:
      {{ test.reference_traj | indent(6, false) }}
    tool:
      name: "{{ test.tool_name }}"
      arguments:
        {{ test.arguments_yaml | indent(8, false) }}
{% endfor %}
