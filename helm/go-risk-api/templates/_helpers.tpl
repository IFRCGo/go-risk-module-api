{{- define "api.serviceAccountName" -}}
{{- if .Values.serviceAccount.create }}
{{- default (printf "%s-api-sa" .Release.Name) .Values.serviceAccount.name }}
{{- else }}
{{- default "default" .Values.serviceAccount.name }}
{{- end }}
{{- end }}

{{- define "secrets.objects" -}}
objects: |
  array:
  {{- range .Values.secret.refs }}
  - |
    objectName: {{ . }}
    objectType: secret
  {{- end }}
{{- end -}}

{{- define "secrets.secretObjects" -}}
secretObjects:
  - secretName: {{ default (printf "%s-secrets" .Release.Name) .Values.secret.name }}
    type: Opaque
    data:
    {{- range $index, $name := .Values.secret.refs }}
    - objectName: {{ $name }}
      key: {{ $name | replace "-" "_" | upper }}
    {{- end }}
{{- end -}}

{{- define "api.secrets" -}}
{{- $root := . }}
{{- range $index, $name := .Values.secret.refs }}
- name: {{ $name | replace "-" "_" | upper }}
  valueFrom:
    secretKeyRef:
      name: {{ default (printf "%s-secrets" $root.Release.Name) $root.Values.secret.name }}
      key: {{ $name | replace "-" "_" | upper }}
{{- end }}
{{- end -}}