from django_hosts import patterns, host

host_patterns = patterns(
    '',
    host('api', 'api.urls', name='api'),
    host('admin', 'main.urls', name='admin')
)

urlpatterns = []
