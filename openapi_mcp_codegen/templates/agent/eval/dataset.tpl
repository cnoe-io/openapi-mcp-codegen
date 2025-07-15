tests:
{% for test in tests %}
  {{ test.id }}:
    input: "{{ test.prompt }}"
    reference_output: "{{ test.answer|escape }}"
    reference_trajectory:
      solution_1: "{{ test.simple_traj }}"
    test_type: basic_functionality
    metadata: {}
{% endfor %}
