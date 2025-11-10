{% if file_headers %}
# {{ file_headers_copyright }}
# {{ file_headers_license }}
# {{ file_headers_message }}
{% endif %}
{% if version %}
__version__ = "{{ version }}"
{% endif %}