{% macro record_source(model_ref=None) %}
  {% if model_ref is none %}
    '{{ this.schema }}.{{ this.name }}'
  {% else %}
    {% set target_model = ref(model_ref) %}
    '{{ target_model.schema }}.{{ target_model.identifier }}'
  {% endif %}
{% endmacro %}
