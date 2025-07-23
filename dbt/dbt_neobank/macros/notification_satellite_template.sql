{% macro notif_satellite(model_name, hub_model, key_field, attribute) %}
SELECT
    h.{{ key_field }} AS {{ key_field }},
    s.{{ attribute }},
    {{ load_date() }} AS load_date,
    {{ load_end_date() }} AS load_end_date,
    {{ record_source(model_name) }} AS record_source
FROM {{ ref(model_name) }} s
JOIN {{ ref(hub_model) }} h
  ON s.notification_id = h.notification_id
{% endmacro %}
