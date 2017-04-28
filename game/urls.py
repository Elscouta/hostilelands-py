from django.conf.urls import url
from . import views
from . import actions
from . import tasks
from . import json_views
from . import json_tasks

urlpatterns = [
    url(r'^(?P<village_id>[0-9]+)/$', 
        views.village, name='game.village'),
    url(r'^(?P<village_id>[0-9]+)/storage/$', 
        json_views.storage, name='game.storage'),
    url(r'^(?P<village_id>[0-9]+)/building/show/(?P<building_textid>[a-z_]+)/$', 
        views.building_show, name='game.building.show'),
    url(r'^(?P<village_id>[0-9]+)/building/list/$',
        json_views.building_list, name='game.building.list'),
    url(r'^(?P<village_id>[0-9]+)/manager/tasks/$',
        views.manager_tasks, name='game.manager.tasks'),
    url(r'^(?P<village_id>[0-9]+)/rename/$', 
        actions.rename, name='rename'),
    url(r'^(?P<village_id>[0-9]+)/reset/$', 
        actions.reset, name='reset'),
    url(r'^(?P<village_id>[0-9]+)/task/start/(?P<task_textid>[a-z_]+/[a-z_]+(\[[a-z0-9=,_]+\])?)/$',
        json_tasks.start, name='tasks:start'),
    url(r'^(?P<village_id>[0-9]+)/task/end/(?P<task_id>[0-9_]+)/$',
        json_tasks.end, name='tasks:end'),
    url(r'^(?P<village_id>[0-9]+)/task/cancel/(?P<task_id>[0-9_]+)/$',
        json_tasks.cancel, name='tasks:cancel'),
    url(r'^(?P<village_id>[0-9]+)/task/addworker/(?P<task_id>[0-9_]+)/$',
        json_tasks.addworker, name='tasks:addworker'),
    url(r'^(?P<village_id>[0-9]+)/task/removeworker/(?P<task_id>[0-9_]+)/$',
        json_tasks.removeworker, name='tasks:removeworker'),
    url(r'^(?P<village_id>[0-9]+)/task/list/possibles/(?P<enctags>[a-z\+_]+)/$',
        json_tasks.possible_task_list, name='tasks:list_possibles'),
    url(r'^(?P<village_id>[0-9]+)/task/list/actives/(?P<enctags>[a-z\+_]+)/$',
        json_tasks.active_task_list, name='tasks:list_actives'),
    url(r'^(?P<village_id>[0-9]+)/property/get/(?P<propid>[a-z:/_\[\]]+)/$',
        json_views.get_property, name='property:get'),
    url(r'^(?P<village_id>[0-9]+)/property/set/(?P<propid>[a-z:_]+)/$',
        json_views.set_property, name='property:set'),
    url(r'^(?P<village_id>[0-9]+)/event/get/(?P<event_id>[0-9]+)/$',
        json_views.get_event, name='event:get'),
    url(r'^(?P<village_id>[0-9]+)/event/list/unread/$',
        json_views.list_unread_events, name='event:list:unread'),
    url(r'^(?P<village_id>[0-9]+)/event/markread/(?P<event_id>[0-9]+)/$',
        json_views.mark_event_read, name='event:markread')
]
