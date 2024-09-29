{{/*
Expand the name of the chart or use nameOverride if provided.
*/}}
{{- define "application.name" -}}
{{- default .Values.nameOverride .Chart.Name | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Create a fully qualified app name using standard override scheme.
If fullnameOverride is provided, use it; otherwise, combine release name and chart name.
*/}}
{{- define "application.fullname" -}}
{{- if .Values.fullnameOverride }}
  {{- .Values.fullnameOverride | trunc 63 | trimSuffix "-" }}
{{- else if .Values.nameOverride }}
  {{- printf "%s-%s" .Release.Name .Values.nameOverride | trunc 63 | trimSuffix "-" }}
{{- else }}
  {{- printf .Release.Name | trunc 63 | trimSuffix "-" }}
{{- end }}
{{- end }}


{{/*
Create the name of the service account to use
*/}}
{{- define "application.serviceAccountName" -}}
{{- if .Values.serviceAccount.create }}
{{- default (include "application.fullname" .) .Values.serviceAccount.name }}
{{- else }}
{{- default "default" .Values.serviceAccount.name }}
{{- end }}
{{- end }}

{{/*
Create the name of the secret to be used by the application
*/}}
{{- define "application.secretname" -}}
{{- if .Values.appSecret.name }}
  {{- .Values.appSecret.name -}}
{{- else }}
  {{- printf "%s-secret" (include "application.fullname" .) -}}
{{- end -}}
{{- end -}}


{{- define "secrets.objects" -}}
objects: |
  array:
  {{- range .Values.appSecret.keys }}
  - |
    objectName: {{ . }}
    objectType: secret
  {{- end }}
{{- end -}}


{{- define "secrets.secretObjects" -}}
secretObjects:
  - secretName: (include "application.secretname" .)
    type: Opaque
    data:
    {{- range $index, $name := .Values.appSecret.keys }}
    - objectName: {{ $name }}
      key: {{ $name | replace "-" "_" | upper }}
    {{- end }}
{{- end -}}


{{/*
Database host
*/}}
{{- define "database.host" -}}
{{- if .Values.externalDatabase.host -}}
{{- .Values.externalDatabase.host -}}
{{- else -}}
{{- $postgresqlServiceName := .Values.postgresql.fullnameOverride | default (printf "%s-postgresql" .Release.Name) -}}
{{- $postgresqlServiceName | trunc 63 | trimSuffix "-" -}}
{{- end -}}
{{- end -}}

{{/*
Database port
*/}}
{{- define "database.port" -}}
{{- if .Values.externalDatabase.host -}}
{{- .Values.externalDatabase.port -}}
{{- else -}}
{{- .Values.global.postgresql.service.ports.postgresql -}}
{{- end -}}
{{- end -}}

{{/*
Database name
*/}}
{{- define "database.name" -}}
{{- if .Values.externalDatabase.host -}}
{{- .Values.externalDatabase.auth.database -}}
{{- else -}}
{{- .Values.global.postgresql.auth.database | default "postgres" -}}
{{- end -}}
{{- end -}}

{{/*
Database user
*/}}
{{- define "database.user" -}}
{{- if .Values.externalDatabase.host -}}
{{- .Values.externalDatabase.auth.username -}}
{{- else -}}
{{- .Values.global.postgresql.auth.username | default "postgres" -}}
{{- end -}}
{{- end -}}

{{/*
Redis service name
*/}}
{{- define "redis.serviceName" -}}
{{- $redisServiceName := .Values.redis.fullnameOverride | default (printf "%s-redis-master" .Release.Name) -}}
{{- $redisServiceName | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{/*
Redis cache URL
*/}}
{{- define "redis.cacheUrl" -}}
{{- if .Values.externalRedis.host -}}
{{- printf "redis://%s:%s/0" .Values.externalRedis.host (.Values.externalRedis.port | toString) -}}
{{- else -}}
{{- printf "redis://%s:%s/0" (include "redis.serviceName" .) (.Values.externalRedis.port | toString) -}}
{{- end -}}
{{- end -}}

{{/*
Redis Celery URL
*/}}
{{- define "redis.celeryUrl" -}}
{{- if .Values.externalRedis.host -}}
{{- printf "redis://%s:%s/1" .Values.externalRedis.host (.Values.externalRedis.port | toString) -}}
{{- else -}}
{{- printf "redis://%s:%s/1" (include "redis.serviceName" .) (.Values.externalRedis.port | toString) -}}
{{- end -}}
{{- end -}}