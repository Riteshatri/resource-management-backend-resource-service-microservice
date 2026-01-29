{{- define "resource.name" -}}
resource
{{- end }}

{{- define "resource.fullname" -}}
{{ .Release.Name }}-resource
{{- end }}
