from django.urls import path, include
from rest_framework import routers

from api import search

router = routers.DefaultRouter()

# Importing models
from api.about import views as about
from api.settings import views as site
from api.news import views as news
from api.gallery import views as gallery
from api.event import views as event
from api.sport import views as sport
from api.docs import views as docs
from api.tender import views as tender
from api.service import views as service
from api.quizz import views as quizz
from api.contact import views as contact
from api.search import views as search
from api.static import views as static
from api.typo import views as typo
from api.rating import views as rating

# router.register(r'index', index.IndexViewSet, basename='index-api')

# Settings
router.register(r'site-contact', site.SiteContactView, basename='site-contact-api')

# Index
router.register(r'header', site.HeaderView, basename='header-api')
router.register(r'footer', site.FooterView, basename='footer-api')
router.register(r'top-news', news.IndexNewsListView, basename='top-news-api')
router.register(r'top-news-medium', news.IndexNewsLongListView, basename='top-news-medium-api')
router.register(r'service', service.ServiceListView, basename='service-api')
router.register(r'contact-stat', contact.IndexContactView, basename='contact-stat-api')
router.register(r'top-event', event.IndexEventListView, basename='top-event-api')
router.register(r'top-gallery', gallery.IndexPhotoListView, basename='top-gallery-api')
router.register(r'poster', site.PosterView, basename='poster-api')
router.register(r'top-quizz', quizz.QuizzView, basename='top-quiz-api')
router.register(r'link', site.UsefulLinkView, basename='link-api')

# About us page
router.register(r'about', about.AboutUsView, basename='about-api')
router.register(r'structure', about.StructureView, basename='structure-api')

# Department & Organization
router.register(r'all-department', about.AllDepartmentView, basename='all-department-api')
router.register(r'department', about.DepartmentView, basename='department-api')
router.register(r'organizations', about.OrganizationView, basename='organization-api')

# Vacancy
router.register(r'vacancy', about.VacancyView, basename='vacancy-api')

# All staff and leaders
router.register(r'leader', about.StaffView, basename='leader-api')
router.register(r'leader-region', about.StaffRegionView, basename='leader-region-api')
router.register(r'leader-organization', about.StaffOrganizationView, basename='leader-organization-api')
router.register(r'leader-central', about.StaffCentralView, basename='leader-central-api')

# Press API
router.register(r'news', news.NewsListView, basename='news-api')
router.register(r'news-integration', news.NewsIntegration, basename='news-api-integration')
router.register(r'news-region', news.NewsRegionView, basename='news-region-api')
router.register(r'news-header', news.HeaderNewsListView, basename='news-header-api')
router.register(r'news-category', news.NewsCategoryView, basename='news-category-api')
router.register(r'news-hashtag', news.NewsHashtagView, basename='news-hashtag-api')
router.register(r'main-news', news.MainNewsListView, basename='main-api')
router.register(r'press', news.PressListView, basename='press-api')
router.register(r'faq', news.FAQListView, basename='faq-api')

# Static page
router.register(r'static', static.StaticView, basename='static-api')

# Gallery
router.register(r'photo', gallery.PhotoListView, basename='photo-api')
router.register(r'video', gallery.VideoListView, basename='video-api')

# Event
router.register(r'event', event.EventListView, basename='event-api')

# Sport
router.register(r'stadion', sport.StadionListView, basename='sport-api')
router.register(r'champion', sport.ChampionView, basename='champion-api')
router.register(r'champion-list', sport.ChampionListView, basename='champion-list-api')

# Docs
router.register(r'docs', docs.DocsListView, basename='docs-api')
router.register(r'doc-type', docs.DocTypeView, basename='doc-type-api')

# Tender
router.register(r'tender', tender.TenderListView, basename='tender-api')

# Quizz
router.register(r'quizz', quizz.QuizzListView, basename='quizz-api')

# Typo
router.register(r'typo', typo.TypoView, basename='typo-api')

# Contact
router.register(r'contact', contact.ContactView, basename='contact-api')
router.register(r'feedback', contact.FeedbackView, basename='feedback-api')
router.register(r'reception', contact.ReceptionView, basename='reception-api')

# Region
router.register(r'regions', site.RegionView, basename='region-api')
router.register(r'districts', site.DistrictView, basename='district-api')
router.register(r'employee-rating', service.EmployeeRatingModalViewSet, basename='employee_rating-api')

router.register(r'regiondepartment', site.RegionDepartmentView, basename='regiondepartment-api')

rating_router = routers.DefaultRouter()
rating_router.register(r'participants', rating.ParticipantsViewSet, basename='participants-api')
rating_router.register(r'evolution_criteria', rating.EvolutionCriteriaViewSet, basename='evolution_criteria-api')
rating_router.register(r'participants_vote', rating.VoteViewSet, basename='participants_vote-api')
rating_router.register(r'participants_filter', rating.ParticipantsFilterViewSet, basename='participants_filter-api')
rating_router.register(r'bot_link', rating.BotLinkViewSet, basename='bot_link-api')

rating_router.register(r'department', about.DepartmentView, basename='department-api')
rating_router.register(r'organizations', about.OrganizationView, basename='organization-api')
rating_router.register(r'regions', site.RegionView, basename='region-api')
rating_router.register(r'districts', site.DistrictView, basename='district-api')

bot_router = routers.DefaultRouter()
bot_router.register(r'bot_db', rating.SubscribersViewSet, basename='bot_db-api')
urlpatterns = [
    path('', include(router.urls)),
    path('search/', search.Search.as_view(), name='search-api'),
    path('upload/', search.ImageUploadView.as_view(), name='image-upload'),
    path('vote/', include(rating_router.urls)),
    path('bot/', include(bot_router.urls)),
]
