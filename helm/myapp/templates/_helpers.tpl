{{/*
Expand the name of the chart.
*/}}

{{- define "myapp.name" -}}
myapp
{{- end }}


{{/*
Create a fully qualified app name.
*/}}

{{- define "myapp.fullname" -}}
{{ include "myapp.name" . }}
{{- end }}


{{/*
Common labels.
*/}}

{{- define "myapp.labels" -}}

app.kubernetes.io/name: {{ include "myapp.name" . }}

app.kubernetes.io/instance: {{ .Release.Name }}

app.kubernetes.io/managed-by: {{ .Release.Service }}

helm.sh/chart: {{ .Chart.Name }}-{{ .Chart.Version }}

{{- end }}
