from django.urls import path
from core import views

urlpatterns = [
    path("tours/", views.ToursList.as_view()),
    path("tours/<uuid:tour_id>/days/", views.TourDaysList.as_view()),
    path("tours/<uuid:tour_id>/personnel/", views.TourPersonnel.as_view()),
    path("tours/<uuid:tour_id>/personnel/<uuid:person_id>/", views.TourPersonnelDetail.as_view()),
    path("tours/<uuid:tour_id>/groups/", views.TourGroups.as_view()),
    path("tours/<uuid:tour_id>/groups/<uuid:group_id>/", views.TourGroupsDetail.as_view()),
    path("days/<uuid:day_id>/schedule/", views.DayScheduleList.as_view()),
    path("days/<uuid:day_id>/context/", views.DayContext.as_view()),
    path("days/<uuid:day_id>/schedule/batch/", views.DayScheduleBatch.as_view()),
    path("tours/<uuid:tour_id>/schedule-templates/", views.TourScheduleTemplateList.as_view()),
    path("days/<uuid:day_id>/schedule-templates/", views.DayScheduleTemplateCreate.as_view()),
    path("tours/<uuid:tour_id>/schedule-templates/<uuid:template_id>/", views.TourScheduleTemplateList.as_view()),
    path("hotels/search/", views.HotelSearchView.as_view(), name="hotel-search"),
    path("days/<uuid:day_id>/lodging/", views.SaveDayLodgingView.as_view(), name="day-lodging"),
    path("days/<uuid:day_id>/notes/", views.DayNotes.as_view()),
    path("days/<uuid:day_id>/notes/<uuid:note_id>/", views.DayNoteDetail.as_view()),
    path("days/<uuid:day_id>/aftershow/", views.DayAftershow.as_view()),
]
