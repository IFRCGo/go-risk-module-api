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
{{- if .Values.secrets.name }}
  {{- .Values.secrets.name -}}
{{- else }}
  {{- printf "%s-secret" (include "application.fullname" .) -}}
{{- end -}}
{{- end -}}

{{/*
The following two templates are required when creating the Azure SecretProviderClass
*/}}
{{- define "secrets.objects" -}}
    objects: |
      array:
    {{- range .Values.secrets.keys }}
        - |
          objectName: {{ . | upper | replace "_" "-" }}
          objectType: secret
    {{- end }}
{{- end -}}

{{- define "secrets.secretObjects" -}}
secretObjects:
  - secretName: {{ include "application.secretname" . }}
    type: Opaque
    data:
    {{- range $index, $name := .Values.secrets.keys }}
      - objectName: {{ $name | replace "_" "-" | upper }}
        key: {{ $name }}
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
Define CELERY_REDIS_URL
*/}}
{{- define "application.celeryRedisUrl" -}}
{{- if .Values.redis.enabled -}}
{{- printf "redis://%s:6379/0" (include "redis.serviceName" .) -}}
{{- else -}}
{{- required "env.CELERY_REDIS_URL" .Values.env.CELERY_REDIS_URL -}}
{{- end -}}
{{- end -}}

{{/*
Define CACHE_REDIS_URL
*/}}
{{- define "application.cacheRedisUrl" -}}
{{- if .Values.redis.enabled -}}
{{- printf "redis://%s:6379/1" (include "redis.serviceName" .) -}}
{{- else -}}
{{- required "env.CACHE_REDIS_URL" .Values.env.CACHE_REDIS_URL -}}
{{- end -}}
{{- end -}}